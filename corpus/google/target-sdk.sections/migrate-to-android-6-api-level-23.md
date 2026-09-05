<!-- source=target-sdk clause=migrate-to-android-6-api-level-23 url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-05T02:02:46+00:00 -->

### Migrate to Android 6 (API level 23)

The following considerations apply to apps targeting Android 6.0 and higher versions of the platform:

- [Runtime Permissions](/training/permissions/requesting)
  Dangerous permissions are only granted at runtime. Your UI flows must provide affordances for granting these permissions.
  Wherever possible, ensure your app is prepared to handle rejection of permission requests. For example, if a user declines a request to access the device's GPS, ensure your app has another way to proceed.

For an exhaustive list of changes introduced in Android 6.0 (API level 23), see the [Behavior Changes](/about/versions/marshmallow/android-6.0-changes)
page for that version of the platform.

Continue by following the instructions in the next section.
