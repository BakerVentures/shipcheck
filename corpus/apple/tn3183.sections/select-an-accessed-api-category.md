<!-- source=tn3183 clause=select-an-accessed-api-category url=https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest fetched=2026-09-04T07:14:03+00:00 -->

## Select an accessed API category

A privacy accessed API category identifies the category of required reason APIs your app or third-party SDK uses. Set the value of the `NSPrivacyAccessedAPIType` key to a privacy accessed API category. For more information, see [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api).

The possible values of a privacy accessed API category are:

- `NSPrivacyAccessedAPICategoryActiveKeyboards`
- `NSPrivacyAccessedAPICategoryDiskSpace`
- `NSPrivacyAccessedAPICategoryFileTimestamp`
- `NSPrivacyAccessedAPICategorySystemBootTime`
- `NSPrivacyAccessedAPICategoryUserDefaults`
