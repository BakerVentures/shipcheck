<!-- source=user-privacy-and-data-use clause=can-i-explain-to-users-why-i-would-like-permission-to-track- url=https://developer.apple.com/app-store/user-privacy-and-data-use/ fetched=2026-09-28T14:01:57+00:00 -->

### Can I explain to users why I would like permission to track them before I show the tracking permission prompt?

Yes, so long as you are transparent to users about your use of the data in your explanation. Per the [App Review Guidelines: 5.1.1 (iv)](/app-store/review/guidelines/#5.1.1), apps must respect the user's permission settings and not attempt to manipulate, trick, or force people to consent to unnecessary data access.

### If I have not received permission from a user via the tracking permission prompt, can I use an identifier other than the IDFA (for example, a hashed email address or hashed phone number) to track that user?

No. You will need to receive the user's permission through the App Tracking Transparency framework to track that user.

### If a user provides permission for tracking via a separate process on our website, but declines permission in the App Tracking Transparency prompt, can I track that user across apps and websites owned by other companies?

Developers must get permission via the App Tracking Transparency prompt for data that's collected in the app and used for tracking. Data collected separately, outside of the app and not related to the app, is not in scope.
