<!-- source=target-sdk clause=migrate-to-android-8-api-level-26 url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-04T16:10:14+00:00 -->

### Migrate to Android 8 (API level 26)

The following considerations apply to apps targeting Android 8.0 and higher versions of the platform:

- [Background Execution Limits](/about/versions/oreo/background)
  The system restricts services for apps not running in the foreground.
  - [`startService()`](/reference/kotlin/android/content/Context#startService(android.content.Intent)) now throws an exception when an app tries to invoke it while `startService()` is
  - To start foreground services, an app must use [`startForeground()`](/reference/kotlin/android/app/Service#startForeground(int, android.app.Notification)) and
  - Carefully review the changes made to the JobScheduler API, as documented on the Android 8.0 (API level 26) [Behavior Changes page](/about/versions/oreo/android-8.0#jobscheduler).
  - [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging/) requires
  - When using [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging/), message delivery is subject to background execution limits. When background work is necessary upon message receipt, such
  Implicit broadcasts
  - Implicit broadcasts are restricted. For information about handling background events, see the documentation for the [`JobScheduler`](/reference/kotlin/android/app/job/JobScheduler) API.
  Background Location Limits
  - Apps running in the background have limited access to location data.
    On devices with Google Play services, use the [fused location provider](https://developers.google.com/android/reference/com/google/android/gms/location/FusedLocationProviderClient) to get periodic location
    updates.
- [Notification Channels](/about/versions/oreo/android-8.0#notifications) You should define [notification interruption properties](/training/notify-user/channels#importance) on a per-channel basis. You must assign notifications to a channel for the notifications to appear.
  You should define [notification interruption properties](/training/notify-user/channels#importance) on a per-channel basis.
  You must assign notifications to a channel for the notifications to appear.
  This version of the platform supports [`NotificationCompat.Builder`](/reference/kotlin/androidx/core/app/NotificationCompat.Builder).
- [Privacy](/about/versions/oreo/android-8.0-changes#privacy-all) [ANDROID_ID](/reference/kotlin/android/provider/Settings.Secure#ANDROID_ID) is scoped per app signing key.
  [ANDROID_ID](/reference/kotlin/android/provider/Settings.Secure#ANDROID_ID) is scoped per app signing key.

For an exhaustive list of changes introduced in Android 8.0 (API level 26), see the [Behavior Changes](/about/versions/oreo/android-8.0-changes)
page for that version of the platform.
