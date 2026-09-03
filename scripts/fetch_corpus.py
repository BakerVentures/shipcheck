#!/usr/bin/env python3
"""ShipCheck corpus fetcher.

Pulls every official policy page in sources.py, converts to clean Markdown,
chunks the App Store Review Guidelines by clause number and Google policy by
named section, and writes corpus/{apple,google}/ plus a manifest.json that
records url, fetched_at, sha256 and section anchors.

Standard library only, on purpose: the plugin installs from GitHub and must not
require a pip step.

Usage:
  python3 fetch_corpus.py                     # fetch all into ./corpus
  python3 fetch_corpus.py --out DIR           # fetch into DIR
  python3 fetch_corpus.py --only asrg,data-safety
  python3 fetch_corpus.py --diff              # fetch, then changelog vs previous manifest
  python3 fetch_corpus.py --offline           # re-chunk what is already on disk
"""
import argparse
import datetime as _dt
import difflib
import gzip
import hashlib
import http.cookiejar
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sources import SOURCES            # noqa: E402
import htmlmd                          # noqa: E402
import docc
import asrg                            # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
DEFAULT_OUT = os.path.abspath(os.path.join(HERE, "..", "corpus"))
TIMEOUT = 45


def _opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def http_get(url, tries=3):
    """GET with a cookie jar. The cookie jar is not optional: developer.android.com
    redirects into an infinite accounts.google.com OAuth loop without it."""
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip",
            })
            with _opener().open(req, timeout=TIMEOUT) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
                charset = r.headers.get_content_charset() or "utf-8"
                return raw.decode(charset, "replace"), r.geturl()
        except Exception as e:                      # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("GET failed after %d tries: %s (%s)" % (tries, url, last))


def fetch_source(src):
    """Returns (markdown, final_url, warnings, raw_html)."""
    warn = []
    strat = src["strategy"]

    if strat == "apple_docc":
        api = "https://developer.apple.com/tutorials/data/%s.json" % src["docc"]
        body, final = http_get(api)
        try:
            md = docc.render(json.loads(body))
        except json.JSONDecodeError:
            raise RuntimeError("DocC endpoint did not return JSON: %s" % api)
        return md, api, warn, None

    if strat == "android_dev":
        url = src["url"] + ("&" if "?" in src["url"] else "?") + "hl=en"
        body, final = http_get(url)
        md = htmlmd.to_markdown(body, "android_dev")
        return md, final, warn, body

    if strat == "google_help":
        url = src["url"] + ("&" if "?" in src["url"] else "?") + "hl=en"
        body, final = http_get(url)
        if final.rstrip("/").endswith("support.google.com"):
            raise RuntimeError("Answer ID is dead; redirected to support root")
        md = htmlmd.to_markdown(body, "google_help")
        return md, final, warn, body

    if strat == "index_only":
        body, final = http_get(src["url"])
        md = htmlmd.to_markdown(body, "generic")
        warn.append("JS-rendered page: only the section index is recoverable. "
                    "Policy text for these sections comes from support.google.com.")
        return md, final, warn, body

    body, final = http_get(src["url"])
    md = htmlmd.to_markdown(body, "apple_html" if strat == "apple_html" else "generic")
    return md, final, warn, body


# ------------------------------------------------------------------ chunking
CLAUSE_RE = re.compile(r"^#{1,6}\s*(\d+(?:\.\d+)*)\.?\s+(.{2,120})$")
# Apple sometimes emits clause headings as bare bold paragraphs
CLAUSE_BOLD_RE = re.compile(r"^\*\*(\d+(?:\.\d+)*)\.?\s+(.{2,120}?)\*\*$")


def chunk_apple_numbered(md):
    """Split the App Store Review Guidelines by clause number (1.1, 2.3.1, 3.1.2)."""
    lines = md.splitlines()
    marks = []
    for i, ln in enumerate(lines):
        s = ln.strip()
        m = CLAUSE_RE.match(s) or CLAUSE_BOLD_RE.match(s)
        if m:
            clause, title = m.group(1), m.group(2).strip().rstrip("*").strip()
            if clause.count(".") <= 3:
                marks.append((i, clause, title))
    chunks = []
    for idx, (i, clause, title) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        text = "\n".join(lines[i:end]).strip()
        if len(text) < 20:
            continue
        chunks.append(dict(anchor=clause, title=title, text=text,
                           line_start=i + 1, line_end=end))
    return chunks


HEADING_RE = re.compile(r"^(#{2,3})\s+(.{2,140})$")


def chunk_named(md):
    """Split a policy page by named h2/h3 section."""
    lines = md.splitlines()
    marks = [(i, m.group(2).strip())
             for i, ln in enumerate(lines)
             for m in [HEADING_RE.match(ln.strip())] if m]
    chunks = []
    for idx, (i, title) in enumerate(marks):
        end = marks[idx + 1][0] if idx + 1 < len(marks) else len(lines)
        text = "\n".join(lines[i:end]).strip()
        if len(text) < 40:
            continue
        anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
        chunks.append(dict(anchor=anchor, title=title, text=text,
                           line_start=i + 1, line_end=end))
    return chunks


def slug(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)


# ------------------------------------------------------------------- writing
def write_source(out_dir, src, md, final_url, warnings, raw_html=None):
    vend = os.path.join(out_dir, src["vendor"])
    os.makedirs(vend, exist_ok=True)
    sha = hashlib.sha256(md.encode("utf-8")).hexdigest()
    now = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()

    if src.get("chunk") == "apple_numbered" and raw_html:
        chunks = asrg.extract(raw_html, src["url"])
    elif src.get("chunk") == "apple_numbered":
        chunks = chunk_apple_numbered(md)
    elif src["vendor"] == "google" and src["strategy"] in ("google_help", "android_dev"):
        chunks = chunk_named(md)
    else:
        chunks = chunk_named(md)

    fm = [
        "---",
        "shipcheck_source_id: %s" % src["id"],
        "title: %s" % json.dumps(src["title"]),
        "url: %s" % src["url"],
        "final_url: %s" % final_url,
        "fetched_at: %s" % now,
        "sha256: %s" % sha,
        "vendor: %s" % src["vendor"],
    ]
    if src.get("substituted_from"):
        fm.append("substituted_from: %s" % src["substituted_from"])
    if src.get("note"):
        fm.append("note: %s" % json.dumps(src["note"]))
    if warnings:
        fm.append("warnings: %s" % json.dumps(warnings))
    fm.append("---")
    body = "\n".join(fm) + "\n\n" + md + "\n"

    path = os.path.join(vend, src["id"] + ".md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)

    # write clause-level chunks so citations can point at an exact file
    sec_dir = os.path.join(vend, src["id"] + ".sections")
    if chunks:
        os.makedirs(sec_dir, exist_ok=True)
        keep = set()
        for c in chunks:
            name = slug(c["anchor"]) + ".md"
            keep.add(name)
            link = c.get("deep_link") or src["url"]
            with open(os.path.join(sec_dir, name), "w", encoding="utf-8") as f:
                f.write("<!-- source=%s clause=%s url=%s fetched=%s -->\n\n%s\n"
                        % (src["id"], c["anchor"], link, now, c["text"]))
        for stale in os.listdir(sec_dir):
            if stale not in keep:
                os.remove(os.path.join(sec_dir, stale))

    return dict(
        id=src["id"], vendor=src["vendor"], title=src["title"],
        url=src["url"], final_url=final_url, requested_url=src["url"],
        substituted_from=src.get("substituted_from"),
        strategy=src["strategy"], fetched_at=now, sha256=sha,
        chars=len(md), path=os.path.relpath(path, out_dir),
        sections_dir=os.path.relpath(sec_dir, out_dir) if chunks else None,
        section_count=len(chunks),
        sections=[dict(anchor=c["anchor"], title=c["title"],
                       deep_link=c.get("deep_link"),
                       chars=len(c["text"]),
                       sha256=hashlib.sha256(c["text"].encode()).hexdigest()[:16])
                  for c in chunks],
        warnings=warnings, note=src.get("note"),
        primary=bool(src.get("primary")),
    )


def load_manifest(out_dir):
    p = os.path.join(out_dir, "manifest.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None


def read_body(out_dir, entry):
    p = os.path.join(out_dir, entry["path"])
    if not os.path.exists(p):
        return ""
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    return txt.split("---\n", 2)[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--only", default="")
    ap.add_argument("--diff", action="store_true",
                    help="print a changelog of what policy text changed")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)
    only = {s.strip() for s in args.only.split(",") if s.strip()}
    todo = [s for s in SOURCES if not only or s["id"] in only]

    prev = load_manifest(out_dir)
    prev_by_id = {e["id"]: e for e in (prev or {}).get("sources", [])}
    prev_bodies = {e["id"]: read_body(out_dir, e) for e in prev_by_id.values()} if args.diff else {}

    entries, failures, changes = [], [], []
    for i, src in enumerate(todo, 1):
        label = "[%d/%d] %s" % (i, len(todo), src["id"])
        try:
            md, final, warn, raw = fetch_source(src)
            if len(md) < 400 and src["strategy"] != "index_only":
                warn.append("Suspiciously short extraction (%d chars) — page shape "
                            "may have changed." % len(md))
            entry = write_source(out_dir, src, md, final, warn, raw)
            entries.append(entry)
            old = prev_by_id.get(src["id"])
            status = "new"
            if old:
                status = "unchanged" if old["sha256"] == entry["sha256"] else "CHANGED"
            if status == "CHANGED":
                changes.append((src, old, entry, prev_bodies.get(src["id"], ""), md))
            if not args.quiet:
                print("%-28s ok  %6d chars  %3d sections  %s%s"
                      % (label, entry["chars"], entry["section_count"], status,
                         "  [%s]" % "; ".join(warn) if warn else ""))
        except Exception as e:                       # noqa: BLE001
            failures.append(dict(id=src["id"], url=src["url"], error=str(e)))
            if not args.quiet:
                print("%-28s FAIL  %s" % (label, e))

    # keep untouched entries when running with --only
    if only and prev:
        kept = [e for e in prev["sources"] if e["id"] not in only]
        entries = kept + entries

    manifest = dict(
        schema_version=1,
        generated_at=_dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat(),
        generator="shipcheck/fetch_corpus.py",
        source_count=len(entries),
        failure_count=len(failures),
        failures=failures,
        sources=sorted(entries, key=lambda e: (e["vendor"], e["id"])),
    )
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    if args.diff:
        print()
        print("=" * 72)
        print("POLICY CHANGELOG")
        print("=" * 72)
        if not prev:
            print("No previous manifest — this is the first fetch, so everything is new.")
        elif not changes:
            print("No policy text changed since %s." % prev.get("generated_at"))
        else:
            for src, old, new, oldmd, newmd in changes:
                print("\n### %s — %s" % (src["title"], src["url"]))
                print("    last fetched %s  ->  %s" % (old["fetched_at"], new["fetched_at"]))
                print("    sha256 %s -> %s" % (old["sha256"][:12], new["sha256"][:12]))
                oldsec = {s["anchor"]: s["sha256"] for s in old.get("sections", [])}
                newsec = {s["anchor"]: s["sha256"] for s in new.get("sections", [])}
                added = [a for a in newsec if a not in oldsec]
                removed = [a for a in oldsec if a not in newsec]
                edited = [a for a in newsec if a in oldsec and newsec[a] != oldsec[a]]
                if added:
                    print("    + added sections:   %s" % ", ".join(sorted(added)[:20]))
                if removed:
                    print("    - removed sections: %s" % ", ".join(sorted(removed)[:20]))
                if edited:
                    print("    ~ edited sections:  %s" % ", ".join(sorted(edited)[:20]))
                diff = list(difflib.unified_diff(
                    oldmd.splitlines(), newmd.splitlines(),
                    fromfile="previous", tofile="current", lineterm="", n=1))
                shown = [d for d in diff[2:] if d.startswith(("+", "-"))][:40]
                for d in shown:
                    print("      %s" % d[:200])
                if len(shown) == 40:
                    print("      ... (truncated)")

    if args.json:
        print(json.dumps(dict(ok=len(entries), failed=len(failures),
                              failures=failures), indent=2))
    if not args.quiet:
        print("\n%d sources written to %s (%d failures)"
              % (len(entries), out_dir, len(failures)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
