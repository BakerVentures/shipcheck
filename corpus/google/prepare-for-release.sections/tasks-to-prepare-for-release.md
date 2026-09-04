<!-- source=prepare-for-release clause=tasks-to-prepare-for-release url=https://developer.android.com/studio/publish/preparing fetched=2026-09-04T15:48:37+00:00 -->

## Tasks to prepare for release

To release your app to users, you need to create a release-ready package that
users can install and run on their Android-powered devices. The release-ready
package contains the same components as the debug APK file—compiled source
code, resources, manifest file, and so on—and is built using the same build
tools. However, unlike the debug APK file, the release-ready APK file is signed
with your own certificate and is optimized with the `zipalign`
tool.

**Figure 2.** There are five main tasks to prepare your app for
release.

The signing and optimization tasks are usually seamless if you are building
your app with Android Studio. For example, you can use Android Studio with the
Gradle build files to compile, sign, and optimize your app all at once. You can
also configure the Gradle build files to do the same when you build from the
command line. For more details about using the Gradle build files, see [Configure your build](/studio/build).

To prepare your app for release, you typically perform five main tasks, as
shown in figure 2. Each main task may include one or more smaller tasks,
depending on how you are releasing your app. For example, if you are releasing
your app through Google Play, you may want to add special filtering rules to
your manifest while you are configuring your app for release. Similarly, to
meet Google Play publishing guidelines you may have to prepare screenshots and
create promotional text while you are gathering materials for release.

You usually perform the tasks listed in figure 2 after you have thoroughly
debugged and tested your app. The Android SDK contains several tools to help
you test and debug your Android apps. For more information, see [Debug your app](/tools/debugging) and [Test your app](/tools/testing).
