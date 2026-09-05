<!-- source=account-deletion-play clause=frequently-asked-questions url=https://support.google.com/googleplay/android-developer/answer/13327111 fetched=2026-09-05T02:02:39+00:00 -->

## Frequently asked questions

Collapse All Expand All

What is an app account?

An app account is a unique user identity that developers provide as a user-facing feature to serve the user across applications and/or devices (can often include use of usernames, email addresses, and passwords). App accounts provide a mechanism for a user to authenticate and generally include a mechanism to verify an identity, such as password, phone number OTP (one-time password), 2FA (two-factor authentication), biometric, SSO (single sign-on), and so on.

What does “if your app allows users to create an account from within the app” mean?

Your app supports account creation within the app if a user can complete creating an app account directly in the app or if the app directs the user to an app account creation flow outside of the app.

What if my app can be used without creating an app account?

If your app offers account creation in any part of the app experience, then you still need to offer app account deletion even if some features can be accessed without an account.

Do users need to be able to complete their account deletion request solely within the app experience?

A full end-to-end mobile first account deletion can be a great user experience. However, we understand that this may not yet be feasible for some developers, so we’re giving you options on how to meet this requirement. As an alternative, you can choose to provide a link within your app that takes users to your app account deletion web resource.

What types of user data are in scope to be deleted?

When you delete an app account based on a user’s request, you must also delete the user data associated with that app account. It is possible that your app may need to retain certain data for legitimate reasons such as security, fraud prevention or regulatory compliance. Examples of user data include: [personal and sensitive user data](https://support.google.com/googleplay/android-developer/answer/10144311#personal-sensitive), personally identifiable information, financial and payment information, authentication information, phonebook, contacts, device location, SMS and call-related data, health data, Health Connect data, inventory of other apps on the device, microphone, camera, and other sensitive device or usage data. All user data indicated as [collected in your data safety section](https://support.google.com/googleplay/android-developer/answer/10787469#data_types) is within scope. Those apps within highly regulated industries that require additional retention periods must clearly inform users within their data retention policies.

Am I required to delete account data that was previously shared with a third party?

If your app relies on service providers to process user data, you should delete the data from your own servers and request the service provider to do the same.

How quickly should I fulfill users’ deletion requests?

You should let users know what to expect and complete their requests within a reasonably quick period of time. Make sure to check with your legal advisors as laws and regulations in some countries impose specific requirements and restrictions concerning data deletion and retention.

Am I required to fill out account deletion questions within the Data safety form in Play Console?

Yes, all developers will be prompted and required to answer a new set of questions in the Data safety form focused around deletion practices. If your app is within the scope of the policy requirements, you must disclose if your app provides account deletion and provide the web link within your Data safety form in Play Console. Some updates to your form will be reflected on your app store listing’s Data safety section.

I offer a fully integrated in-app account deletion experience. Why do I still need to provide a link to a web resource?

Some users may have already uninstalled your app or not be able to access your in-app experience for a variety of other reasons. We want to ensure that all users can still exercise control over their data by being able to go to the web link based deletion resource that developers provide. This means that your web resource should give users a way to request that their data be deleted without sending the user back to the app and requiring them to re-download it to submit their request.

What are the requirements for the web link and resource?

The weblink must be functional (for example, loads without error), relevant in scope (for example, the pathway to request account deletion should be prominently featured and easily discoverable on the page) and reference the app or developer name (that is, as it appears on your store listing in Google Play). The user must be able to request deletion of their account through the pathway. You can offer this in many ways, like an additional link that initiates account deletion, a customer service email or a form they can submit a request through. If the user needs to take additional steps before deleting their account (for example, canceling a subscription), this must be clearly outlined, and a support flow must be available for users to initiate. If you plan to use existing privacy or data retention policies to fulfill this requirement, the data deletion section should be highlighted and reasonably prominent (for example, through an anchor link).

Are there any exemptions to this policy requirement?

Permanently private and enterprise device management apps are exempt from this policy requirement. Please note if your app falls within a highly regulated industry (such as utilities, healthcare, or financial services, for example), it is permissible if you need to provide additional flows to facilitate account deletion requests to completion. As a reminder, accounts that are created and operated offline are not app accounts and do not fall within policy scope.

Are there any circumstances where my app can retain certain data in the account deletion process?

It is possible that your app may need to retain certain data for legitimate reasons such as security, fraud prevention or regulatory compliance. In that case, you must clearly inform users about your data retention practices, for example, within your privacy policy.

What should my in-app deletion experience look like?

The requirements for your in-app path to deletion should be intuitive for the user. Meaning, the pathway should be prominent (for example, within the account settings or a similar section). We recognize that there are many ways developers can implement this within their apps.

What if my app functions on multiple non-mobile surfaces (for example: Android TV, Wear OS, or similar), how do these requirements apply?

We understand that a non-mobile in-app account deletion experience can be challenging for both the developer and the user. That is why non-mobile apps do not have to provide an option to initiate app account deletion from within the app. They are still required to have a readily discoverable option to initiate account deletion outside the app (for example, by visiting your website), and they must enter a link to this web resource in the designated URL form field within Play Console. Common non-mobile app surface experiences can include those on: web, Android TV, Wear OS, and similar.
