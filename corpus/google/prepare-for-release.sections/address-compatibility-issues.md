<!-- source=prepare-for-release clause=address-compatibility-issues url=https://developer.android.com/studio/publish/preparing fetched=2026-09-04T15:48:37+00:00 -->

### Address compatibility issues

Android provides several tools and techniques to make your app compatible
with a wide range of devices. To make your app available to the largest number
of users, consider doing the following:

Add support for multiple screen configurations. Make sure you meet the best practices for
[supporting multiple screens](/guide/practices/screens_support#screen-independence). By supporting multiple screen configurations,
you can create an app that functions properly and looks good on any of the screen sizes
supported by Android. Optimize your app for larger displays. You can optimize your app to work well on devices with large displays
such as tablets and foldables. For example, [list-detail layouts](/guide/topics/large-screens/large-screen-canonical-layouts#list-detail) can improve usability on larger screens. Consider using Jetpack libraries. Jetpack is a suite of libraries to help developers follow best
practices, reduce boilerplate code, and write code that works consistently
across Android versions and devices.
