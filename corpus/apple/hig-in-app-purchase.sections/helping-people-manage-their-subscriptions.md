<!-- source=hig-in-app-purchase clause=helping-people-manage-their-subscriptions url=https://developer.apple.com/design/human-interface-guidelines/in-app-purchase fetched=2026-09-04T16:10:00+00:00 -->

### Helping people manage their subscriptions

Supporting subscription management means people can upgrade, downgrade, or cancel a subscription without leaving your app. Offering subscription management within your app also gives you a natural place to provide help for common subscriber issues and present alternative offers for people to consider.

![A screenshot of an app’s subscription settings screen on iPhone. It includes the app name, subscription level, price, and next billing date, above buttons for Manage Subscription, Restore Purchase, and Redeem Code.](https://developer.apple.com/images/com.apple.HIG/subscription-management@2x.png)

**Provide summaries of the customer’s subscriptions.** In particular, people appreciate viewing the upcoming renewal date without having to search for it. Consider displaying this information in a settings or account screen, near the subscription-management option. For developer guidance, see [Product.SubscriptionInfo](https://developer.apple.com/documentation/storekit/product/subscriptioninfo).

**Consider using the system-provided subscription-management UI.** Using StoreKit APIs lets you present a consistent experience that helps people manage or cancel their subscriptions without leaving your app. For developer guidance, see [showManageSubscriptions(in:)](https://developer.apple.com/documentation/storekit/appstore/showmanagesubscriptions(in:)).

**Consider ways to encourage a subscriber to keep their subscription or resubscribe later.** When you use StoreKit APIs, your app is notified when someone chooses to cancel their subscription. In this scenario, you might want to extend a personalized offer as an alternative to cancellation or invite people to describe their reasons for canceling in an exit survey. In addition to giving you insights into various customer problems, survey feedback can also help inform messaging for retention and win-back strategies.

![A screenshot of a resubscribe screen in the Math School app running on iPhone. The bottom half of the screen includes the label Resubscribe to Math School in large text, and the first of five pages which describe benefits of resubscribing. Below the page view area is a Resubscribe Now button with a six-month resubscription offer at 50 percent off, and a Sign In button.](https://developer.apple.com/images/com.apple.HIG/promotional-offer@2x.png)

**Always make it easy for customers to cancel an auto-renewable subscription.** If the manage subscription action is deep within an app — or hard to recognize — subscribers can feel they’re being discouraged or prevented from canceling.

**Consider creating a branded, contextual experience to complement the system-provided management UI.** Within your custom UI, you might offer a popular premium tier or provide personalized suggestions for alternative plans based on what you know about the customer’s preferences or how they use your app. For example, you can create a promotional offer that provides a discounted price for a specific period of time. You might also consider subscription [offer codes](https://developer.apple.com/design/human-interface-guidelines/in-app-purchase#Supporting-offer-codes) to help you win back lapsed subscribers and encourage existing subscribers to upgrade.
