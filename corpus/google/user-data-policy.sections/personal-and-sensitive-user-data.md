<!-- source=user-data-policy clause=personal-and-sensitive-user-data url=https://support.google.com/googleplay/android-developer/answer/10144311 fetched=2026-09-05T02:02:36+00:00 -->

## Personal and Sensitive User Data

**Policy Summary**

Google's User Data policy requires you to be transparent about how your app handles personal and sensitive user data. You must disclose what data you collect, how you use it, and who it's shared with. You must provide a valid privacy policy, obtain user consent, and handle data securely. Additionally, you must offer users a way to delete their accounts and associated data. Please review the full policy to ensure compliance.

**Full Policy**

Personal and sensitive user data includes, but isn't limited to, personally identifiable information, financial and payment information, authentication information, phonebook, contacts, [device location](https://developer.android.com/training/location), SMS and call-related data, [health data](https://support.google.com/googleplay/android-developer/answer/12261419#health_apps), [Health Connect](https://support.google.com/googleplay/android-developer/answer/9888170#ahp) data, inventory of other apps on the device, microphone, camera, and other sensitive device or usage data. If your app handles personal and sensitive user data, then you must:

- Limit the access, collection, use and sharing of personal and sensitive user data acquired through the app to app and service functionality and policy-conforming purposes reasonably expected by the user:
  Apps that extend usage of personal and sensitive user data for serving advertising must comply with Google Play’s [Ads policy](https://support.google.com/googleplay/android-developer/answer/9857753#location-data).

- You may also transfer data as necessary to [service providers](https://support.google.com/googleplay/android-developer/answer/10787469#service-provider&zippy=%2Csharing%2Cdata-sharing) or for legal reasons such as to comply with a valid governmental request, applicable law, or as part of a merger or acquisition with legally adequate notice to users.
- Handle all personal and sensitive user data securely, including transmitting it using modern cryptography (for example, over HTTPS).
- Use a runtime permissions request whenever available, prior to accessing data gated by [Android permissions](https://developer.android.com/guide/topics/permissions/overview).
- Not sell personal and sensitive user data.
  "Sale" means the exchange or transfer of personal and sensitive user data to a [third party](https://support.google.com/googleplay/android-developer/answer/10787469#first-and-third&zippy=%2Csharing%2Cdata-sharing) for monetary consideration.
  - User-initiated transfer of personal and sensitive user data (for example, when the user is using a feature of the app to transfer a file to a third party, or when the user chooses to use a dedicated purpose research study app), is not regarded as sale.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Have a valid privacy policy in both the app's store listing and within the app itself. | Don't provide misleading or inaccurate information about your data practices. |
| Discloseyour data collection and sharing practices in the Play Console's Data safety section. | Don't collect data that is not critical to your app's core purpose. |
| Obtain clear, affirmative user consent before collecting any personal or sensitive data. | Don't sellpersonal and sensitive user data. |
| Protect all user data with appropriate security measures, including modern cryptography for data in transit. | Don't violate child safety policies. If your app is for children, you must comply with the [Google Play Families](https://support.google.com/googleplay/android-developer/answer/9893335) policy, which includes specific rules for handling user data. |
| Only collect and use data that is necessary for your app's functionality. | Don't collect data without the user's consent or manipulate them into giving it. |
| Allow account deletion. This must be available both in-app and on an external web resource. | Don't neglect account deletion. Provide a clear and easy way for users to delete their accounts and data. Account freezing is not a valid substitute. |

---
