<!-- source=subscriptions clause=family-sharing url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-04T07:14:04+00:00 -->

### Family Sharing

Family Sharing allows a subscriber to share access to an auto-renewable subscription with up to five family members across their Apple devices. With a streamlined, convenient user experience, Family Sharing can help you attract subscribers, encourage paid subscriptions, increase engagement, and improve retention. You can enable Family Sharing for your subscription in App Store Connect. Please note that this can’t be undone.

Verify subscription access using purchase validation, then provide the proper access to subscribers and their family members. Whether a subscription is shared with a subscriber’s family by default depends on their subscription sharing settings and if the purchase was made before or after you enabled Family Sharing in App Store Connect. Subscribers whose settings don’t share the subscription by default are informed by Apple via push notification that the subscription can be shared with their family.

You can highlight Family Sharing in several ways:

**Highlight Family Sharing to potential subscribers.** Include Family Sharing in your subscription’s display name so it’s easy to spot when reviewing subscription options. If you offer a Family Sharing-enabled subscription alongside subscriptions that don’t include Family Sharing, you can note the price difference for the Family Sharing option on the sign up screen.

**Remind subscribers to enable Family Sharing.** Mention Family Sharing within your app — for example, as part of onboarding for new subscribers or via in-app messaging for existing subscribers. Consider explaining how to confirm they’ve turned on Family Sharing for the subscription. If you offer a Family Sharing-enabled subscription they’re not currently subscribed to, you might provide a way for them to upgrade without leaving your app. Make sure you’ve ranked your subscriptions within the same subscription level in App Store Connect to provide a seamless upgrade experience.

**Help subscribers share subscriptions.** You can use in-app messaging to ask subscribers to confirm their Family Sharing settings, or implement share extensions so they can easily share your app. Within the transaction information, you can look at [ownershipType](/documentation/storekit/transaction/3749705-ownershiptype/) to see if someone is the subscriber or a family member, so you can make sure to display your message to the person who completed the purchase.

Resources:

- [Turn on Family Sharing for in-app purchases](/help/app-store-connect/configure-in-app-purchase-settings/turn-on-family-sharing-for-in-app-purchases/)
- [Support Family Sharing in your app](/documentation/storekit/original_api_for_in-app_purchase/supporting_family_sharing_in_your_app/)
- [Family Sharing for in-app purchases](/videos/play/tech-talks/110345)
