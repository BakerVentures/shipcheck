<!-- source=target-sdk clause=migrate-from-android-11-api-level-30-to-android-12-api-level url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-03T19:54:43+00:00 -->

## Migrate from Android 11 (API level 30) to Android 12 (API level 31)

**Security and Permissions**

- [Bluetooth](/guide/topics/connectivity/bluetooth/permissions): You must replace declarations for the [`BLUETOOTH`](/reference/android/Manifest.permission#BLUETOOTH) and
- Location: Users can request apps to retrieve only approximate location
  Intent filters: If your app contains
  activities
  ,
  services
  ,
  or
  broadcast receivers
  that use
  intent filters
  , you must
  explicitly declare the
  android:exported
  attribute for these
  components.
- Hibernation: Apps may be put into hibernation mode if they are not used over
- [Pending intent mutability](/about/versions/12/behavior-changes-12#pending-intent-mutability): You must specify the mutability of each

**User Experience**

- [Custom notifications](/about/versions/12/behavior-changes-12#custom-notifications): Notifications with custom content views will no
- [Android App Links verification changes](/about/versions/12/behavior-changes-12#android-app-links-verification-changes): When using Android App Link

**Performance**

- [Foreground service launch restrictions](/about/versions/12/behavior-changes-12#foreground-service-launch-restrictions): To target Android 12 or
- [Notification trampoline restrictions](/about/versions/12/behavior-changes-12#notification-trampolines): When users tap notifications,

View the complete set of [changes that affect apps targeting Android 12 (API
level 31)](/about/versions/12/behavior-changes-12).
