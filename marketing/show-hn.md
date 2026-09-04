# Show HN post

Title (under 80 chars):
Show HN: Shipcheck – catch App Store rejections in React Native/Expo apps before submitting

URL: https://github.com/BakerVentures/shipcheck

First comment (post immediately after submitting, from the same account):

I build a subscription iOS app in Expo. The rejection that actually cost me a review cycle was paywall copy -- fake-discount pricing that got flagged because the price on the button has to be the real one, not a struck-through inflated anchor. Nothing about that was visible from my JavaScript, and it's exactly the kind of thing that's easy to miss when you're not the one reading the guidelines line by line.

Shipcheck is a Claude Code plugin that reads the project (app.json, plist, entitlements, the PrivacyInfo.xcprivacy of every package in node_modules, AndroidManifest) plus a short file describing the store listing, and checks all of it against the App Store Review Guidelines and Google Play policies. The guidelines are fetched live and cached with a hash, so /shipcheck:refresh shows you a diff of what Apple changed since your last scan. Each finding cites the clause, quotes the current text, and gives the fix.

It runs in your own Claude Code session, so your code stays on your machine and there's no per-scan cost to me, which is why every app gets a free scan, not just a one-time trial.

Limitations, honestly: it can't run your app, so it won't catch crashes (guideline 2.1) or judge whether your app is "minimum functionality" beyond structural signals. It's best on RN/Expo; native Swift projects work with less depth. And it's a judgment tool, not a guarantee.

Happy to answer questions about how the corpus chunking works or what rejections it does and doesn't catch.

Rules for the day:
- Post Tue–Thu, 9–11am ET.
- Reply to every comment within an hour for the first six hours.
- Do not ask anyone to upvote. Do not post the HN link anywhere else the same day.
