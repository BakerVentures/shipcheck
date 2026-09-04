# X launch thread

1/ The App Store rejection that actually cost me a review cycle was paywall copy: fake-discount pricing, flagged because the price on the button has to be the real one. Not something I'd have caught reading my own JavaScript.

So I built the check I wished I'd had.

2/ shipcheck is a Claude Code plugin. Run /shipcheck:scan in your RN/Expo repo and it reads app.json, plists, entitlements, every SDK's PrivacyInfo.xcprivacy, and your listing metadata, then checks all of it against the App Store guidelines.

[GIF: docs/demo/shipcheck-scan.gif -- real output, not staged]

3/ Every finding gives you the clause, the current guideline text, what the reviewer will say, and the fix. Not "review privacy settings." The actual key to add and the actual reason code.

4/ Guidelines are fetched live and hashed. /shipcheck:refresh shows a diff of what Apple changed since your last scan. Nobody else is watching that page for you.

5/ Already rejected? /shipcheck:reply takes the Resolution Center message and drafts the response in the register reviewers respond to.

[GIF: docs/demo/shipcheck-reply.gif]

6/ It runs inside your own Claude Code. Your code stays on your machine. That also means it costs me nothing per scan, so every app gets a free scan, not just a one-time trial.

$29 per app after that, $49/yr unlimited.

/plugin marketplace add BakerVentures/shipcheck

Post the GIF in tweet 2, not tweet 1. Pin the thread. Reply to every response for 48 hours.
