<!-- source=account-deletion clause=how-do-i-handle-people-with-auto-renewable-subscriptions-i-d url=https://developer.apple.com/support/offering-account-deletion-in-your-app/ fetched=2026-10-19T13:24:34+00:00 -->

### How do I handle people with auto-renewable subscriptions? I don't want to accidentally charge someone after they've deleted their account.

If a person has an auto-renewable subscription, notify them that billing will continue through Apple and ask them to cancel their subscription before continuing. If you use [App Store Server Notifications](https://developer.apple.com/documentation/appstoreservernotifications/) for auto-renewable subscriptions, you can verify the status of the person's subscription in real time, or use the [Subscription Status API](https://developer.apple.com/documentation/appstoreserverapi/get-all-subscription-statuses) to identify subscription status.

Use [showManageSubscriptions](https://developer.apple.com/documentation/storekit/appstore/showmanagesubscriptions(in:)) in iOS 15 and iPadOS 15, or later, or provide this link to let people manage their subscriptions: [https://apps.apple.com/account/subscriptions/](https://apps.apple.com/account/subscriptions/). For tvOS, provide onscreen instructions to change or cancel a subscription, as described in the [Apple TV User Guide](https://support.apple.com/guide/tv/manage-subscriptions-atvb0d233668/tvos).

You can also use [beginRefundRequest](https://developer.apple.com/documentation/storekit/transaction/beginrefundrequest(in:)-9k0pj) in iOS 15 and iPadOS 15, or later, or provide this Apple Support link to let customers submit refund requests: [https://support.apple.com/118223](https://support.apple.com/118223).

Additionally, you can offer to schedule account deletion for a later date, aligned with the subscription's expiration, as long as there's also an option to delete the account immediately.

**Related** [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) [Manage Accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts)
