<!-- source=subscriptions clause=getting-ready url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-03T19:54:29+00:00 -->

### Getting ready

To offer subscriptions, youʼll need to configure them in App Store Connect and use StoreKit APIs in your app. You’ll also need to assign each subscription to a subscription group (a group of subscriptions with different access levels, prices, and durations that people can choose from), then add details such as a name, price, and description. This information displays in the In-App Purchases section of your app’s product page on the App Store. Ensure that the subscriptions are available across all device types that your app supports. Consider allowing a way for subscribers to see the status of their subscription within your app, along with upgrade, crossgrade, and downgrade options, as well as a way to easily manage or turn off their auto-renewable subscription. Make sure to follow our design and review guidelines.

To get ready:

- Watch the [In-App Purchase and Subscriptions videos](/videos/app-store-distribution-marketing/).
- Refer to the [In-App Purchase StoreKit API documentation](/documentation/storekit/in-app_purchase/).
- Learn how to configure your subscriptions in [App Store Connect Help](/help/app-store-connect/).
- Use the [App Store Server API](/documentation/appstoreserverapi/) and enable [App Store Server Notifications](/documentation/appstoreservernotifications/) to get real-time changes to the status of your subscriptions.
