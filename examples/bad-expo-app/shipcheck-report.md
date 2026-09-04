# ShipCheck report

**Bad App** · v1.0.0 · generated 2026-09-03 17:59

## Rejection risk: 100 / 100

**Very likely to be rejected**

`[████████████████████]` 19 critical · 16 high · 14 medium · 3 low

**15 block the upload** — App Store Connect will not accept a build until these are fixed · **14 are metadata only** and need no new build — you can fix those in App Store Connect right now.

> Checked against policy text fetched 2026-09-03 from 37 official Apple and Google sources. Run `/shipcheck:refresh` to re-fetch and see what changed.

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


### 2. 🔴 CRITICAL app/index.tsx imports expo-tracking-transparency, which is not a dependency

**Guideline 2.1** · confidence: high · both · blocks upload · judgment

> 2.1 App Completeness
> 
> - **(a)**![ASR & NR] Submissions to App Review, including apps you make available for pre-order, should be final versions with all necessary metadata and fully functional URLs included; placeholder text, empty websites, and other temporary content should be scrubbed before submission. Make sure your app has been tested on-device for bugs and stability before you submit it, and include demo account info (and turn on your back-end service!) if your app includes a login. If you are unable to provide a demo account due to legal or security obligations, you may include a built-in demo mode in lieu of a demo account with prior approval by Apple. Ensure the demo mode exhibits your app’s full features and functionality. We will reject incomplete app bundles and binaries that crash or exhibit obvious technical problems.
> - **(b)** If you offer in-app purchases in your app, […]
> 
> — [2.1](https://developer.apple.com/app-store/review/guidelines/#app-completeness)

**What ShipCheck found**

app/index.tsx:4 `import { requestTrackingPermissionsAsync } from 'expo-tracking-transparency';`. expo-tracking-transparency does not appear in package.json dependencies or devDependencies, and there is no node_modules/expo-tracking-transparency. Metro will fail to resolve the module.

**What the reviewer will likely say**

> We were unable to review your app as it crashed on launch. Please revise your app and test it on a device to ensure it will launch without crashing.

**Fix**

Run `npx expo install expo-tracking-transparency` so it is added to package.json, and add the config plugin entry:

  "plugins": [["expo-tracking-transparency", { "userTrackingPermission": "<your specific reason>" }]]

If you do not intend to ship App Tracking Transparency, delete the import and the `trackMe` function from app/index.tsx instead.


### 3. 🔴 CRITICAL App icon contains an alpha channel

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

assets/icon.png (ios.icon.light) has color type 6

**Fix**

Flatten the icon onto an opaque background and re-export without transparency (color type 2, no tRNS). App Store Connect rejects icons with alpha at upload time.


### 4. 🔴 CRITICAL ios.icon.dark icon contains an alpha channel

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

assets/icon-dark.png has color type 6

**Fix**

Flatten the ios.icon.dark icon variant onto an opaque background and re-export without transparency.


### 5. 🔴 CRITICAL ios.icon.tinted icon contains an alpha channel

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

assets/icon-tinted.png has color type 6

**Fix**

Flatten the ios.icon.tinted icon variant onto an opaque background and re-export without transparency.


### 6. 🔴 CRITICAL The Go Pro button references an undefined variable and will throw

**Guideline 2.1** · confidence: high · both · blocks review · judgment

> 2.1 App Completeness
> 
> - **(a)**![ASR & NR] Submissions to App Review, including apps you make available for pre-order, should be final versions with all necessary metadata and fully functional URLs included; placeholder text, empty websites, and other temporary content should be scrubbed before submission. Make sure your app has been tested on-device for bugs and stability before you submit it, and include demo account info (and turn on your back-end service!) if your app includes a login. If you are unable to provide a demo account due to legal or security obligations, you may include a built-in demo mode in lieu of a demo account with prior approval by Apple. Ensure the demo mode exhibits your app’s full features and functionality. We will reject incomplete app bundles and binaries that crash or exhibit obvious technical problems.
> - **(b)** If you offer in-app purchases in your app, […]
> 
> — [2.1](https://developer.apple.com/app-store/review/guidelines/#app-completeness)

**What ShipCheck found**

app/index.tsx:37 `<Button title="Go Pro" onPress={() => Purchases.purchasePackage(pkg)} />`. `pkg` is never declared, imported, or fetched in the file. Tapping Go Pro throws a ReferenceError. There is also no `Purchases.configure()` call anywhere in the project, so the RevenueCat SDK is never initialised.

**What the reviewer will likely say**

> We found that your in-app purchase products exhibited one or more bugs when reviewed on iPhone. Specifically, the app did not respond when we tapped Go Pro.

**Fix**

Fetch offerings before purchase and configure the SDK at startup:

  // app/_layout.tsx
  Purchases.configure({ apiKey: process.env.EXPO_PUBLIC_RC_IOS_KEY });

  // app/index.tsx
  const [pkg, setPkg] = useState(null);
  useEffect(() => {
    Purchases.getOfferings().then(o => setPkg(o.current?.availablePackages[0] ?? null));
  }, []);
  <Button title="Go Pro" disabled={!pkg} onPress={() => Purchases.purchasePackage(pkg)} />


### 7. 🔴 CRITICAL eas.json production profile sets developmentClient: true

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


### 8. 🔴 CRITICAL Paywall discloses no price, period, or renewal terms before purchase

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

The entire purchase surface is app/index.tsx:37 — a single `Button` labelled "Go Pro". The metadata `Paywall` field confirms it: "A screen with a Go Pro button." The subscription is "Pro Monthly $4.99", but nothing in the app states the price, the one-month period, that it auto-renews, or what Pro includes, and there are no Terms of Use (EULA) or Privacy Policy links on the purchase screen.

**What the reviewer will likely say**

> Your app's binary does not include the required information for auto-renewable subscriptions. Specifically, the app is missing the title of the subscription, the length of the subscription, and the price of the subscription, including price per unit.

**Fix**

Render these on the purchase screen itself, above the buy button, before any purchase can be initiated:

  Pro Monthly — $4.99/month
  Unlimited workout logs, AI coaching, and progress photos.
  Subscription automatically renews monthly unless auto-renew is turned off
  at least 24 hours before the end of the current period. Manage or cancel
  in your App Store account settings.
  [Terms of Use (EULA)]  [Privacy Policy]

Both links must be tappable and resolve. Alternatively, adopt a RevenueCat prebuilt paywall template, which ships these elements.


### 9. 🔴 CRITICAL Missing NSCameraUsageDescription

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


### 10. 🔴 CRITICAL Missing NSUserTrackingUsageDescription

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


### 11. 🔴 CRITICAL Third-party login present with no Sign in with Apple

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


### 12. 🔴 CRITICAL App has accounts but no demo account for review

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


### 13. 🔴 CRITICAL Placeholder text in Description

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


### 14. 🔴 CRITICAL Placeholder text in Privacy Policy Url

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


### 15. 🔴 CRITICAL Placeholder text in Support Url

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


### 16. 🔴 CRITICAL Placeholder text in What'S New

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


### 17. 🔴 CRITICAL Privacy Policy Url is not reachable

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


### 18. 🔴 CRITICAL Support Url is not reachable

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


### 19. 🔴 CRITICAL App creates accounts but no in-app account deletion found

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


### 20. 🟠 HIGH 2 sensitive permission(s) require a Play Console declaration

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


### 21. 🟠 HIGH App icon is 512x512, not 1024x1024

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

assets/icon.png (ios.icon.light) is 512x512

**Fix**

Export a 1024x1024 PNG. App Store Connect rejects the upload outright at any other size.


### 22. 🟠 HIGH App Name is 51 chars (limit 30)

**Guideline 2.3** · confidence: high · iOS · blocks upload · deterministic

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


### 23. 🟠 HIGH Foreground service type 'location' without FOREGROUND_SERVICE_LOCATION

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


### 24. 🟠 HIGH Background location is requested but the code only ever asks for foreground location

**Guideline play:permissions-policy** · confidence: high · Android · blocks review · judgment

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

android/app/src/main/AndroidManifest.xml declares ACCESS_BACKGROUND_LOCATION and a `.TrackingService` with `foregroundServiceType="location"`, and app.json lists ACCESS_BACKGROUND_LOCATION under expo.android.permissions. The only location code in the project is app/index.tsx:24, `Location.requestForegroundPermissionsAsync()`, behind a "Find gyms near me" button. No `startLocationUpdatesAsync`, no background task, and no `TrackingService` implementation exists in the repo. On iOS there is likewise no NSLocationAlwaysAndWhenInUseUsageDescription.

**What the reviewer will likely say**

> Your app requests background location access but we could not identify a feature that requires it. Apps requesting background location must demonstrate a core user-facing feature that depends on it.

**Fix**

Remove the permission — this is the fast path. Delete ACCESS_BACKGROUND_LOCATION from both android/app/src/main/AndroidManifest.xml and expo.android.permissions in app.json, and remove the `.TrackingService` declaration if nothing implements it. If you genuinely need background location later, budget several review rounds: Play reviews it individually and requires a demo video of the in-app flow plus a prominent consent screen.


### 25. 🟠 HIGH Play needs both an in-app deletion path and a web deletion URL; neither exists

**Guideline play:account-deletion-play** · confidence: high · Android · blocks review · judgment

> # Understanding Google Play’s app account deletion requirements
> 
> Google Play’s data deletion badge and Data deletion area within the Data safety section give users a new set of transparency and controls over their user data while providing developers a way to showcase how they treat user data responsibly. If your app allows users to create an account from within your app, our [User data](https://support.google.com/googleplay/android-developer/answer/13316080) policy requires that it must also allow users to request for their account to be deleted.
> 
> **Tip:** To learn about best practices for designing your account deletion experience with users in mind, visit the [Android Developers Blog](https://android-developers.googleblog.com/2024/03/designing-your-account-deletion-experience-google-play.html).
> 
> ## Overview
> 
> The User Data policy's [Account Deletion […]
> 
> — [play:account-deletion-play](https://support.google.com/googleplay/android-developer/answer/13327111)

**What ShipCheck found**

The app creates accounts (metadata `Accounts: yes`, Supabase auth in lib/supabase.ts). lib/supabase.ts exports only `signOut()`, which ends the session and deletes nothing. No deletion URL appears anywhere in the project or in shipcheck.metadata.md. Play requires an in-app path *and* a web link, so the iOS fix for ACCOUNT-DELETE-MISSING is not sufficient on its own here.

**What the reviewer will likely say**

> Your app allows users to create an account but does not provide a way for users to request account deletion. Complete the Data deletion questions in the Data safety form and provide a web link where users can request deletion.

**Fix**

1. In-app: add a Delete account control that calls a Supabase Edge Function running `supabase.auth.admin.deleteUser(user.id)` plus your own row cleanup — a service-role call, not the client. Confirm destructively, then sign out.
2. Web: publish a page (e.g. https://yourdomain.com/delete-account) where a user can request the same without installing the app.
3. Enter that URL in Play Console > App content > Data safety > Data deletion.


### 26. 🟠 HIGH Declared data does not cover the permissions or the Meta SDK

**Guideline play:data-safety** · confidence: high · Android · blocks review · judgment

> # Provide information for Google Play's Data safety section
> 
> Google Play's Data safety section provides developers with a transparent way to show users if and how they collect, share, and protect user data, before users install an app. Developers are required to tell us about their apps' privacy and security practices by completing a form in Play Console. This information is then shown on your app's store listing on Google Play.
> 
> This article provides an overview of the Data safety form requirements, guidance for completing the form, and information about any recent or upcoming changes.
> 
> [Collapse all](https://support.google.com/googleplay/android-developer/answer/10787469) Expand all
> 
> ## Overview
> 
> The Data safety section on Google Play is a simple way for you to help people understand what user data your app collects or shares, and to showcase your app’s key privacy and security […]
> 
> — [play:data-safety](https://support.google.com/googleplay/android-developer/answer/10787469)

**What ShipCheck found**

The metadata `Data collected` field says "email, location, usage". The manifest requests CAMERA, RECORD_AUDIO and READ_MEDIA_IMAGES (photos/videos and audio, both undeclared), and ACCESS_BACKGROUND_LOCATION (approximate vs. precise location not distinguished). react-native-fbsdk-next shares data with Meta for advertising, which is a sharing declaration, not just collection. Google states: "You alone are responsible for making complete and accurate declarations in your app's store listing on Google Play."

**What the reviewer will likely say**

> Your app's Data safety section is inaccurate. It does not declare the Photos and videos and Audio data types your app has access to, nor the sharing of data with third parties for advertising.

**Fix**

In Play Console > App content > Data safety, add: Photos and videos → Photos; Audio → Voice or sound recordings (or remove RECORD_AUDIO, which nothing in the source uses); Location → both Approximate and Precise; and mark Device or other IDs as both collected and *shared* with third parties for Advertising or marketing. Keep this in sync with the Apple privacy labels in JUDGE-PRIVACY-LABEL-TRACKING — reviewers on both stores compare them.


### 27. 🟠 HIGH Meta SDK is installed and ATT is called, but tracking is not declared anywhere

**Guideline 5.1.2** · confidence: high · iOS · blocks review · judgment

> 5.1.2
> 
> Data Use and Sharing
> 
> - **(i)**Unless otherwise permitted by law, you may not use, transmit, or share someone’s personal data without first obtaining their permission. You must provide access to information about how and where the data will be used. You must clearly disclose where personal data will be shared with third parties, including with third-party AI, and obtain explicit permission before doing so. Data collected from apps may only be shared with third parties to improve the app or serve advertising (in compliance with the [Apple Developer Program License Agreement](/support/terms/)). You must receive explicit permission from users via the App Tracking Transparency APIs to track their activity. Learn more about [tracking](/app-store/user-privacy-and-data-use/). Your app may not require users to enable system functionalities (e.g. push notifications, location services, […]
> 
> — [5.1.2](https://developer.apple.com/app-store/review/guidelines/#data-use-and-sharing)

**What ShipCheck found**

react-native-fbsdk-next is a dependency and app/index.tsx:20 calls `requestTrackingPermissionsAsync()` behind a "Personalize ads" button. The metadata `Data collected` field lists only "email, location, usage" — no advertising data, no identifiers, no tracking. There is also no app-level PrivacyInfo.xcprivacy, so `NSPrivacyTracking` and `NSPrivacyTrackingDomains` are undeclared. Apple defines placing a third-party SDK that combines your users' data with data from other developers' apps to target advertising as tracking, "even if you don't use the SDK for these purposes".

**What the reviewer will likely say**

> Your app's privacy practices do not match the privacy information you provided in App Store Connect. Specifically, your app uses the Facebook SDK to track users but 'Used to Track You' is not declared.

**Fix**

Three places, all of which must agree:
1. App Store Connect > App Privacy: set Identifiers (Device ID) and Usage Data to "Used to Track You", and add Advertising Data.
2. Add `expo.ios.privacyManifests` to app.json with `"NSPrivacyTracking": true` and `"NSPrivacyTrackingDomains": ["graph.facebook.com", "app-measurement.com"]` (list the domains your build actually contacts).
3. Update the `Data collected` line in shipcheck.metadata.md to match.
If you do not actually want ad tracking, remove react-native-fbsdk-next and the ATT call instead — that is the cheaper fix.


### 28. 🟠 HIGH 4+ age rating is not compatible with a dating and wellness app

**Guideline asc:age-ratings** · confidence: high · iOS · metadata only — no new build · judgment

> # Age ratings values and definitions
> 
> The *age rating* is a required [app information](/help/app-store-connect/reference/app-information/app-information) field used for property used by the parental controls. These controls enable parents and guardians to establish a safe online environment for children. As a developer, you can deliver age-appropriate experiences tailored for users across all age groups.
> 
> In App Store Connect, you'll find a list of content descriptors, in-app controls, and capabilities that allow you to specify the frequency or presence of each in your app. Apple generates appropriate ratings based on your answer to the age rating questionnaire. [Learn how to set an app age rating.](/help/app-store-connect/manage-app-information/set-an-app-age-rating)
> 
> The tables below provide detailed information about the different age rating categories and age rating values by […]
> 
> — [asc:age-ratings](https://developer.apple.com/help/app-store-connect/reference/age-ratings)

**What ShipCheck found**

shipcheck.metadata.md declares "Age rating: 4+" while marketing the app as a dating companion with accounts and third-party login, in the Health & Fitness category. Apple's age rating reference puts "Health or Wellness Topics" (calorie tracking, dieting advice, exercise recommendations) under Medical or Wellness, and dating pulls in Mature or Suggestive Themes plus the Messaging and Chat / User-Generated Content capabilities. 4+ is defined as containing "no objectionable material".

**What the reviewer will likely say**

> The age rating you selected in App Store Connect does not reflect your app's content. Specifically, your app includes dating and health content that requires a higher age rating.

**Fix**

Re-answer the age rating questionnaire in App Store Connect > App Information > Age Rating, declaring at minimum Health or Wellness Topics, and — if dating ships — Mature or Suggestive Themes plus the Messaging and Chat and User-Generated Content capabilities. Expect 12+ or 17+. Dating apps generally cannot carry a 4+ rating.


### 29. 🟠 HIGH Description and screenshots reference Android and the web

**Guideline 2.3.10** · confidence: high · iOS · metadata only — no new build · judgment

> 2.3.10
> 
> Make sure your app is focused on the experience of the Apple platforms it supports, and don’t include names, icons, or imagery of other mobile platforms or alternative app marketplaces in your app or metadata, unless there is specific, approved interactive functionality. Make sure your app metadata is focused on the app itself and its experience. Don’t include irrelevant information.
> 
> — [2.3.10](https://developer.apple.com/app-store/review/guidelines/#2.3.10)

**What ShipCheck found**

Description: "Also available on Android and on our website." Screenshot description 2: text overlay "Now on Android too!" Both appear in shipcheck.metadata.md.

**What the reviewer will likely say**

> Your app's metadata includes references to a third-party platform. Specifically, your app description and screenshots reference Android.

**Fix**

Delete the sentence "Also available on Android and on our website." from the description, and re-export screenshot 2 without the "Now on Android too!" overlay. Fixable in App Store Connect with no new build.


### 30. 🟠 HIGH Seven SDKs on Apple's required-manifest list are present and unverified

**Guideline apple:third-party-sdk-requirements** · confidence: medium · iOS · blocks upload · judgment

> # Third-party SDK requirements
> 
> Third-party software development kits (SDKs) can provide great functionality for apps; they can also have the potential to impact user privacy in ways that aren’t obvious to developers and users. As a reminder, when you use a third-party SDK with your app, you are responsible for all the code the SDK includes in your app, and need to be aware of its data collection and use practices. At [WWDC23](/videos/play/wwdc2023/10060/), we introduced new privacy manifests and signatures for SDKs to help bring more awareness for how third-party SDKs use data. This functionality is a step forward for all apps, and we encourage all SDKs to adopt it to better support the apps that depend on them.
> 
> #### Privacy Manifests
> 
> [Privacy manifest files](/documentation/bundleresources/privacy_manifest_files/describing_data_use_in_privacy_manifests) outline the privacy practices […]
> 
> — [apple:third-party-sdk-requirements](https://developer.apple.com/support/third-party-SDK-requirements/)

**What ShipCheck found**

The dependency tree pulls in AppAuth, FBAEMKit, FBSDKCoreKit, FBSDKLoginKit, FBSDKShareKit, GTMAppAuth and GoogleSignIn (via @react-native-google-signin/google-signin and react-native-fbsdk-next). All seven appear on Apple's list of SDKs that must ship a privacy manifest and signature. ios/Pods is not present in this project, so ShipCheck could not confirm the installed pod versions actually carry them.

**What the reviewer will likely say**

> ITMS-91065: Missing signature — the following SDKs are missing a required signature: FBSDKCoreKit.

**Fix**

Run `npx expo prebuild --clean && (cd ios && pod install)`, then re-run this scan so the pods can be checked. Independently, pin `react-native-fbsdk-next` at 13.x or newer and `@react-native-google-signin/google-signin` at 11.x or newer — earlier releases vendor Meta and Google SDK versions that predate the manifest requirement. Patching a pod by hand does not satisfy the signature requirement; you must upgrade.


### 31. 🟠 HIGH No PrivacyInfo.xcprivacy in the app target

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


### 32. 🟠 HIGH expo-device uses required-reason API but ships no privacy manifest

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


### 33. 🟠 HIGH expo-file-system uses required-reason API but ships no privacy manifest

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


### 34. 🟠 HIGH No restore-purchases call found in source

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


### 35. 🟠 HIGH Listing markets an AI coach and dating features that are not in the build

**Guideline 2.3** · confidence: medium · iOS · metadata only — no new build · judgment

> 2.3
> 
> Accurate Metadata
> 
> Customers should know what they’re getting when they download or buy your app, so make sure all your app metadata, including privacy information, your app description, screenshots, and previews accurately reflect the app’s core experience and remember to keep them up-to-date with new versions.
> 
> — [2.3](https://developer.apple.com/app-store/review/guidelines/#accurate-metadata)

**What ShipCheck found**

Screenshot description 1 is "Home screen showing the AI coach feature"; the app name and keywords market dating ("The Ultimate Fitness and Dating Companion", keywords "dating"). The build is a single expo-router route (app/index.tsx) containing a camera view, an Add photo button, a tracking button, a location button, two social login buttons and a Go Pro button. There is no AI dependency in package.json and no profile, match, or messaging code anywhere in app/ or lib/.

**What the reviewer will likely say**

> The app or metadata includes content or features you have not implemented. Specifically, your screenshots display an AI coach feature that we were unable to locate in the app.

**Fix**

Either ship the features before submitting, or align the listing with what the build does: drop screenshot 1's AI coach framing, remove "Dating" from the app name and "dating" from the keywords, and rewrite the description around the features that actually exist. If the AI and dating features do exist in a build ShipCheck could not see, point the reviewer at them explicitly in the review notes.


### 36. 🟡 MEDIUM ITSAppUsesNonExemptEncryption is not declared

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


### 37. 🟡 MEDIUM eas.json production profile uses internal distribution

confidence: high · iOS · blocks review · deterministic

**What ShipCheck found**

build.production.distribution = internal

**Fix**

Set `"distribution": "store"` for the profile you submit to the App Store.


### 38. 🟡 MEDIUM Pricing appears in the screenshots and the description

**Guideline 2.3.7** · confidence: high · iOS · metadata only — no new build · judgment

> 2.3.7
> 
> Choose a unique app name, assign keywords that accurately describe your app, and don’t try to pack any of your metadata with trademarked terms, popular app names, pricing information, or other irrelevant phrases just to game the system. App names must be limited to 30 characters. Metadata such as app names, subtitles, screenshots, and previews should not include prices, terms, or descriptions that are not specific to the metadata type. App subtitles are a great way to provide additional context for your app; they must follow our standard metadata rules and should not include inappropriate content, reference other apps, or make unverifiable product claims. Apple may modify inappropriate keywords at any time or take other appropriate steps to prevent abuse.
> 
> — [2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)

**What ShipCheck found**

Screenshot description 3: "Paywall showing \"$4.99/mo\"". Description: "Download now, only $4.99/month!" The guideline names screenshots explicitly.

**What the reviewer will likely say**

> Your app's metadata includes pricing information. Specifically, your screenshots display the subscription price.

**Fix**

Re-export screenshot 3 with the price cropped or blurred out of the frame, and remove "Download now, only $4.99/month!" from the description — the price is already shown on your product page from the IAP configuration. Note this does not apply to the paywall inside the app, where the price is required (see JUDGE-PAYWALL-TERMS).


### 39. 🟡 MEDIUM Review notes say "Nothing special" for an app with four things that need explaining

**Guideline 2.1** · confidence: high · iOS · metadata only — no new build · judgment

> 2.1 App Completeness
> 
> - **(a)**![ASR & NR] Submissions to App Review, including apps you make available for pre-order, should be final versions with all necessary metadata and fully functional URLs included; placeholder text, empty websites, and other temporary content should be scrubbed before submission. Make sure your app has been tested on-device for bugs and stability before you submit it, and include demo account info (and turn on your back-end service!) if your app includes a login. If you are unable to provide a demo account due to legal or security obligations, you may include a built-in demo mode in lieu of a demo account with prior approval by Apple. Ensure the demo mode exhibits your app’s full features and functionality. We will reject incomplete app bundles and binaries that crash or exhibit obvious technical problems.
> - **(b)** If you offer in-app purchases in your app, […]
> 
> — [2.1](https://developer.apple.com/app-store/review/guidelines/#app-completeness)

**What ShipCheck found**

shipcheck.metadata.md `Review notes: Nothing special.` The app has a login wall with no demo account, background location, an ATT prompt, and a subscription paywall — each of which a reviewer routinely asks about, and each of which costs a full review cycle when unanswered.

**What the reviewer will likely say**

> We need additional information to continue the review of your app.

**Fix**

Replace the review notes with something like:

  Demo account: review@yourdomain.com / <password> (pre-verified, no SMS or email code required).
  Location: tap "Find gyms near me" on the home screen; foreground location only.
  Subscription: tap "Go Pro". Pro Monthly, $4.99/month, auto-renewing. Sandbox purchases work with the demo account.
  Tracking: the ATT prompt appears only after tapping "Personalize ads"; no functionality is gated on consent.

Fixable in App Store Connect with no new build.


### 40. 🟡 MEDIUM ios.icon.dark icon is 512x512, not 1024x1024

**Guideline ASC:screenshot-specifications** · confidence: medium · iOS · blocks upload · deterministic

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

assets/icon-dark.png is 512x512

**Fix**

Export the ios.icon.dark variant at 1024x1024 to match the others.


### 41. 🟡 MEDIUM ios.icon.tinted icon is 512x512, not 1024x1024

**Guideline ASC:screenshot-specifications** · confidence: medium · iOS · blocks upload · deterministic

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

assets/icon-tinted.png is 512x512

**Fix**

Export the ios.icon.tinted variant at 1024x1024 to match the others.


### 42. 🟡 MEDIUM 6 runtime permission(s) need prominent in-app disclosure

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


### 43. 🟡 MEDIUM expo-dev-client is a production dependency

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


### 44. 🟡 MEDIUM ATT prompt fires from a bare button with no explanatory screen

**Guideline 5.1.2** · confidence: medium · iOS · blocks review · judgment

> 5.1.2
> 
> Data Use and Sharing
> 
> - **(i)**Unless otherwise permitted by law, you may not use, transmit, or share someone’s personal data without first obtaining their permission. You must provide access to information about how and where the data will be used. You must clearly disclose where personal data will be shared with third parties, including with third-party AI, and obtain explicit permission before doing so. Data collected from apps may only be shared with third parties to improve the app or serve advertising (in compliance with the [Apple Developer Program License Agreement](/support/terms/)). You must receive explicit permission from users via the App Tracking Transparency APIs to track their activity. Learn more about [tracking](/app-store/user-privacy-and-data-use/). Your app may not require users to enable system functionalities (e.g. push notifications, location services, […]
> 
> — [5.1.2](https://developer.apple.com/app-store/review/guidelines/#data-use-and-sharing)

**What ShipCheck found**

app/index.tsx:33 `<Button title="Personalize ads" onPress={trackMe} />` calls `requestTrackingPermissionsAsync()` directly. Nothing is rendered beforehand to explain what data is used or why, and NSUserTrackingUsageDescription is absent from app.json (see PLIST-MISSING-NSUserTrackingUsageDescription), so the system prompt would render with no purpose string.

**What the reviewer will likely say**

> Your app requests permission to track without providing sufficient context about how tracking will benefit the user.

**Fix**

Show your own explanatory screen before calling the API — state what is collected, who it is shared with, and what the user gets — then request. Set a specific NSUserTrackingUsageDescription such as "Used to measure which of our ads led you here, so we can spend less on advertising and more on the app." Do not gate any feature on the user granting tracking.


### 45. 🟡 MEDIUM Health & Fitness app ships an advertising SDK in the same binary

**Guideline 5.1.3** · confidence: medium · iOS · blocks review · judgment

> 5.1.3
> 
> Health and Health Research
> 
> Health, fitness, and medical data are especially sensitive and apps in this space have some additional rules to make sure customer privacy is protected:
> 
> - **(i)** Apps may not use or disclose to third parties data gathered in the health, fitness, and medical research context—including from the Clinical Health Records API, HealthKit API, Motion and Fitness, MovementDisorder APIs, or health-related human subject research—for advertising, marketing, or other use-based data mining purposes other than improving health management, or for the purpose of health research, and then only with permission. Apps may, however, use a user’s health or fitness data to provide a benefit directly to that user (such as a reduced insurance premium), provided that the app is submitted by the entity providing the benefit, and the data is not shared with a third party. You […]
> 
> — [5.1.3](https://developer.apple.com/app-store/review/guidelines/#health-and-health-research)

**What ShipCheck found**

Declared category is Health & Fitness. react-native-fbsdk-next is installed and app/index.tsx:33 offers a "Personalize ads" control. 5.1.3(i) prohibits using or disclosing fitness-context data to third parties for advertising or marketing. ShipCheck cannot see what your Supabase schema sends where, so this is a risk flag, not a confirmed violation.

**What the reviewer will likely say**

> Please explain how health and fitness data collected by your app is used, and confirm it is not shared with third parties for advertising or marketing purposes.

**Fix**

Confirm no workout, body-measurement or other fitness data is passed to Meta's SDK — including as custom app events or as parameters on standard events. Then state that explicitly in the App Review notes: "Fitness data is stored only in our Supabase backend and is never sent to the Meta SDK, which receives only install and purchase events." If any fitness data does reach an advertising SDK, remove it before submitting.


### 46. 🟡 MEDIUM NSLocationWhenInUseUsageDescription uses a generic purpose string

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


### 47. 🟡 MEDIUM NSPhotoLibraryUsageDescription uses a generic purpose string

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


### 48. 🟡 MEDIUM Dating positioning invites a 4.3(b) spam rejection

**Guideline 4.3** · confidence: low · iOS · blocks review · judgment

> 4.3 Spam
> 
> - **(a)**![ASR & NR] Don’t create multiple Bundle IDs of the same app (for example, submitting a separate map app for every city in the world instead of a single worldwide map that allows users to search any city). This practice results in unnecessary apps, which makes it hard for users to find the apps they want. If your app has different versions for specific locations, sports teams, universities, etc., consider submitting a single app and providing the variations using in-app purchase.
> - **(b)** Don’t submit apps that are indistinguishable from what's already widely available. Opportunistically creating variants of existing app categories or popular apps degrades App Store discovery, reduces overall app quality, and harms both users and developers. Certain kinds of apps, such as dating, flashlight, sound effects, wallpaper, simple timers, and fortune telling, are well […]
> 
> — [4.3](https://developer.apple.com/app-store/review/guidelines/#spam)

**What ShipCheck found**

The app name, subtitle and keywords all market dating ("The Ultimate Fitness and Dating Companion", "Get fit, get dates, get going", keywords include "dating"). Apple names dating explicitly as a category where new submissions are not accepted without a meaningfully different experience. The differentiator here would be the fitness angle, which the build does not currently demonstrate.

**What the reviewer will likely say**

> We found that your app provides the same feature set as other apps already on the App Store, and did not offer a meaningfully different experience.

**Fix**

Make the fitness-plus-dating combination visible in the first screen a reviewer sees, and describe the differentiator in the App Review notes in one sentence. If dating is aspirational rather than built, drop it from the name, subtitle and keywords and submit as a fitness app — which also resolves JUDGE-AGE-RATING and part of JUDGE-SCREENSHOT-FEATURE-MISMATCH.


### 49. 🟡 MEDIUM The shipped build is one screen of permission buttons

**Guideline 4.2** · confidence: low · iOS · blocks review · judgment

> 4.2 Minimum Functionality
> 
> Your app should include features, content, and UI that elevate it beyond a repackaged website. If your app is not particularly useful, unique, or “app-like,” it doesn’t belong on the App Store. If your App doesn’t provide some sort of lasting entertainment value or adequate utility, it may not be accepted. Apps that are simply a song or movie should be submitted to the iTunes Store. Apps that are simply a book or game guide should be submitted to the Apple Books Store.
> 
> — [4.2](https://developer.apple.com/app-store/review/guidelines/#minimum-functionality)

**What ShipCheck found**

app/ contains exactly one route, index.tsx, whose entire UI is a "Welcome" label, a camera view and six buttons — Add photo, Personalize ads, Find gyms near me, two social logins, and Go Pro. There is no workout logging, no dating surface, and no persistence code beyond a Supabase client. Flagging as a risk, not a certainty: a larger build may exist that ShipCheck cannot see from this source tree.

**What the reviewer will likely say**

> We found that the usefulness of your app is limited by the minimal amount of content or features it includes.

**Fix**

Before submitting, confirm the binary you upload contains the feature set the listing describes. If this source tree is the shipping app, it will not clear 4.2 — a reviewer reaches the end of the app in under a minute. If a fuller build exists, no action beyond making sure you submit that one.


### 50. ⚪ LOW Keywords contain spaces after commas

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


### 51. ⚪ LOW expo-camera pulls in NSMicrophone but nothing calls it

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


### 52. ⚪ LOW App name and description make unverifiable superlative claims

**Guideline 2.3.7** · confidence: medium · iOS · metadata only — no new build · judgment

> 2.3.7
> 
> Choose a unique app name, assign keywords that accurately describe your app, and don’t try to pack any of your metadata with trademarked terms, popular app names, pricing information, or other irrelevant phrases just to game the system. App names must be limited to 30 characters. Metadata such as app names, subtitles, screenshots, and previews should not include prices, terms, or descriptions that are not specific to the metadata type. App subtitles are a great way to provide additional context for your app; they must follow our standard metadata rules and should not include inappropriate content, reference other apps, or make unverifiable product claims. Apple may modify inappropriate keywords at any time or take other appropriate steps to prevent abuse.
> 
> — [2.3.7](https://developer.apple.com/app-store/review/guidelines/#2.3.7)

**What ShipCheck found**

App name: "Bad App — The Ultimate Fitness and Dating Companion". Description: "Bad App is the best app." 2.3.7 requires subtitles to not "make unverifiable product claims", and this framing extends the same problem into the name.

**What the reviewer will likely say**

> Your app's metadata includes claims that cannot be verified.

**Fix**

Trim the name to the brand alone (which also fixes the 30-character limit in META-LEN-app-name) and replace "the best app" in the description with a concrete statement of what the app does. Fixable in App Store Connect with no new build.


---

## Likely to pass

Checked and found clean, so you can trust the list above is the whole problem:

- ✅ **No external purchase steering in the app** *(3.1.1)* — Grepped app/ and lib/ for web checkout, Stripe, Gumroad and 'manage your subscription' links: none. Purchases go through react-native-purchases -> StoreKit, not a custom unlock mechanism.
- ✅ **No loot boxes, gambling or real-money mechanics** *(5.3)* — No randomized-item purchase, wagering or virtual-currency code in the project, so the 5.3 entitlement and odds-disclosure requirements do not apply.
- ✅ **Not a web wrapper** *(4.2.2)* — react-native-webview is not a dependency and no route renders remote web content, so the usual 4.2.2 'repackaged website' rejection path does not apply. (Thinness is flagged separately under JUDGE-MINIMUM-FUNCTIONALITY.)
- ✅ **@react-native-async-storage/async-storage ships its own privacy manifest** *(apple:required-reason-api)* — node_modules/@react-native-async-storage/async-storage carries a PrivacyInfo.xcprivacy declaring NSPrivacyAccessedAPICategoryFileTimestamp. Verified on disk, not assumed.
- ✅ **Not in the Kids Category** *(5.1.4)* — Category is Health & Fitness, so the 5.1.4 ban on third-party analytics and advertising does not apply here -- which matters, because the Meta SDK would be disqualifying if it did. The 4+ age rating is a separate problem (JUDGE-AGE-RATING).
- ✅ **Foreground location is requested in context** *(5.1.1)* — app/index.tsx:24 requests location inside the 'Find gyms near me' handler rather than at launch or during onboarding, which is the correct 5.1.1 pattern. The purpose string itself is still weak (PLIST-WEAK-NSLocationWhenInUseUsageDescription).
- ✅ **iOS bundle identifier and Android package match** — Both are com.example.badapp, consistent between app.json ios.bundleIdentifier and android.package. (Change the com.example prefix to your own reverse-domain before you register the app.)

---

## Not checked

ShipCheck could not verify these. They are not passes:

- ⚠️ **Uninstalled dependencies** — These are in package.json but not under node_modules, so their privacy manifests could not be checked: react-native. Run a full install and re-scan.
- ⚠️ **Pod-delivered privacy manifests** — These packages ship their native SDK through CocoaPods, and ios/Pods is not present, so ShipCheck cannot confirm the pod carries its privacy manifest: react-native-purchases. Run `npx expo prebuild` (or `pod install`) and re-scan.
- ⚠️ **Apple-listed SDK manifests** — @react-native-google-signin/google-signin, react-native-fbsdk-next deliver their SDK through CocoaPods and ios/Pods is absent, so ShipCheck cannot confirm the pod ships a manifest and signature. Run `npx expo prebuild` and re-scan.
- ⚠️ **Play closed-testing gate (personal accounts)** — Google requires personal developer accounts created after November 13, 2023 to run a closed test with 'at least 12 testers ... opted in continuously for the preceding 14 days' before Production unlocks. ShipCheck cannot see your Play Console account type. If your account is a personal one created after that date, this is a hard multi-week gate, not a code fix -- start the closed test now, in parallel with the fixes below. Quoted from corpus/google/testing-requirements.md.
- ⚠️ **User-generated content obligations (1.2)** — The listing markets dating, but no profile, matching, messaging or moderation code exists in app/ or lib/. If dating features ship in a build ShipCheck could not see, guideline 1.2 additionally requires content filtering, a report mechanism, user blocking and published contact information -- none of which could be verified here.
- ⚠️ **Privacy policy page content** — https://example.com/privacy returns HTTP 404, so ShipCheck could not read the page. Even once the URL resolves, a generic template that does not name the app and the specific data it collects is still a rejection, and that can only be checked by reading the published page.
- ⚠️ **Actual screenshot images** — Only the textual descriptions in shipcheck.metadata.md were available. Device frames showing an Android status bar, non-iOS UI chrome, and required screenshot dimensions could not be verified.
- ⚠️ **Play Console declaration state** — ShipCheck reads the repo, not your Play Console. Whether the ACCESS_BACKGROUND_LOCATION and QUERY_ALL_PACKAGES declaration forms, the Data safety form, and the foreground-service use-case justification are already filled in could not be checked.
- ⚠️ **Paywall UI beyond the Go Pro button** — There is no dedicated paywall component in the project -- the only purchase surface is app/index.tsx:37. If a real paywall screen exists elsewhere, re-run the scan against that source so 3.1.2(c) can be assessed against the actual screen.

---

<sub>ShipCheck v0.1.0 · unlimited tier · findings are advisory: App Review outcomes are decided by Apple and Google, not by this tool.</sub>
