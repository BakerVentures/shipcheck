<!-- source=expo-submit-ios clause=automate-with-eas-workflows url=https://docs.expo.dev/submit/ios/ fetched=2026-09-04T16:10:04+00:00 -->

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
