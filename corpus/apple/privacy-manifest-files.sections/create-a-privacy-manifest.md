<!-- source=privacy-manifest-files clause=create-a-privacy-manifest url=https://developer.apple.com/documentation/bundleresources/privacy-manifest-files fetched=2026-09-04T01:32:38+00:00 -->

### Create a privacy manifest

To add the privacy manifest to your app or third-party SDK in Xcode, follow these steps:

- Choose File > New File.
- Scroll down to the Resource section, and select App Privacy File type.
- Click Next.
- Check your app or third-party SDK’s target in the Targets list.
- Click Create.

By default, the file is named `PrivacyInfo.xcprivacy`; this is the required file name for bundled privacy manifests.

> **Note:** You need to add the privacy manifest file to your target’s resources for Xcode to use it when you generate a privacy report. If you distribute your third-party SDK as a static library, use the support for static frameworks in Xcode 15 or later to bundle resources, including the privacy manifest file. Create a framework target in Xcode that builds your product, set its Mach-O type build setting to “Static Library,” and add the privacy manifest file to your target’s bundle resources along with any other resources, for example, image files.

At the top level of this property list file, add the following keys to the dictionary:

- **[NSPrivacyTracking](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytracking)** — A Boolean that indicates whether your app or third-party SDK uses data for tracking as defined under the App Tracking Transparency framework. When set to `true` you need to provide a list of internet domains in `NSPrivacyTrackingDomains`. For more information, see [User Privacy and Data Use](https://developer.apple.com/app-store/user-privacy-and-data-use/).

- **[NSPrivacyTrackingDomains](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacytrackingdomains)** — An array of strings that lists the internet domains your app or third-party SDK connects to that engage in tracking. If the user has not granted tracking permission through the App Tracking Transparency framework, network requests to these domains fail and your app receives an error. To provide a list of internet domains in `NSPrivacyTrackingDomains`, set `NSPrivacyTracking` to `true`.

- **[NSPrivacyCollectedDataTypes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacycollecteddatatypes)** — An array of dictionaries that describes the data types your app or third-party SDK collects. For information on the keys and values to use in the dictionaries, see [Describing data use in privacy manifests](https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests).

- **[NSPrivacyAccessedAPITypes](https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes)** — An array of dictionaries that describe the API types your app or third-party SDK accesses that have been designated as APIs that require reasons to access. For information on the keys and values to use in the dictionaries, see [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api).
