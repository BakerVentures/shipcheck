<!-- source=subscriptions clause=retaining-subscribers url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-04T16:10:00+00:00 -->

### Retaining subscribers

Use the [Get All Subscription Statuses](/documentation/appstoreserverapi/get_all_subscription_statuses/) endpoint and [Get Transaction History](/documentation/appstoreserverapi/get_transaction_history/) endpoint to determine the status of your users’ subscriptions and view transaction history, so you can identify and act on:

**Voluntary churn.** Determine if a subscriber has turned off auto-renew for a particular subscription using the [Get All Subscription Statuses](/documentation/appstoreserverapi/get_all_subscription_statuses/) endpoint. You can also use App Store Server Notifications to get real-time updates about changes in a user’s status and key events related to their In-App Purchases, such as a change in renewal status. Use this information to take action in response. For example, you might present a promotional offer or suggest an alternate tier that better fits their needs. When a subscription expires, you can lock access to the subscription’s content or service. Be sure to inform the user of any changes and let them know if there’s anything they need to do in response and how to resubscribe if needed.

**Involuntary churn.** Sometimes a subscriber might experience a billing issue, such as an expired credit card, that causes their subscription to expire. Starting in iOS 16.4 and iPadOS 16.4, if a subscription doesn’t successfully renew, a system-provided sheet appears in your app upon launch with a prompt that lets customers update the payment method for their Apple Account. If you’d like, you can choose to delay or suppress this sheet in StoreKit using [messages](/documentation/storekit/message) and [display](/documentation/storekit/message/3963915-display/).

You can learn when a subscription fails to renew using:

- App Store server notifications, which sends a DID_FAIL_TO_RENEW notification type.
- [StoreKit renewal state](/documentation/storekit/product/subscriptioninfo/renewalstate/) to get information about the renewal state.
- [The App Store Server API](/documentation/appstoreserverapi/get_all_subscription_statuses/) to get all subscription statuses.

When a subscription renewal fails, Apple attempts to recover it for 60 days. If you’ve chosen to pause access to your service or content during this time, you’ll need to reinstate access once the issue is resolved. If the subscription renews within 60 days, the days of paid service resume from the renewal date.

To prevent service interruptions due to billing issues, enable Billing Grace Period in App Store Connect. Apple attempts to address the billing issue and recover the subscription while the subscriber retains subscription access. You can choose to apply Billing Grace Period to all renewals (existing paid renewals and free offers transitioning to paid renewals) or only to existing paid renewals. You can also set a duration of 3, 16, or 28 days. Be sure to consider what Billing Grace Period configuration best aligns with your business. If the subscription is recovered within the Billing Grace Period, there won’t be any interruption to the days of paid service or to your revenue. If someone resubscribes after 60 days, the days of paid service reset and you’ll receive the standard one-year subscription rate until the next year of paid service passes.

**Price increase consent.** When you increase the price of a subscription and Apple asks affected subscribers to agree to the new price, you can keep track of their consent status before the change takes effect. Before displaying the price increase sheet to affected users, you might show an in-app message that explains the benefits of the subscription and how the price increase improves the service. If someone doesn’t respond to the increase, their subscription expires at the end of their current billing cycle.

Resources:

- [App Store Server API](/documentation/appstoreserverapi/)
- [App Store Server Notifications](/documentation/appstoreservernotifications/)
- [Reduce involuntary subscriber churn](/documentation/storekit/original_api_for_in-app_purchase/subscriptions_and_offers/reducing_involuntary_subscriber_churn/)
- [Enable Billing Grace Period](/help/app-store-connect/manage-subscriptions/enable-billing-grace-period-for-auto-renewable-subscriptions/)
