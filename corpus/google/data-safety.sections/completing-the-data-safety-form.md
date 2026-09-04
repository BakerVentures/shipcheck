<!-- source=data-safety clause=completing-the-data-safety-form url=https://support.google.com/googleplay/android-developer/answer/10787469 fetched=2026-09-04T16:10:05+00:00 -->

### Completing the Data safety form

What if my app behaves differently in different supported Android versions?

Google Play has one global Data safety form and Data safety section in the Google Play store listing per package name that is agnostic to usage, app version, region, and user age. In other words, if any of the collection, uses, or linkages are present in any version of the app presently distributed on Google Play, anywhere in the world, you must indicate such on the form. Therefore, your Data safety section describes the sum of your app’s data collection and sharing across all its versions currently distributed on Google Play. You can use the “About this app” section to share version-specific information with your users.

How can I show that we may have different practices in different regions? For example, we don’t use certain libraries in Europe, but we may use them in others.

At this time, we reflect the global representation of your data practices per app. Your Data safety section describes the sum of your app’s data collection and sharing across all its versions currently distributed on Google Play. You can use the “About this app” section to share version-specific information with your users. The Data safety section includes a clarification for Google Play users that an app’s data collection and security practices may vary based on a number of factors such as the region.

Are the Data safety sections gated by a consent mechanism for users? Do I need to take any extra steps and create an in-app prominent disclosure?

No, the Data safety section is only presented on your app's store listing on Google Play; there is no new disclosure in the user app install process, and there is no new user consent related to this feature. Developers that collect personal and sensitive user data must implement in-app disclosures and consent where required by the existing Google Play [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311).

How should I mark required or optional collection when different versions of my app that show a Data safety section do different things?

Your Data safety section describes the sum of your app’s data collection and sharing across all its versions currently distributed on Google Play. If any version of your app requires the collection of certain data, you must declare its collection as required for the Data safety section. You should not describe collection as optional if it is required for any of your app’s users. You can use the “About this app” section to share version-specific information with your users.

Do I need to declare data if my app includes a permission but does not actually collect or share the data?

You do not need to declare collection or sharing unless data is actually collected and/or shared. Your app must comply with all Google Play Developer Program policies, including our policy for [Permissions and APIs that Access Sensitive Information](https://support.google.com/googleplay/android-developer/answer/9888170).

If one data type is collected as part of another, should I declare both? For example, if I collected Contacts which includes the user's email, do I declare both the "Contacts" and "Email address" data types?

If you are purposefully collecting a data type during the collection of another data type, you should disclose both. For example, if you collect user photos and use them to determine users’ characteristics (such as ethnicity or race) you should also disclose the collection of ethnicity and race.

Am I required to provide a deletion mechanism? Must it be for any and all user data?

The Data safety section provides a surface for you to share if you provide a mechanism to receive data deletion requests from your users. As part of completing the Data safety form, you are required to indicate if you provide such a mechanism.

Is there a specific type of mechanism that I must provide to indicate my app supports user data deletion requests?

There is no prescribed mechanism, however as best practice the request mechanism should be easily discoverable and accessible by users. Common examples of mechanisms that clearly indicate a path by which users can request data deletion may include but are not limited to: in-app features, contact forms, or a dedicated email alias.

How should I indicate in my Data safety form that I provide a request for deletion mechanism for data that is automatically deleted or anonymized?

You may select the deletion request mechanism badge in Data safety form if you:

- provide users with a mechanism to request data deletion; or
- automatically initiate deletion or anonymization of collected data within 90 days of collection.

You may select the deletion request mechanism badge even if you need to retain certain data for legitimate reasons such as legal compliance or abuse prevention.

What if the deletion mechanism I provide is not available globally to all users ⁠⁠— can I still indicate I provide a deletion request mechanism?

Google Play provides one global Data safety form and Data safety section in the Google Play store listing per package name that should cover data practices based on any usage, app version, region, and user age. In other words, if any of the data practices are present in any version of the app presently distributed on Google Play, anywhere in the world, you must indicate these practices on the form. Therefore, your Data safety section will describe the sum of your app’s data collection and sharing across all its versions currently distributed on Google Play.

What kinds of techniques can be used to make data anonymous?

There are a variety of potential methods to anonymize data such that it cannot be associated with an individual user. You should consult with your privacy and security experts to identify the methods applicable to your use case. As an example, [this page](https://policies.google.com/technologies/anonymization) discusses some of the data anonymization methods used by Google, such as differential privacy.

How should I treat the collection and use of IP addresses?

As with other data types, you should disclose your collection, use and sharing of IP addresses based on their particular usage and practices. For example, where developers use IP addresses as a means to determine location, then that data type should be declared.

How should I disclose the collection and sharing of other kinds of identifiers?

As with other data types, you should disclose your collection, use and sharing of different kinds of identifiers based on your particular usage and practices. For example, the collection of an account name associated with an identifiable person should be declared as a “Personal identifier,” and the collection of a user’s Android Advertising ID should be declared as “Device or other identifiers.” As another example, an identifier related to a specific in-app event, but that does not reasonably relate to an individual device, browser or app, would not need to be disclosed as “Device or other identifiers.”

As noted above, the collection of data pseudonymously should be disclosed on your survey under the relevant data type. For example, if you collect diagnostic information with a device identifier, you should still disclose the collection of “Diagnostics” in your Data safety form.

What kinds of activities can “service providers” perform?

A service provider may only process user data on your behalf. For example, an analytics provider that processes user data from your app solely on your behalf, or a cloud provider hosting user data from your app for your use, will typically qualify as “service providers.” On the other hand, if an SDK provider is building advertising profiles across multiple customers based on your app data, that would not be considered “service provider” activity for purposes of the Data safety section, and would need to be disclosed as "sharing" in your Data safety form.

My app uses an external payment service to enable financial transactions. Does my app need to disclose financial information like credit card info in its Data safety section?

It depends on the nature of your integration with the payment service. If your app uses a payment service such as PayPal, Google Pay, Google Play's billing system, or similar services to complete payment transactions, you don’t need to declare collection of the data that the payment service collects in connection with its processing of financial transactions, such as a credit card number, if the following conditions are met:

- Your app never accesses this information; and
- The payment service collects this information directly from the user, and collection is governed by that service’s terms.

You should review your integration with the payment service closely to ensure that your app’s Data safety section declares any relevant data collection and sharing that does not meet these conditions. You should also consider whether your app collects other financial information, like purchase history, and whether your app receives any relevant data from the payments service, for example for risk and anti-fraud purposes.

My app enables users to upload their data directly to Google Drive or Dropbox for backup or storage. My app does not access any of this data. Should that still be disclosed as “collection”?

It depends on the particular implementation. If the user chooses to upload their data directly to their own external drive or cloud storage account (such as Google Drive, Dropbox, or similar services) and this upload is governed by the external drive or cloud storage provider's terms of service and privacy policy, and your app never collects or accesses the data in question, then your app does not need to declare the collection of this data.

How should I encrypt data in transit?

You should follow best industry standards to safely encrypt your app’s data in transit. Common encryption protocols include TLS (Transport Layer Security) and HTTPS.

My app lets the user create an account or add information to their account, for example, birthday or gender. How should I declare the data that the user adds to their account?

You should declare the collection of this data for account management, denoting (if applicable) where collection is optional for the user.

In addition, as with any data types collected by your app, you should disclose this data for the purpose(s) for which your app uses it. For example, if your app allows a user to add a birthday to their account and also uses that data to send timely push notifications, your app should also declare this purpose in addition to account management.

Account management can be used to cover general uses of account data that are not specific to the particular app. For example, if you use account information for fraud prevention, advertising, marketing, or developer communications across your services, and this use is not specific to your app, or activities in your app, declaring “account management” as the purpose of collecting this account data will be sufficient to cover those general uses in your Data safety section. However, your app must always declare all purposes for which the app itself uses the data. As a best practice, we recommend disclosing how your app handles user data for account services as part of your account-level documentation and sign-up process.

What are System services?

[System services](https://support.google.com/googleplay/android-developer/answer/12085265) are pre-installed software that support core system functionality. System services can apply for an exemption from completing the Data safety form.

My app’s Data safety section submission was approved but I recently received a notification regarding an update. How do I check the current status of my submission and is that not permanent?

You can check the status of your submission on the [**App content**](https://play.google.com/console/app/app-content/summary) page in Play Console. If your submission is compliant, you will see a green check mark in the “Data safety” section.

**Note:** Our policies are enforced through systems and processes that are continuously improved over time. Additionally, changes and updates to our policies can result in apps which were approved earlier to be enforced upon at a later time following initial submission due to non-compliance.

Google Play will notify developers regarding any updates. You can check our [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311) and this Help Center article to make sure you are aware of the most up to date guidance.

How do I declare collection of data that is used in a transient way to load pages and service other client-side requests in real time before that data is logged on our servers and used for other purposes?

If this use is ephemeral, you do not need to include it in your form response. However, you must declare any use of that user data beyond the ephemeral processing, including any purposes for which you use the user data that you log. Please review the definition of ephemeral processing in the [Data collection](https://support.google.com/googleplay/android-developer/answer/10787469#collection) section above.

What is the difference between the permissions list and the Data safety section of an app?

Google gathers information for the permissions list based on the install-time permissions that an app declares in its manifest.

The Data safety section shares what data the app collects and shares with third parties.
