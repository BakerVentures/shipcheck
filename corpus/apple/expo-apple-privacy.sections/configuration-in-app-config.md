<!-- source=expo-apple-privacy clause=configuration-in-app-config url=https://docs.expo.dev/guides/apple-privacy/ fetched=2026-09-05T02:02:34+00:00 -->

## Configuration in app config

You can include an iOS privacy manifest by using the `privacyManifests` field under `expo.ios` in your app config.

app.json

```
{ "expo": { "name": "My App", "slug": "my-app", %%placeholder-start%%... %%placeholder-end%% "ios": { "privacyManifests": { "NSPrivacyAccessedAPITypes": [ { "NSPrivacyAccessedAPIType": "NSPrivacyAccessedAPICategoryUserDefaults", "NSPrivacyAccessedAPITypeReasons": ["CA92.1"] } ] } } } }
```

Make sure you have updated your Expo SDK libraries to the latest versions for your SDK version using `npx expo install --fix`.

Are you using this library in an existing React Native app?

You can include an iOS privacy manifest in an [existing React Native project](/bare/overview) by creating a PrivacyInfo.xcprivacy file using Xcode and adding it to your iOS app target.
Follow [Apple's Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files) guide to create a PrivacyInfo.xcprivacy file.

You can identify the `NSPrivacyAccessedAPITypes` and `NSPrivacyAccessedAPITypeReasons` values by looking at the [Apple Developer documentation](https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api).
