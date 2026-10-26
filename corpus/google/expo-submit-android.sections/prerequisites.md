<!-- source=expo-submit-android clause=prerequisites url=https://docs.expo.dev/submit/android/ fetched=2026-10-26T13:10:26+00:00 -->

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

EAS requires a Google Service Account key to submit on your behalf. Follow the [Creating a Google Service Account key](https://expo.fyi/creating-google-service-account) guide to create one. Then, upload the key and assign it to your app with the EAS dashboard or EAS CLI:

- Go to your project's EAS dashboard, click Credentials, and under Android, click your app's Application identifier.
- Under Service credentials, in Google service account key for EAS Submit, click Add a Google service account key.
- Ensure Upload new key is selected, upload the downloaded JSON key, and click Save.

- Run `eas credentials --platform android`
- When prompted Which build profile do you want to configure?, select production
- When prompted What do you want to do?, select Google Service Account > Manage your Google Service Account Key for Play Store Submissions > Set up a Google Service Account Key for Play Store Submissions
- Enter the path to the JSON key file, or choose a key that you already uploaded

EAS stores the key on your Expo account. You assign a key to each Android application identifier. To use the same key for another app in your account, select Choose saved key in the EAS dashboard. In EAS CLI, select Select an existing Google Service Account Key for Play Store Submissions.

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
