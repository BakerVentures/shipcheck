<!-- source=subscriptions clause=promotional-offers url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-03T19:54:29+00:00 -->

### Promotional offers

Grow and retain your customer base by giving existing or former subscribers a free or discounted subscription for a specific duration. You decide the business logic for promotional offers, giving you the flexibility to create unique promotions within your app, such as:

- An upgraded subscription at a special price for people who have canceled their subscription
- A free month of service for a tenured subscriber who has renewed multiple times
- A discounted price on a month of service for a subscriber who may not be consistently engaging with your app or game

Use [StoreKit](/documentation/storekit/original_api_for_in-app_purchase/subscriptions_and_offers/implementing_promotional_offers_in_your_app/) or App Store Server APIs to identify the auto-renewal statuses of your subscribers and understand which offers might be most effective. To easily determine eligibility, enable App Store Server Notifications for your app. This allows you to receive notifications when a subscriber's status changes, helping you understand when to display an offer to someone. You can have up to 10 offers for each subscription — be sure to consider the implications of having multiple offers in effect. Learn about [configuring promotional offers](/help/app-store-connect/manage-subscriptions/set-up-promotional-offers-for-auto-renewable-subscriptions/) in App Store Connect.
