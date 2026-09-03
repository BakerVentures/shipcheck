<!-- source=user-data-policy clause=restrictions-for-personal-and-sensitive-data-access url=https://support.google.com/googleplay/android-developer/answer/10144311 fetched=2026-09-03T19:54:35+00:00 -->

## Restrictions for Personal and Sensitive Data Access

**Policy Summary**

Google Play enforces specific restrictions on apps that handle financial, contact, or persistent identifier data. You must never publicly expose financial or government ID numbers. Unauthorized publishing of private contacts is forbidden. Apps for children must use approved SDKs. Apps that link persistent identifiers to other data must be for specific telephony or enterprise management purposes, with clear user disclosures. Please review the full policy to ensure compliance.

**Full Policy**

In addition to the requirements above, the table below describes requirements for specific activities.

| **Activity** | **Requirement** |
| --- | --- |
| Your app handles financial or payment information or government identification numbers | Your app must never publicly disclose any personal and sensitive user data related to financial or payment activities or any government identification numbers. |
| Your app handles non-public phonebook or contact information | We don't allow unauthorized publishing or disclosure of people's non-public contacts. |
| Your app contains anti-virus or security functionality, such as anti-virus, anti-malware, or security-related features | Your app must post a privacy policy that, together with any in-app disclosures, explain what user data your app collects and transmits, how it's used, and the type of parties with whom it's shared. |
| Your app targets children | Your app must not include an SDK that is not approved for use in child-directed services. See [Designing Apps for Children and Families](https://support.google.com/googleplay/android-developer/answer/9893335) for full policy language and requirements. |
| Your app collects or links persistent device identifiers (for example, IMEI, IMSI, SIM Serial #, etc.) | Persistent device identifiers may not be linked to other personal and sensitive user data or resettable device identifiers except for the purposes of Telephony linked to a SIM identity (for example, wifi calling linked to a carrier account), and Enterprise device management apps using device owner mode. These uses must be prominently disclosed to users as specified in the [User Data](https://support.google.com/googleplay/android-developer/answer/10144311) policy. Please [consult this resource](https://developer.android.com/training/articles/user-data-ids) for alternative unique identifiers. Please read the [Ads](https://support.google.com/googleplay/android-developer/answer/9857753) policy for additional guidelines for Android Advertising ID. |

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Handle contacts securely. | Don't publicly disclose any financial information or government ID numbers. |
| Ensure any SDKs used in child-directed apps are approved for that purpose. | Don't disclose sensitive data publicly. Do not make financial data or government IDs public. |
| Disclose data use for security apps. If your app has anti-virus or security features, its privacy policy must clearly explain all data collection and sharing. | Don’t publish or share people's non-public contacts without authorization. |
| Only link persistent identifiers (like IMEI) to other user data for specific telephony or enterprise management purposes. | Don't use unapproved SDKs for children's apps. Do not include unapproved SDKs in apps targeting children. |
| Disclose use of identifiers. All permitted uses of persistent identifiers must be prominently disclosed to users. | Don't link identifiers unnecessarily. Avoid linking persistent identifiers to other user data unless for the two approved use cases. |

---
