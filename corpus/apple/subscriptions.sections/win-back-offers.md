<!-- source=subscriptions clause=win-back-offers url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-04T07:14:04+00:00 -->

### Win-back offers

Reach previous subscribers and encourage them to resubscribe with win-back offers. Based on your configuration, Apple displays these offers to eligible customers in various places, such as on the App Store or in your app or game. For example, you can create a pay up front offer for a reduced subscription price of $9.99 for six months, with a standard renewal price of $39.99 per year.

#### Discovery and redemption

Eligible customers can discover and redeem win-back offers in several places, including:

**On the App Store:** On your product page and in editorial selections and personalized recommendations on the Today, Games, and Apps tabs if you’ve been featured. People can tap your offer to learn more details about your offer and open or redownload your app or game to seamlessly redeem your offer.

**In-app:** A win-back [offer sheet](/documentation/storekit/in-app_purchase/supporting_win-back_offers_in_your_app) automatically appears to eligible customers within your app or game, with no additional work required. For additional control and display customization, you can use StoreKit views or [StoreKit 2 APIs](/documentation/storekit/message) to merchandise win-back offers in your app.

**In their Apple account under their Subscription settings.** People can tap your app or game to view and redeem any available offers. This appears automatically with no additional work required.

**Using a direct link.** Similar to offer codes, you can use the URL provided in App Store Connect and share it with people through your own channels, such as email.

For more information on these placement types, see [set up win-back offers](/help/app-store-connect/manage-subscriptions/set-up-win-back-offers).

#### Configuration and merchandising

When [configuring win-back offers](/help/app-store-connect/manage-subscriptions/set-up-win-back-offers/) in App Store Connect, you provide offer details and select the offer priority. Your priority selection affects how your offer is ranked within your app, in someone’s Subscription settings, and on the App Store (if you’ve chosen to promote it). Apple uses your subscription display name and description when displaying your win-back offer, so be sure this information is accurate.

If you’d like to display your offer on the App Store, you’ll need an approved [subscription image](/help/app-store-connect/manage-in-app-purchases/view-and-edit-in-app-purchase-information#add-or-remove-an-image). Aim for a simple graphic that’s different than your app icon or screenshots that conveys the essence of the In-App Purchase included as part of the offer.

By default, [streamlined purchasing](/help/app-store-connect/manage-subscriptions/manage-streamlined-purchasing) is turned on for your app or game, which lets people complete a purchase from outside your app. You can turn this off in App Store Connect if you wish.

[Implement App Store Offers](/videos/play/wwdc2024/10110/)
