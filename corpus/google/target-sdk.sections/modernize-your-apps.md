<!-- source=target-sdk clause=modernize-your-apps url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-04T07:14:18+00:00 -->

## Modernize your apps

As you update the target API level for your apps, consider adopting recent
platform features to modernize your apps and delight your users.

- Consider using [CameraX](/camerax), which is in Beta, to make the most of using
- Use [Jetpack](/jetpack) components to help you follow best practices, free you
- Use [Kotlin](/kotlin) to write better apps faster, and with less code.
- Ensure you are following [privacy](/privacy) requirements and best practices.
- Add [dark theme](/guide/topics/ui/look-and-feel/darktheme) support to your apps.
- Add [gesture navigation](/guide/navigation/gesturenav) support to your apps.
- [Migrate your app](https://developers.google.com/cloud-messaging/android/android-migrate-fcm) from Google Cloud Messaging (GCM) to the latest
- Take advantage of advanced window management.
  Support larger aspect ratios (more than 16:9) to take advantage of
  recent advances in hardware. Ensure that your app resizes to fill the
  available screen space. Only declare a maximum aspect ratio as a last
  resort. For more information about maximum aspect ratios, see [Declare
  Restricted Screen Support](/guide/practices/screens-distribution#MaxAspectRatio).
  Add [multi-window support](/guide/topics/ui/multi-window) to help your app increase productivity,
  and to manage [multiple displays](/about/versions/oreo/android-8.0#mds).
  If a great minimized app experience would improve the user experience,
  add support for [Picture-in-Picture](/guide/topics/ui/picture-in-picture).
  - Optimize for devices with display cutout.
  - Don't assume status bar height. Instead, use [`WindowInsets`](/reference/kotlin/android/view/WindowInsets)
  - Don't assume that the app has the entire window. Instead, confirm
