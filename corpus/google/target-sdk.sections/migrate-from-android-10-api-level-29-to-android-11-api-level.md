<!-- source=target-sdk clause=migrate-from-android-10-api-level-29-to-android-11-api-level url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-05T02:02:46+00:00 -->

### Migrate from Android 10 (API level 29) to Android 11 (API level 30)

- Privacy
  [Scoped storage enforcement](/about/versions/11/privacy/storage) : Apps should adopt the scoped storage model where app-specific, media, and other file types are saved and accessed using dedicated locations.
  [Permissions auto-reset](/about/versions/11/privacy/permissions#auto-reset): If users
  haven't interacted with an app for a few months, the system auto-resets the app's sensitive permissions.
  This shouldn't affect most apps. If your app primarily works in the background without user interactions, you may
  consider [requesting users to disable
  auto reset.](/guide/topics/permissions/overview#auto-reset-permissions-unused-apps)
  [Background location access](/about/versions/11/privacy/location#background-location): Apps must
  request foreground and background location permission separately. [Granting access to background location permission can only be done in app settings](/training/location/permissions#request-background-location) instead of runtime permission dialogs.
  [Package Visibility](/training/basics/intents/package-visibility-use-cases): When an app queries
  for the list of installed apps and services on the device, the returned list is filtered.
  - If you use [Text-to-speech](/about/versions/11/behavior-changes-11#tts-engines) or

For an exhaustive list of changes introduced in Android 11 (API level 30), see
the [Behavior Changes](/about/versions/11/behavior-changes-11) page.

Continue to update to API 31 by following the instructions in the previous section.
