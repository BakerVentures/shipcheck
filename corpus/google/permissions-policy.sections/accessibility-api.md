<!-- source=permissions-policy clause=accessibility-api url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T15:48:35+00:00 -->

## Accessibility API

**Policy Summary**

Google Play permits the use of the AccessibilityService API across a wide range of applications. However, only services designed to help people with disabilities access their devices or overcome challenges due to their disabilities are eligible to declare themselves as accessibility tools by setting isAccessibilityTool=true in their metadata. These apps are exempt from the prominent disclosure and consent requirements. For all other uses, or if not declaring your app as an accessibility tool, you will be required to complete an accessibility declaration in Play Console and must implement a clear in-app disclosure explaining data access and use, and obtain affirmative user consent. Please review the full policy to ensure compliance.

**Full Policy**

The Accessibility API cannot be used to:

- Change user settings without their permission or prevent the ability for users to disable or uninstall any app or service unless authorized by a parent or guardian through a parental control app or by authorized administrators through enterprise management software;
- Work around Android built-in platform security controls, privacy controls and notifications; or
- Change or leverage the user interface in a way that is deceptive or otherwise violates Google Play Developer Policies.

The Accessibility API is not designed and cannot be requested for:

- remote call audio recording
- an app that autonomously initiates, plans, and executes actions or decisions

The use of the Accessibility API must be documented in the Google Play listing.

#### Guidelines for **IsAccessibilityTool**

Apps with a core functionality intended to directly support people with disabilities are eligible to use the **IsAccessibilityTool** to appropriately publicly designate themselves as an accessibility app.

Apps not eligible for **IsAccessibilityTool** may not use the flag and must meet prominent disclosure and consent requirements as outlined in the [User Data](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en&ref_topic=9877467) policy as the accessibility related functionality is not obvious to the user.

Apps must use more narrowly scoped [APIs and permissions](https://developer.android.com/privacy/best-practices#permissions) in lieu of the Accessibility API when possible to achieve the desired functionality.

Please refer to the [AccessibilityService API](https://support.google.com/googleplay/android-developer/answer/10964491?hl=en) help center article for more information regarding prohibited use cases and guidance for using IsAccessibilityTool.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| [Declare](https://support.google.com/googleplay/android-developer/answer/9214102) `isAccessibilityTool=true` accurately if your app’s main goal is disability support in your service’s metadata file. | Don't misuse the `isAccessibilityTool` flag. Don’t use it if your app is not a disability support tool. |
| Provide a clear Play Console declaration and demo video if using AccessibilityService API. | Don't change user settings without permission, bypass privacy controls, or record remote call audio. |
| Implement clear in-app disclosure and obtain user consent if not a designated accessibility tool. | Don't use the API to autonomously initiate, plan, and execute actions or decisions. |
| Complete an accessibility declaration when you submit a [declaration form](https://support.google.com/googleplay/android-developer/answer/9214102) in your Play Console if you have not declared your app to be an accessibility tool but use the [AccessibilityService API](https://support.google.com/googleplay/android-developer/answer/10964491?utm_source=android-studio). | Don't deceive or mislead users. The API cannot be used to change or leverage the UI in a deceptive way. |
| Limit data collection and use strictly to the disclosed and declared purposes. | Don't collect unnecessary data. The data collected must be strictly limited to the disclosed purposes. |
| Use more narrowly scoped [APIs and permissions](https://developer.android.com/privacy/best-practices#permissions) in lieu of the Accessibility API when possible to achieve the desired functionality. | Don't bypass disclosure requirements. Disclosures cannot be a substitute for privacy policy or other app descriptions. |

---
