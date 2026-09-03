<!-- source=subscriptions clause=configuring-subscription-offers url=https://developer.apple.com/app-store/subscriptions/ fetched=2026-09-03T19:54:29+00:00 -->

### Configuring subscription offers

When setting up offers in App Store Connect, you’ll choose the offer type, eligibility, duration, pricing, and more. To support offers within your app, you’ll use [StoreKit APIs](/documentation/storekit/in-app_purchase/supporting_subscription_offer_codes_in_your_app/). For each offer you create, you’ll choose one of the following [offer discount types](/help/app-store-connect/reference/pricing-and-availability/app-pricing-and-availability/):

**Free trial.** A subscriber can access your subscription for free for a specific duration — for example, a one-month free offer for a subscription with a standard renewal price of $4.99 per month. Their subscription begins immediately, but they won’t be billed until the offer duration ends. This discount type may be useful if you want to let people experience your subscription at no immediate cost to them.

**Pay as you go.** A subscriber pays a discounted price each billing period for a specific duration — for example, $1.99 per month for three months for a subscription with a standard renewal price of $9.99 per month. Once the duration is over, they’re billed at the standard renewal price. This option may be useful if you want to attract price-sensitive people with a recurring discount without having to offer that discount for the lifetime of the subscription.

**Pay up front.** A subscriber pays a one-time price for a specific duration — for example, $9.99 up front for the first six months of a subscription with a standard renewal price of $39.99 per year. Once the duration is over, they’ll be billed at the standard renewal price. This may be useful if you want to offer an extended experience that gives people time to enjoy the subscription before the next renewal.
