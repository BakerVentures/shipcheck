<!-- source=expo-submit-android clause=automate-with-eas-workflows url=https://docs.expo.dev/submit/android/ fetched=2026-09-05T02:02:46+00:00 -->

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
