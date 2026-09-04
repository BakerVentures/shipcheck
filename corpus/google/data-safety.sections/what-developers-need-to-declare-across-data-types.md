<!-- source=data-safety clause=what-developers-need-to-declare-across-data-types url=https://support.google.com/googleplay/android-developer/answer/10787469 fetched=2026-09-04T07:14:10+00:00 -->

### What developers need to declare across data types

Click on the sections below to expand or collapse them.

Data collection

"Collect" means transmitting data from your app off a user’s device. Please note the following guidelines:

- **Libraries and SDKs:** This includes user data transmitted off device from your app by libraries and/or SDKs used in your app, irrespective of whether data is transmitted to you or a third-party server.
- **Webview:** It also includes user data collected from a webview which has been opened from your app, if your app is in control of the code/behavior delivered through that webview.
  You do not need to declare data collection from a webview in which users are navigating the open web.
- **Ephemeral processing:** User data transmitted off device that is processed ephemerally needs to be included in your form response, but if it meets the standard below, it will **not** be disclosed in your app’s Data safety section on Google Play.
  Processing data "ephemerally" means accessing and using it while the data is only stored in memory and retained for no longer than necessary to service the specific request in real-time.
  For example, a weather app that transmits user location off the device to fetch the current weather at the user's location but only uses location data in memory and does not store that data once the request has been fulfilled, can treat its transient use of location as ephemeral. However, using data to build advertising profiles or other user profiles cannot be treated as ephemeral and must be declared as collection or sharing for the relevant purposes.
- **Pseudonymous data:** User data collected pseudonymously must be disclosed. For example, data that can reasonably be re-associated with a user must be disclosed.

#### Not in scope for data collection

The following use cases do not need to be disclosed as collected:

- **On-device access/processing:** User data accessed by your app that is only processed locally on the user’s device and not sent off device does **not** need to be disclosed.
- **End-to-end encryption:** User data that is sent off device, but that is unreadable by you or anyone other than the sender and recipient as a result of end-to-end encryption does **not** need to be disclosed.
  The encrypted data must not be readable by any intermediary entity, including the developer, and only sender and recipient may have necessary keys.

Data sharing

"Sharing" refers to transferring user data collected from your app to a third party. This includes user data transferred:

- **Off-device, such as** s**erver to server transfers.** For example, if you transfer user data collected from your app from your server to a third-party server.
- **On-device transfer to another app.** Transferring user data from your app to another app directly on the device. In this case, you must disclose data sharing in your Data safety section declarations even if your app does not transmit the data off the user’s device.
- **From your app libraries and SDKs.** Transferring data collected from your app off a user’s device directly to a third party via libraries and/or SDKs included in your app.
- **From webview which has been opened through your app.** Transferring user data to a third party via a webview which has been opened from your app, if your app is in control of code/behavior delivered through that webview.
  You do not need to declare data sharing from a webview in which users are navigating the open web.

The following types of data transfers do not need to be disclosed as "sharing":

- **Service providers.** Transferring user data to a "service provider" that processes it on behalf of the developer.
  **"Service provider"** means an entity that processes user data on behalf of the developer and based on the developer’s instructions.
- **Legal purposes.** Transferring user data for specific legal purposes, such as in response to a legal obligation or government requests.
- **User-initiated action or prominent disclosure and user consent.** Transferring user data to a third party based on a specific user-initiated action, where the user reasonably expects the data to be shared, or based on a prominent in-app disclosure and consent that meets the requirements described in our [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311).
- **Anonymous data.** Transferring user data that has been fully anonymized so that it can no longer be associated with an individual user.

**First and third parties.**

- "First party" means the primary organization responsible for processing data collected by the app, which is typically the organization publishing the app on Google Play and appearing on the store listing.
  The first party has an obligation to make reasonably clear to users which organization is primarily responsible for processing data collected by the app.
- "Third party" means any organization other than the first party or its service providers.

Data handling

You can also disclose whether each data type collected by your app is "optional" or "required." "Optional" includes the ability to opt into or opt out of data collection. For example, you can declare a data type as "optional" where a user has control over its collection and can use the app without providing it; or where a user chooses whether to manually provide that data type. If your app’s primary functionality requires the data type, you should declare that data as "required."

You can declare that your app collects certain data optionally only if all users – regardless of device or region – can either optionally provide information, opt-out, or opt-in to have the data collected.

Examples of optional data collection include:

- A social media app that asks for a user's birthday for marketing communication, but that info is not required – the user can still sign up without providing that information.
- User data that is only collected when a user signs in where users have the ability to engage with the app without being signed-in.

Other app and data disclosures

The Data safety section is also an opportunity for you to showcase your app’s privacy and security practices to your users. For example, you can highlight the following information:

- **Encryption in transit:** Is data collected or shared by your app using encryption in transit to protect the flow of user data from the end user’s device to the server.
  Some apps are designed to let users transfer data to another site or service. For example, a messaging app may give users an option to send an SMS message through their mobile services provider, which maintains different encryption practices. These apps may declare in their Data safety section that data is transferred over a secure connection as long as they use best industry standards to safely encrypt data while it travels between a user’s device and the app’s servers.
- **Deletion request mechanism:** Does your app provide a way for users to request deletion of their data?

Committed to follow the Families policy (available March 2022 to applicable apps)

Apps that have children as a target audience must follow Google Play's [Families policy](https://support.google.com/googleplay/android-developer/answer/9893335) requirements. If your app falls in this category and you’ve reviewed its compliance with the Families policy requirements, you can choose to display a badge on your Data safety section stating that you have "Committed to follow the Play Families Policy."

To display the badge, go to the "Security practices" section of your Data safety form and click **Go to Target audience and content** to opt-in

Independent security review (available to all apps)

You may choose to declare in your Data safety form that your app has been independently validated against a global security standard. This is an optional review undertaken and paid for by developers. Through [MASA](https://appdefensealliance.dev/masa) (Mobile Application Security Assessment) developers can work directly with a Google Authorized Lab to have their apps evaluated against [OWASP’s MASVS](https://owasp.org/www-project-mobile-security-testing-guide/) (Mobile Application Security Verification Standard). The third-party organizations performing the reviews are doing so on the developer’s behalf.

If you're interested in participating, you can contact a Google Authorized Lab directly to initiate the testing process. Once the lab has verified your app satisfies all security requirements, you can choose to display a badge on your Data safety section stating that you have completed the "Independent Security Review."

Authorized Labs have a dedicated practice area around mobile app security and provide comprehensive security testing capabilities and experience. These labs also comply with ISO 17025 or an equivalent industry-recognized standard**.** If you meet this criteria and are interested in becoming a lab partner, please complete and submit this [form](https://docs.google.com/forms/d/1vvnbgJ1RqdBSHXAyrxd0hkCRTcykPhznHVhbk812gW4/edit?ts=6168803d) with your company details.

**Important:** This independent review may not be scoped to verify the accuracy and completeness of your Data safety declarations. Even if you use third-party tools to diagnose your app’s security controls, you remain solely responsible for making complete and accurate declarations in your app’s store listing on Google Play.

Unified Payments Interface Badge (UPI)

The [Unified Payments Interface (UPI)](https://www.npci.org.in/what-we-do/upi/product-overview) is an instant money transfer system, developed by the National Payments Corporation of India (NPCI), a RBI-regulated entity. If you currently utilize this payments transfer system, you can choose to declare so in your Data safety form. If you are interested in participating or have questions, you can contact NCPI directly for eligibility criteria on how to have your app accredited. Apps with this accreditation may be eligible to display a badge on their Play Store listing verifying that NPCI has validated this app’s implementation of UPI. The badge will read "Offers Payments through UPI," and will not appear to users unless you indicate so by opting in within the Data safety form in Play Console. The badge is only visible to Google Play users based in India.
