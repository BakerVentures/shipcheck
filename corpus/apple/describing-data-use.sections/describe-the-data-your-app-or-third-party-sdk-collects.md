<!-- source=describing-data-use clause=describe-the-data-your-app-or-third-party-sdk-collects url=https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests fetched=2026-09-04T15:48:25+00:00 -->

### Describe the data your app or third-party SDK collects

For each type of data your app or third-party SDK collects, add a dictionary to the [NSPrivacyCollectedDataTypes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes) array in your privacy information file. Add the following keys to the dictionary.

- **[NSPrivacyCollectedDataType](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatype)** — A string that identifies the type of data your app or third-party SDK collects. Choose the value from the list of data types below that matches the data your app or third-party SDK collects.

- **[NSPrivacyCollectedDataTypeLinked](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypelinked)** — A Boolean that indicates whether your app or third-party SDK links this data type to the user’s identity. For more information, see Data linked to the user in [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/#linked-data).

- **[NSPrivacyCollectedDataTypeTracking](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypetracking)** — A Boolean that indicates whether your app or third-party SDK uses this data type to track.

- **[NSPrivacyCollectedDataTypePurposes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypepurposes)** — An array of strings that lists the reasons your app or third-party SDK collects the data. Choose values from the list of purposes below that match the reasons your app or third-party SDK collects this data type.

Xcode won’t generate a privacy report correctly if you define your own collected data types for the `NSPrivacyCollectedDataType` key, or provide your own reasons for the `NSPrivacyCollectedDataTypePurposes` key. Use values listed in the documentation for the keys.
