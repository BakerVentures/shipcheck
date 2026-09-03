<!-- source=data-safety clause=which-developers-need-to-complete-the-data-safety-form-in-pl url=https://support.google.com/googleplay/android-developer/answer/10787469 fetched=2026-09-03T19:55:34+00:00 -->

### Which developers need to complete the Data safety form in Play Console?

All developers that have an app published on Google Play must complete the Data safety form, including apps on closed, open, or production testing tracks. This also applies to pregranted and preloaded apps that update through Google Play.

Apps that are active on [internal testing tracks](https://support.google.com/googleplay/android-developer/answer/9845334#internal_test) are exempt from inclusion in the data safety section. Apps that are exclusively active on this track do not need to complete the Data safety form.

Even developers with apps that do not collect any user data must complete this form and provide a link to their privacy policy. In this case, the completed form and privacy policy can indicate that no user data is collected or shared.

[System services](https://support.google.com/googleplay/android-developer/answer/12085265) and [private](https://support.google.com/a/answer/2494992) apps do not need to complete the Data safety form.

While a global form is required for each app defined at the app package level, developers may exclude old artifacts from their form. This is applicable for artifacts with effective target SdkVersion below 21 where the majority of the app’s active user install base (90%+) is on artifacts with effective [target SdkVersion](https://developer.android.com/guide/topics/manifest/uses-sdk-element#target) 21 or higher.
