<!-- source=permissions-policy clause=location-permissions url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T15:48:35+00:00 -->

## Location Permissions

**Policy Summary**

To protect user privacy, the background location policy requires apps to provide a strong justification and obtain explicit user consent for access. Device location data is limited to essential functions that directly benefit the user and are central to the app's core purpose; it is never permitted solely for advertising or analytics. Minimize your requests, choosing lesser sensitive options like coarse location and foreground access whenever possible. Foreground Services access of device location must be user-initiated and temporary, while background is only for critical features. Please review the full policy to ensure compliance.

**Full Policy**

[Device location](https://developer.android.com/training/location) is regarded as personal and sensitive user data subject to the [Personal and Sensitive Information](/googleplay/android-developer/answer/9888076#personal_sensitive) policy and the [Background Location policy](https://support.google.com/googleplay/android-developer/answer/9799150?hl=en#zippy=), and the following requirements:

- Apps may not access data protected by location permissions (for example, `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `ACCESS_BACKGROUND_LOCATION`) after it is no longer necessary to deliver current features or services in your app.
- You should never request location permissions from users for the sole purpose of advertising or analytics. Apps that extend permitted usage of this data for serving advertising must be in compliance with our [Ads Policy](/googleplay/android-developer/answer/9857753).
- Apps should request the minimum scope necessary (for example, coarse instead of fine, and foreground instead of background) to provide the current feature or service requiring location and users should reasonably expect that the feature or service needs the level of location requested. For example, we may reject apps that request or access background location without compelling justification.
- Background location may only be used to provide features beneficial to the user and relevant to the core functionality of the app.

Apps are allowed to access location using foreground service (when the app only has foreground access for example, "while in use") permission if the use:

- has been initiated as a continuation of an in-app user-initiated action, and
- is terminated immediately after the intended use case of the user-initiated action is completed by the application.

Apps designed specifically for children must comply with the [Designed for Families](/googleplay/android-developer/answer/9893335#designed_for_families_prog)policy.

For more information on the policy requirements, please see [this help article](https://support.google.com/googleplay/android-developer/answer/9799150?hl=en&ref_topic=2364761).

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Comply with the [Designed for Families](https://support.google.com/googleplay/android-developer/answer/9893335?sjid=7274498547371890152-NC#designed_for_families_prog) policy for apps targeting children. | Don't use [device location](https://developer.android.com/develop/sensors-and-location/location) solely for advertising or analytics purposes. |
| Review [important permission requirements](https://goo.gle/play-help-background-location) before you submit your app for publishing. | Don't access data after it's no longer needed. |
| Complete the [Console declaration](https://goo.gle/play-permission-decl-form) for [background location](https://support.google.com/googleplay/android-developer/answer/9799150?hl=en&sjid=7274498547371890152-NC#zippy=). | Don't request device location for apps directed at children. |
|  | Don't sell device location. |

---
