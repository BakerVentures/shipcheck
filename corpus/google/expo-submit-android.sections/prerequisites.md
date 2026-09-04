<!-- source=expo-submit-android clause=prerequisites url=https://docs.expo.dev/submit/android/ fetched=2026-09-04T07:14:19+00:00 -->

## Prerequisites

Prerequisites

5 requirements

1.

Sign up for a Google Play Developer account

A Google Play Developer account is required to submit your app to the Google Play Store. Sign up on the [Google Play Console sign-up page](https://play.google.com/apps/publish/signup/).

2.

Create an app on Google Play Console

Create an app by clicking Create app in the [Google Play Console](https://play.google.com/apps/publish/).

3.

Create a Google Service Account key and upload it to EAS

EAS requires a Google Service Account key to submit on your behalf. Follow the [Creating a Google Service Account key](https://expo.fyi/creating-google-service-account) guide to create one. Then, upload the key to your project's credentials with the EAS dashboard or EAS CLI:

- Go to your project's EAS dashboard, click Credentials, and under Android, click your app's Application identifier.
- Under Service Credentials, click Add a Google Service Account Key.
- Ensure Upload new key is selected and upload the downloaded JSON key.

- Run `eas credentials --platform android`
- When prompted Which build profile do you want to configure?, select production
- When prompted What do you want to do?, select Google Service Account > Upload a Google Service Account Key
- Enter the path to the JSON key file

4.

Include a package name in app config

Include your app's package name in app.json:

app.json

```
{ "android": { "package": "com.yourcompany.yourapp" } }
```

5.

Install EAS CLI and authenticate with your Expo account

Install EAS CLI and log in with your Expo account:

Terminal

`-` `npm install --global eas-cli && eas login`

`-` `yarn global add eas-cli && eas login`

`-` `pnpm add --global eas-cli && eas login`

`-` `bun add --global eas-cli && eas login`
