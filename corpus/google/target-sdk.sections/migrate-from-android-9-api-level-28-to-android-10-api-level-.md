<!-- source=target-sdk clause=migrate-from-android-9-api-level-28-to-android-10-api-level- url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-03T19:54:43+00:00 -->

### Migrate from Android 9 (API level 28) to Android 10 (API level 29)

- [Notifications
  Need to request the normal permission
  USE_FULL_SCREEN_INTENT
  (not runtime permission).
- Support for [foldables](/guide/topics/ui/foldables) and large
  Multiple activities can now be in the "resumed" state at the same time, but only one actually has focus.
  - This change affects
  - New lifecycle concept of "topmost resumed" which can be detected
    Only one activity can be "topmost resumed."
  When
  resizeableActivity
  is set to
  false
  , apps can additionally specify a
  minAspectRatio
  which automatically letterboxes the app on narrower aspect ratios.
- [Privacy changes](/about/versions/10/privacy/changes) [Scoped storage](/training/data-storage#scoped-storage)
  Scoped storage
  - External storage access is limited only to an app-specific
  Restricted access to location while the app is in the background,
  requiring
  ACCESS_BACKGROUND_LOCATION
  permission.
  Restricted access to non-resettable identifiers such as IMEI and
  serial number.
  Restricted access to physical activity information such as the
  user's step count, requiring
  ACTIVITY_RECOGNITION
  permission.
  Restricted access to
  some
  telephony, Bluetooth, and Wi-Fi APIs
  , requiring
  ACCESS_FINE_LOCATION
  permission.
  Restricted access to Wi-Fi settings
  - Apps can no longer directly enable or disable Wi-Fi and need to
  - Restrictions on initiating a connection to a Wi-Fi network,
