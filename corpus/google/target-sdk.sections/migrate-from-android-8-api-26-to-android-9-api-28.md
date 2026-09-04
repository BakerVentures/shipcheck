<!-- source=target-sdk clause=migrate-from-android-8-api-26-to-android-9-api-28 url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-04T15:48:40+00:00 -->

### Migrate from Android 8 (API 26) to Android 9 (API 28)

- [Power Management](/about/versions/pie/power) [App Standby buckets](/about/versions/pie/power#buckets) bring new
  [App Standby buckets](/about/versions/pie/power#buckets) bring new
  background restrictions based on app engagement, such as deferred jobs,
  alarms and quotas on high-priority messages
  [Battery saver improvements](/about/versions/pie/power#battery-saver)
  increase the limitations on app standby apps
- [Foreground service permission](/about/versions/pie/android-9.0-changes-28#fg-svc) Need to request the normal permission
  Need to request the normal permission
  [`FOREGROUND_SERVICE`](/reference/kotlin/android/Manifest.permission#FOREGROUND_SERVICE)
  (not runtime permission)
- [Privacy changes](/about/versions/pie/android-9.0-changes-all#privacy-changes-all) [Limited access to background sensors](/about/versions/pie/android-9.0-changes-all#bg-sensor-access) Restricted access to call logs, now in [`CALL_LOG`](/reference/kotlin/android/Manifest.permission_group#CALL_LOG)
  [Limited access to background sensors](/about/versions/pie/android-9.0-changes-all#bg-sensor-access)
  Restricted access to call logs, now in [`CALL_LOG`](/reference/kotlin/android/Manifest.permission_group#CALL_LOG)
  permission group
  Restricted access to phone numbers, requiring
  [`READ_CALL_LOG`](/reference/kotlin/android/Manifest.permission#READ_CALL_LOG) permission
  Restricted access to Wi-Fi information

For an exhaustive list of changes introduced in Android 9.0 (API level
28), see [behavior
changes](/about/versions/pie/android-9.0-changes-28).
