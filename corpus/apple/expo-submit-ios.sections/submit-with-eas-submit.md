<!-- source=expo-submit-ios clause=submit-with-eas-submit url=https://docs.expo.dev/submit/ios/ fetched=2026-09-03T19:55:49+00:00 -->

## Submit with `eas submit`

Once the build is ready, submit it to the Apple App Store:

Terminal

-

eas

submit

--platform

ios

The command will walk you through selecting a build, prompt for your Apple ID on first run, and upload the binary to App Store Connect. The build appears in [TestFlight](/submit/testflight) after processing (usually 10-15 minutes). To release to production, log in to [App Store Connect](https://appstoreconnect.apple.com/) and submit the build for App Review.
