<!-- source=app-review-overview clause=unclear-data-access-requests url=https://developer.apple.com/distribute/app-review/ fetched=2026-09-04T07:14:02+00:00 -->

### Unclear data access requests

When requesting permission to access user or usage data, you should clearly and completely describe how your app will use the data. Including an example can help users understand why your app is requesting access to their personal information. [View guideline 5.1.](/app-store/review/guidelines/#5.1)

If your app’s code references one or more APIs that access sensitive user data, the app’s Info.plist file should contain a `$!{infoPlistKey}` key with a user-facing purpose string explaining clearly and completely why your app needs the data. All apps submitted to App Store Connect that access user data are required to include a purpose string.

[Learn about requesting permission](/design/human-interface-guidelines/privacy/)

[Watch “Write clear purpose strings”](/videos/play/tech-talks/110152/)
