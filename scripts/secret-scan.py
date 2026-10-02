#!/usr/bin/env python3
"""secret-scan.py -- block credentials before they reach a commit.

Why this exists, and why it is not just gitleaks
------------------------------------------------
The 2026-10-01 Baker Ventures secrets sweep found 14 real credential exposures
across 37 repos. gitleaks 8.30.1, run over full history with its default
ruleset, found 2 of them. It missed every single demo-account password, because
its rules target vendor-prefixed tokens (ghp_, sk-ant-, AKIA, AIza) and the
things that actually leaked here were:

  1. assignment-shaped literals --  DEMO_PASSWORD = "...."  in a seed script
  2. credentials written into prose -- "the review account password is ...."
     in a markdown launch doc

A gitleaks-only gate would have passed all 14. So this scanner leads with (1)
and (2) and keeps the vendor-token shapes as a third rule, not the first.

It never prints a value it finds. Findings are reported as path:line plus the
*shape* of the value (length, Shannon entropy, character classes) -- the same
discipline the sweep report itself used, for the same reason: a tool that
quotes the secret it caught has copied it somewhere new.

Usage
-----
  secret-scan.py --staged        scan what is staged (the pre-commit use)
  secret-scan.py --stdin LABEL   scan piped content (a historical blob, no disk copy)
  secret-scan.py --tracked       scan every tracked file (audit / CI use)
  secret-scan.py FILE [FILE...]  scan specific files
  secret-scan.py --self-test     prove the rules fire on built-in fixtures

Exit status: 0 = clean, 1 = findings (block), 2 = usage error.

Wiring it up as a commit gate
-----------------------------
The intended use is a pre-commit gate that runs `secret-scan.py --staged` and
aborts the commit on a non-zero exit. That installation step is NOT done by this
file and was NOT done by the worker that added it: installing a git hook is
ASK-tier under rules/hard-constraints.md, and guard.sh refused it verbatim --
"BLOCKED (ASK tier): workers do not edit shell startup files or git hooks". It is
queued for Ryan in ryan-queue.md instead of being routed around.

Until that is installed, this is a manual/CI gate. Both of these work today and
neither needs any approval:

    python3 scripts/secret-scan.py --staged     # before you commit
    python3 scripts/secret-scan.py --tracked    # audit the whole repo
    python3 scripts/secret-scan.py --self-test  # prove the rules still fire

Allowlisting
------------
Two ways, both deliberate and both auditable:
  * put `secret-scan:allow` in a comment on the offending line, or
  * add a line to `.secret-scan-allow` in the repo root: `<glob>` to skip a
    path, or `<glob>:<line>` to skip one line of one path.
Blank lines and `#` comments are ignored there.
"""
from __future__ import annotations

import fnmatch
import math
import os
import re
import subprocess
import sys
from collections import Counter

ALLOW_MARKER = "secret-scan:allow"
ALLOW_FILE = ".secret-scan-allow"

# Words that introduce a credential. Two deliberate narrowings, both from tuning
# against four real repos rather than from guessing:
#   * "pass" must carry a suffix. A bare `pass` is the English verb, and it was
#     the sole cause of all 19 false positives in the first tuning run
#     ("stress-test pass", "compliance pass", "pass --auto-submit", "the judgment
#     pass", "signInWithPassword" is fine but "pass X" is not).
#   * "key" alone is never a keyword: keyExtractor, object keys, keyboard.
KEYWORD = (
    r"(?:pass(?:word|wd|phrase|code)|pwd|secret|api[_-]?key|apikey|auth[_-]?token|"
    r"access[_-]?token|refresh[_-]?token|client[_-]?secret|access[_-]?key|"
    r"private[_-]?key|service[_-]?role(?:[_-]?key)?|anon[_-]?key|credential)"
)

RULES: list[tuple[str, re.Pattern[str]]] = [
    # 1. assignment to a quoted literal:  PASSWORD = "...."   password: '....'
    ("assign-literal", re.compile(
        r"(?i)" + KEYWORD + r"[A-Za-z0-9_]*\s*(?:=|:|=>|:=)\s*[\"'`]([^\"'`\n]{6,120})[\"'`]")),
    # 2. unquoted assignment:  PASSWORD=....   (shell, dotenv, CI yaml)
    ("assign-bare", re.compile(
        r"(?i)(?:^|[\s;&|({\[,])" + KEYWORD + r"[A-Za-z0-9_]*\s*=\s*([^\s\"'`,;)\]}\n]{8,120})")),
    # 3. command-line flag:  --password hunter2 / --password=hunter2  # secret-scan:allow
    ("cli-flag", re.compile(
        r"(?i)--" + KEYWORD + r"[A-Za-z0-9_-]*[= ]([^\s\"'`\n]{6,120})")),
    # 4a. prose with an explicit separator:  "Password: ....", "- password = ...."
    #     This is the shape of the markdown leak gitleaks missed. The separator is
    #     REQUIRED -- without it the rule degenerates into "keyword followed by the
    #     next English word", which is exactly how the first version flagged 19
    #     clean lines.
    ("prose-colon", re.compile(
        r"(?i)\b" + KEYWORD + r"[A-Za-z0-9_]*[ \t]*[:=][ \t]*"
        r"[`\"']?([^\s,;:)`\"'\n]{6,120})[`\"']?")),
    # 4b. prose with a copula, allowing a few words of filler in between:
    #     "the App Review demo account password is ....".
    ("prose-verb", re.compile(
        r"(?i)\b" + KEYWORD + r"\b(?:[ \t]+(?:for|of|on|to|the|a|an|this|that|demo|"
        r"review|test|account|user|login|sandbox)){0,6}[ \t]+(?:is|was)[ \t]+"
        r"[`\"']?([^\s,;:)`\"'\n]{6,120})[`\"']?")),
    # 5. vendor-prefixed tokens (the gitleaks-shaped half).
    ("vendor-token", re.compile(
        r"(?<![A-Za-z0-9_])("
        r"sk-ant-[A-Za-z0-9_-]{16,}"
        r"|sk-[A-Za-z0-9]{32,}"
        r"|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|ghs_[A-Za-z0-9]{20,}"
        r"|github_pat_[A-Za-z0-9_]{20,}"
        r"|xox[baprs]-[A-Za-z0-9-]{10,}"
        r"|AKIA[0-9A-Z]{16}"
        r"|AIza[0-9A-Za-z_-]{30,}"
        r"|sbp_[a-f0-9]{40,}"
        r"|SG\.[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}"
        r"|rk_(?:live|test)_[A-Za-z0-9]{16,}|sk_(?:live|test)_[A-Za-z0-9]{16,}"
        r"|phc_[A-Za-z0-9]{32,}"
        r"|eyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}"
        r")")),
    # 6. private key blocks, in any file type.
    ("private-key-block", re.compile(
        r"(-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----)")),
]

# A captured value that looks like any of these is a reference or a placeholder,
# not a credential. Entries marked below with a real-FP note came from an actual
# false positive while tuning against rigsheet, hormonelog, shipcheck and
# hormonelog-legal; the rest are anticipatory shapes for value types this
# portfolio handles (dotenv placeholders, 1Password refs, env lookups).
NOT_A_SECRET = [
    re.compile(r"(?i)^(?:x{3,}|\*{3,}|\.{3,}|-{3,}|_{3,})"),          # xxxx / ****
    re.compile(r"^<.*>$"),                                             # <your-key>
    re.compile(r"^\$"),                                                # $VAR ${VAR}
    re.compile(r"\$\{"),                                               # `Bearer ${t}`
    re.compile(r"(?i)^(?:your|my|the|a|an|some|new|old|same|real|valid|invalid)[-_ ]"),
    re.compile(r"(?i)^(?:changeme|placeholder|example|redacted|dummy|sample|todo|tbd|"
               r"null|none|nil|undefined|true|false|empty|unset|omitted|hidden|"
               r"required|optional|string|number|boolean|object)$"),
    re.compile(r"(?i)^op://"),                                         # 1Password ref
    re.compile(r"(?i)(?:process\.env|import\.meta\.env|Deno\.env|os\.environ|"
               r"getenv|ENV\[|System\.getenv|Platform\.select|Constants\.|"
               r"expoConfig|require\(|import\()"),
    re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)+"),  # a.b.c
    re.compile(r"^(?:/|\./|~/|[A-Za-z0-9_.-]+/)"),                     # a path
    re.compile(r"(?i)^https?://"),
    re.compile(r"^[^A-Za-z0-9]+$"),                                    # punctuation only
    re.compile(r"(?i)^(?:keychain|1password|op|env|environment|file|vault)$"),
    # A value that announces itself as a fixture. `test-anon-key` in a vi.mock()
    # block is the real case this came from (rigsheet
    # apps/mobile/src/lib/purchases.test.ts). The marker must be a delimited
    # component, so `testing123` as a password is still caught -- and the tradeoff
    # is stated plainly: a credential that genuinely contains "-test-" or "_mock_"
    # will be missed, which is an acceptable price for a gate developers do not
    # route around. Real Supabase anon keys are JWTs and are caught by the
    # vendor-token rule regardless.
    re.compile(r"(?i)(?:^|[-_.])(?:test|mock|fake|dummy|fixture|sample|stub)(?:[-_.]|$)"),
]

# These disqualify a value ONLY when it was not captured from inside a quoted
# string literal. A bare identifier next to `password:` is a *reference* to the
# value; the same characters inside quotes are the value itself.
#
# This distinction is not theoretical. The first version of this scanner missed a
# real 20-character credential in rigsheet's history -- `const ..._PASSWORD =
# "...."` -- because the value was a hyphenated word-style passphrase and the
# "plain word" rule discarded it. Word-shaped passwords are the normal case for a
# human-typed demo account, so a quoted literal in a credential slot is reported
# regardless of how word-like it looks.
NOT_A_SECRET_UNQUOTED = [
    re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+$"),                    # UPPER_SNAKE name
    re.compile(r"^[a-z]+(?:[A-Z][a-z0-9]*)+$"),                        # camelCaseName  (real FP)
    re.compile(r"^[A-Za-z]+(?:[-\u2019'][A-Za-z]{1,12})*$"),            # a plain word   (real FP)
    re.compile(r"^</?[A-Za-z]"),                                       # </Text> markup (real FP)
    re.compile(r"^[<>{}\[\]()]"),                                      # stray bracket  (real FP)
]

# Kinds whose captured value came from inside a quoted string literal.
QUOTED_KINDS = {"assign-literal"}

# Extensions with no plausible credential content, plus lockfiles and corpora.
SKIP_PATH = [
    "*.lock", "*-lock.json", "*.lockb", "package-lock.json", "yarn.lock",
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.ico", "*.pdf", "*.mp4",
    "*.mov", "*.zip", "*.gz", "*.tgz", "*.woff", "*.woff2", "*.ttf", "*.otf",
    "*.svg", "node_modules/*", "*/node_modules/*", "*.min.js", "*.map",
]

# A plain English word, including possessives written with either apostrophe
# (U+2019 is what a markdown editor actually inserts) and hyphenated compounds.
WORDISH = re.compile(r"^[A-Za-z]+(?:[-\u2019'][A-Za-z]{1,12})*$")


def entropy(s: str) -> float:
    counts = Counter(s)
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def char_classes(s: str) -> str:
    return (("u" if re.search(r"[A-Z]", s) else "")
            + ("l" if re.search(r"[a-z]", s) else "")
            + ("d" if re.search(r"\d", s) else "")
            + ("p" if re.search(r"[^A-Za-z0-9]", s) else ""))


def is_reference_or_placeholder(value: str, kind: str) -> bool:
    if any(rx.search(value) for rx in NOT_A_SECRET):
        return True
    if kind not in QUOTED_KINDS:
        return any(rx.search(value) for rx in NOT_A_SECRET_UNQUOTED)
    return False


def credential_shaped(kind: str, value: str) -> bool:
    """Shape test. Deliberately stricter for prose than for assignments."""
    if kind in ("vendor-token", "private-key-block"):
        return True
    if is_reference_or_placeholder(value, kind):
        return False
    if len(value) < 6:
        return False
    ent = entropy(value)
    classes = char_classes(value)
    if kind.startswith("prose"):
        # In prose the capture after a keyword is often just the next English word
        # -- "the database password was Supabase's own auto-generated one" is the
        # exact sentence that the 2026-10-01 sweep reported as a HIGH-severity
        # credential in hormonelog's launch doc. It was not one: the "10-character,
        # entropy 2.92 value" was the word `Supabase's`. So prose findings have to
        # clear a real bar -- an English word is not a credential, and a credential
        # has at least two character classes.
        if WORDISH.match(value):
            return False
        if len(classes) < 2:
            return False
        return ent >= 2.2 and len(value) >= 6
    # Assignment to a literal is already a strong signal: someone wrote a value
    # where a credential belongs. Accept all-letter values here too, because
    # `password = "letmeinnow"` is a real leak.  # secret-scan:allow
    return ent >= 2.0


def load_allowlist(root: str) -> list[tuple[str, int | None]]:
    path = os.path.join(root, ALLOW_FILE)
    entries: list[tuple[str, int | None]] = []
    if not os.path.exists(path):
        return entries
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line and line.rsplit(":", 1)[1].isdigit():
                glob, num = line.rsplit(":", 1)
                entries.append((glob, int(num)))
            else:
                entries.append((line, None))
    return entries


def allowed(path: str, lineno: int, allowlist) -> bool:
    for glob, num in allowlist:
        if fnmatch.fnmatch(path, glob) and (num is None or num == lineno):
            return True
    return False


def skip_path(path: str) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in SKIP_PATH)


def scan_text(path: str, text: str, allowlist) -> list[str]:
    out = []
    seen: set[tuple[int, str]] = set()
    for lineno, line in enumerate(text.split("\n"), 1):
        if len(line) > 2000 or ALLOW_MARKER in line:
            continue
        if allowed(path, lineno, allowlist):
            continue
        for kind, rx in RULES:
            for match in rx.finditer(line):
                value = match.group(1).rstrip("\u2019\u201d\u2018\u201c.,;:!?)")
                if not credential_shaped(kind, value):
                    continue
                key = (lineno, kind)
                if key in seen:
                    continue
                seen.add(key)
                ent = "n/a" if kind == "private-key-block" else f"{entropy(value):.2f}"
                out.append(
                    f"{path}:{lineno}  [{kind}]  len={len(value)} entropy={ent} "
                    f"classes={char_classes(value) or '-'}")
    return out


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          check=False).stdout


def repo_root() -> str:
    root = git("rev-parse", "--show-toplevel").strip()
    return root or os.getcwd()


def staged_files() -> list[str]:
    out = git("diff", "--cached", "--name-only", "--diff-filter=ACM", "-z")
    return [p for p in out.split("\0") if p]


def read_staged(path: str) -> str | None:
    res = subprocess.run(["git", "show", f":{path}"], capture_output=True, check=False)
    if res.returncode != 0:
        return None
    try:
        return res.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def read_disk(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (OSError, UnicodeDecodeError):
        return None


SELF_TEST_FIXTURES = [
    # (fixture text, must_be_flagged, label)
    ('const DEMO_PASSWORD = "Tr0ub4dor&3xyz";', True, "assignment literal"),  # secret-scan:allow
    ('The App Review demo account password is Tr0ub4dor&3xyz until rotated.',  # secret-scan:allow
     True, "credential in prose"),
    ('- Password: Tr0ub4dor&3xyz', True, "markdown bullet disclosure"),  # secret-scan:allow
    ('ANTHROPIC_API_KEY=sk-ant-api03-AAAAAAAAAAAAAAAAAAAAAAAA', True, "vendor token"),  # secret-scan:allow
    ('psql --password Tr0ub4dor&3xyz', True, "cli flag"),  # secret-scan:allow
    ('-----BEGIN PRIVATE KEY-----', True, "private key block"),  # secret-scan:allow
    ('const password = process.env.DEMO_PASSWORD;', False, "env reference"),
    ('password: DEMO_PASSWORD,', False, "constant reference"),
    ('The database password was Supabase’s own auto-generated one.', False,
     "prose: next word is English"),
    ('The database password was Supabase\'s own auto-generated one.', False,  # secret-scan:allow
     "prose: next word is English (ascii apostrophe)"),
    ('headers: { Authorization: `Bearer ${token}` },', False, "template literal"),
    ('api_key: posthogKey,', False, "camelCase reference"),
    ('PASSWORD=changeme', False, "placeholder"),
    ('password: "op://Private/demo/password"', False, "1Password reference"),
    ('DEMO_PASSWORD="xxxxxxxxxxxx"', False, "masked placeholder"),
    ("supabaseAnonKey: 'test-anon-key',", False, "declared test fixture"),
    ('const DEMO_PASSWORD = "testing123xyz";', True,  # secret-scan:allow
     "fixture marker must be delimited, not a substring"),
    ('const DEMO_PASSWORD = "correct-horse-batter";', True,  # secret-scan:allow
     "passphrase-style literal (the shape missed on the first tuning pass)"),
    ("password: DEMO_PASSWORD,", False, "UPPER_SNAKE reference"),
]


def self_test() -> int:
    failures = 0
    print("secret-scan self-test (no real credentials; fixtures are synthetic)")
    for text, should_flag, label in SELF_TEST_FIXTURES:
        hits = scan_text("<fixture>", text, [])
        flagged = bool(hits)
        ok = flagged == should_flag
        if not ok:
            failures += 1
        print(f"  [{'ok  ' if ok else 'FAIL'}] expect={'BLOCK ' if should_flag else 'pass  '} "
              f"got={'BLOCK ' if flagged else 'pass  '}  {label}")
    print(f"  {len(SELF_TEST_FIXTURES) - failures}/{len(SELF_TEST_FIXTURES)} fixtures behaved as specified")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--self-test":
        return self_test()

    root = repo_root()
    allowlist = load_allowlist(root)
    findings: list[str] = []

    if argv[0] == "--stdin":
        # Scan content piped in, e.g. `git cat-file blob <sha> | secret-scan.py --stdin <label>`.
        # Lets a historical blob be checked without ever writing it to disk.
        label = argv[1] if len(argv) > 1 else "<stdin>"
        findings += scan_text(label, sys.stdin.read(), allowlist)
    elif argv[0] == "--staged":
        for path in staged_files():
            if skip_path(path):
                continue
            text = read_staged(path)
            if text is not None:
                findings += scan_text(path, text, allowlist)
    elif argv[0] == "--tracked":
        for path in [p for p in git("ls-files", "-z").split("\0") if p]:
            if skip_path(path):
                continue
            text = read_disk(os.path.join(root, path))
            if text is not None:
                findings += scan_text(path, text, allowlist)
    else:
        for path in argv:
            text = read_disk(path)
            if text is not None:
                findings += scan_text(path, text, allowlist)

    if not findings:
        return 0

    print("BLOCKED: credential-shaped values found.", file=sys.stderr)
    print("", file=sys.stderr)
    for line in findings:
        print("  " + line, file=sys.stderr)
    print("", file=sys.stderr)
    print("No value is printed above, by design -- a scanner that quotes the secret it "
          "caught has copied it somewhere new.", file=sys.stderr)
    print("Fix the line, do not just delete it from the tip: read the value from the "
          "environment or the macOS Keychain (`jarvis/<name>`).", file=sys.stderr)
    print("If the value is already in a pushed commit, removing it here does NOT remove "
          "it from history -- it still needs rotating.", file=sys.stderr)
    print(f"False positive? Add `{ALLOW_MARKER}` in a comment on the line, or an entry in "
          f"{ALLOW_FILE} (`path/glob` or `path/glob:line`).", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
