<!-- source=expo-submit-android clause=use-other-ci-cd-services url=https://docs.expo.dev/submit/android/ fetched=2026-10-26T13:10:26+00:00 -->

## Use other CI/CD services

You can run `eas submit` from any CI/CD service, such as GitHub Actions, GitLab CI, and others:

Terminal

`-` `eas submit --platform android --profile production`

This requires a [personal access token](/accounts/programmatic-access/#personal-access-tokens) to authenticate with your Expo account. Set the `EXPO_TOKEN` environment variable in your CI service so `eas submit` can run non-interactively.

With `--non-interactive`, `eas submit` and `eas build --auto-submit` cannot prompt you for a Google Service Account key. Unless your submission profile sets [`serviceAccountKeyPath`](/eas/json/#serviceaccountkeypath), they use the key that is assigned to your app. If no key is assigned, they fail with the following error:

```
Google Service Account Keys cannot be set up in --non-interactive mode.
```

To fix this, assign a key to your app as described in [Prerequisites](/submit/android/#prerequisites). You can also set `serviceAccountKeyPath` to the path of a key file on the CI machine.
