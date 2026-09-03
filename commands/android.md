---
name: android
description: Google Play-only rejection-risk scan (Data safety, permissions, target API, testing gate).
---

Run a ShipCheck review restricted to Google Play.

Follow `${CLAUDE_PLUGIN_ROOT}/skills/shipcheck/SKILL.md`, but pass
`--platform android` to `scan.py` and limit judgment checks to the Play
sections: Data safety vs declared permissions, prominent disclosure, sensitive
permission declarations, target API level, foreground service types, account
deletion (including the web-accessible route Play requires and Apple does not),
Play Billing disclosures, and the closed-testing gate for new personal
developer accounts.

Read the current tester count and duration out of
`corpus/google/testing-requirements.md`. Do not quote those numbers from memory —
they have changed before.
