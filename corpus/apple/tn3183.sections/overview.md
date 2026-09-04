<!-- source=tn3183 clause=overview url=https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest fetched=2026-09-04T15:48:24+00:00 -->

## Overview

When you build an app or third-party SDK that uses any required reason API, perform these steps in your privacy manifest (`PrivacyInfo.xcprivacy`):

1. Add the `NSPrivacyAccessedAPITypes` key and set its value to the dictionary.
2. For each required reason API your app or third-party SDK uses, add a dictionary as a value for the `NSPrivacyAccessedAPITypes` key. The dictionary includes the category of the reason API and a list of reasons for using this API. For more information, see [Add an accessed API type and reasons dictionary](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Add-an-accessed-API-type-and-reasons-dictionary).

See [Privacy manifest files](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files) and [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api) for more information about the privacy manifest and these keys.

This document describes how to add the `NSPrivacyAccessedAPIType`, `NSPrivacyAccessedAPITypeReasons`, and `NSPrivacyAccessedAPITypes` keys to your privacy manifest in Xcode. If you work outside of Xcode, review this document to learn about the expected structure of each key.

> **Note:** Before you start adding the keys to your privacy manifest, enable raw keys and values in Xcode to view the raw keys and hide their human-readable names. Click anywhere in the privacy manifest, then choose Xcode > Editor > Raw Keys and Values. Repeat the process to disable this feature.
