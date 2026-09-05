<!-- source=permissions-policy clause=restricted-permissions-with-minimum-scope-alternatives url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-05T02:02:40+00:00 -->

## Restricted Permissions with minimum scope alternatives

System pickers and alternatives like [Sharesheet](https://developer.android.com/training/sharing/send#why-to-use-system-sharesheet) are designed to support a privacy-oriented path for developers. Photos, Videos, Contacts, and other personal and sensitive data gated by restricted permissions should be treated with privacy best practices. Your app should only request and carry the sensitive permissions below if minimum scope alternatives are not sufficient to provide your core functionality. For more information, see our [Help Center](https://support.google.com/googleplay/android-developer/answer/16935362).

- Photo and Video Permissions

- All user Photos are personal and sensitive data subject to the [User Data](https://support.google.com/googleplay/android-developer/answer/10144311) policy.

- Apps that target Android 13 or later (API level 33+) may only request the `READ_MEDIA_IMAGES` and `READ_MEDIA_VIDEO` permissions if system pickers (like the [Android Photo Picker](https://developer.android.com/training/data-storage/shared/photo-picker)) are not sufficient for your app to provide core functionality. Apps that still request the `READ_MEDIA_IMAGES` and `READ_MEDIA_VIDEO` permissions must submit a Play Console declaration to demonstrate access needs for Photos and why Android Photo Picker (or alternatives) would not suffice.

---
