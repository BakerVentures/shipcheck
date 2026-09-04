<!-- source=expo-submit-android clause=use-other-ci-cd-services url=https://docs.expo.dev/submit/android/ fetched=2026-09-04T07:14:19+00:00 -->

## Use other CI/CD services

You can run `eas submit` from any CI/CD service, such as GitHub Actions, GitLab CI, and others:

Terminal

`-` `eas submit --platform android --profile production`

This requires a [personal access token](/accounts/programmatic-access#personal-access-tokens) to authenticate with your Expo account. Set the `EXPO_TOKEN` environment variable in your CI service so `eas submit` can run non-interactively.
