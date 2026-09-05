<!-- source=target-sdk clause=why-target-newer-sdks url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-05T02:02:46+00:00 -->

## Why target newer SDKs?

Every new Android version introduces changes that bring security and performance
improvements and enhance the Android user experience. Some of these changes only
apply to apps that explicitly declare support through their `targetSdkVersion`
manifest attribute (also known as the target API level).

Configuring your app to target a recent API level ensures that users can benefit
from these improvements, while your app can still run on older Android versions.
Targeting a recent API level also allows your app to take advantage of the
platform's latest features to delight your users. Furthermore, as of
Android 10 (API level 29), users [see a warning](/about/versions/10/behavior-changes-all#low-target-sdk-warnings) when they start an app for
the first time if the app targets Android 5.1 (API level 22) or lower.

This document highlights important points you need to know in updating your
target API level to meet the [Google Play requirement](https://support.google.com/googleplay/android-developer/answer/11926878). See the instructions
in the following sections, depending on which version you are migrating to.
