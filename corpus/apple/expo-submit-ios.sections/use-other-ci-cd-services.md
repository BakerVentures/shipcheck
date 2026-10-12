<!-- source=expo-submit-ios clause=use-other-ci-cd-services url=https://docs.expo.dev/submit/ios/ fetched=2026-10-12T15:33:41+00:00 -->

## Use other CI/CD services

You can run `eas submit` from any CI/CD service, such as GitHub Actions, GitLab CI, and others:

Terminal

`-` `eas submit --platform ios --profile production`

This requires a [personal access token](/accounts/programmatic-access/#personal-access-tokens) to authenticate with your Expo account. Set the `EXPO_TOKEN` environment variable in your CI service so `eas submit` can run non-interactively.

With `--non-interactive`, `eas submit` and `eas build --auto-submit` cannot prompt you for an App Store Connect API Key. Unless you bring your own credentials, they use the key assigned to your app. If your app has no key, they fail with the following error:

```
App Store Connect API Keys cannot be set up in --non-interactive mode.
```

To fix this, assign a key to your app or bring your own credentials, as described in [Automate with EAS Workflows](/submit/ios/#automate-with-eas-workflows). In non-interactive mode, your submission profile also needs [`ascAppId`](/submit/ios/#configure-a-submission-profile).
