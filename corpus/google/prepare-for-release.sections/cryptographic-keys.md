<!-- source=prepare-for-release clause=cryptographic-keys url=https://developer.android.com/studio/publish/preparing fetched=2026-09-05T02:02:42+00:00 -->

### Cryptographic keys

Android requires that all APKs are digitally signed with a certificate
before they are installed on a device or updated. For [Google Play Store](https://play.google.com), all apps created after
August 2021 are required to use [Play App
Signing](/studio/publish/app-signing#app-signing-google-play). But uploading your AAB to Play Console still requires you to sign
it with your developer certificate. Older apps can still self-sign, but whether
you're using Play App Signing or you're self-signing, you must sign your app
before you can upload it.

To learn about certificate requirements, see [Sign your app](/tools/publishing/app-signing).

**Important:** Your app must be signed with a
cryptographic key that has a validity period ending after October 22,
2033.

You might also have to obtain other release keys if your app accesses a
service or uses a third-party library that requires you to use a key that is
based on your private key.
