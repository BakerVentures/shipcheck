<!-- source=expo-submit-ios clause=prerequisites url=https://docs.expo.dev/submit/ios/ fetched=2026-09-04T07:14:08+00:00 -->

## Prerequisites

Prerequisites

3 requirements

1.

Sign up for an Apple Developer account

A paid Apple Developer account is required to submit apps to the Apple App Store. Sign up on the [Apple Developer Portal](https://developer.apple.com/account/).

2.

Include a bundle identifier in app config

Include your app's bundle identifier in app.json:

app.json

```
{ "ios": { "bundleIdentifier": "com.yourcompany.yourapp" } }
```

3.

Install EAS CLI and authenticate with your Expo account

Install EAS CLI and log in with your Expo account:

Terminal

`-` `npm install --global eas-cli && eas login`

`-` `yarn global add eas-cli && eas login`

`-` `pnpm add --global eas-cli && eas login`

`-` `bun add --global eas-cli && eas login`
