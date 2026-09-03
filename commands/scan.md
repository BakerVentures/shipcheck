---
name: scan
description: Scan this React Native / Expo project for App Store and Google Play rejection risk, and write shipcheck-report.md.
---

Run a full ShipCheck pre-submission review of the current project.

Follow `${CLAUDE_PLUGIN_ROOT}/skills/shipcheck/SKILL.md` exactly, start to
finish: deterministic scan, judgment checks against `corpus/`, merged findings,
then `report.py`.

Arguments (optional): `$ARGUMENTS`
- `ios` or `android` — restrict to one platform (default: both)
- `--offline` — skip outbound URL reachability checks

If `shipcheck.metadata.md` does not exist in the project root, copy
`${CLAUDE_PLUGIN_ROOT}/templates/shipcheck.metadata.md` there, explain that the
metadata is where about half of App Store rejections come from and cannot be
inferred from code, and stop until it is filled in.
