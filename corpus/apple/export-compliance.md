---
shipcheck_source_id: export-compliance
title: "Overview of export compliance"
url: https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance
final_url: https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance
fetched_at: 2026-09-04T07:14:07+00:00
sha256: 7cfd85641bba161780caf6356cda14a8609373d26fb1735e2ad85032f10f10ba
vendor: apple
---

[App Store Connect Help](/help/app-store-connect/)

[App Store Connect](/help/app-store-connect/) Manage app information Overview of export compliance

Manage app information

# Overview of export compliance

If your app uses, accesses, contains, implements, or incorporates encryption, and you intend to upload, test, and distribute it, you need to determine your export compliance requirements in App Store Connect.

Examples of apps requiring an export compliance determination include, but aren’t limited to, apps that use:

- Standard encryption algorithms.
- Crypto functionality within Apple’s operating system.
- Proprietary or non-standard encryption algorithms. The US Government defines "non-standard cryptography" as any implementation of “cryptography” involving the incorporation or use of proprietary or unpublished cryptographic functionality, including encryption algorithms or protocols that have not been adopted or approved by a duly recognized international standards body (e.g., IEEE, IETF, ISO, ITU, ETSI, 3GPP, TIA, and GSMA) and haven’t otherwise been published.

Please note that it’s your responsibility to review the [Export Administration Regulation](https://bis.doc.gov/index.php/policy-guidance/encryption) to determine whether your app's use of encryption requires a formal classification (Commodity Classification Automated Tracking System or CCATS) from BIS. you're responsible for all liabilities associated with misinterpretation of export regulations or claiming exemption inaccurately. To learn about encryption export controls, search for "encryption policy" on the US Department of Commerce [Bureau of Industry and Security (BIS)](https://www.bis.doc.gov/) website. The import and export of encryption apps distributed in France are also controlled by the French Government. The main items of control for France are Secure Storage, Secure Communications, and Security Anti-Virus applications. Exemptions include Banking and Medical applications. For more information about these French controls, visit the [Agence nationale de la sécurité des systèmes d’information (ANSSI)](https://www.ssi.gouv.fr/) website.

When you submit a new version of your app, you’ll need to answer questions in App Store Connect about your app's use of encryption. Follow the steps below before submitting your app to App Review to ensure that you’re submitting the right documentation and to bypass these questions if your app doesn’t use encryption.

## Determine your export compliance requirements

App Store Connect provides a simple way for you to [determine your export compliance requirements](/help/app-store-connect/manage-app-information/determine-and-upload-app-encryption-documentation) by presenting you with a set of questions about your app and where you plan to make it available. Based on your answers, complete the following steps:

| Scenario | Next Steps |
| --- | --- |
| No export compliance documentation required | [Update your app’s information property list (Info.plist) file in Xcode](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations) so that you don’t need to answer encryption questions with each app submission. |
| Export compliance documentation required | Use App Store Connect to [submit your app encryption documentation](/help/app-store-connect/manage-app-information/determine-and-upload-app-encryption-documentation). Once the documentation is approved, attach it to your [beta build](/help/app-store-connect/test-a-beta-version/provide-export-compliance-information-for-beta-builds) or [app version build](/help/app-store-connect/manage-builds/choose-a-build-to-submit). [Update your app’s information property list (Info.plist) file in Xcode](https://developer.apple.com/documentation/security/complying_with_encryption_export_regulations) so that you don’t need to answer encryption questions with each app submission. |
