<!-- source=account-deletion clause=frequently-asked-questions url=https://developer.apple.com/support/offering-account-deletion-in-your-app/ fetched=2026-09-04T07:14:07+00:00 -->

## Frequently asked questions

##### Can I direct users to a customer service flow to complete account deletion?

It depends. Apps in highly regulated industries, as described in [App Store Review Guideline 5.1.1(ix)](/app-store/review/guidelines/#data-collection-and-storage), may use additional customer service flows to confirm and facilitate the account deletion process. Apps not operating in highly regulated industries should not require people to make a phone call, send an email, or go through other support flows.

##### Can I require reauthentication or add confirmation steps to ensure that the account isn’t deleted by accident or by someone other than the account holder?

Yes. It is appropriate to ensure that the deletion is intentional and desired by the user. You may add steps to verify the identity of the person making the request, and to confirm that they want to delete the account (such as by entering a code from an email or phone number already associated with the account). However, apps that make it unnecessarily difficult for a user to delete their account will not pass review.

##### My app uses Sign in with Apple to provide account creation and authentication to users. What changes are necessary to support users who delete their accounts?

Apps that support Sign in with Apple should use the Sign in with Apple REST API to revoke user tokens. To learn more, [review the documentation](/documentation/sign_in_with_apple/revoke_tokens/) and [design recommendations](/design/human-interface-guidelines/ios/user-interaction/accounts/).

##### If my app links out to the default web browser for account creation, does it still need to offer account deletion within the app?

Yes. Additionally, note that linking out to the default web browser to sign in or register an account provides a poor user experience and is not appropriate, per [App Store Review Guideline 4](/app-store/review/guidelines/#design).

##### My app automatically creates an account for the user. Do I need to include an option to initiate account deletion?

Yes. Users should have the option to delete automatically generated accounts (sometimes called “guest” accounts) and the data associated with those accounts. Ensure any automatic account creation in your app complies with local laws where your app is available.

##### I manually delete user accounts and this takes time. Does account deletion need to be immediate and automatic?

No. If your process for account deletion is manual or otherwise takes time to complete, this is acceptable. Inform the user how long it will take to delete the account and provide a confirmation when the deletion has been completed. Ensure the time taken to delete accounts complies with local laws where your app is available.

##### Does the content provided by a user need to be deleted in apps that display and share user-generated content?

Yes. People expect that all data associated with their account will be deleted when the account is deleted. This includes user-generated content that’s shared with others, such as photos, video, text posts, and reviews. If local laws or regulations require that you maintain some data, let your users know.

##### I currently allow account deletion in compliance with CCPA, GDPR, or other local laws in some of the locations where my app is available. Is this sufficient?

No. All users should be allowed to delete their accounts, regardless of where they’re located. The existing account deletion flows you’ve created to comply with local legal requirements may be made available to all users, as long as they meet the requirements of [App Store Review Guideline 5.1.1(v)](/app-store/review/guidelines/#data-collection-and-storage).

##### How do I handle users with auto-renewable subscriptions? I don’t want to accidentally charge someone after they’ve deleted their account.

If the user has auto-renewable subscriptions, notify them that their billing will continue through Apple and request that they cancel their subscription before continuing. If you’re using [App Store Server Notifications](/documentation/appstoreservernotifications/) for auto-renewable subscriptions, you can verify the status of the user’s subscription in real time, or use the [Subscription Status API](/documentation/appstoreserverapi/get_all_subscription_statuses/) to identify subscription status.

Use [showManageSubscription](/documentation/storekit/appstore/3803198-showmanagesubscriptions/) in iOS 15 and iPadOS 15, or later, or provide the following link to let users manage their subscriptions: [https://apps.apple.com/account/subscriptions](https://apps.apple.com/account/subscriptions/). For tvOS, provide onscreen instructions to change or cancel a subscription, as described in the [Apple TV User Guide](https://support.apple.com/guide/tv/subscriptions-atvb0d233668/tvos/).

In addition, you can use [beginRefundRequest](/documentation/storekit/transaction/3803220-beginrefundrequest/) in iOS 15 and iPadOS 15, or later, or provide the following Apple Support link to allow customers to submit refund requests: [https://support.apple.com/en-us/HT204084](https://support.apple.com/HT204084/).

You can also provide an option to schedule account deletion at a later time to align with the subscription’s expiration date, as long as there is also an option to delete the account immediately.
