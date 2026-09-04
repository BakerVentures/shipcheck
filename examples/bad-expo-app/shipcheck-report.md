# ShipCheck report

**Bad App** · v1.0.0 · generated 2026-09-04 12:52

## Rejection risk: 100 / 100

**Very likely to be rejected**

`[████████████████████]` 16 critical · 8 high · 8 medium · 2 low

**13 block the upload** — App Store Connect will not accept a build until these are fixed · **8 are metadata only** and need no new build — you can fix those in App Store Connect right now.

> Checked against policy text fetched 2026-09-04 from 37 official Apple and Google sources. Run `/shipcheck:refresh` to re-fetch and see what changed.

---

## Findings

### 1. 🔴 CRITICAL targetSdkVersion is 33, below Play's floor of API 36

**Guideline play:target-api-level** · confidence: high · Android · blocks upload · deterministic

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

android/build.gradle sets targetSdkVersion = 33. Play requires API 36 for new apps and updates (from August 31, 2026), and API 35 for an existing app to stay available to users on newer Android versions.

**Fix**

Set `targetSdkVersion = 36` in android/build.gradle (or `expo.android.targetSdkVersion` / the expo-build-properties plugin) and re-test. Below API 35 the Play Console rejects the upload outright.


### 2. 🔴 CRITICAL App icon contains an alpha channel

**Guideline ASC:screenshot-specifications** · confidence: high · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:** Images can’t include alpha channels or transparencies.
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

assets/icon.png (ios.icon.light) has color type 6

**Fix**

Flatten the icon onto an opaque background and re-export without transparency (color type 2, no tRNS). App Store Connect rejects icons with alpha at upload time.


### 3. 🔴 CRITICAL ios.icon.dark icon contains an alpha channel

**Guideline ASC:screenshot-specifications** · confidence: high · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:** Images can’t include alpha channels or transparencies.
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

assets/icon-dark.png has color type 6

**Fix**

Flatten the ios.icon.dark icon variant onto an opaque background and re-export without transparency.


### 4. 🔴 CRITICAL ios.icon.tinted icon contains an alpha channel

**Guideline ASC:screenshot-specifications** · confidence: high · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:** Images can’t include alpha channels or transparencies.
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

assets/icon-tinted.png has color type 6

**Fix**

Flatten the ios.icon.tinted icon variant onto an opaque background and re-export without transparency.


### 5. 🔴 CRITICAL eas.json production profile sets developmentClient: true

**Guideline 2.2** · confidence: high · iOS · blocks review · deterministic

> **2.2 Beta Testing**
> 
> Demos, betas, and trial versions of your app don’t belong on the App Store – use TestFlight instead. Any app submitted for beta distribution via TestFlight should be intended for public distribution and should comply with the App Review Guidelines. Note, however, that apps using TestFlight cannot be distributed to testers in exchange for compensation of any kind, including as a reward for crowd-sourced funding. Significant updates to your beta build should be submitted to TestFlight App Review before being distributed to your testers. To learn more, visit the [TestFlight Beta Testing](/testflight/) page.
> 
> — [2.2](https://developer.apple.com/app-store/review/guidelines/#beta-testing)

**What ShipCheck found**

build.production.developmentClient = true

**Fix**

Remove `developmentClient` from the production profile. A dev-client build shows the Expo dev menu and will be rejected as a beta/incomplete app.


### 6. 🔴 CRITICAL Missing NSCameraUsageDescription

**Guideline 5.1.1** · confidence: high · iOS · blocks review · deterministic

> **5.1.1 Data Collection and Storage**
> 
> - **(i) Privacy Policies:** All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
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


### 7. 🔴 CRITICAL Missing NSUserTrackingUsageDescription

**Guideline 5.1.1** · confidence: high · iOS · blocks review · deterministic

> **5.1.1 Data Collection and Storage**
> 
> - **(i) Privacy Policies:** All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
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


### 8. 🔴 CRITICAL Third-party login present with no Sign in with Apple

**Guideline 4.8** · confidence: high · iOS · blocks review · deterministic

> **4.8 Login Services**
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


### 9. 🔴 CRITICAL App has accounts but no demo account for review

**Guideline 2.1** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.1 App Completeness**
> 
> - **(a)** Submissions to App Review, including apps you make available for pre-order, should be final versions with all necessary metadata and fully functional URLs included; placeholder text, empty websites, and other temporary content should be scrubbed before submission. Make sure your app has been tested on-device for bugs and stability before you submit it, and include demo account info (and turn on your back-end service!) if your app includes a login. If you are unable to provide a demo account due to legal or security obligations, you may include a built-in demo mode in lieu of a demo account with prior approval by Apple. Ensure the demo mode exhibits your app’s full features and functionality. We will reject incomplete app bundles and binaries that crash or exhibit obvious technical problems.
> - **(b)** If you offer in-app purchases in your app, make […]
> 
> — [2.1](https://developer.apple.com/app-store/review/guidelines/#app-completeness)

**What ShipCheck found**

Accounts = yes, Demo account = (blank)

**Fix**

Put working credentials in App Review notes. A reviewer who hits a login wall with no credentials rejects under 2.1 App Completeness, and it costs you a full review cycle.


### 10. 🔴 CRITICAL Placeholder text in Description

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.3.1**
> 
> - **(a)** Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App Store a […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Description contains "Lorem ipsum"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 11. 🔴 CRITICAL Placeholder text in Privacy Policy Url

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.3.1**
> 
> - **(a)** Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App Store a […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Privacy Policy Url contains "example.com"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 12. 🔴 CRITICAL Placeholder text in Support Url

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.3.1**
> 
> - **(a)** Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App Store a […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

Support Url contains "example.com"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 13. 🔴 CRITICAL Placeholder text in What'S New

**Guideline 2.3.1** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.3.1**
> 
> - **(a)** Don’t include any hidden, dormant, or undocumented features in your app; your app’s functionality should be clear to end users and App Review. All new features, functionality, and product changes must be described with specificity in the Notes for Review section of App Store Connect (generic descriptions will be rejected) and accessible for review. Similarly, marketing your app in a misleading way, such as by promoting content or services that it does not actually offer (e.g. iOS-based virus and malware scanners) or promoting a false price, whether within or outside of the App Store, is grounds for removal of your app from the App Store or a block from installing via alternative distribution and termination of your developer account.
> - **(b)** Egregious or repeated behavior is grounds for removal from the Apple Developer Program. We work hard to make the App Store a […]
> 
> — [2.3.1](https://developer.apple.com/app-store/review/guidelines/#2.3.1)

**What ShipCheck found**

What'S New contains "TODO"

**Fix**

Replace it with real copy. Placeholder or template text in the listing is a guaranteed 2.3 rejection.


### 14. 🔴 CRITICAL Privacy Policy Url is not reachable

**Guideline 5.1.1** · confidence: high · iOS · metadata only — no new build · deterministic

> **5.1.1 Data Collection and Storage**
> 
> - **(i) Privacy Policies:** All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
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


### 15. 🔴 CRITICAL Support Url is not reachable

**Guideline 2.3.8** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.3.8** Metadata should be appropriate for all audiences, so make sure your app and in-app purchase icons, screenshots, and previews adhere to a 4+ age rating even if your app is rated higher. For example, if your app is a game that includes violence, select images that don’t depict a gruesome death or a gun pointed at a specific character. Use of terms like “For Kids” and “For Children” in app metadata is reserved in the App Store for the Kids Category. Remember to ensure your metadata, including app name and icons (small, large, Apple Watch app, alternate icons, etc.), are similar to avoid creating confusion.
> 
> — [2.3.8](https://developer.apple.com/app-store/review/guidelines/#2.3.8)

**What ShipCheck found**

https://example.com/support -> HTTP 404

**Fix**

Fix or replace the URL. Reviewers open every link in the listing; a dead privacy policy URL is an automatic rejection.


### 16. 🔴 CRITICAL App creates accounts but no in-app account deletion found

**Guideline 5.1.1v** · confidence: medium · iOS · blocks review · deterministic

> **(v) Account Sign-In:** If your app doesn’t include significant account-based features, let people use it without a login. If your app supports account creation, you must also [offer account deletion within the app](/support/offering-account-deletion-in-your-app/). Apps may not require users to enter personal information to function, except when directly relevant to the core functionality of the app or required by law. If your core app functionality is not related to a specific social network (e.g. Facebook, WeChat, Weibo, X, etc.), you must provide access without a login or via another mechanism. Pulling basic profile information, sharing to the social network, or inviting friends to use the app are not considered core app functionality. The app must also include a mechanism to revoke social network credentials and disable data access between the app and social network from within the […]
> 
> — [5.1.1v](https://developer.apple.com/app-store/review/guidelines/#5.1.1v)

**What ShipCheck found**

Auth via @supabase/supabase-js; no delete-account code path found in source.

**Fix**

Add an in-app control that permanently deletes the account (not just a link to support, and not sign-out). Apple has required this since 30 June 2022 for any app that supports account creation.


### 17. 🟠 HIGH 2 sensitive permission(s) require a Play Console declaration

**Guideline play:permissions-policy** · confidence: high · Android · blocks upload · deterministic

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

For each one, either remove the permission or complete the matching declaration form in Play Console > App content. A release with an undeclared sensitive permission is rejected.

- **ACCESS_BACKGROUND_LOCATION** — reviewed individually, and it needs a demo video of the in-app flow plus user-facing consent. Confirm foreground location genuinely is not enough; if it is, remove this. Budget several review rounds if you keep it.
- **QUERY_ALL_PACKAGES** — replace with a <queries> element naming the packages or intents you actually need. Keep the permission only with an approved declaration — broad package visibility is reserved for launchers, antivirus and accessibility tools.


### 18. 🟠 HIGH App icon is 512x512, not 1024x1024

**Guideline ASC:screenshot-specifications** · confidence: high · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:** Images can’t include alpha channels or transparencies.
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

assets/icon.png (ios.icon.light) is 512x512

**Fix**

Export a 1024x1024 PNG. App Store Connect rejects the upload outright at any other size.


### 19. 🟠 HIGH App Name is 51 chars (limit 30)

**Guideline 2.3** · confidence: high · iOS · blocks upload · deterministic

> **2.3 Accurate Metadata**
> 
> Customers should know what they’re getting when they download or buy your app, so make sure all your app metadata, including privacy information, your app description, screenshots, and previews accurately reflect the app’s core experience and remember to keep them up-to-date with new versions.
> 
> — [2.3](https://developer.apple.com/app-store/review/guidelines/#accurate-metadata)

**What ShipCheck found**

51 characters

**Fix**

Trim to 30 characters. App Store Connect will not accept the listing otherwise.


### 20. 🟠 HIGH Foreground service type 'location' without FOREGROUND_SERVICE_LOCATION

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


### 21. 🟠 HIGH No PrivacyInfo.xcprivacy in the app target

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


### 22. 🟠 HIGH expo-device uses required-reason API but ships no privacy manifest

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


### 23. 🟠 HIGH expo-file-system uses required-reason API but ships no privacy manifest

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


### 24. 🟠 HIGH No restore-purchases call found in source

**Guideline 3.1.1** · confidence: medium · iOS · blocks review · deterministic

> **3.1.1 In-App Purchase:**
> 
> - If you want to unlock features or functionality within your app, (by way of example: subscriptions, in-game currencies, game levels, access to premium content, or unlocking a full version), you must use in-app purchase. Apps may not use their own mechanisms to unlock content or functionality, such as license keys, augmented reality markers, QR codes, cryptocurrencies and cryptocurrency wallets, etc.
> - Apps may use in-app purchase currencies to enable customers to “tip” the developer or digital content providers in the app.
> - Any credits or in-game currencies purchased via in-app purchase may not expire, and you should make sure you have a restore mechanism for any restorable in-app purchases.
> - Apps may enable gifting of items that are eligible for in-app purchase to others. Such gifts may only be refunded to the original purchaser and may not be […]
> 
> — [3.1.1](https://developer.apple.com/app-store/review/guidelines/#in-app-purchase)

**What ShipCheck found**

IAP via react-native-purchases but no restorePurchases/restoreTransactions/syncPurchases call found in app source.

**Fix**

Add a visible "Restore Purchases" control that calls `Purchases.restorePurchases()` (RevenueCat) or the equivalent. Apps selling non-consumables or subscriptions must let a returning user restore entitlements.


### 25. 🟡 MEDIUM ITSAppUsesNonExemptEncryption is not declared

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


### 26. 🟡 MEDIUM eas.json production profile uses internal distribution

confidence: high · iOS · blocks review · deterministic

**What ShipCheck found**

build.production.distribution = internal

**Fix**

Set `"distribution": "store"` for the profile you submit to the App Store.


### 27. 🟡 MEDIUM ios.icon.dark icon is 512x512, not 1024x1024

**Guideline ASC:screenshot-specifications** · confidence: medium · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:** Images can’t include alpha channels or transparencies.
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

assets/icon-dark.png is 512x512

**Fix**

Export the ios.icon.dark variant at 1024x1024 to match the others.


### 28. 🟡 MEDIUM ios.icon.tinted icon is 512x512, not 1024x1024

**Guideline ASC:screenshot-specifications** · confidence: medium · iOS · blocks upload · deterministic

> # Screenshot specifications
> 
> You can upload one to 10 screenshots in `.jpeg`, `.jpg`, and `.png` formats, with the following specifications.
> 
> **Note:** Images can’t include alpha channels or transparencies.
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

assets/icon-tinted.png is 512x512

**Fix**

Export the ios.icon.tinted variant at 1024x1024 to match the others.


### 29. 🟡 MEDIUM 6 runtime permission(s) need prominent in-app disclosure

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


### 30. 🟡 MEDIUM expo-dev-client is a production dependency

**Guideline 2.2** · confidence: medium · iOS · blocks review · deterministic

> **2.2 Beta Testing**
> 
> Demos, betas, and trial versions of your app don’t belong on the App Store – use TestFlight instead. Any app submitted for beta distribution via TestFlight should be intended for public distribution and should comply with the App Review Guidelines. Note, however, that apps using TestFlight cannot be distributed to testers in exchange for compensation of any kind, including as a reward for crowd-sourced funding. Significant updates to your beta build should be submitted to TestFlight App Review before being distributed to your testers. To learn more, visit the [TestFlight Beta Testing](/testflight/) page.
> 
> — [2.2](https://developer.apple.com/app-store/review/guidelines/#beta-testing)

**What ShipCheck found**

expo-dev-client present in package.json dependencies

**Fix**

Move it to devDependencies. If it is bundled into the release binary the Expo dev menu can surface in the shipped app, which reads as a beta build to review.


### 31. 🟡 MEDIUM NSLocationWhenInUseUsageDescription uses a generic purpose string

**Guideline 5.1.1** · confidence: medium · iOS · blocks review · deterministic

> **5.1.1 Data Collection and Storage**
> 
> - **(i) Privacy Policies:** All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
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


### 32. 🟡 MEDIUM NSPhotoLibraryUsageDescription uses a generic purpose string

**Guideline 5.1.1** · confidence: medium · iOS · blocks review · deterministic

> **5.1.1 Data Collection and Storage**
> 
> - **(i) Privacy Policies:** All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
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


### 33. ⚪ LOW Keywords contain spaces after commas

**Guideline 2.3.7** · confidence: high · iOS · metadata only — no new build · deterministic

> **2.3.7** Choose a unique app name, assign keywords that accurately describe your app, and don’t try to pack any of your metadata with trademarked terms, popular app names, pricing information, or other irrelevant phrases just to game the system. App names must be limited to 30 characters. Metadata such as app names, subtitles, screenshots, and previews should not include prices, terms, or descriptions that are not specific to the metadata type. App subtitles are a great way to provide additional context for your app; they must follow our standard metadata rules and should not include inappropriate content, reference other apps, or make unverifiable product claims. Apple may modify inappropriate keywords at any time or take other appropriate steps to prevent abuse.
> 
> — [2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)

**What ShipCheck found**

keywords = "fitness, dating, workout, gym, health"

**Fix**

Use commas with no spaces — each space costs you a character of the 100-character budget.


### 34. ⚪ LOW expo-camera pulls in NSMicrophone but nothing calls it

**Guideline 5.1.1** · confidence: medium · iOS · blocks review · deterministic

> **5.1.1 Data Collection and Storage**
> 
> - **(i) Privacy Policies:** All apps must include a link to their privacy policy in the App Store Connect metadata field and within the app in an easily accessible manner. The privacy policy must clearly and explicitly:
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

## Not checked

ShipCheck could not verify these. They are not passes:

- ⚠️ **Uninstalled dependencies** — These are in package.json but not under node_modules, so their privacy manifests could not be checked: react-native. Run a full install and re-scan.
- ⚠️ **Pod-delivered privacy manifests** — These packages ship their native SDK through CocoaPods, and ios/Pods is not present, so ShipCheck cannot confirm the pod carries its privacy manifest: react-native-purchases. Run `npx expo prebuild` (or `pod install`) and re-scan.
- ⚠️ **Apple-listed SDK manifests** — @react-native-google-signin/google-signin, react-native-fbsdk-next deliver their SDK through CocoaPods and ios/Pods is absent, so ShipCheck cannot confirm the pod ships a manifest and signature. Run `npx expo prebuild` and re-scan.

---

<sub>ShipCheck v0.2.10 · unlimited tier · findings are advisory: App Review outcomes are decided by Apple and Google, not by this tool.</sub>
