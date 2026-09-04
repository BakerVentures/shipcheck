---
shipcheck_source_id: expo-submit-ios
title: "Expo: Submit to the App Store"
url: https://docs.expo.dev/submit/ios/
final_url: https://docs.expo.dev/submit/ios/
fetched_at: 2026-09-04T15:48:30+00:00
sha256: 348d91ea3264018b38f78b093f9c4f3aa5b84f2745157c7f5e391b18eaf05a4e
vendor: apple
---

# Submit to the Apple App Store with EAS Submit

[Edit page](https://github.com/expo/expo/edit/main/docs/pages/submit/ios.mdx)

Learn how to submit your iOS app to the Apple App Store with EAS Submit.

[Edit page](https://github.com/expo/expo/edit/main/docs/pages/submit/ios.mdx)

---

[EAS Submit](/deploy/submit-to-app-stores) is the recommended way to upload your iOS app to the Apple App Store. The `eas submit` command works the same way on your machine and inside CI/CD. [EAS Workflows](/eas/workflows/introduction) is the simplest way to run it automatically after a build. EAS Submit works on macOS, Linux, and Windows, so you don't need a Mac to ship iOS builds.

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

## Build a production app

You need a production .ipa to submit. Create one with [EAS Build](/build/introduction):

Terminal

`-` `eas build --platform ios --profile production`

Alternatively, build on your own computer with `eas build --platform ios --profile production --local` or with Xcode.

## Submit with `eas submit`

Once the build is ready, submit it to the Apple App Store:

Terminal

`-` `eas submit --platform ios`

The command will walk you through selecting a build, prompt for your Apple ID on first run, and upload the binary to App Store Connect. The build appears in [TestFlight](/submit/testflight) after processing (usually 10-15 minutes). To release to production, log in to [App Store Connect](https://appstoreconnect.apple.com/) and submit the build for App Review.

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

### Build and submit in one step

Pass `--auto-submit` to `eas build` to hand the finished build off to EAS Submit automatically:

Terminal

`-` `eas build --platform ios --auto-submit`

See [Automate submissions](/build/automate-submissions) for details.

## Automate with EAS Workflows

[EAS Workflows](/eas/workflows/introduction) runs the same submit step on EAS infrastructure, triggered by a git push or run manually from the CLI. First, configure an App Store Connect API Key so workflows can authenticate with Apple non-interactively:

Terminal

`-` `eas credentials --platform ios`

1. Select the `production` build profile.
2. Log in with your Apple Developer account and follow the prompts.
3. Select App Store Connect: Manage your API Key.
4. Select Set up your project to use an API Key for EAS Submit.

Prefer to bring your own credentials?

App Store Connect API Key: Create your own [API Key](https://expo.fyi/creating-asc-api-key) and set it with the `ascApiKeyPath`, `ascApiKeyIssuerId`, and `ascApiKeyId` fields in eas.json.

App-specific password: Provide your [app-specific password](https://expo.fyi/apple-app-specific-password) via the `EXPO_APPLE_APP_SPECIFIC_PASSWORD` environment variable and set your Apple ID with the `appleId` field in eas.json.

Create a workflow file named .eas/workflows/submit-ios.yml with the following contents:

.eas/workflows/submit-ios.yml

```
name: Submit iOS

on: push: branches: ['main'] jobs: build_ios: name: Build iOS app
type: build
params: platform: ios
profile: production

submit_ios: name: Submit to TestFlight
needs: [build_ios] type: testflight
params: build_id: ${{ needs.build_ios.outputs.build_id }}
```

This builds an iOS app on every push to `main` and submits it to TestFlight. The [pre-packaged `testflight` job](/eas/workflows/pre-packaged-jobs#testflight) can also share the build with internal and external testing groups. Trigger the workflow manually with:

Terminal

`-` `eas workflow:run submit-ios.yml`

See the [workflow examples guide](/eas/workflows/examples/introduction) for more patterns.

## Use other CI/CD services

You can run `eas submit` from any CI/CD service, such as GitHub Actions, GitLab CI, and others:

Terminal

`-` `eas submit --platform ios --profile production`

This requires a [personal access token](/accounts/programmatic-access#personal-access-tokens) to authenticate with your Expo account. Set the `EXPO_TOKEN` environment variable in your CI service so `eas submit` can run non-interactively.

## Manual fallback

If EAS Submit is temporarily unavailable, you can upload to the Apple App Store manually from a Mac with Xcode.

[Manually submit an iOS app with XcodeArchive and upload an iOS app to App Store Connect using Xcode on macOS.](/submit/ios-manual)
