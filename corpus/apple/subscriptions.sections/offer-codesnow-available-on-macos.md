<!-- source=subscriptions clause=offer-codesnow-available-on-macos url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-03T19:54:29+00:00 -->

### Offer codesNow available on macOS

Use offer codes to acquire, retain, and re-acquire subscribers by providing a subscription at a discount or for free for a limited time. You can create two types of offer codes: one-time-use codes (18-digit unique codes), or custom codes (such as SPRINGPROMO). Learn how to [create offer codes](/help/app-store-connect/manage-subscriptions/set-up-offer-codes) and how to [support offer codes](/documentation/storekit/appstore/supporting_subscription_offer_codes_in_your_app) using StoreKit. To get notified of redemptions, ensure you've set up App Store Server Notifications.

#### Distribution

When distributing offer codes, you can use your online and offline marketing channels, such as in-app merchandising, email, or print campaigns. Consider which channels might be most effective at reaching your intended customers.

Offer codes can be used in a variety of ways — for example, you can:

- Send an email sharing the latest features and recently added content with an offer code to current or previous subscribers, so they can experience your service for a limited time.
- Distribute flyers that include custom codes to promote your service to event attendees.
- Partner with another company on a marketing initiative or campaign to help promote your app to new subscribers.
- Create a peer-to-peer member referral program that enables current subscribers to share an offer code and receive a benefit for promoting your app. You are responsible for distributing any benefits or rewards to subscribers.
- Provide a code to a subscriber with a customer service issue to compensate for the issue and encourage retention.
- Distribute one-time-use codes within an app that you’re sunsetting as a way to transition current subscribers to your new app and promote your service.
- Display a save offer in your app to a subscriber who has turned off auto-renew but their subscription hasn’t expired yet.

#### Redemption

Customers can redeem offer codes using a [redemption URL](/news/?id=dopmcbjk) or on the App Store (in iOS 14.2, iPadOS 14.2, and macOS 15 or later). They can also redeem offer codes within your app if your app supports the [offerCodeRedemption](/documentation/storekit/storeview/4203466-offercoderedemption) method. For a smooth customer experience, be sure to mention any eligibility or availability limits in your communications.

Apple handles the redemption experience, which includes an offer details screen that includes your app icon, subscription display name, duration, and pricing. If you’ve previously added a promotional image for the subscription, this is shown instead of your app icon. To help people make an informed decision, make sure that these details clearly describe the subscription experience. In order for offer codes to be redeemed, your app must be available on the App Store. If someone doesn’t have your app, they’ll be able to download it during the redemption experience.

Depending on your subscription setup, existing subscribers may be able to redeem more than one offer if the offers are in different subscription groups. If you intend for someone to subscribe to only one subscription group at a time, make sure the offer is within their current subscription group. Existing subscribers can only redeem codes that are an upgrade from or at the same level as their current subscription.

Be sure to provide a relevant experience based on someone’s subscription status. For example, you might provide onboarding that highlights the benefits of your subscription for new subscribers. If your app includes account creation or requires agreement to additional terms, make this process as smooth as possible for customers who redeemed a code and are new to your app.

#### Subscription offer codes essentials

#### Get started with custom offer codes
