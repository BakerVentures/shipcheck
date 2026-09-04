<!-- source=permissions-policy clause=package-app-visibility-permission url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T16:10:09+00:00 -->

## Package (App) Visibility Permission

**Policy Summary**

Accessing a user's installed app inventory is sensitive data. Google Play policy strictly limits broad visibility (``QUERY_ALL_PACKAGES``), allowing it only for core app functionality that requires extensive knowledge of installed apps for interoperability. You must prioritize using finite, targeted queries to access specific apps when possible, which is more privacy-friendly. Under no circumstances can data from the installed app inventory be sold or shared for advertising or analytics monetization. Please review the full policy to ensure compliance.

**Full Policy**

The inventory of installed apps queried from a device are regarded as personal and sensitive user data subject to the [Personal and Sensitive Information](https://support.google.com/googleplay/android-developer/answer/9888076/) policy, and the following requirements:

Apps that have a core purpose to launch, search, or interoperate with other apps on the device, may obtain scope-appropriate visibility to other installed apps on the device as outlined below:

- **Broad app visibility:** Broad visibility is the capability of an app to have extensive (or “broad”) visibility of the installed apps (“packages”) on a device.
  For apps targeting [API level 30 or later](https://developer.android.com/studio/releases/platforms), broad visibility to installed apps via the [``QUERY_ALL_PACKAGES``](https://developer.android.com/reference/kotlin/android/Manifest.permission#query_all_packages) permission is restricted to specific use cases where awareness of and/or interoperability with any and all apps on the device are required for the app to function.
  - You may not use ``QUERY_ALL_PACKAGES`` if your app can operate with a more [targeted scoped package visibility declaration](https://developer.android.com/training/basics/intents/package-visibility#declare-other-apps)(for example, querying and interacting with specific packages instead of requesting broad visibility).
  Use of alternative methods to approximate the broad visibility level associated with ``QUERY_ALL_PACKAGES`` permission are also restricted to user-facing core app functionality and interoperability with any apps discovered via this method.
  Please see this [Help Center article](https://support.google.com/googleplay/android-developer/answer/10158779) for allowable use cases for the ``QUERY_ALL_PACKAGES`` permission.
- **Limited app visibility**: Limited visibility is when an app minimizes access to data by querying for specific apps using more targeted (instead of “broad”) methods(for example, querying for specific apps that satisfy your app’s manifest declaration). You may use this method to query for apps in cases where your app has policy compliant interoperability, or management of these apps.
- Visibility to the inventory of installed apps on a device must be directly related to the core purpose or core functionality that users access within your app.

App inventory data queried from Play-distributed apps may never be sold nor [shared](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en&sjid=9328586825007120077-NA#sharing&zippy=%2Cdata-types%2Cdata-sharing) for analytics or ads monetization purposes.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Submit a [declaration form](https://goo.gle/play-permission-decl-form) in your Play Console for `QUERY_ALL_PACKAGES` and any other high-risk permissions. | Don't request `QUERY_ALL_PACKAGES` if your need can be met with finite, targeted queries. |
| For your app review, clearly document why your app needs app visibility whether broad or more targeted. | Don't gain broad app visibility via methods not explicitly allowed by policy. |
| Access only the minimum data needed. | Don't provide false information about your app's core functionality or data needs. |
| Review the [Permitted uses of the QUERY_ALL_PACKAGES permission](https://support.google.com/googleplay/android-developer/answer/10158779?utm_source=android-studio#zippy=,permitted-uses-of-the-query-all-packages-permission) for allowable use cases. | Don't collect or use unnecessary data from installed app data. |

---
