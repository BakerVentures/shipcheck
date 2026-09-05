<!-- source=hig-in-app-purchase clause=supporting-offer-codes url=https://developer.apple.com/design/human-interface-guidelines/in-app-purchase fetched=2026-09-05T02:02:31+00:00 -->

### Supporting offer codes

In iOS and iPadOS, subscription offer codes let you use both online and offline channels to give new, existing, and lapsed subscribers free or discounted access to your subscription content. For example, you might provide offer codes through email, give them out at a store or event, or print one on a physical product.

There are two types of offer codes you can support:

- A *one-time use code* is a unique code you generate in App Store Connect. People can redeem a one-time use code through a [redemption URL](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-offer-codes/#distribute-offer-codes) (a shareable link), within your app (when you support redemption), or by entering it in the App Store, where they’re prompted to install your app if they haven’t already. Consider using one-time use codes when your distribution is small or when you need to restrict access to a code.
- A *custom code* is a code you create, such as NEWYEAR or SPRINGSALE. People can redeem a custom code through a redemption URL or within your app (when you support redemption). Consider using a custom code when you want to support a large campaign that requires a mass distribution of codes.

For developer guidance on implementing offer codes, see [Offer codes](https://developer.apple.com/documentation/storekit/implementing-offer-codes-in-your-app) and [Set up offer codes](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-offer-codes). For guidance on other types of offers, see [Providing subscription offers](https://developer.apple.com/app-store/subscriptions/#providing-subscription-offers).

**Clearly explain offer details.** To help people make an informed decision, provide a straightforward and succinct description of your offer in your marketing materials.

**Follow guidelines for creating a custom code.** A custom code can contain only alphanumeric ASCII characters. Don’t use special characters, including Chinese and Arabic characters.

**Tell people how to redeem a custom code.** Because people can’t redeem a custom code by entering it in their App Store account settings, it’s important to let them know that they can redeem it through a redemption URL or within your app.

**Consider supporting offer redemption within your app.** The system automatically provides screens that present the offer-redemption flow, whether people redeem the offer in your app or in the App Store. When you use StoreKit API to let people redeem offer codes within your app, the only custom UI you need to create is one that initiates the system-provided flow. For developer guidance, see [presentOfferCodeRedeemSheet(in:)](https://developer.apple.com/documentation/storekit/appstore/presentoffercoderedeemsheet(in:)) and [offerCodeRedemption(isPresented:onCompletion:)](https://developer.apple.com/documentation/swiftui/view/offercoderedemption(ispresented:oncompletion:)). There are several natural places to provide this custom UI. For example, you could add a “Redeem Code” button to your paywall, onboarding screens, or your app’s settings screen.

After people tap your custom redeem button, the system automatically provides a series of code-redemption screens like the ones shown below.

**Supply an engaging and informative promotional image.** Creating this optional image can help people understand the value of your content. If you don’t supply a promotional image, the code redemption screens use your app icon by default. To learn more, see [Promoting your in-app purchases](https://developer.apple.com/app-store/promoting-in-app-purchases/).

**Help people benefit from unlocked content as soon as they complete the redemption flow.** Think about ways to align the post-redemption experience in your app with the subscriber’s new status. For example, you might provide a welcome experience for new subscribers or a brief tour of new features for an existing subscriber who’s unlocked additional functionality. In particular, be prepared to welcome people who subscribe before they open your app for the first time. For example, if you require people to create an account or sign in before they can use your app, make this process as smooth as possible for new subscribers who haven’t experienced it before.
