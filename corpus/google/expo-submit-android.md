---
shipcheck_source_id: expo-submit-android
title: "Expo: Submit to Google Play"
url: https://docs.expo.dev/submit/android/
final_url: https://docs.expo.dev/submit/android/
fetched_at: 2026-09-05T02:02:46+00:00
sha256: 57a8113bd50136a7ce85336009b84634b4dbd72c7d9c4c0d3fac4cdac4d902d4
vendor: google
---

# Submit to the Google Play Store with EAS Submit

[Edit page](https://github.com/expo/expo/edit/main/docs/pages/submit/android.mdx)

Learn how to submit your Android app to the Google Play Store with EAS Submit.

[Edit page](https://github.com/expo/expo/edit/main/docs/pages/submit/android.mdx)

---

[EAS Submit](/deploy/submit-to-app-stores) is the recommended way to upload your Android app to the Google Play Store. The `eas submit` command works the same way on your machine and inside CI/CD. [EAS Workflows](/eas/workflows/introduction) is the simplest way to run it automatically after a build.

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

## Build a production app

You need a production .aab (Android App Bundle) to submit. Google Play requires new apps to be published as app bundles instead of .apk files, and generates optimized APKs for each device from the bundle. Create one with [EAS Build](/build/introduction):

Terminal

`-` `eas build --platform android --profile production`

Alternatively, build on your own computer with `eas build --platform android --profile production --local` or with Android Studio.

The default `production` profile produces a .aab. A build profile only produces a .apk when it sets [`android.buildType`](/eas/json#buildtype) to `apk`, which is useful for [installing on an emulator or device](/build-reference/apk) but cannot be submitted to the Google Play Store.

## First-time submission

If this is your app's first submission, the default `eas submit` command works out of the box and creates your app's first release on the [internal testing track](/eas/json#track). Before running it, complete the [prerequisites](/submit/android#prerequisites) so that your app exists on Google Play Console and EAS has a [Google Service Account key](https://expo.fyi/creating-google-service-account) to submit on your behalf. The app stays in draft status in Play Console until you complete the store listing and setup tasks, which are required before a release can be promoted to production.

- Prefer doing the first upload yourself? Follow the [manual submission guide](/submit/android-manual) to create the first release in Play Console.
- Want to upload without rolling out? Set [`releaseStatus`](/eas/json#releasestatus) to `draft` in the submission profile in eas.json, and complete the release in Play Console.

## Submit with `eas submit`

Once the build is ready, submit it to the Google Play Store:

Terminal

`-` `eas submit --platform android`

The command will walk you through selecting a build and uploading it. Configure the submission process by adding a submission profile in eas.json. See the [eas.json reference](/eas/json#android-specific-options-1) for every available option.

### Build and submit in one step

Pass `--auto-submit` to `eas build` to hand the finished build off to EAS Submit automatically:

Terminal

`-` `eas build --platform android --auto-submit`

See [Automate submissions](/build/automate-submissions) for details.

## Automate with EAS Workflows

[EAS Workflows](/eas/workflows/introduction) runs the same `eas submit` command on EAS infrastructure, triggered by a git push or run manually from CLI. Workflows authenticate with Google Play using the Google Service Account key you uploaded in the [prerequisites](/submit/android#prerequisites).

Create a workflow file named .eas/workflows/submit-android.yml with the following contents:

.eas/workflows/submit-android.yml

```
name: Submit Android

on: push: branches: ['main'] jobs: build_android: name: Build Android app
type: build
params: platform: android
profile: production

submit_android: name: Submit to Google Play Store
needs: [build_android] type: submit
params: profile: production
build_id: ${{ needs.build_android.outputs.build_id }}
```

This builds an Android app on every push to `main` and submits it to Google Play. Trigger it manually with:

Terminal

`-` `eas workflow:run submit-android.yml`

See the [workflow examples guide](/eas/workflows/examples/introduction) for more patterns.

## Use other CI/CD services

You can run `eas submit` from any CI/CD service, such as GitHub Actions, GitLab CI, and others:

Terminal

`-` `eas submit --platform android --profile production`

This requires a [personal access token](/accounts/programmatic-access#personal-access-tokens) to authenticate with your Expo account. Set the `EXPO_TOKEN` environment variable in your CI service so `eas submit` can run non-interactively.
