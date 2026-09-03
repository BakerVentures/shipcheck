---
name: shipcheck
description: >-
  Check a React Native or Expo app for App Store / Google Play rejection risk
  before submitting. Scans the project and the developer's store-listing
  metadata, cites the exact guideline clause from a locally cached copy of
  Apple and Google policy, and gives the file-level fix. Use when the user is
  about to submit an app, was just rejected, or asks whether their app will
  pass review.
---

# ShipCheck

You are running a pre-submission review of an app the way an App Review or Play
policy reviewer would, and producing a report the developer can act on line by
line.

`${CLAUDE_PLUGIN_ROOT}` is the plugin root. Everything below is relative to it.

## The one rule that matters

**Never state a guideline requirement from memory.** Every policy claim must come
from `corpus/`, which was fetched from Apple and Google and carries a fetch date
and hash. Apple and Google change these pages constantly; a confidently wrong
clause number is worse than no report, because the developer will paste it into
a Resolution Center reply.

If you need a rule that is not in `corpus/`, say so in the report's *Not checked*
section instead of filling the gap from memory.

`corpus/patterns/rn-expo-rejections.md` is the exception: it is hand-curated and
tells you *what to look for*. Use it to direct the search, never as the citation.

## Step 1 — deterministic scan

Run it first. It resolves everything a script can decide, so you spend your
reasoning on the parts that need judgment.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/scan.py" \
  --project . --platform both --out .shipcheck/scan.json
```

Read `.shipcheck/scan.json`. It has three keys:

- `facts` — dependencies, Info.plist keys, permissions, icon, metadata fields,
  target SDK. This is your ground truth about the project. Do not re-derive it.
- `findings` — deterministic findings, already carrying clause, evidence and fix.
  Keep them. Do not rewrite their fixes unless something is wrong.
- `gaps` — what could not be verified (no `node_modules`, dynamic
  `app.config.js`). These must appear in the report as *Not checked*. Never
  silently treat a gap as a pass.

If `facts.metadata_present` is false, copy `templates/shipcheck.metadata.md` to
the project root, tell the user to fill it in, and stop. Roughly half of App
Store rejections are metadata problems that are invisible from the code, so a
scan without it is not worth delivering.

## Step 2 — judgment checks

For each area below, read the relevant corpus file, then look at the actual
project. Add findings the script cannot reach.

Work through `corpus/patterns/rn-expo-rejections.md` and handle every entry
marked `detect: judgment`. The high-value ones:

| Area | Read from corpus | Look at |
|---|---|---|
| Metadata accuracy (2.3.x) | `apple/asrg.sections/2.3*.md` | description, keywords, What's New, screenshot descriptions |
| Paywall disclosure (3.1.2) | `apple/asrg.sections/3.1.2*.md`, `apple/subscriptions.md`, `apple/hig-in-app-purchase.md` | the `Paywall` + `Subscriptions` metadata, and the paywall component in source |
| Minimum functionality (4.2) | `apple/asrg.sections/4.2*.md` | dependency list, route count, whether `react-native-webview` carries the app |
| Login services (4.8) | `apple/asrg.sections/4.8.md` | check the exemptions before asserting |
| Privacy labels vs SDKs | `apple/app-privacy-details.md`, `apple/describing-data-use.md` | analytics/attribution SDKs vs the `Data collected` field |
| Listed SDKs | `apple/third-party-sdk-requirements.md` | cross-reference `facts.dependencies` against the live SDK list |
| Category rules | `apple/asrg.sections/1.1*.md`, `1.4.1`, `5.1.3`, `5.1.4`, `5.3` | the declared category and age rating |
| Data safety (Play) | `google/data-safety.md`, `google/user-data-policy.md` | permissions vs declared data |
| Testing gate (Play) | `google/testing-requirements.md` | quote the current tester count and duration from the file, never from memory |

Rules for judgment findings:

- Quote the clause verbatim from the corpus file, and keep the quote short.
- Set `confidence` honestly. `high` only when you can point at specific evidence.
  4.2 minimum-functionality calls are almost never `high`.
- Write `reviewer_says` as the sentence a reviewer would actually send. This is
  the most useful field in the report; it tells the developer what they are
  about to receive.
- Write `fix` as something executable: a file, a key, a snippet, or a rewritten
  string. "Add subscription terms" is useless. Give them the paragraph.
- No speculation. If you cannot see the paywall because the code does not make
  it clear, that is a *Not checked* gap, not a medium-confidence finding.

## Step 3 — record what passes

Build a `passes` list of things you actively checked and found clean. This is
what makes the developer trust the findings, and it is what separates the report
from a generic checklist. Be specific: "Sign in with Apple present via
expo-apple-authentication" beats "login OK".

## Step 4 — merge and render

Write the merged object to `.shipcheck/findings.json`:

```json
{
  "facts":   { ...verbatim from scan.json... },
  "findings": [ ...deterministic findings..., ...your judgment findings... ],
  "passes":  [ { "title": "...", "note": "...", "clause": "..." } ],
  "gaps":    [ ...from scan.json, plus anything you could not verify... ]
}
```

Each judgment finding:

```json
{
  "id": "JUDGE-PAYWALL-TERMS",
  "severity": "critical|high|medium|low",
  "confidence": "high|medium|low",
  "platform": "ios|android|both",
  "clause": "3.1.2c",
  "clause_text": "<verbatim quote from corpus, or omit to have it pulled from disk>",
  "clause_url": "<deep link if you have one>",
  "title": "Paywall does not disclose the renewal period",
  "evidence": "<what you saw, with file paths>",
  "reviewer_says": "<the sentence a reviewer would send>",
  "fix": "<exact change>",
  "blocks": "upload|review|metadata",
  "source": "judgment"
}
```

`blocks` says which wall the developer hits first, and it drives ordering:

- `upload` — App Store Connect refuses the build (icon alpha, privacy manifest,
  export compliance). These come first because nothing else matters until the
  binary is accepted.
- `review` — the build uploads, a human rejects it (4.8, 5.1.1(v), 3.1.2).
- `metadata` — fixable in App Store Connect with **no new build**. Call these out;
  a developer who can fix six things without waiting on a build wants to know.

Omit it and `report.py` infers it from the finding id, which is right often
enough — set it explicitly when you know better.

Omitting `clause_text` is usually better: `report.py` pulls the clause off disk
verbatim, which is guaranteed accurate. Set `clause` to the ASRG number
(`3.1.2c`, `5.1.1v`) or a corpus id (`play:data-safety`, `asc:export-compliance`)
and it resolves automatically.

Then render:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/report.py" \
  --findings .shipcheck/findings.json --out shipcheck-report.md
```

`report.py` computes the score, ranks by rejection likelihood, and applies the
licence tier. Do not compute the score yourself and do not hand-write the
report file.

## Step 5 — tell the user what to do next

In chat, give them: the score, the count by severity, and the three things to
fix first — in the order that unblocks submission fastest. Point at
`shipcheck-report.md` for the rest. Keep it short; the report is the deliverable.

If the report was gated to the free tier, say so plainly once and move on. Do
not editorialise about the paywall.

## Severity calibration

- `critical` — blocks the upload, or a reviewer will almost certainly reject.
  Missing privacy manifest, missing usage description, no Sign in with Apple
  with third-party login, icon with alpha, placeholder metadata, no demo
  account behind a login wall.
- `high` — likely rejection or a guaranteed round trip. Missing restore
  purchases, target SDK below the floor, undeclared sensitive permission.
- `medium` — plausible rejection, often a "please explain" reply. Weak purpose
  strings, ATT timing, missing export compliance.
- `low` — will not get you rejected but is wrong. Keyword formatting.

Do not inflate. A report where everything is critical is a report nobody acts on.
