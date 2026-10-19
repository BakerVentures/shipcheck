<!-- source=account-deletion clause=can-i-direct-people-to-a-customer-service-flow-to-complete-a url=https://developer.apple.com/support/offering-account-deletion-in-your-app/ fetched=2026-10-19T13:24:34+00:00 -->

### Can I direct people to a customer service flow to complete account deletion?

It depends. Apps in highly regulated industries, as described in [App Review Guideline 5.1.1(ix)](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage), may use additional customer service flows to confirm and facilitate the account deletion process. Apps not operating in highly regulated industries should not require people to make a phone call, send an email, use a chat support flow, or go through other support flows.

### Can I require reauthentication or add confirmation steps to ensure the account isn't deleted by accident or by someone other than the account holder?

Yes. It's appropriate to confirm the user genuinely intends to delete their account. You may add steps to verify the identity of the person making the request, and to confirm that they want to delete the account, such as by entering a code from an email or phone number already associated with the account. However, apps that make it unnecessarily difficult for someone to delete their account will not pass review.

### My app uses Sign in with Apple to provide account creation and authentication. What changes are necessary to support people who delete their accounts?

Apps that support Sign in with Apple should use the [Sign in with Apple REST API](https://developer.apple.com/documentation/signinwithapplerestapi) to [revoke user tokens](https://developer.apple.com/documentation/signinwithapplerestapi/revoke-tokens). Use server-to-server notification endpoints to [process changes for Sign in with Apple accounts](https://developer.apple.com/documentation/signinwithapple/processing-changes-for-sign-in-with-apple-accounts). Note that developers based in the Republic of Korea must [provide a server‑to‑server notification endpoint when registering a new Services ID](https://developer.apple.com/news/?id=j9zukcr6).
