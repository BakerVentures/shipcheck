<!-- source=prepare-for-release clause=build-your-app-for-release url=https://developer.android.com/studio/publish/preparing fetched=2026-09-04T15:48:37+00:00 -->

## Build your app for release

After you finish configuring your app, you can build it into a release-ready
APK file that is signed and optimized. The JDK includes the tools for signing
the APK file (Keytool and Jarsigner); the Android SDK includes the tools for
compiling and optimizing the APK file. If you are using Android Studio or you
are using the Gradle build system from the command line, you can automate the
entire build process. For more information about configuring Gradle builds, see
[Configure build
variants](/tools/building/configuring-gradle).

If you are using a [continuous integration
system](/studio/projects/continuous-integration), you can configure a task to automate your release process. This is
not limited to building your release APK or AAB. You can also configure it to
automatically upload the build artifact(s) to Play Console.
