<!-- source=expo-submit-android clause=first-time-submission url=https://docs.expo.dev/submit/android/ fetched=2026-09-04T07:14:19+00:00 -->

## First-time submission

If this is your app's first submission, the default `eas submit` command works out of the box and creates your app's first release on the [internal testing track](/eas/json#track). Before running it, complete the [prerequisites](/submit/android#prerequisites) so that your app exists on Google Play Console and EAS has a [Google Service Account key](https://expo.fyi/creating-google-service-account) to submit on your behalf. The app stays in draft status in Play Console until you complete the store listing and setup tasks, which are required before a release can be promoted to production.

- Prefer doing the first upload yourself? Follow the [manual submission guide](/submit/android-manual) to create the first release in Play Console.
- Want to upload without rolling out? Set [`releaseStatus`](/eas/json#releasestatus) to `draft` in the submission profile in eas.json, and complete the release in Play Console.
