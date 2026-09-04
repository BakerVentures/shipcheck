#!/usr/bin/env python3
"""Render shipcheck-report.md from merged findings.

Input JSON:
  { "facts": {...},
    "findings": [ {id, severity, title, clause, clause_text, clause_url,
                   evidence, reviewer_says, fix, confidence, platform, source} ],
    "passes":  [ {title, note, clause} ],
    "gaps":    [ {what, why} ] }

Free tier shows the score and the top 3 findings; the rest are counted, not
shown. Ordering is by rejection likelihood so the free preview is still the
three things most likely to get the app bounced.
"""
import argparse
import datetime as _dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import license as lic                                # noqa: E402


def _default_corpus_dir():
    """Prefer the corpus /shipcheck:refresh wrote, if there is one.

    See the matching helper and comment in scan.py -- report.py is what
    actually resolves a finding's `corpus` reference to clause text, so this
    is the more consequential of the two places this mattered.
    """
    bundled = os.path.join(HERE, "..", "corpus")
    data_dir = os.environ.get("CLAUDE_PLUGIN_DATA", "").strip()
    if data_dir:
        refreshed = os.path.join(data_dir, "corpus")
        if os.path.isdir(refreshed):
            return refreshed
    return bundled

WEIGHT = {"critical": 22, "high": 12, "medium": 5, "low": 2, "info": 0}
CONF = {"high": 1.0, "medium": 0.75, "low": 0.5}
BADGE = {"critical": "🔴 CRITICAL", "high": "🟠 HIGH", "medium": "🟡 MEDIUM",
         "low": "⚪ LOW", "info": "· INFO"}



def load_clause(corpus_dir, clause):
    """Pull verbatim clause text out of the cached corpus.

    Citations are read off disk rather than written by the model, so a quoted
    guideline in the report is always the text ShipCheck actually fetched.
    Returns (text, url) or (None, None).
    """
    if not clause:
        return None, None
    candidates = []
    c = str(clause).strip()
    if re.match(r"^\d+(\.\d+)*[a-z]?$", c):
        candidates.append(os.path.join(corpus_dir, "apple", "asrg.sections", c + ".md"))
    if ":" in c:
        vendor_key, name = c.split(":", 1)
        vendor = {"play": "google", "google": "google", "apple": "apple",
                  "asc": "apple"}.get(vendor_key.lower())
        if vendor:
            candidates.append(os.path.join(corpus_dir, vendor, name + ".md"))
    for path in candidates:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        url = None
        m = re.search(r"<!--.*?url=(\S+).*?-->", raw)
        if m:
            url = m.group(1)
        body = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
        body = re.sub(r"(?s)^---\n.*?\n---\n", "", body).strip()
        # Apple's help pages open with breadcrumb chrome ("App Store Connect
        # Help", nav links, "Reference") before the real H1. Quoting that makes
        # the citation look broken, so start at the title when there is one.
        h1 = re.search(r"^# .+$", body, re.M)
        if h1 and h1.start() < 600:
            body = body[h1.start():]
        if not url:
            # prefer the canonical human URL; final_url can be the DocC JSON
            # endpoint for developer.apple.com/documentation pages
            m2 = re.search(r"^url:\s*(\S+)", raw, re.M) or \
                 re.search(r"^final_url:\s*(\S+)", raw, re.M)
            if m2:
                url = m2.group(1)
        if len(body) > 900:
            body = body[:900].rsplit(" ", 1)[0] + " […]"
        return body, url
    return None, None


def score(findings):
    raw = sum(WEIGHT.get(f.get("severity"), 0) * CONF.get(f.get("confidence", "high"), 1.0)
              for f in findings)
    return int(min(100, round(raw)))


def band(s):
    if s >= 70:
        return "Very likely to be rejected"
    if s >= 45:
        return "Likely to be rejected"
    if s >= 20:
        return "At risk — fix the criticals first"
    if s > 0:
        return "Probably fine, with cleanup"
    return "Nothing blocking found"


UPLOAD_IDS = ("ICON-", "EXPORT-COMPLIANCE", "BUNDLE-ID", "PRIVACY-MANIFEST",
              "SDK-NO-MANIFEST", "SDK-MANIFEST-REQUIRED", "REASON-MISSING",
              "TARGET-SDK", "PLAY-DECLARATION", "META-LEN-")
METADATA_IDS = ("META-", "URL-DEAD", "DEMO-ACCOUNT", "JUDGE-OTHER-PLATFORM",
                "JUDGE-PRICE-IN-METADATA", "JUDGE-SCREENSHOT", "JUDGE-AGE-RATING",
                "JUDGE-REVIEW-NOTES", "META-KEYWORDS")
BLOCK_RANK = {"upload": 0, "review": 1, "metadata": 2}
BLOCK_LABEL = {
    "upload": "blocks upload",
    "review": "blocks review",
    "metadata": "metadata only — no new build",
}


def blocks(f):
    """What wall does this hit first? Drives ordering, and tells the developer
    whether a fix costs them a new build or just an App Store Connect edit."""
    if f.get("blocks"):
        return f["blocks"]
    fid = f.get("id", "")
    if f.get("itms") or fid.startswith(UPLOAD_IDS):
        return "upload"
    if fid.startswith(METADATA_IDS):
        return "metadata"
    return "review"


def rank(findings):
    return sorted(findings, key=lambda f: (
        -WEIGHT.get(f.get("severity"), 0) * CONF.get(f.get("confidence", "high"), 1.0),
        BLOCK_RANK.get(blocks(f), 1),
        f.get("platform", "ios"), f.get("id", "")))


def render(data, tier_info, corpus_manifest=None, corpus_dir=None):
    findings = rank(data.get("findings") or [])
    if corpus_dir:
        for f in findings:
            if not f.get("clause_text"):
                txt, url = load_clause(corpus_dir, f.get("clause"))
                if txt:
                    f["clause_text"] = txt
                    f.setdefault("clause_url", url)
    passes = data.get("passes") or []
    gaps = data.get("gaps") or []
    facts = data.get("facts") or {}
    s = score(findings)
    limit = tier_info.get("limit")
    shown = findings if limit is None else findings[:limit]
    hidden = 0 if limit is None else max(0, len(findings) - limit)

    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    L = []
    L.append("# ShipCheck report")
    L.append("")
    L.append("**%s** · %s · generated %s" % (
        facts.get("app_name") or "(unnamed app)",
        "v%s" % facts.get("version") if facts.get("version") else "no version",
        now))
    L.append("")
    L.append("## Rejection risk: %d / 100" % s)
    L.append("")
    L.append("**%s**" % band(s))
    L.append("")
    bar_full = int(round(s / 5))
    L.append("`[%s%s]` %d critical · %d high · %d medium · %d low" % (
        "█" * bar_full, "░" * (20 - bar_full),
        sum(1 for f in findings if f["severity"] == "critical"),
        sum(1 for f in findings if f["severity"] == "high"),
        sum(1 for f in findings if f["severity"] == "medium"),
        sum(1 for f in findings if f["severity"] == "low")))
    L.append("")
    upload = [f for f in findings if blocks(f) == "upload"]
    meta_only = [f for f in findings if blocks(f) == "metadata"]
    bits = []
    if upload:
        bits.append("**%d block the upload** — App Store Connect will not accept a "
                    "build until these are fixed" % len(upload))
    if meta_only:
        bits.append("**%d are metadata only** and need no new build — you can fix "
                    "those in App Store Connect right now" % len(meta_only))
    if bits:
        L.append(" · ".join(bits) + ".")
        L.append("")

    if corpus_manifest:
        L.append("> Checked against policy text fetched %s from %d official Apple and "
                 "Google sources. Run `/shipcheck:refresh` to re-fetch and see what "
                 "changed." % (corpus_manifest.get("generated_at", "?")[:10],
                               corpus_manifest.get("source_count", 0)))
        L.append("")

    L.append("---")
    L.append("")
    L.append("## Findings")
    L.append("")
    if not findings:
        L.append("Nothing found." +
                 (" See *Likely to pass* below for what was checked." if passes else ""))
        L.append("")

    for i, f in enumerate(shown, 1):
        L.append("### %d. %s %s" % (i, BADGE.get(f["severity"], ""), f["title"]))
        L.append("")
        meta = []
        if f.get("clause"):
            meta.append("**Guideline %s**" % f["clause"])
        meta.append("confidence: %s" % f.get("confidence", "high"))
        meta.append("%s" % ("iOS" if f.get("platform") == "ios" else
                            "Android" if f.get("platform") == "android" else "both"))
        meta.append(BLOCK_LABEL[blocks(f)])
        if f.get("itms"):
            meta.append("**%s**" % f["itms"])
        if f.get("source"):
            meta.append(f["source"])
        L.append(" · ".join(meta))
        L.append("")
        if f.get("clause_text"):
            L.append("> %s" % f["clause_text"].strip().replace("\n", "\n> "))
            if f.get("clause_url"):
                L.append("> ")
                L.append("> — [%s](%s)" % (f.get("clause") or "guideline", f["clause_url"]))
            L.append("")
        if f.get("evidence"):
            L.append("**What ShipCheck found**")
            L.append("")
            L.append(f["evidence"])
            L.append("")
        if f.get("reviewer_says"):
            L.append("**What the reviewer will likely say**")
            L.append("")
            L.append("> %s" % f["reviewer_says"].strip().replace("\n", "\n> "))
            L.append("")
        if f.get("fix"):
            L.append("**Fix**")
            L.append("")
            L.append(f["fix"])
            L.append("")
        L.append("")

    if hidden:
        L.append("---")
        L.append("")
        L.append("### 🔒 %d more finding%s — unlock the full report" % (
            hidden, "s" if hidden != 1 else ""))
        L.append("")
        by_sev = {}
        for f in findings[limit:]:
            by_sev[f["severity"]] = by_sev.get(f["severity"], 0) + 1
        summary = ", ".join("%d %s" % (v, k) for k, v in
                            sorted(by_sev.items(), key=lambda kv: -WEIGHT.get(kv[0], 0)))
        L.append("The free scan shows your score and the three findings most likely to "
                 "get this build rejected. The remaining **%s** finding%s "
                 "(%s) — including the exact guideline text, what the reviewer will "
                 "say, and the file-level fix for each — are in the full report."
                 % (hidden, "s" if hidden != 1 else "", summary))
        L.append("")
        L.append("**$29 one-time for this app**, unlimited scans of it forever — or "
                 "**$49/year for unlimited apps** if you ship more than one.")
        L.append("")
        L.append("Unlock: <https://shipcheck.dev> — then run "
                 "`/shipcheck:license <your-key>` and re-scan.")
        L.append("")

    if passes:
        L.append("---")
        L.append("")
        L.append("## Likely to pass")
        L.append("")
        L.append("Checked and found clean, so you can trust the list above is the "
                 "whole problem:")
        L.append("")
        for p in passes:
            note = " — %s" % p["note"] if p.get("note") else ""
            clause = " *(%s)*" % p["clause"] if p.get("clause") else ""
            L.append("- ✅ **%s**%s%s" % (p["title"], clause, note))
        L.append("")

    if gaps:
        L.append("---")
        L.append("")
        L.append("## Not checked")
        L.append("")
        L.append("ShipCheck could not verify these. They are not passes:")
        L.append("")
        for g in gaps:
            L.append("- ⚠️ **%s** — %s" % (g["what"], g["why"]))
        L.append("")

    L.append("---")
    L.append("")
    tier = tier_info.get("tier", "free")
    note = ""
    if tier_info.get("degraded"):
        note = " (licence server unreachable, treated as paid)"
    elif tier == "single":
        note = " (licensed to this app)"
    L.append("<sub>ShipCheck v%s · %s tier%s · findings are advisory: App Review "
             "outcomes are decided by Apple and Google, not by this tool.</sub>"
             % (lic.VERSION, tier, note))
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--findings", required=True)
    ap.add_argument("--out", default="shipcheck-report.md")
    ap.add_argument("--corpus", default=_default_corpus_dir())
    ap.add_argument("--force-tier", default="", choices=["", "free", "pro"])
    args = ap.parse_args()

    with open(args.findings, encoding="utf-8") as f:
        data = json.load(f)

    facts = data.get("facts") or {}
    app_id = facts.get("bundle_id") or facts.get("android_package") or ""

    if args.force_tier == "free":
        tier = dict(tier="free", valid=False, limit=lic.FREE_FINDING_LIMIT,
                    reason="forced")
    elif args.force_tier == "pro":
        tier = dict(tier="unlimited", valid=True, limit=None, reason="forced")
    else:
        # per-app binding: a $29 single-app licence is pinned to this bundle id
        tier = lic.check(app_id=app_id or None)

    cm = None
    mpath = os.path.join(args.corpus, "manifest.json")
    if os.path.exists(mpath):
        with open(mpath, encoding="utf-8") as f:
            cm = json.load(f)

    text = render(data, tier, cm, os.path.abspath(args.corpus))
    outd = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(outd, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text + "\n")
    print("wrote %s — score %d/100, %d findings, tier=%s (%s)"
          % (args.out, score(data.get("findings") or []),
             len(data.get("findings") or []), tier["tier"], tier["reason"]))


if __name__ == "__main__":
    main()
