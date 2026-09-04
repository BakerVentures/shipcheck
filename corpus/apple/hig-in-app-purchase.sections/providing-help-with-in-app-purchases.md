<!-- source=hig-in-app-purchase clause=providing-help-with-in-app-purchases url=https://developer.apple.com/design/human-interface-guidelines/in-app-purchase fetched=2026-09-04T07:14:04+00:00 -->

### Providing help with in-app purchases

Sometimes, people need help with a purchase or want to request a refund. To help make this experience convenient, you can present custom UI within your app that provides assistance, offers alternative solutions, and helps people initiate the system-provided refund flow. For developer guidance, see [beginRefundRequest(for:in:)](https://developer.apple.com/documentation/storekit/transaction/beginrefundrequest(for:in:)-65tph); for related guidance specific to auto-renewable subscriptions, see [Helping people manage their subscriptions](https://developer.apple.com/design/human-interface-guidelines/in-app-purchase#Helping-people-manage-their-subscriptions).

**Provide help that customers can view before they request a refund.** In addition to including a link to the system-provided refund flow, your custom purchase-help screen can provide assistance you tailor to your app. For example, your custom screen might help people resolve problems with missing purchases, answer frequently asked questions about the in-app purchases you offer, and give people ways to submit feedback or contact you directly for support.

![A partial screenshot of an app’s help screen on iPhone. The Back button is in the top-left of the screen. In a list titled ’How can we help?’ there are the following five help items, each of which can open a new screen: Missing a Purchase, Frequently Asked Questions, Request a Refund, Submit Feedback, and Contact Us.]

**Use a simple title for the refund action, like “Refund” or “Request a Refund”.** The system-provided refund flow makes it clear that people request a refund from Apple, so there’s no need to reiterate this information.

**Help people find the problematic purchase.** For each recent purchase you display, include contextual information that helps people identify the one they want. For example, you might display an image of the product — along with its name and description — and list the original purchase date.

![A partial screenshot of an app’s refund screen titled Request a Refund on iPhone. The Back button in the top-left of the screen is labeled 'Help' to indicate it takes people back to the help screen. In a list titled Purchases, the screen displays the following three recent purchases: Power Surge, Les Cheneaux Islands, and Cape Cod.]

**Consider offering alternative solutions.** For example, if the customer didn’t receive the item they purchased, you might offer immediate fulfillment or a conciliatory item. Regardless of the alternatives you offer, make it clear that people can still request a refund.

**Make it easy for people to request a refund.** Although your purchase-help screen can offer useful information and alternative solutions, make sure this content doesn’t create a barrier to requesting a refund. For example, avoid making people scroll or open another screen to reveal your refund-request button. When people choose your refund-request item, they automatically enter the system-provided refund flow shown below.

**Avoid characterizing or providing guidance on Apple’s refund policies.** For example, don’t speculate about whether customers will receive the refund they request. To help people understand the refund-request process, you can provide a link to [Request a refund for apps or content that you bought from Apple](https://support.apple.com/en-us/HT204084).
