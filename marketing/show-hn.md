# Show HN post

Title (under 80 chars):
Show HN: Shipcheck – catch App Store rejections in React Native/Expo apps before submitting

URL: https://github.com/BakerVentures/shipcheck

First comment (post immediately after submitting, from the same account):

I build a subscription iOS app in Expo and got rejected three times on the same release: once for a missing privacy manifest in a transitive SDK, once because my paywall showed the price but not the renewal period, and once because a screenshot showed a feature that was behind a flag in that build. None of those were visible from my JavaScript.

Shipcheck is a Claude Code plugin that reads the project (app.json, plist, entitlements, the PrivacyInfo.xcprivacy of every package in node_modules, AndroidManifest) plus a short file describing the store listing, and checks all of it against the App Store Review Guidelines and Google Play policies. The guidelines are fetched live and cached with a hash, so /shipcheck:refresh shows you a diff of what Apple changed since your last scan. Each finding cites the clause, quotes the current text, and gives the fix.

It runs in your own Claude Code session, so your code stays on your machine and there's no per-scan cost to me, which is why every app gets a free scan, not just a one-time trial.

Limitations, honestly: it can't run your app, so it won't catch crashes (guideline 2.1) or judge whether your app is "minimum functionality" beyond structural signals. It's best on RN/Expo; native Swift projects work with less depth. And it's a judgment tool, not a guarantee.

Happy to answer questions about how the corpus chunking works or what rejections it does and doesn't catch.

Rules for the day:
- Post Tue–Thu, 9–11am ET.
- Reply to every comment within an hour for the first six hours.
- Do not ask anyone to upvote. Do not post the HN link anywhere else the same day.
