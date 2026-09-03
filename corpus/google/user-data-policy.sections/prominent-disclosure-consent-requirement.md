<!-- source=user-data-policy clause=prominent-disclosure-consent-requirement url=https://support.google.com/googleplay/android-developer/answer/10144311 fetched=2026-09-03T19:54:35+00:00 -->

## Prominent Disclosure & Consent Requirement

**Policy Summary**

Google Play policy mandates stringent requirements for handling sensitive personal or device data, particularly when its collection or use might not be expected by the user (e.g., background data collection). You must provide prominent, accessible, and descriptive in-app disclosure detailing data access, collection, use, and sharing *before* requesting any permissions or obtaining consent. Following disclosure, you are required to obtain clear user consent through a distinct, affirmative user action, ensuring informed user choice.

**Full Policy**

In cases where your app's access, collection, use, or sharing of personal and sensitive user data may not be within the reasonable expectation of the user of the product or feature in question (for example, if data collection occurs in the background when the user is not engaging with your app), you must meet the following requirements:

**Prominent disclosure: You must provide an in-app disclosure of your data access, collection, use, and sharing. The in-app disclosure:**

- Must be within the app itself, not only in the app description or on a website;
- Must be displayed in the normal usage of the app and not require the user to navigate into a menu or settings;
- Must describe the data being accessed or collected;
- Must explain how the data will be used and/or shared;
- Cannot only be placed in a privacy policy or terms of service; and
- Cannot be included with other disclosures unrelated to personal and sensitive user data collection.

**Consent and runtime permissions: Requests for in-app user consent and runtime permission requests must be immediately preceded by an in-app disclosure that meets the requirement of this policy. The app's request for consent:**

- Must present the consent dialog clearly and unambiguously;
- Must require affirmative user action (for example, tap to accept, tick a check-box);
- Must not interpret navigation away from the disclosure (including tapping away or pressing the back or home button) as consent;
- Must not use auto-dismissing or expiring messages as a means of obtaining user consent; and
- Must be granted by the user before your app can begin to collect or access the personal and sensitive user data.

Apps that rely on other legal bases to process personal and sensitive user data without consent, such as a legitimate interest under the EU GDPR, must comply with all applicable legal requirements and provide appropriate disclosures to the users, including in-app disclosures as required under this policy.

To meet policy requirements, it's recommended that you reference the following example format for Prominent Disclosure when it's required:

- "[This app] collects/transmits/syncs/stores [type of data] to enable ["feature"], [in what scenario]."
- *Example: "Fitness Funds collects location data to enable fitness tracking even when the app is closed or not in use and is also used to support advertising."*
- *Example: "Call buddy collects read and write call log data to enable contact organization even when the app is not in use."*

If your app integrates third party code (for example, an SDK) that is designed to collect personal and sensitive user data by default, you must, within 2 weeks of receipt of a request from Google Play (or, if Google Play's request provides for a longer time period, within that time period), provide sufficient evidence demonstrating that your app meets the Prominent Disclosure and Consent requirements of this policy, including with regard to the data access, collection, use, or sharing via the third party code.

Examples of common violations

- An app collects device location but does not have a prominent disclosure explaining which feature uses this data and/or indicates the app's usage in the background.
- An app has a runtime permission requesting access to data before the prominent disclosure which specifies what the data is used for.
- An app that accesses a user's inventory of installed apps and doesn't treat this data as personal or sensitive data subject to the above Privacy Policy, data handling, and Prominent Disclosure and Consent requirements.
- An app that accesses a user's phone or contact book data and doesn't treat this data as personal or sensitive data subject to the above Privacy Policy, data handling, and Prominent Disclosure and Consent requirements.
- An app that records a user's screen and doesn't treat this data as personal or sensitive data subject to this policy.
- An app that collects [device location](https://developer.android.com/training/location) and does not comprehensively disclose its use and obtain consent in accordance with the above requirements.
- An app that uses restricted permissions in the background of the app including for tracking, research, or marketing purposes and does not comprehensively disclose its use and obtain consent in accordance with the above requirements.
- An app with an SDK that collects personal and sensitive user data and doesn't treat this data as subject to this User Data Policy, access, data handling (including disallowed sale), and prominent disclosure and consent requirements.

Refer to this [article](https://support.google.com/googleplay/android-developer/answer/11150561) for more information on the Prominent Disclosure and Consent requirement.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Provide prominent, accessible, in-app disclosure of data handling. | Don't handle sensitive data beyond user expectation without prior, prominent in-app disclosure. |
| Clearly describe all sensitive data access, use, and sharing. | Don't attempt to hide data practices or evade disclosure requirements. |
| Present disclosure *before* requesting consent or permissions. | Don't use passive user actions (like backing out) as consent. |
| Require a clear, affirmative user action to grant consent. | Don't implement auto-dismissing popups for consent purposes. |
| Ensure disclosure highlights relevant permissions. | Don't request permissions before the user has seen disclosure. |
| Familiarize yourself with common policy violations related to disclosure/consent. | Don't fail to provide a descriptive and accessible disclosure format. |

---
