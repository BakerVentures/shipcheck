<!-- source=subscriptions clause=managing-prices url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-03T19:54:29+00:00 -->

### Managing prices

You can price your auto-renewable subscriptions by storefront and choose from 800 price points across all available currencies and price tiers, with an additional 100 higher price points available upon request. After you set a starting price for your auto-renewable subscription, you can schedule one future price change at a time, per territory in App Store Connect.

**Price decreases.** If you decrease the price of your auto-renewable subscription, existing subscriptions will automatically renew at the lower price. You don’t have the option to preserve the higher price for existing subscribers. Existing subscribers don’t receive any communications and don’t need to take any action.

**Price increases.** When you increase the price of an auto-renewable subscription, Apple automatically provides push notifications, email, and in-app messaging to let subscribers know about the upcoming change and how to manage their subscription. Some price increases require subscribers to opt in, while smaller, infrequent price increases can result in notifications without the need to opt in.

If needed, you can temporarily delay the in-app price consent sheet to avoid interrupting someone during a critical moment.

You can keep an unlimited number of active subscribers at their existing price while increasing the price for new subscribers. If you don’t preserve the price for existing subscribers, and they need to consent, they must agree to the new price. If they don’t agree, their subscription expires at the end of their current billing cycle.

If you have several cohorts of subscribers at different prices and want to move all subscribers to the current price, increase the price for those paying closest to the current price first (for example, $2.99 to $3.99), then the next closest, and so on. This ensures that people don’t experience multiple price increases. Before you make any pricing decisions, research your target market’s pricing expectations and weigh the potential impact of raising the price against retaining subscribers.

Resources:

- [Manage pricing for auto-renewable subscriptions](/help/app-store-connect/manage-subscriptions/manage-pricing-for-auto-renewable-subscriptions/)
- [Manage auto-renewable subscription pricing in App Store Connect](/videos/play/tech-talks/110350/)
- [Delay the price consent sheet](/documentation/storekit/skpaymentqueuedelegate/3521328-paymentqueueshouldshowpriceconse/)
