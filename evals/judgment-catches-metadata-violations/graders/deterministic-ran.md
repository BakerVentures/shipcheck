---
type: llm
weight: 1
---

The agent should have actually run `scripts/scan.py` (or the `bin/shipcheck`
CLI) rather than hand-writing findings from imagination, and the resulting
report should include these deterministic findings, which the script always
produces on this fixture: a missing Sign in with Apple option alongside
third-party login (guideline 4.8), the app icon having an alpha channel, and
no in-app account deletion despite the app having accounts (5.1.1(v)).

Score 1 if the report contains all three. Score 0 if any is missing, or if the
report looks hand-written rather than script-derived (e.g. no risk score, no
severity levels, generic findings not matching the fixture's actual content).
