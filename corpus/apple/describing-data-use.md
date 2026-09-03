---
shipcheck_source_id: describing-data-use
title: "Describing data use in privacy manifests"
url: https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests
final_url: https://developer.apple.com/tutorials/data/documentation/bundleresources/describing-data-use-in-privacy-manifests.json
fetched_at: 2026-09-03T19:56:58+00:00
sha256: 0d100d5ed30f2c3343f01d47445e477dc2b9258a1795d2328e816ffb5f53ef4b
vendor: apple
note: "NSPrivacyCollectedDataTypes vocabulary, which must line up with the App Privacy nutrition labels."
---

# Describing data use in privacy manifests

Declare the data collected by your app or by third-party SDKs.

## Overview

Record the categories of data that your app or third-party SDK collects about the person using the app, and the reasons it collects the data. App developers can use Xcode to create a privacy report, summarizing the information about collected data in their app and the third-party SDKs the app links to.

> **Important:** Third-party SDKs need to provide their own privacy manifest files that record the types of data they collect. Your app’s privacy manifest file doesn’t need to cover data collected by third-party SDKs that your app links to.

### Describe the data your app or third-party SDK collects

For each type of data your app or third-party SDK collects, add a dictionary to the [NSPrivacyCollectedDataTypes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes) array in your privacy information file. Add the following keys to the dictionary.

- **[NSPrivacyCollectedDataType](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatype)** — A string that identifies the type of data your app or third-party SDK collects. Choose the value from the list of data types below that matches the data your app or third-party SDK collects.

- **[NSPrivacyCollectedDataTypeLinked](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypelinked)** — A Boolean that indicates whether your app or third-party SDK links this data type to the user’s identity. For more information, see Data linked to the user in [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/#linked-data).

- **[NSPrivacyCollectedDataTypeTracking](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypetracking)** — A Boolean that indicates whether your app or third-party SDK uses this data type to track.

- **[NSPrivacyCollectedDataTypePurposes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes/nsprivacycollecteddatatypepurposes)** — An array of strings that lists the reasons your app or third-party SDK collects the data. Choose values from the list of purposes below that match the reasons your app or third-party SDK collects this data type.

Xcode won’t generate a privacy report correctly if you define your own collected data types for the `NSPrivacyCollectedDataType` key, or provide your own reasons for the `NSPrivacyCollectedDataTypePurposes` key. Use values listed in the documentation for the keys.

### Create your app’s privacy report

Xcode can create a privacy report by aggregating the privacy manifests from your app and the third-party SDKs it links to. Use the privacy report to better understand all of the data collected by your app and whether it tracks. Create the privacy report for your app by doing the following:

1. Open your project in Xcode.
2. Choose Product > Archive. Xcode creates the archive and reveals it in the organizer.
3. Control-click the archive in the organizer and choose Generate Privacy Report.
4. Choose a location to save the privacy report.
5. Switch to Finder.
6. Navigate to the location where you saved the privacy report, and double-click to open the report in Preview.

The privacy report is organized in a similar way to Privacy Nutrition Labels. Refer to this report when you provide your app’s privacy details in App Store Connect. For more information on providing your app’s privacy details, see [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/).

## See Also

- [Adding a privacy manifest to your app or third-party SDK](https://developer.apple.com/documentation/bundleresources/adding-a-privacy-manifest-to-your-app-or-third-party-sdk)
- [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)
- [Editing property list files](https://developer.apple.com/documentation/xcode/editing-property-list-files)
- [App Privacy Configuration](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration)
