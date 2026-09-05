<!-- source=user-data-policy clause=data-safety-section url=https://support.google.com/googleplay/android-developer/answer/10144311 fetched=2026-09-05T02:02:36+00:00 -->

## Data safety section

**Policy Summary**

Google Play requires full transparency about the user data your app collects and how it's used. You must complete and maintain an accurate Data safety section for each of your apps in the Play Console, detailing data collection, use, and sharing (including by any SDKs in your app). The information in this section must consistently match your app's privacy policy disclosures. This information will show up in your app's Data safety section on Google Play, helping users understand how their data will be handled and make informed choices. Please review the full policy to ensure compliance.

**Full Policy**

All developers must complete a clear and accurate Data safety section for every app detailing collection, use, and sharing of user data. The developer is responsible for the accuracy of the label and keeping this information up-to-date. Where relevant, the section must be consistent with the disclosures made in the app's privacy policy.

Please refer to [this article](https://support.google.com/googleplay/android-developer/answer/10787469#types) for additional information on completing the Data safety section.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Share your privacy policy in Play Console and within the app itself. | Don't attempt to hide data collection or usage from users. |
| Provide prominent and accessible in-app data disclosure and obtain user consent via affirmative action when required. Affirmative action means that the user must complete an action in order to indicate that they agree. Update regularly information in your app's Data safety section and your privacy policy as you change how your app handles user data. | Don't request device permissions before users have provided their consent. |
| Verify data handling procedures of all third parties (SDKs). This is an important opportunity to audit your app, know your code, and what you integrate into it. Many SDKs share their data practices on Play SDK Index. | Don't use auto-dismissing consent popups when affirmative action is required to obtain user consent. |

---
