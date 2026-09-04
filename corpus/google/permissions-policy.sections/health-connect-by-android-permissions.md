<!-- source=permissions-policy clause=health-connect-by-android-permissions url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T15:48:35+00:00 -->

## Health Connect by Android Permissions

**Policy Summary**

Access to Health Connect data is restricted to apps with approved health, fitness, medical care, or health research core use cases. You must strictly limit data access to the minimum scope necessary for these approved functions and obtain explicit user consent before sharing any health data with third parties. Transparency is key, so provide clear disclosures and a comprehensive privacy policy explaining data collection, use, management, and deletion. Secure user data against unauthorized access and comply with all applicable laws and regulations (for example, HIPAA, GDPR). Please review the full policy to ensure compliance.

**Full Policy**

[Health Connect](https://developer.android.com/guide/health-and-fitness/health-connect) is an Android platform that allows health and fitness apps to store and share the same on-device data, within a unified ecosystem. It also offers a single place for users to control which apps can read and write health and fitness data, including health records. Health Records may include medical history, diagnoses, treatments, medications, lab results, and other clinical data, obtained from healthcare providers or institutions, or through supported third-party health platforms.

Health Connect supports reading and writing a [variety of data types](https://developer.android.com/reference/kotlin/androidx/health/connect/client/records/package-summary#classes), from steps to body temperature, to health record data.

Data accessed through Health Connect Permissions is regarded as personal and sensitive user data subject to the [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311). If your app qualifies as a health app or has health-related features and accesses health data including Health Connect data, it must also comply with the [Health apps policy](https://support.google.com/googleplay/android-developer/answer/13996823).

Please see this [Android developer guide](https://developer.android.com/health-and-fitness/guides/health-connect) on how to get started with Health Connect. To request access to Health Connect data types and other FAQs, see [Android Health Permissions: Guidance & FAQs](https://support.google.com/googleplay/android-developer/answer/12991134).

Apps distributed through Google Play must meet the following policy requirements in order to read and/or write data to Health Connect.

#### **Appropriate Access to and Use of Health Connect**

Health Connect may only be used in accordance with the applicable policies, terms and conditions, and for approved use cases as set forth in this policy. This means you may only request access to permissions when your application or service meets one of the approved use cases.

Approved use cases include: fitness and wellness, rewards, fitness coaching, corporate wellness, medical care, health research, and games. Applications granted access to these use cases may not extend its use to undisclosed or non-permitted purposes.

Only applications or services with one or more features designed to benefit users' health and fitness are permitted to request access to Health Connect Permissions. These include:

- Applications or services allowing users **to directly journal, report, monitor, and/or analyze** their physical activity, sleep, mental well-being, nutrition, health measurements, physical descriptions, health records, and/or other health or fitness-related descriptions and measurements.
- Applications or services allowing users **to store their physical activity, sleep, mental well-being, nutrition, health measurements, physical descriptions**, **health records,** and/or other health or fitness-related descriptions and measurements on their device, and share their data with other on-device apps that satisfy these use cases.
- Applications or services enabling users to manage chronic conditions, medical treatments, or care support.

Access to Health Connect may not be used in violation of this policy or other applicable Health Connect terms and conditions or policies, including for the following purposes:

- Do not use Health Connect in developing, or for incorporation into, applications, environments or activities where the use or failure of Health Connect could reasonably be expected to lead to death, personal injury, harm to individuals, or environmental or property damage (such as the creation or operation of nuclear facilities, air traffic control, life support systems, or weaponry).
- Do not access data obtained through Health Connect using headless apps. Apps must display a clearly identifiable icon in the app tray, device app settings, notification icons, etc.
- Do not use Health Connect with apps that sync data between incompatible devices or platforms.
- Do not use Health Connect to connect to applications, services, or features that solely target children.
- Take reasonable and appropriate steps to protect all applications or systems that make use of Health Connect against unauthorized or unlawful access, use, destruction, loss, alteration, or disclosure.

It is also your responsibility to ensure compliance with any regulatory or legal requirements that may apply based on your intended use of Health Connect and any data from Health Connect. For example, if you are a covered entity or business associate subject to the Health Insurance Portability and Accountability Act (HIPAA), you must comply with applicable requirements for your access and use of information from Health Connect. If you are a developer subject to the General Data Protection Regulation (GDPR) for EU users, you must similarly comply with your obligations under the GDPR. These laws and regulations may require you to execute additional agreements prior to sharing data (for example, a Business Associate Agreement or Data Processing Agreement) with the relevant entities involved in your processing activities. It is also the responsibility of app developers to determine whether their activities require such agreements. Developers must provide evidence of such agreement or compliance to Google upon request.

Except as explicitly noted in the labeling or information provided by Google for specific Google products or services, Google does not endorse the use of or warrant the accuracy of any data contained in Health Connect for any use or purpose, and, in particular, for research, health, or medical uses. Google disclaims all liability associated with use of data obtained through Health Connect.

#### **Limited Use**

When using Health Connect, data access and use must adhere to specific limitations:

- Data use should be limited to providing or improving the appropriate use case or features visible in the application's user interface.
- User data may only be transferred to third parties with explicit user consent: for security purposes (for example, to investigate abuse), to comply with applicable laws or regulations, or as part of mergers/acquisitions.
- Human access to user data is restricted unless explicit user consent is obtained, for security purposes, to comply with laws, or when aggregated for internal operations as per legal requirements.
- **All other transfers, uses, or sale of Health Connect data is prohibited, including:** Transferring or selling user data to third parties like advertising platforms, data brokers, or any information resellers. Transferring, selling, or using user data for serving ads, including personalized or interest-based advertising. Transferring, selling, or using user data to determine credit-worthiness or for lending purposes. Transferring, selling, or using user data with any product or service that may qualify as a medical device, unless the medical device app complies with all applicable regulations, including obtaining necessary clearances or approvals from relevant regulatory bodies (for example, U.S. FDA) for its intended use of Health Connect data, and the user has provided explicit consent for such use. Transferring, selling, or using user data for any purpose or in any manner involving Protected Health Information (as defined by HIPAA) unless user-initiated and in compliance with HIPAA regulations.
  Transferring or selling user data to third parties like advertising platforms, data brokers, or any information resellers.
  Transferring, selling, or using user data for serving ads, including personalized or interest-based advertising.
  Transferring, selling, or using user data to determine credit-worthiness or for lending purposes.
  Transferring, selling, or using user data with any product or service that may qualify as a medical device, unless the medical device app complies with all applicable regulations, including obtaining necessary clearances or approvals from relevant regulatory bodies (for example, U.S. FDA) for its intended use of Health Connect data, and the user has provided explicit consent for such use.
  Transferring, selling, or using user data for any purpose or in any manner involving Protected Health Information (as defined by HIPAA) unless user-initiated and in compliance with HIPAA regulations.

#### **Minimum Scope**

You must only request access to the permissions that are necessary to implementing your product's features or services. Such access requests should be specific and limited to the data which is needed.

#### **Transparent and Accurate Notice and Control**

Health Connect handles health and fitness data that includes personal and sensitive information. Developers must provide clear and accessible disclosures about their data practices through a comprehensive privacy policy. These disclosures must include:

- Accurate representation of the identity of the application or service requesting access to user data.
- Clear and accurate information explaining the types of data being accessed, requested, and/or collected. The data must be related to a user-facing feature or recommendation offered in your app.
- Explanation for how the data will be used and/or shared: if you request data for one reason, but the data will also be utilized for a secondary purpose, you must disclose all use cases to users.
- User help documentation explaining how users can manage and delete their data from the app, and what happens to the data when an account is deactivated and/or deleted.
- Information regarding handling all personal and sensitive user data securely, including transmitting it using modern cryptography (for example, over HTTPS).

For more information on requirements for apps connecting to Health Connect, please see this [Help Center](https://support.google.com/googleplay/android-developer/answer/12991134) article.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Your app must comply with the [Health apps policy](https://support.google.com/googleplay/android-developer/answer/12261419) if it qualifies as a health app or has health-related features and accesses health data including [Health Connect data](https://developer.android.com/reference/kotlin/androidx/health/connect/client/records/package-summary#classes). | Don't use [Health Connect](https://developer.android.com/health-and-fitness/guides/health-connect) in high-risk apps (for example, aviation, control of life-critical systems such as pacemakers) or in apps that solely target children. |
| See [Android Health Permissions: Guidance and FAQs](https://support.google.com/googleplay/android-developer/answer/12991134) to request access to Health Connect data types and other FAQs. | Don't sell or transfer user data for advertising, creditworthiness, or data brokers. |
| Submit a [declaration form](https://goo.gle/play-permission-decl-form) in your Play Console and provide a clear and detailed justification explaining how your app will use the data to benefit the user. | Don't use with medical devices without required regulatory compliance/clearances. |
| Request only the minimum necessary data types. | Don't access [Health Connect data](https://developer.android.com/reference/kotlin/androidx/health/connect/client/records/package-summary#classes) for secondary or unapproved purposes. |
| Securely handle user data (for example, use modern cryptography). | Don't request data permissions beyond your app's core functionality. |

---
