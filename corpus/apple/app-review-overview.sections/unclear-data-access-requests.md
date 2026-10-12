<!-- source=app-review-overview clause=unclear-data-access-requests url=https://developer.apple.com/distribute/app-review/ fetched=2026-10-12T15:33:26+00:00 -->

### Unclear data access requests

When requesting permission to access user or usage data, you should clearly and completely describe how your app will use the data. Including an example can help users understand why your app is requesting access to their personal information.

If your app’s code references one or more APIs that access sensitive user data, the app’s Info.plist file should contain a `$!{infoPlistKey}` key with a user-facing purpose string explaining clearly and completely why your app needs the data. All apps submitted to App Store Connect that access user data are required to include a purpose string.

To learn more, visit [5.1.1(ii) - Write clear purpose strings](/help/app-review/guideline-reference/5-1-1-purpose-strings) on App Review Help and [view guideline 5.1.](/app-store/review/guidelines/#5.1)
