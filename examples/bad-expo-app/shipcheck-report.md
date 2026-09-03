# ShipCheck report

**Bad App** · v1.0.0 · generated 2026-09-03 14:32

## Rejection risk: 100 / 100

**Very likely to be rejected**

`[████████████████████]` 16 critical · 12 high · 6 medium · 2 low

**6 block the upload** — App Store Connect will not accept a build until these are fixed · **14 are metadata only** and need no new build — you can fix those in App Store Connect right now.

> Checked against policy text fetched 2026-09-03 from 37 official Apple and Google sources. Run `/shipcheck:refresh` to re-fetch and see what changed.

---

## Findings

### 1. 🔴 CRITICAL App icon contains an alpha channel

**Guideline ASC:screenshot-specifications** · confidence: high · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:**Images can’t include alpha channels or transparencies.
> 
> ## iPhone
> 
> 6.9" Display
> 
> iPhone Air
> 
> iPhone 17 Pro Max
> 
> iPhone 16 Pro Max
> 
> iPhone 16 Plus
> 
> iPhone 15 Pro Max
> 
> iPhone 15 Plus
> 
> iPhone 14 Pro Max
> 
> **Screenshot size**
> 
> 1260 x 2736 pixels
> 
> (portrait)
> 
> 2736 x 1260 pixels
> 
> (landscape)
> 
> 1290 x 2796 pixels
> 
> (portrait)
> 
> 2796 x 1290 pixels
> 
> (landscape)
> 
> 1320 x 2868 pixels
> 
> (portrait)
> 
> 2868 x 1320 pixels
> 
> (landscape)
> 
> 6.5" Display
> 
> iPhone 14 Plus
> 
> iPhone 13 Pro Max
> 
> iPhone 12 Pro Max
> 
> iPhone 11 Pro Max
> 
> iPhone 11
> 
> iPhone XS Max
> 
> iPhone XR
> 
> **Screenshot size**
> 
> 1284 x 2778 pixels
> 
> (portrait)
> 
> 2778 x 1284 pixels
> 
> (landscape)
> 
> 1242 x 2688 pixels
> 
> (portrait)
> 
> 2688 x 1242 pixels
> 
> (landscape)
> 
> **Requirement**
> 
> Required if app runs on iPhone and […]
> 
> — [ASC:screenshot-specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)

**What ShipCheck found**

assets/icon.png has color type 6

**Fix**

Flatten the icon onto an opaque background and re-export without transparency (color type 2, no tRNS). App Store Connect rejects icons with alpha at upload time.


### 2. 🔴 CRITICAL eas.json production profile sets developmentClient: true

**Guideline 2.2** · confidence: high · iOS · blocks review · deterministic

> 2.2 Beta Testing
> 
> Demos, betas, and trial versions of your app don’t belong on the App Store – use TestFlight instead. Any app submitted for beta distribution via TestFlight should be intended for public distribution and should comply with the App Review Guidelines. Note, however, that apps using TestFlight cannot be distributed to testers in exchange for compensation of any kind, including as a reward for crowd-sourced funding. Significant updates to your beta build should be submitted to TestFlight App Review before being distributed to your testers. To learn more, visit the [TestFlight Beta Testing](/testflight/) page.
> 
> — [2.2](https://developer.apple.com/app-store/review/guidelines/#beta-testing)

**What ShipCheck found**

build.production.developmentClient = true

**Fix**

Remove `developmentClient` from the production profile. A dev-client build shows the Expo dev menu and will be rejected as a beta/incomplete app.


### 3. 🔴 CRITICAL Paywall discloses no subscription terms before purchase

**Guideline 3.1.2c** · confidence: high · iOS · blocks review · judgment

> 3.1.2(c) Subscription Information:
> 
> Before asking a customer to subscribe, you should clearly describe what the user will get for the price. How many issues per month? How much cloud storage? What kind of access to your service? Ensure you clearly communicate the requirements described in
> 
> Schedule 2 of the Apple Developer Program License Agreement
> 
> .
> 
> — [3.1.2c](https://developer.apple.com/app-store/review/guidelines/#3.1.2c)

**What ShipCheck found**

Paywall is described in full as: "A screen with a Go Pro button." Subscriptions field says "yes — Pro Monthly $4.99" with no terms text. react-native-purchases is in dependencies, so this is a real auto-renewing subscription.

**What the reviewer will likely say**

> Your app's binary does not include the required subscription information. Before asking a customer to subscribe you must display the title, length, and price of the subscription, and what the user receives, along with functional links to your Terms of Use (EULA) and Privacy Policy.

**Fix**

Put this on the paywall itself, visible before the purchase button, not behind a link:

    Pro Monthly — $4.99 per month
    Unlimited workouts and coaching. Renews automatically each month
    until cancelled. Cancel any time in Settings.
    [Terms of Use]  [Privacy Policy]  [Restore Purchases]

RevenueCat's prebuilt paywall templates already satisfy this; a hand-rolled paywall usually does not.


### 4. 🔴 CRITICAL Missing NSCameraUsageDescription

**Guideline 5.1.1** · confidence: high · iOS · blocks review · deterministic

> 5.1.1
> 
> Data Collection and Storage
> 
> - **(i) Privacy Policies:**All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
>   Identify what data, if any, the app/service collects, how it collects that data, and all uses of that data.
>   Confirm that any third party with whom an app shares user data (in compliance with these Guidelines)—such as analytics tools, advertising networks and third-party SDKs, as well as any parent, subsidiary or other related entities that will have access to user data—will provide the same or equal protection of user data as stated in the app’s privacy policy and required by these Guidelines.
>   Explain its data retention/deletion policies and describe how a user can revoke consent and/or request deletion of the user’s data.
> - […]
> 
> — [5.1.1](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)

**What ShipCheck found**

app/index.tsx calls this API (expo-camera, expo-image-picker) and NSCameraUsageDescription is not set in app.json

**Fix**

Add to app.json under expo.ios.infoPlist:
  "NSCameraUsageDescription": "<specific reason this app needs it>"
Without the key iOS terminates the app the moment the permission is requested, which reviewers hit immediately and reject under 2.1.


### 5. 🔴 CRITICAL Missing NSUserTrackingUsageDescription

**Guideline 5.1.1** · confidence: high · iOS · blocks review · deterministic

> 5.1.1
> 
> Data Collection and Storage
> 
> - **(i) Privacy Policies:**All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
>   Identify what data, if any, the app/service collects, how it collects that data, and all uses of that data.
>   Confirm that any third party with whom an app shares user data (in compliance with these Guidelines)—such as analytics tools, advertising networks and third-party SDKs, as well as any parent, subsidiary or other related entities that will have access to user data—will provide the same or equal protection of user data as stated in the app’s privacy policy and required by these Guidelines.
>   Explain its data retention/deletion policies and describe how a user can revoke consent and/or request deletion of the user’s data.
> - […]
> 
> — [5.1.1](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)

**What ShipCheck found**

app/index.tsx calls this API (react-native-fbsdk-next) and NSUserTrackingUsageDescription is not set in app.json

**Fix**

Add to app.json under expo.ios.infoPlist:
  "NSUserTrackingUsageDescription": "<specific reason this app needs it>"
Without the key iOS terminates the app the moment the permission is requested, which reviewers hit immediately and reject under 2.1.


### 6. 🔴 CRITICAL Third-party login present with no Sign in with Apple

**Guideline 4.8** · confidence: high · iOS · blocks review · deterministic

> 4.8
> 
> Login Services
> 
> Apps that use a third-party or social login service (such as Facebook Login, Google Sign-In, Log in with X, Sign In with LinkedIn, Login with Amazon, or WeChat Login) to set up or authenticate the user’s primary account with the app must also offer as an equivalent option another login service with the following features:
> 
> - the login service limits data collection to the user’s name and email address;
> - the login service allows users to keep their email address private as part of setting up their account; and
> - the login service does not collect interactions with your app for advertising purposes without consent.
> 
> A user’s primary account is the account they establish with your app for the purposes of identifying themselves, signing in, and accessing your features and associated services.
> 
> Another login service is not required if:
> Your app exclusively uses your […]
> 
> — [4.8](https://developer.apple.com/app-store/review/guidelines/#login-services)

**What ShipCheck found**

Third-party login from: @react-native-google-signin/google-signin, @supabase/supabase-js, react-native-fbsdk-next. No expo-apple-authentication or @invertase/react-native-apple-authentication in dependencies.

**Fix**

Add `expo-apple-authentication`, render an `AppleAuthenticationButton` alongside your other login buttons, and enable the Sign In with Apple capability (`expo.ios.usesAppleSignIn: true`). Guideline 4.8 requires an equivalent privacy-preserving login option whenever a third-party service sets up the primary account.


### 7. 🔴 CRITICAL App has accounts but no demo account for review

**Guideline 2.1** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.1 App Completeness
> 
> - **(a)**![ASR & NR] Submissions to App Review, including apps you make available for pre-order, should be final versions with all necessary metadata and fully functional URLs included; placeholder text, empty websites, and other temporary content should be scrubbed before submission. Make sure your app has been tested on-device for bugs and stability before you submit it, and include demo account info (and turn on your back-end service!) if your app includes a login. If you are unable to provide a demo account due to legal or security obligations, you may include a built-in demo mode in lieu of a demo account with prior approval by Apple. Ensure the demo mode exhibits your app’s full features and functionality. We will reject incomplete app bundles and binaries that crash or exhibit obvious technical problems.
> - **(b)** If you offer in-app purchases in your app, […]
> 
> — [2.1](https://developer.apple.com/app-store/review/guidelines/#app-completeness)

**What ShipCheck found**

Accounts = yes, Demo account = (blank)

**Fix**

Put working credentials in App Review notes. A reviewer who hits a login wall with no credentials rejects under 2.1 App Completeness, and it costs you a full review cycle.


### 8. 🔴 CRITICAL Description and a screenshot advertise Android

**Guideline 2.3.10** · confidence: high · iOS · metadata only — no new build · judgment

> 2.3.10
> 
> Make sure your app is focused on the experience of the Apple platforms it supports, and don’t include names, icons, or imagery of other mobile platforms or alternative app marketplaces in your app or metadata, unless there is specific, approved interactive functionality. Make sure your app metadata is focused on the app itself and its experience. Don’t include irrelevant information.
> 
> — [2.3.10](https://developer.apple.com/app-store/review/guidelines/#2.3.10)

**What ShipCheck found**

Description: "Also available on Android and on our website." Screenshot 2 is described as: text overlay "Now on Android too!"

**What the reviewer will likely say**

> We noticed your app or its metadata includes references to other mobile platforms. Please remove these references from your app description and screenshots.

**Fix**

Delete the sentence "Also available on Android and on our website." and re-export screenshot 2 without the Android overlay. This is one of the fastest rejections to earn and one of the cheapest to avoid — it needs no new build, only a metadata edit.


### 9. 🔴 CRITICAL Placeholder text in Description

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3.1
> 
> - **(a)**![ASR & NR] Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Description contains "Lorem ipsum"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 10. 🔴 CRITICAL Placeholder text in Privacy Policy Url

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3.1
> 
> - **(a)**![ASR & NR] Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Privacy Policy Url contains "example.com"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 11. 🔴 CRITICAL Placeholder text in Support Url

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3.1
> 
> - **(a)**![ASR & NR] Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Support Url contains "example.com"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 12. 🔴 CRITICAL Placeholder text in What'S New

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3.1
> 
> - **(a)**![ASR & NR] Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

What'S New contains "TODO"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 13. 🔴 CRITICAL Privacy Policy Url is not reachable

**Guideline 5.1.1** · confidence: high · iOS · metadata only — no new build · deterministic

> 5.1.1
> 
> Data Collection and Storage
> 
> - **(i) Privacy Policies:**All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
>   Identify what data, if any, the app/service collects, how it collects that data, and all uses of that data.
>   Confirm that any third party with whom an app shares user data (in compliance with these Guidelines)—such as analytics tools, advertising networks and third-party SDKs, as well as any parent, subsidiary or other related entities that will have access to user data—will provide the same or equal protection of user data as stated in the app’s privacy policy and required by these Guidelines.
>   Explain its data retention/deletion policies and describe how a user can revoke consent and/or request deletion of the user’s data.
> - […]
> 
> — [5.1.1](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)

**What ShipCheck found**

https://example.com/privacy -> HTTP 404

**Fix**

Fix or replace the URL. Reviewers open every link in the listing; a dead privacy policy URL is an automatic rejection.


### 14. 🔴 CRITICAL Support Url is not reachable

**Guideline 2.3.8** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3.8
> 
> Metadata should be appropriate for all audiences, so make sure your app and in-app purchase icons, screenshots, and previews adhere to a 4+ age rating even if your app is rated higher. For example, if your app is a game that includes violence, select images that don’t depict a gruesome death or a gun pointed at a specific character. Use of terms like “For Kids” and “For Children” in app metadata is reserved in the App Store for the Kids Category. Remember to ensure your metadata, including app name and icons (small, large, Apple Watch app, alternate icons, etc.), are similar to avoid creating confusion.
> 
> — [2.3.8](https://developer.apple.com/app-store/review/guidelines/#2.3.8)

**What ShipCheck found**

https://example.com/support -> HTTP 404

**Fix**

Fix or replace the URL. Reviewers open every link in the listing; a dead privacy policy URL is an automatic rejection.


### 15. 🔴 CRITICAL App creates accounts but no in-app account deletion found

**Guideline 5.1.1v** · confidence: medium · iOS · blocks review · deterministic

> (v) Account Sign-In:
> 
> If your app doesn’t include significant account-based features, let people use it without a login. If your app supports account creation, you must also
> 
> offer account deletion within the app
> 
> . Apps may not require users to enter personal information to function, except when directly relevant to the core functionality of the app or required by law. If your core app functionality is not related to a specific social network (e.g. Facebook, WeChat, Weibo, X, etc.), you must provide access without a login or via another mechanism. Pulling basic profile information, sharing to the social network, or inviting friends to use the app are not considered core app functionality. The app must also include a mechanism to revoke social network credentials and disable data access between the app and social network from within the app. An app may not store credentials or tokens to […]
> 
> — [5.1.1v](https://developer.apple.com/app-store/review/guidelines/#5.1.1v)

**What ShipCheck found**

Auth via @supabase/supabase-js; no delete-account code path found in source.

**Fix**

Add an in-app control that permanently deletes the account (not just a link to support, and not sign-out). Apple has required this since 30 June 2022 for any app that supports account creation.


### 16. 🔴 CRITICAL Screenshot 1 advertises an "AI coach" the build does not contain

**Guideline 2.3.3** · confidence: medium · iOS · metadata only — no new build · judgment

> 2.3.3
> 
> Screenshots should show the app in use, and not merely the title art, login page, or splash screen. They may also include text and image overlays (e.g. to demonstrate input mechanisms, such as an animated touch point or Apple Pencil) and show extended functionality on device, such as Touch Bar.
> 
> — [2.3.3](https://developer.apple.com/app-store/review/guidelines/#2.3.3)

**What ShipCheck found**

Screenshot 1 is described as: Home screen showing the AI coach feature. No AI/LLM dependency appears in package.json (45 deps scanned) and no route or component references a coach.

**What the reviewer will likely say**

> Your screenshots include content that does not reflect the app in use. Please update them to show the app's actual features.

**Fix**

Either remove screenshot 1, or ship the feature. If the AI coach exists but is server-driven and therefore invisible to a dependency scan, say so in the review notes and tell the reviewer how to reach it — that converts this from a rejection into a non-issue.


### 17. 🟠 HIGH App icon is 512x512, not 1024x1024

**Guideline ASC:screenshot-specifications** · confidence: high · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:**Images can’t include alpha channels or transparencies.
> 
> ## iPhone
> 
> 6.9" Display
> 
> iPhone Air
> 
> iPhone 17 Pro Max
> 
> iPhone 16 Pro Max
> 
> iPhone 16 Plus
> 
> iPhone 15 Pro Max
> 
> iPhone 15 Plus
> 
> iPhone 14 Pro Max
> 
> **Screenshot size**
> 
> 1260 x 2736 pixels
> 
> (portrait)
> 
> 2736 x 1260 pixels
> 
> (landscape)
> 
> 1290 x 2796 pixels
> 
> (portrait)
> 
> 2796 x 1290 pixels
> 
> (landscape)
> 
> 1320 x 2868 pixels
> 
> (portrait)
> 
> 2868 x 1320 pixels
> 
> (landscape)
> 
> 6.5" Display
> 
> iPhone 14 Plus
> 
> iPhone 13 Pro Max
> 
> iPhone 12 Pro Max
> 
> iPhone 11 Pro Max
> 
> iPhone 11
> 
> iPhone XS Max
> 
> iPhone XR
> 
> **Screenshot size**
> 
> 1284 x 2778 pixels
> 
> (portrait)
> 
> 2778 x 1284 pixels
> 
> (landscape)
> 
> 1242 x 2688 pixels
> 
> (portrait)
> 
> 2688 x 1242 pixels
> 
> (landscape)
> 
> **Requirement**
> 
> Required if app runs on iPhone and […]
> 
> — [ASC:screenshot-specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications)

**What ShipCheck found**

assets/icon.png is 512x512

**Fix**

Export a 1024x1024 PNG. App Store Connect rejects the upload outright at any other size.


### 18. 🟠 HIGH Foreground service type 'location' without FOREGROUND_SERVICE_LOCATION

**Guideline play:permissions-policy** · confidence: high · Android · blocks review · deterministic

> # Permissions and APIs that Access Sensitive Information
> 
> ***Disclaimer:** Policy summaries and Key Considerations are overviews only; always refer to the full policy for compliance. The full policy takes precedence in case of conflict.*
> 
> **Changes are coming to this article**
> 
> This article will be updated with recently [announced](https://support.google.com/googleplay/android-developer/announcements/13412212) changes.
> 
> - To better protect user privacy, we're updating our [Location Permissions](https://support.google.com/googleplay/android-developer/answer/16909972#location-permissions) policy. We're introducing the [location button](https://developer.android.com/guide/topics/permissions/private-alternatives/location-button) as the recommended minimum scope for precise location in line with our user data and sensitive permissions requirements.
> 
> - We're introducing the[Contacts […]
> 
> — [play:permissions-policy](https://support.google.com/googleplay/android-developer/answer/16558241)

**What ShipCheck found**

android/app/src/main/AndroidManifest.xml declares foregroundServiceType=location

**Fix**

Add <uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" /> to AndroidManifest.xml. Android 14+ crashes the service without it and Play blocks the release.


### 19. 🟠 HIGH 2 sensitive permission(s) require a Play Console declaration

**Guideline play:permissions-policy** · confidence: high · Android · blocks review · deterministic

> # Permissions and APIs that Access Sensitive Information
> 
> ***Disclaimer:** Policy summaries and Key Considerations are overviews only; always refer to the full policy for compliance. The full policy takes precedence in case of conflict.*
> 
> **Changes are coming to this article**
> 
> This article will be updated with recently [announced](https://support.google.com/googleplay/android-developer/announcements/13412212) changes.
> 
> - To better protect user privacy, we're updating our [Location Permissions](https://support.google.com/googleplay/android-developer/answer/16909972#location-permissions) policy. We're introducing the [location button](https://developer.android.com/guide/topics/permissions/private-alternatives/location-button) as the recommended minimum scope for precise location in line with our user data and sensitive permissions requirements.
> 
> - We're introducing the[Contacts […]
> 
> — [play:permissions-policy](https://support.google.com/googleplay/android-developer/answer/16558241)

**What ShipCheck found**

Requested in android/app/src/main/AndroidManifest.xml: android.permission.ACCESS_BACKGROUND_LOCATION, android.permission.QUERY_ALL_PACKAGES

**Fix**

For each one, either remove the permission or complete the matching declaration form in Play Console > App content. A release with an undeclared sensitive permission is rejected. Most affected here: android.permission.ACCESS_BACKGROUND_LOCATION.


### 20. 🟠 HIGH targetSdkVersion is 33

**Guideline play:target-api-level** · confidence: high · Android · blocks review · deterministic

> # Target API level requirements for Google Play apps
> 
> Starting August 31, 2026:
> 
> - New apps and app updates must target Android 16 (API level 36) or higher to be submitted to Google Play; except for Wear OS, and Android Automotive OS apps, which must target Android 15 (API level 35) or higher, and Android TV and Android XR apps, which must target Android 14 (API level 34) or higher.
> - Existing apps must target Android 15 (API level 35) or higher to remain available to new users on devices running Android OS higher than your app’s target API level. Apps that target Android 14 (API level 34) or lower, including Android 13 (API level 33) or lower for Wear OS and Android TV, and Android XR, and Android 12 (API level 31) or lower for Android Automotive OS will only be available on devices running Android OS that are the same or lower than your apps’ target API level.
> 
> You will be able to […]
> 
> — [play:target-api-level](https://support.google.com/googleplay/android-developer/answer/11926878)

**What ShipCheck found**

android/build.gradle targetSdkVersion = 33

**Fix**

Raise targetSdkVersion. Play blocks new apps and updates below its rolling target-API requirement; check corpus/google/target-api-level.md for the current floor and deadline.


### 21. 🟠 HIGH Price appears in the description and in a screenshot

**Guideline 2.3.7** · confidence: high · iOS · metadata only — no new build · judgment

> 2.3.7
> 
> Choose a unique app name, assign keywords that accurately describe your app, and don’t try to pack any of your metadata with trademarked terms, popular app names, pricing information, or other irrelevant phrases just to game the system. App names must be limited to 30 characters. Metadata such as app names, subtitles, screenshots, and previews should not include prices, terms, or descriptions that are not specific to the metadata type. App subtitles are a great way to provide additional context for your app; they must follow our standard metadata rules and should not include inappropriate content, reference other apps, or make unverifiable product claims. Apple may modify inappropriate keywords at any time or take other appropriate steps to prevent abuse.
> 
> — [2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)

**What ShipCheck found**

Description ends "Download now, only $4.99/month!" and screenshot 3 is described as: Paywall showing "$4.99/mo".

**What the reviewer will likely say**

> Your app's metadata includes pricing information. Price should be communicated through the App Store's own pricing display.

**Fix**

Remove the price from the description. Pricing in a screenshot of your actual paywall UI is normally fine — what is not fine is price text in the description or as an added overlay. If the $4.99 in screenshot 3 is part of the real paywall screen, keep it; if it is an overlay, remove it.


### 22. 🟠 HIGH Review notes say "Nothing special." behind a login wall

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · judgment

> 2.3.1
> 
> - **(a)**![ASR & NR] Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Review notes field reads "Nothing special." The app has accounts (@supabase/supabase-js) and a subscription paywall, neither of which a reviewer can reach without credentials.

**What the reviewer will likely say**

> We were unable to review your app because we could not sign in. Please provide a valid demo account, or a way to demonstrate the app's full functionality.

**Fix**

Replace with: working demo credentials; how to reach the paywall; how to test a purchase in sandbox; and a one-line description of anything server-gated. 2.3.1 requires new features to be described with specificity and states plainly that generic descriptions will be rejected.


### 23. 🟠 HIGH App Name is 51 chars (limit 30)

**Guideline 2.3** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3
> 
> Accurate Metadata
> 
> Customers should know what they’re getting when they download or buy your app, so make sure all your app metadata, including privacy information, your app description, screenshots, and previews accurately reflect the app’s core experience and remember to keep them up-to-date with new versions.
> 
> — [2.3](https://developer.apple.com/app-store/review/guidelines/#accurate-metadata)

**What ShipCheck found**

51 characters

**Fix**

Trim to 30 characters. App Store Connect will not accept the listing otherwise.


### 24. 🟠 HIGH No PrivacyInfo.xcprivacy in the app target

**Guideline apple:required-reason-api** · confidence: medium · iOS · blocks upload · **ITMS-91053** · deterministic

> # Describing use of required reason API
> 
> Ensure your use of covered API is consistent with policy.
> 
> ## Overview
> 
> Some APIs that your app uses to deliver its core functionality — in code you write or included in a third-party SDK — have the potential of being misused to access device signals to try to identify the device or user, also known as fingerprinting. Regardless of whether a user gives your app permission to track, fingerprinting is not allowed. Describe the reasons your app or third-party SDK on iOS, iPadOS, tvOS, visionOS, or watchOS uses these APIs, and check that your app or third-party SDK only uses the APIs for the expected reasons.
> 
> > **Important:** If you upload an app to App Store Connect that uses required reason API without describing the reason in its privacy manifest file, Apple sends you an email reminding you to add the reason to the app’s privacy manifest. […]
> 
> — [apple:required-reason-api](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)

**What ShipCheck found**

1 SDK manifest(s) found under node_modules, but the app target has none. An app manifest is also where NSPrivacyTracking and NSPrivacyCollectedDataTypes live.

**Fix**

Add `expo.ios.privacyManifests` to app.json (Expo SDK 50+) or ios/<App>/PrivacyInfo.xcprivacy, declaring any required-reason API your own native code uses plus your data-collection and tracking posture.


### 25. 🟠 HIGH expo-device uses required-reason API but ships no privacy manifest

**Guideline apple:required-reason-api** · confidence: medium · iOS · blocks upload · **ITMS-91061** · deterministic

> # Describing use of required reason API
> 
> Ensure your use of covered API is consistent with policy.
> 
> ## Overview
> 
> Some APIs that your app uses to deliver its core functionality — in code you write or included in a third-party SDK — have the potential of being misused to access device signals to try to identify the device or user, also known as fingerprinting. Regardless of whether a user gives your app permission to track, fingerprinting is not allowed. Describe the reasons your app or third-party SDK on iOS, iPadOS, tvOS, visionOS, or watchOS uses these APIs, and check that your app or third-party SDK only uses the APIs for the expected reasons.
> 
> > **Important:** If you upload an app to App Store Connect that uses required reason API without describing the reason in its privacy manifest file, Apple sends you an email reminding you to add the reason to the app’s privacy manifest. […]
> 
> — [apple:required-reason-api](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)

**What ShipCheck found**

No PrivacyInfo.xcprivacy found under node_modules/expo-device. Expected it to declare: NSPrivacyAccessedAPICategorySystemBootTime

**Fix**

Upgrade expo-device to a version that ships its own PrivacyInfo.xcprivacy. If no such version exists, declare the categories in your app's manifest as a stopgap and open an issue upstream — Apple emails ITMS-91053/91061 on upload and, since 1 May 2024, blocks the build.


### 26. 🟠 HIGH expo-file-system uses required-reason API but ships no privacy manifest

**Guideline apple:required-reason-api** · confidence: medium · iOS · blocks upload · **ITMS-91061** · deterministic

> # Describing use of required reason API
> 
> Ensure your use of covered API is consistent with policy.
> 
> ## Overview
> 
> Some APIs that your app uses to deliver its core functionality — in code you write or included in a third-party SDK — have the potential of being misused to access device signals to try to identify the device or user, also known as fingerprinting. Regardless of whether a user gives your app permission to track, fingerprinting is not allowed. Describe the reasons your app or third-party SDK on iOS, iPadOS, tvOS, visionOS, or watchOS uses these APIs, and check that your app or third-party SDK only uses the APIs for the expected reasons.
> 
> > **Important:** If you upload an app to App Store Connect that uses required reason API without describing the reason in its privacy manifest file, Apple sends you an email reminding you to add the reason to the app’s privacy manifest. […]
> 
> — [apple:required-reason-api](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api)

**What ShipCheck found**

No PrivacyInfo.xcprivacy found under node_modules/expo-file-system. Expected it to declare: NSPrivacyAccessedAPICategoryDiskSpace, NSPrivacyAccessedAPICategoryFileTimestamp

**Fix**

Upgrade expo-file-system to a version that ships its own PrivacyInfo.xcprivacy. If no such version exists, declare the categories in your app's manifest as a stopgap and open an issue upstream — Apple emails ITMS-91053/91061 on upload and, since 1 May 2024, blocks the build.


### 27. 🟠 HIGH No restore-purchases call found in source

**Guideline 3.1.1** · confidence: medium · iOS · blocks review · deterministic

> 3.1.1 In-App Purchase:
> 
> - If you want to unlock features or functionality within your app, (by way of example: subscriptions, in-game currencies, game levels, access to premium content, or unlocking a full version), you must use in-app purchase. Apps may not use their own mechanisms to unlock content or functionality, such as license keys, augmented reality markers, QR codes, cryptocurrencies and cryptocurrency wallets, etc.
> - Apps may use in-app purchase currencies to enable customers to “tip” the developer or digital content providers in the app.
> - Any credits or in-game currencies purchased via in-app purchase may not expire, and you should make sure you have a restore mechanism for any restorable in-app purchases.
> - Apps may enable gifting of items that are eligible for in-app purchase to others. Such gifts may only be refunded to the original purchaser and may not be exchanged.
> - […]
> 
> — [3.1.1](https://developer.apple.com/app-store/review/guidelines/#in-app-purchase)

**What ShipCheck found**

IAP via react-native-purchases but no restorePurchases/restoreTransactions/syncPurchases call found in app source.

**Fix**

Add a visible "Restore Purchases" control that calls `Purchases.restorePurchases()` (RevenueCat) or the equivalent. Apps selling non-consumables or subscriptions must let a returning user restore entitlements.


### 28. 🟠 HIGH 4+ age rating conflicts with the app's own dating positioning

**Guideline 1.1.4** · confidence: medium · iOS · metadata only — no new build · judgment

> 1.1.4
> 
> Overtly sexual or pornographic material, defined as “explicit descriptions or displays of sexual organs or activities intended to stimulate erotic rather than aesthetic or emotional feelings.” This includes “hookup” apps and other apps that may include pornography or be used to facilitate prostitution, or human trafficking and exploitation.
> 
> — [1.1.4](https://developer.apple.com/app-store/review/guidelines/#1.1.4)

**What ShipCheck found**

App name is "Bad App — The Ultimate Fitness and Dating Companion", keywords include "dating", category is Health & Fitness, and the declared age rating is 4+.

**What the reviewer will likely say**

> The age rating you selected does not reflect your app's content. Apps in the dating category require a higher age rating.

**Fix**

Raise the age rating in the App Store Connect questionnaire, and decide what the app actually is — the name claims fitness and dating, the category says Health & Fitness, and the keywords say both. A reviewer reads that as an app trying to rank in two categories at once, which also invites 2.3.7 and 4.3 scrutiny.


### 29. 🟡 MEDIUM ITSAppUsesNonExemptEncryption is not declared

**Guideline ASC:export-compliance** · confidence: high · iOS · blocks upload · deterministic

> # Overview of export compliance
> 
> If your app uses, accesses, contains, implements, or incorporates encryption, and you intend to upload, test, and distribute it, you need to determine your export compliance requirements in App Store Connect.
> 
> Examples of apps requiring an export compliance determination include, but aren’t limited to, apps that use:
> 
> - Standard encryption algorithms.
> - Crypto functionality within Apple’s operating system.
> - Proprietary or non-standard encryption algorithms. The US Government defines "non-standard cryptography" as any implementation of “cryptography” involving the incorporation or use of proprietary or unpublished cryptographic functionality, including encryption algorithms or protocols that have not been adopted or approved by a duly recognized international standards body (e.g., IEEE, IETF, ISO, ITU, ETSI, 3GPP, TIA, and GSMA) and haven’t otherwise […]
> 
> — [ASC:export-compliance](https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance)

**What ShipCheck found**

Key absent from Info.plist / expo.ios.infoPlist

**Fix**

Add "ITSAppUsesNonExemptEncryption": false to expo.ios.infoPlist if you only use standard HTTPS. Without it every single upload stops and asks you the export compliance question before it can be submitted.


### 30. 🟡 MEDIUM eas.json production profile uses internal distribution

confidence: high · iOS · blocks review · deterministic

**What ShipCheck found**

build.production.distribution = internal

**Fix**

Set `"distribution": "store"` for the profile you submit to the App Store.


### 31. 🟡 MEDIUM 6 runtime permission(s) need prominent in-app disclosure

**Guideline play:user-data-policy** · confidence: medium · Android · blocks review · deterministic

> # User Data
> 
> Help us improve this policy article by taking a**[2-minute survey](https://google.qualtrics.com/jfe/form/SV_9YPSYrwjw03d7cG/?Source=10144311)**.
> 
> ***Disclaimer:** Policy summaries and Key Considerations are overviews only; always refer to the full policy for compliance. The full policy takes precedence in case of conflict.*
> 
> **Policy Summary**
> 
> Google Play prohibits linking persistent device identifiers (such as IMEI, IMSI, or SIM Serial #) to personal and sensitive user data or resettable device identifiers. Other than for limited exceptions related to enterprise device management and telephony, if your app or any SDK integrated into your app performs such linking then you are in violation of the User Data policy. Please review the full policy to ensure compliance.
> 
> **Full Policy**
> 
> You must be transparent in how you handle user data (for example, information collected […]
> 
> — [play:user-data-policy](https://support.google.com/googleplay/android-developer/answer/10144311)

**What ShipCheck found**

Requested via android/app/src/main/AndroidManifest.xml: android.permission.ACCESS_BACKGROUND_LOCATION, android.permission.ACCESS_COARSE_LOCATION, android.permission.ACCESS_FINE_LOCATION, android.permission.CAMERA, android.permission.READ_MEDIA_IMAGES, android.permission.RECORD_AUDIO

**Fix**

Before each runtime permission dialog, show an in-app screen that names the data, says what it is used for, and is not buried in a privacy policy or ToS. Then declare the same data in the Data safety form.


### 32. 🟡 MEDIUM expo-dev-client is a production dependency

**Guideline 2.2** · confidence: medium · iOS · blocks review · deterministic

> 2.2 Beta Testing
> 
> Demos, betas, and trial versions of your app don’t belong on the App Store – use TestFlight instead. Any app submitted for beta distribution via TestFlight should be intended for public distribution and should comply with the App Review Guidelines. Note, however, that apps using TestFlight cannot be distributed to testers in exchange for compensation of any kind, including as a reward for crowd-sourced funding. Significant updates to your beta build should be submitted to TestFlight App Review before being distributed to your testers. To learn more, visit the [TestFlight Beta Testing](/testflight/) page.
> 
> — [2.2](https://developer.apple.com/app-store/review/guidelines/#beta-testing)

**What ShipCheck found**

expo-dev-client present in package.json dependencies

**Fix**

Move it to devDependencies. If it is bundled into the release binary the Expo dev menu can surface in the shipped app, which reads as a beta build to review.


### 33. 🟡 MEDIUM NSLocationWhenInUseUsageDescription uses a generic purpose string

**Guideline 5.1.1** · confidence: medium · iOS · blocks review · deterministic

> 5.1.1
> 
> Data Collection and Storage
> 
> - **(i) Privacy Policies:**All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
>   Identify what data, if any, the app/service collects, how it collects that data, and all uses of that data.
>   Confirm that any third party with whom an app shares user data (in compliance with these Guidelines)—such as analytics tools, advertising networks and third-party SDKs, as well as any parent, subsidiary or other related entities that will have access to user data—will provide the same or equal protection of user data as stated in the app’s privacy policy and required by these Guidelines.
>   Explain its data retention/deletion policies and describe how a user can revoke consent and/or request deletion of the user’s data.
> - […]
> 
> — [5.1.1](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)

**What ShipCheck found**

NSLocationWhenInUseUsageDescription = "We need your location."

**Fix**

Rewrite it to name the specific feature and benefit, e.g. "Used to attach a photo to your progress log." Reviewers reject boilerplate and Expo's plugin default strings.


### 34. 🟡 MEDIUM NSPhotoLibraryUsageDescription uses a generic purpose string

**Guideline 5.1.1** · confidence: medium · iOS · blocks review · deterministic

> 5.1.1
> 
> Data Collection and Storage
> 
> - **(i) Privacy Policies:**All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
>   Identify what data, if any, the app/service collects, how it collects that data, and all uses of that data.
>   Confirm that any third party with whom an app shares user data (in compliance with these Guidelines)—such as analytics tools, advertising networks and third-party SDKs, as well as any parent, subsidiary or other related entities that will have access to user data—will provide the same or equal protection of user data as stated in the app’s privacy policy and required by these Guidelines.
>   Explain its data retention/deletion policies and describe how a user can revoke consent and/or request deletion of the user’s data.
> - […]
> 
> — [5.1.1](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)

**What ShipCheck found**

NSPhotoLibraryUsageDescription = "Allow $(PRODUCT_NAME) to access your photos"

**Fix**

Rewrite it to name the specific feature and benefit, e.g. "Used to attach a photo to your progress log." Reviewers reject boilerplate and Expo's plugin default strings.


### 35. ⚪ LOW Keywords contain spaces after commas

**Guideline 2.3.7** · confidence: high · iOS · metadata only — no new build · deterministic

> 2.3.7
> 
> Choose a unique app name, assign keywords that accurately describe your app, and don’t try to pack any of your metadata with trademarked terms, popular app names, pricing information, or other irrelevant phrases just to game the system. App names must be limited to 30 characters. Metadata such as app names, subtitles, screenshots, and previews should not include prices, terms, or descriptions that are not specific to the metadata type. App subtitles are a great way to provide additional context for your app; they must follow our standard metadata rules and should not include inappropriate content, reference other apps, or make unverifiable product claims. Apple may modify inappropriate keywords at any time or take other appropriate steps to prevent abuse.
> 
> — [2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)

**What ShipCheck found**

keywords = "fitness, dating, workout, gym, health"

**Fix**

Use commas with no spaces — each space costs you a character of the 100-character budget.


### 36. ⚪ LOW expo-camera pulls in NSMicrophone but nothing calls it

**Guideline 5.1.1** · confidence: medium · iOS · blocks review · deterministic

> 5.1.1
> 
> Data Collection and Storage
> 
> - **(i) Privacy Policies:**All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
>   Identify what data, if any, the app/service collects, how it collects that data, and all uses of that data.
>   Confirm that any third party with whom an app shares user data (in compliance with these Guidelines)—such as analytics tools, advertising networks and third-party SDKs, as well as any parent, subsidiary or other related entities that will have access to user data—will provide the same or equal protection of user data as stated in the app’s privacy policy and required by these Guidelines.
>   Explain its data retention/deletion policies and describe how a user can revoke consent and/or request deletion of the user’s data.
> - […]
> 
> — [5.1.1](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage)

**What ShipCheck found**

No call site found for expo-camera, and NSMicrophoneUsageDescription is not set. The dependency looks unused.

**Fix**

Either remove the unused dependency, or add NSMicrophoneUsageDescription before you ship the feature. Do not add the key speculatively — shipping a permission you never use widens your privacy surface and invites questions at review.


---

## Likely to pass

Checked and found clean, so you can trust the list above is the whole problem:

- ✅ **App icon** *(ASC:screenshot-specifications)* — found and readable at assets/icon.png (dimensions and alpha are reported separately as findings)
- ✅ **Bundle identifier set** — com.example.badapp
- ✅ **Android package set** — com.example.badapp
- ✅ **Support and marketing URLs present in metadata** — both are filled in; reachability is reported separately

---

## Not checked

ShipCheck could not verify these. They are not passes:

- ⚠️ **Uninstalled dependencies** — These are in package.json but not under node_modules, so their privacy manifests could not be checked: react-native. Run a full install and re-scan.
- ⚠️ **Pod-delivered privacy manifests** — These packages ship their native SDK through CocoaPods, and ios/Pods is not present, so ShipCheck cannot confirm the pod carries its privacy manifest: react-native-purchases. Run `npx expo prebuild` (or `pod install`) and re-scan.
- ⚠️ **Apple-listed SDK manifests** — @react-native-google-signin/google-signin, react-native-fbsdk-next deliver their SDK through CocoaPods and ios/Pods is absent, so ShipCheck cannot confirm the pod ships a manifest and signature. Run `npx expo prebuild` and re-scan.
- ⚠️ **Paywall UI** — ShipCheck read the Paywall metadata field, not the running screen. If the built paywall already shows terms, this finding is a false alarm — update the metadata file to describe what is actually on screen and re-scan.
- ⚠️ **Guideline 4.2 minimum functionality** — Not assessed. The fixture has too few routes to judge, and a 4.2 call needs the running app, not a dependency list.

---

<sub>ShipCheck v0.1.0 · unlimited tier · findings are advisory: App Review outcomes are decided by Apple and Google, not by this tool.</sub>
