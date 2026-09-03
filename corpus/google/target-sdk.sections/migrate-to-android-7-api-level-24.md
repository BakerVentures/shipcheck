<!-- source=target-sdk clause=migrate-to-android-7-api-level-24 url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-03T19:54:43+00:00 -->

### Migrate to Android 7 (API level 24)

The following considerations apply to apps targeting Android 7.0 and higher versions of the platform:

- Doze and App Standby Design for behaviors described in [Optimizing for Doze and App Standby](/training/monitoring-device-state/doze-standby), which encompasses incremental changes introduced across several platform releases. When a device is in Doze and App Standby Mode, the system behaves as follows: Restricts network access Defers alarms, syncs, and jobs Restricts GPS and Wi-Fi scans
  Restricts network access
  Defers alarms, syncs, and jobs
  Restricts GPS and Wi-Fi scans
  Restricts normal-priority
  Firebase Cloud Messaging
  messages.
- Permission Changes The system restricts access to app private directories.
  The system restricts access to app private directories.
  Exposing a
  file://
  URI outside of your app triggers a
  FileUriExposedException
  . If you need to share files outside of your app, implement
  FileProvider
- The system [forbids linking](/about/versions/nougat/android-7.0-changes#ndk)

For an exhaustive list of changes introduced in Android 7.0 (API level 24), see the [Behavior Changes](/about/versions/nougat/android-7.0-changes)
page for that version of the platform.

Continue by following the instructions in the next section.
