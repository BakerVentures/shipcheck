<!-- source=subscriptions clause=providing-support url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-04T07:14:04+00:00 -->

### Providing support

Thoughtful customer support helps you manage relationships with your subscribers and can lead to improved engagement, higher retention, and better ratings and reviews. Use StoreKit and App Store server APIs to provide more seamless subscriber support, and to resolve issues in a more timely and efficient manner.

#### Letting people manage their subscriptions

A subscriber’s preferences may change during a subscription period. You can use the [showManageSubscriptions(in:)](/documentation/storekit/appstore/3803198-showmanagesubscriptions/) method to let them manage their subscription within your app. By providing a dedicated place in your app to manage subscriptions, you can also display other options to complement the system-provided management UI. For example, you might show a promotional offer that provides a higher service level for a discounted price. If they cancel, you might provide an offer to help win them back and encourage them to resubscribe. Or you might present a survey where they can share feedback about their subscription experience and reasons for cancelling, which can inform your marketing strategy. To ensure a positive experience, always make it easy for people to access the system-provided management UI where they can cancel if they wish.

#### Extending a subscription’s renewal date

In cases of service or content delivery issues — such as a server outage or technical glitch — you can extend the renewal date of a subscription using the [Renewal Date Extension endpoint](/documentation/appstoreserverapi/extend_a_subscription_renewal_date/). For example, if a sports match is canceled or there’s an interruption to a livestreamed event, you might extend free service for a specified time in order to make up for the issue. You can move the renewal date for a customer’s subscription twice per calendar year, each up to 90 days in the future. Any days included in an extension won’t count toward the one year of paid service needed to receive an 85% proceeds rate.

Alternatively, you can use [offer codes](/app-store/subscriptions/#offer-codes) to compensate dissatisfied subscribers with a free or discounted subscription for a specific period of time. These codes can be redeemed on the App Store or within your app.

#### Determining subscriber status

The [Get All Subscription Statuses](/documentation/appstoreserverapi/get_all_subscription_statuses/) endpoint lets you determine in one simple check whether a subscription is active, expired, in billing retry, or in grace period. Use this information to inform your retention strategy and provide subscribers with relevant information within your app, such as their upcoming renewal date. You can also use this endpoint alongside the [OfferID](/documentation/storekit/transaction/3822312-offerid/) and [OfferType](/documentation/storekit/transaction/3822313-offertype/) transaction properties in StoreKit to identify offer redemptions.

- [Learn to support customers with StoreKit 2 and the App Store Server API](/videos/play/tech-talks/10887/)
- [Learn to support customers and manage refunds](/videos/play/wwdc2021/10175/)
- [Learn to help people manage their subscriptions](/design/human-interface-guidelines/in-app-purchase#Providing-help-with-in-app-purchases)
