<!-- source=expo-submit-ios clause=use-other-ci-cd-services url=https://docs.expo.dev/submit/ios/ fetched=2026-09-04T07:14:08+00:00 -->

## Use other CI/CD services

You can run `eas submit` from any CI/CD service, such as GitHub Actions, GitLab CI, and others:

Terminal

`-` `eas submit --platform ios --profile production`

This requires a [personal access token](/accounts/programmatic-access#personal-access-tokens) to authenticate with your Expo account. Set the `EXPO_TOKEN` environment variable in your CI service so `eas submit` can run non-interactively.
