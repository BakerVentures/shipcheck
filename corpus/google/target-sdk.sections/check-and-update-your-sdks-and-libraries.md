<!-- source=target-sdk clause=check-and-update-your-sdks-and-libraries url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-04T16:10:14+00:00 -->

## Check and update your SDKs and libraries

Make sure that your third-party SDK dependencies support API 31: Some SDK
providers publish it in their manifest; others will require additional
investigation. If you use an SDK that doesn't support API 31, make it a priority
to work with the SDK provider to resolve the issue.

Additionally, note that your app or game's `targetSdkVersion` may restrict
access to private Android platform libraries; see [NDK Apps Linking to Platform
Libraries](/about/versions/nougat/android-7.0-changes#ndk) for details.

You should also verify any restrictions that may exist in the version of the
Android Support Library that you're using. As always, you must ensure
compatibility between the major version of Android Support Library and your
app's `compileSdkVersion`.

We recommend that you choose a `targetSdkVersion` smaller than or equal to the
Support Library's major version. We encourage you to update to a recent
compatible Support Library in order to take advantage of the latest
compatibility features and bug fixes.
