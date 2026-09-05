<!-- source=prepare-for-release clause=review-and-update-your-manifest-and-gradle-build-settings url=https://developer.android.com/studio/publish/preparing fetched=2026-09-05T02:02:42+00:00 -->

### Review and update your manifest and Gradle build settings

Verify that the following manifest and build files items are set
correctly:

- `[<uses-permission>](/guide/topics/manifest/uses-permission-element)` element
- `android:icon` and `android:label` attributes
- `versionCode` and `versionName` properties

There are several additional build file elements that you can set if you
are releasing your app on Google Play. For example, the `minSdk` and
`targetSdk` attributes, which are located in the app module-level
`build.gradle` or `build.gradle.kts` file. For more
information about these and other Google Play settings, see [Filters on Google Play](/google/play/filters).
