<!-- source=describing-data-use clause=create-your-app-s-privacy-report url=https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests fetched=2026-09-04T16:09:59+00:00 -->

### Create your app’s privacy report

Xcode can create a privacy report by aggregating the privacy manifests from your app and the third-party SDKs it links to. Use the privacy report to better understand all of the data collected by your app and whether it tracks. Create the privacy report for your app by doing the following:

1. Open your project in Xcode.
2. Choose Product > Archive. Xcode creates the archive and reveals it in the organizer.
3. Control-click the archive in the organizer and choose Generate Privacy Report.
4. Choose a location to save the privacy report.
5. Switch to Finder.
6. Navigate to the location where you saved the privacy report, and double-click to open the report in Preview.

The privacy report is organized in a similar way to Privacy Nutrition Labels. Refer to this report when you provide your app’s privacy details in App Store Connect. For more information on providing your app’s privacy details, see [App privacy details on the App Store](https://developer.apple.com/app-store/app-privacy-details/).
