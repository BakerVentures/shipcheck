<!-- source=expo-submit-ios clause=configure-a-submission-profile url=https://docs.expo.dev/submit/ios/ fetched=2026-09-05T02:02:34+00:00 -->

### Configure a submission profile

Add a submission profile in eas.json with your App Store Connect app ID:

eas.json

```
{ "submit": { "production": { "ios": { "ascAppId": "your-app-store-connect-app-id" } } } }
```

How to find `ascAppId`

1. Sign in to [App Store Connect](https://appstoreconnect.apple.com/) and select your team.
2. Navigate to [Apps](https://appstoreconnect.apple.com/apps).
3. Click your app.
4. Ensure the App Store tab is active.
5. On the left pane, under General, select App Information.
6. Your `ascAppId` is listed under General Information as Apple ID.

See the [eas.json reference](/eas/json#ios-specific-options-1) for every available option.
