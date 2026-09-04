<!-- source=expo-submit-android clause=build-a-production-app url=https://docs.expo.dev/submit/android/ fetched=2026-09-04T07:14:19+00:00 -->

## Build a production app

You need a production .aab (Android App Bundle) to submit. Google Play requires new apps to be published as app bundles instead of .apk files, and generates optimized APKs for each device from the bundle. Create one with [EAS Build](/build/introduction):

Terminal

`-` `eas build --platform android --profile production`

Alternatively, build on your own computer with `eas build --platform android --profile production --local` or with Android Studio.

The default `production` profile produces a .aab. A build profile only produces a .apk when it sets [`android.buildType`](/eas/json#buildtype) to `apk`, which is useful for [installing on an emulator or device](/build-reference/apk) but cannot be submitted to the Google Play Store.
