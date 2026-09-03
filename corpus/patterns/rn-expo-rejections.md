---
shipcheck_source_id: rn-expo-rejections
title: "React Native / Expo rejection patterns"
maintained: hand-curated
updated: 2026-09-03
---

# React Native / Expo rejection patterns

Hand-maintained. Unlike the rest of `corpus/`, this file is not fetched — it is
the accumulated shape of how RN/Expo apps specifically get rejected, which the
guideline text never spells out because Apple and Google write for all apps.

**How to use this file.** Each pattern names the clause it maps to. Always quote
the clause from `corpus/apple/asrg.sections/<clause>.md` or the relevant vendor
page, never from this file — this file's job is to tell you *what to look for*
and *what the fix is*, not to be the citation. If a statement here conflicts
with the fetched corpus, the fetched corpus wins and this file is stale.

`detect: deterministic` means `scripts/scan.py` already checks it and you should
not re-derive it. `detect: judgment` means it needs you to read the code or the
metadata and decide.

---

## A. Privacy manifests and required-reason APIs

### P-01 Missing app-level PrivacyInfo.xcprivacy
- **Clause:** `apple:required-reason-api`; App Store Connect rejects at upload, before review.
- **Detect:** deterministic (`PRIVACY-MANIFEST-MISSING`)
- **Why RN/Expo trips this:** almost every Expo app pulls `expo-file-system`,
  `expo-device`, `expo-constants` or `@react-native-async-storage/async-storage`
  transitively, all of which touch required-reason API. Developers assume the
  library's own manifest covers them. It does not: an SDK's manifest covers the
  SDK's binary, and the app target still needs its own for code the app calls.
- **Fix:** set `expo.ios.privacyManifests` in app.json (Expo SDK 50+) or add
  `ios/<App>/PrivacyInfo.xcprivacy` in a bare project, declaring
  `NSPrivacyAccessedAPITypes` with an approved reason code from
  `corpus/apple/required-reason-codes.md`.
- **Most common correct answers:** UserDefaults → `CA92.1`; File timestamp →
  `C617.1`; Disk space → `E174.1`; System boot time → `35F9.1`; Active keyboards
  → `3EC4.1`. Verify each against the corpus before quoting — Apple revises the
  list.

### P-02 Declared categories do not cover the installed SDKs
- **Clause:** `apple:required-reason-api`
- **Detect:** deterministic (`REASON-MISSING-*`)
- **Note:** the failure mode is an email from Apple ("ITMS-91053: Missing API
  declaration") rather than a review rejection, which developers often ignore
  until the build will not go to TestFlight.

### P-03 A listed third-party SDK ships no privacy manifest or signature
- **Clause:** `apple:third-party-sdk-requirements`
- **Detect:** judgment — cross-reference `facts.dependencies` against the SDK
  list in `corpus/apple/third-party-sdk-requirements.md`, which is fetched live.
- **RN/Expo specifics:** the common offenders are pinned-old versions of
  Firebase pods, `react-native-fbsdk-next` below v13, `AppAuth` via
  `@react-native-google-signin/google-signin`, and any library vendoring
  `OpenSSL`/`BoringSSL`.
- **Fix:** upgrade to a version that ships `PrivacyInfo.xcprivacy`. Downgrading
  or patching the pod by hand does not satisfy the signature requirement.

### P-04 Privacy manifest contradicts the App Privacy nutrition labels
- **Clause:** `5.1.2`, plus `apple:app-privacy-details`
- **Detect:** judgment — compare `NSPrivacyCollectedDataTypes` and the
  `Data collected` metadata field against what the analytics/attribution SDKs in
  `dependencies` actually collect.
- **Classic case:** PostHog or Firebase Analytics installed, but the labels say
  "Data Not Collected". Reviewers check this and it reads as a false declaration.

---

## B. Permissions and purpose strings

### P-05 Missing NSUsageDescription for a transitively pulled permission
- **Clause:** `5.1.1`
- **Detect:** deterministic (`PLIST-MISSING-*`)
- **Why RN/Expo trips this:** the developer never wrote camera code — they added
  `expo-image-picker` for an avatar. The config plugin adds the *Android*
  permission automatically but the iOS string only appears if the plugin is
  configured. On device the app hard-crashes at the permission prompt, which is
  a 2.1 rejection as well as a 5.1.1 one.

### P-06 Generic or Expo-default purpose strings
- **Clause:** `5.1.1`
- **Detect:** deterministic (`PLIST-WEAK-*`)
- **What reviewers reject:** `"Allow $(PRODUCT_NAME) to access your camera"` —
  Expo's own plugin default. Also `"We need your location."`, `"Required for the
  app to work."`
- **Fix shape:** name the feature and the user benefit —
  `"Used to attach a photo to a workout log so you can track progress visually."`

### P-07 Requesting permissions at launch instead of in context
- **Clause:** `5.1.1`, `5.1.2`
- **Detect:** judgment — look for permission requests in the root layout,
  `App.tsx`, a splash screen, or an onboarding step that runs before the feature
  that needs them.
- **Note:** this is one of the most common causes of a "please explain" reply
  rather than an outright rejection, but it costs a review cycle either way.

### P-08 ATT prompt timing and wording
- **Clause:** `5.1.2`, plus `apple:user-privacy-and-data-use`
- **Detect:** judgment — `expo-tracking-transparency` present.
- **Two failure modes:** (a) `NSUserTrackingUsageDescription` missing while an
  attribution SDK (AppsFlyer, Meta) is installed; (b) the prompt appears before
  the app has explained anything, or the app gates functionality on consent,
  which is explicitly not allowed. Offering an incentive for granting tracking
  is also a rejection.

---

## C. Accounts, login, deletion

### P-09 Third-party login without Sign in with Apple
- **Clause:** `4.8`
- **Detect:** deterministic (`SIWA-MISSING`)
- **RN/Expo specifics:** triggered by `@react-native-google-signin/google-signin`,
  `react-native-fbsdk-next`, and `expo-auth-session` used for social providers.
  The remedy is `expo-apple-authentication` plus `expo.ios.usesAppleSignIn: true`.
- **Exemptions worth checking before you assert this** (they are in the clause
  text): the app uses only your own account system; it is an education,
  enterprise or business app using an existing institutional account; it uses a
  government or industry-backed citizen ID; or it is a client for a specific
  third-party service.

### P-10 No in-app account deletion
- **Clause:** `5.1.1v`
- **Detect:** deterministic (`ACCOUNT-DELETE-MISSING`), then confirm by reading
  the code — the deterministic check greps for a delete path and can miss one
  that is worded unusually.
- **What does not count:** a mailto: link, a "contact support to delete" note, a
  web page the user must visit, or sign-out. It must be initiated and completed
  in the app, and it must delete the account, not just the local session.
- **Also:** if the app offers account creation it must also appear in the
  Play listing under the same requirement — see
  `corpus/google/account-deletion-play.md`, which additionally requires a
  web-accessible deletion route.

### P-11 Login wall with no demo account
- **Clause:** `2.1`
- **Detect:** deterministic (`DEMO-ACCOUNT-MISSING`)
- **Note:** a demo account that requires SMS or an email code the reviewer
  cannot receive is the same rejection. Provide a bypass or a pre-verified
  account, and say so in the review notes.

---

## D. Purchases, subscriptions, paywalls

### P-12 Subscription terms not shown before purchase
- **Clause:** `3.1.2`, and specifically `3.1.2c`
- **Detect:** judgment — read the `Paywall` and `Subscriptions` metadata fields
  and the paywall component.
- **Required on the paywall screen itself, before the buy button:** title of the
  subscription, length of the period, price (and price per unit if relevant),
  what is included, and that it auto-renews until cancelled. Plus functional
  links to the Terms of Use (EULA) and Privacy Policy.
- **RN/Expo specifics:** RevenueCat's prebuilt paywall templates satisfy most of
  this; hand-rolled paywalls usually do not. A paywall that shows only
  `"$4.99"` with no period is the single most common 3.1.2 rejection.

### P-13 Free trial framing
- **Clause:** `3.1.2`
- **Detect:** judgment
- **What gets rejected:** the trial length or the post-trial price is not
  disclosed adjacent to the CTA; "Free" as the button label on a paid
  subscription; a trial that is really an introductory price described as free.

### P-14 No restore purchases
- **Clause:** `3.1.1`
- **Detect:** deterministic (`RESTORE-MISSING`)
- **Fix:** a visible control calling `Purchases.restorePurchases()` (RevenueCat)
  or `getAvailablePurchases()` (react-native-iap). It must be reachable without
  logging in if the app allows purchase without login.

### P-15 Paywall obscures price, or the dismiss control is hidden
- **Clause:** `3.1.2`, `4.2`
- **Detect:** judgment — check the paywall description for a close button.
- **Note:** a hard paywall (no dismiss) is allowed, but the app must then be
  clearly presented as paid and the reviewer needs a way in — which loops back
  to P-11.

### P-16 External purchase links / steering
- **Clause:** `3.1.1`, `3.1.3`
- **Detect:** judgment — grep for links to a web checkout, Stripe, Gumroad, or
  "manage your subscription on our website" inside the app.
- **Note:** this area changes frequently (US storefront entitlements, reader
  apps, link-out entitlements). Re-read `corpus/apple/asrg.sections/3.1.1.md`
  and `3.1.3.md` before asserting anything — do not answer from memory.

---

## E. Metadata and the store listing

### P-17 Placeholder or template text
- **Clause:** `2.3.1`
- **Detect:** deterministic (`META-PLACEHOLDER-*`)

### P-18 Metadata mentions other platforms or pricing
- **Clause:** `2.3.7`, `2.3.10`
- **Detect:** judgment — scan the description, What's New, and screenshot
  descriptions for "Android", "Google Play", "Web version", "$", "% off", or
  competitor names.

### P-19 Screenshots show features not in the build
- **Clause:** `2.3.3`
- **Detect:** judgment — compare `Screenshot descriptions` against the actual
  feature set implied by `dependencies` and the app's routes.
- **Very common in RN/Expo:** marketing screenshots generated before a feature
  was cut, or device frames showing an Android status bar on an iOS listing.

### P-20 Broken or placeholder URLs
- **Clause:** `5.1.1` (privacy policy), `2.3.8` (support URL)
- **Detect:** deterministic (`URL-DEAD-*`)
- **Note:** a privacy policy URL that 200s but returns a generic template with
  the app name missing is still a rejection; the deterministic check cannot see
  that, so read the page if it matters.

### P-21 Keyword stuffing or competitor names in keywords
- **Clause:** `2.3.7`
- **Detect:** judgment

### P-22 Age rating mismatch
- **Clause:** `asc:age-ratings`, plus `1.1` for the content itself
- **Detect:** judgment — compare the declared rating against the category and
  what the app does. Dating, user-generated content, and unmoderated chat all
  force a higher rating; UGC additionally requires filtering, reporting, and
  blocking under `1.2`.

---

## F. Build and submission hygiene

### P-23 Dev-client or Expo Go artifacts in the production build
- **Clause:** `2.2`
- **Detect:** deterministic (`EAS-DEVCLIENT`, `DEV-CLIENT-DEP`)

### P-24 Missing export compliance declaration
- **Clause:** `asc:export-compliance`
- **Detect:** deterministic (`EXPORT-COMPLIANCE`)
- **Note:** not a rejection so much as a submission blocker, but it stalls every
  upload until answered, and answering it wrong is a legal problem.

### P-25 Icon problems
- **Clause:** `asc:screenshot-specifications`
- **Detect:** deterministic (`ICON-ALPHA`, `ICON-SIZE`, `ICON-MISSING`)
- **Why RN/Expo trips this:** the Expo template icon is a PNG with alpha. It
  works fine in the simulator and is rejected at upload.

### P-26 Minimum functionality / web wrapper
- **Clause:** `4.2`
- **Detect:** judgment — a `react-native-webview` dependency that carries most
  of the app's routes, few native capabilities, and a thin feature set.
- **Note:** this is the highest-stakes judgment call in the whole scan. Be
  careful about asserting it; flag it as a risk with the reasoning, not as a
  certainty.

---

## G. Category-specific

### P-27 Health
- **Clause:** `1.4.1`, `5.1.3`
- Health data must not go to third-party advertising or analytics. HealthKit
  data specifically may not be used for advertising or sold. Apps that could
  cause physical harm through inaccuracy (dosage calculators, diagnosis) face a
  much higher bar and often need documentation from a recognised institution.

### P-28 Dating
- **Clause:** `1.1.4`, `1.2`, `4.3`
- Hookup framing draws `1.1.4`. UGC forces moderation, reporting, blocking, and
  a published means of contacting the developer. Dating apps are also a common
  `4.3` spam target because the category is saturated.

### P-29 Gambling / real money / loot boxes
- **Clause:** `5.3`
- Odds must be disclosed before purchase for loot boxes. Real-money gaming needs
  the correct entitlements, geo-restriction, and a licensed operator — an indie
  developer account will not clear this.

### P-30 Kids category
- **Clause:** `5.1.4`, `1.3`
- No third-party analytics or advertising, no external links without a parental
  gate, and a much stricter data posture. Most RN analytics SDKs are
  disqualifying by default here.

---

## H. Google Play specifics

### P-31 Data safety form does not match the manifest or SDKs
- **Clause:** `play:data-safety`, `play:user-data-policy`
- **Detect:** judgment — compare declared permissions and analytics SDKs against
  the `Data collected` metadata field.

### P-32 Missing prominent disclosure for a runtime permission
- **Clause:** `play:user-data-policy`
- **Detect:** deterministic (`PLAY-DISCLOSURE`), then judgment on whether the
  in-app disclosure actually exists and precedes the prompt.

### P-33 Sensitive permission without the declaration form
- **Clause:** `play:permissions-policy`
- **Detect:** deterministic (`PLAY-DECLARATION`)
- **RN/Expo specifics:** `QUERY_ALL_PACKAGES` gets merged in by some libraries
  without the developer ever asking for it. Check the merged manifest, not just
  `app.json`.

### P-34 Target API level below the current floor
- **Clause:** `play:target-api-level`
- **Detect:** deterministic (`TARGET-SDK`) — the floor rises annually, so read
  the current requirement and deadline out of
  `corpus/google/target-api-level.md` rather than hardcoding a number.

### P-35 Foreground service type without its permission or declaration
- **Clause:** `play:permissions-policy`
- **Detect:** deterministic (`FGS-PERM-*`)
- Android 14+ also requires a use-case justification in Play Console for most
  foreground service types.

### P-36 Closed-testing requirement for new personal developer accounts
- **Clause:** `play:testing-requirements`
- **Detect:** judgment — ask the developer whether the Play account is a
  personal account created after the policy took effect.
- **Why it matters commercially:** it is a hard gate measured in weeks, not a
  fix. Read the current tester count and duration out of
  `corpus/google/testing-requirements.md`; the numbers have changed at least
  once and must not be quoted from memory.

### P-37 Account deletion must also be reachable from the web
- **Clause:** `play:account-deletion-play`
- Play requires an in-app path *and* a web-accessible request URL supplied in
  the Play Console. Apple does not require the web route, so apps that shipped
  for iOS first usually miss this one.
