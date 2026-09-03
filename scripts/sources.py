"""ShipCheck corpus source registry.

Every entry is an official Apple/Google/Expo page. `strategy` selects the
extractor in fetch_corpus.py, because several of these pages cannot be read
with a naive HTTP GET:

  apple_html    plain server-rendered developer.apple.com page
  apple_docc    developer.apple.com/documentation/* and /design/* are a JS SPA.
                A bare GET returns ~50 chars of shell. The content is served as
                structured JSON at https://developer.apple.com/tutorials/data/<path>.json
  google_help   support.google.com article (server-rendered)
  android_dev   developer.android.com. Requires a cookie jar AND ?hl=en, otherwise
                it 302s into an infinite accounts.google.com OAuth loop.
  generic       docs.expo.dev and other well-behaved pages
  index_only    JS-rendered; we can only recover the section index, not policy text

`substituted_from` records a URL that was dead or moved, per the Phase 0 audit.
"""

SOURCES = [
    # ---------------------------------------------------------------- APPLE
    dict(id="asrg", vendor="apple", strategy="apple_html", primary=True,
         title="App Store Review Guidelines",
         url="https://developer.apple.com/app-store/review/guidelines/",
         chunk="apple_numbered",
         note="Primary citation source. Chunked by clause number (1.1, 2.3.1, 3.1.2...)."),

    dict(id="app-review-overview", vendor="apple", strategy="apple_html",
         title="App Review (overview and common rejections)",
         url="https://developer.apple.com/distribute/app-review/",
         substituted_from="https://developer.apple.com/app-store/review/",
         note="Original URL is a meta-refresh stub that redirects here."),

    dict(id="privacy-manifest-files", vendor="apple", strategy="apple_docc",
         title="Privacy manifest files",
         url="https://developer.apple.com/documentation/bundleresources/privacy-manifest-files",
         docc="documentation/bundleresources/privacy-manifest-files"),

    dict(id="required-reason-api", vendor="apple", strategy="apple_docc",
         title="Describing use of required reason API",
         url="https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api",
         docc="documentation/bundleresources/describing-use-of-required-reason-api",
         substituted_from="https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api",
         note="Apple moved this from underscore to hyphen slugs."),

    dict(id="tn3183", vendor="apple", strategy="apple_docc",
         title="TN3183: Adding required reason API entries to your privacy manifest",
         url="https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest",
         docc="documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest"),

    dict(id="required-reason-codes", vendor="apple", strategy="apple_docc", primary=True,
         title="NSPrivacyAccessedAPITypeReasons (approved reason codes)",
         url="https://developer.apple.com/documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitypereasons",
         docc="documentation/bundleresources/app-privacy-configuration/nsprivacyaccessedapitypes/nsprivacyaccessedapitypereasons",
         note="Carries the actual approved reason codes (C617.1, CA92.1, E174.1, 35F9.1, "
              "3EC4.1 ...). Without this the checker cannot tell a developer which "
              "value to put in NSPrivacyAccessedAPITypeReasons."),

    dict(id="describing-data-use", vendor="apple", strategy="apple_docc",
         title="Describing data use in privacy manifests",
         url="https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests",
         docc="documentation/bundleresources/describing-data-use-in-privacy-manifests",
         note="NSPrivacyCollectedDataTypes vocabulary, which must line up with the "
              "App Privacy nutrition labels."),

    dict(id="third-party-sdk-requirements", vendor="apple", strategy="apple_html",
         title="Third-party SDK requirements",
         url="https://developer.apple.com/support/third-party-SDK-requirements/",
         note="Authoritative list of SDKs that must ship a privacy manifest and signature."),

    dict(id="app-privacy-details", vendor="apple", strategy="apple_html",
         title="App privacy details on the App Store (nutrition labels)",
         url="https://developer.apple.com/app-store/app-privacy-details/"),

    dict(id="user-privacy-and-data-use", vendor="apple", strategy="apple_html",
         title="User privacy and data use (App Tracking Transparency)",
         url="https://developer.apple.com/app-store/user-privacy-and-data-use/"),

    dict(id="subscriptions", vendor="apple", strategy="apple_html",
         title="Auto-renewable subscriptions",
         url="https://developer.apple.com/app-store/subscriptions/"),

    dict(id="hig-in-app-purchase", vendor="apple", strategy="apple_docc",
         title="HIG: In-app purchase",
         url="https://developer.apple.com/design/human-interface-guidelines/in-app-purchase",
         docc="design/human-interface-guidelines/in-app-purchase"),

    dict(id="hig-sign-in-with-apple", vendor="apple", strategy="apple_docc",
         title="HIG: Sign in with Apple",
         url="https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple",
         docc="design/human-interface-guidelines/sign-in-with-apple"),

    dict(id="product-page", vendor="apple", strategy="apple_html",
         title="App Store product page",
         url="https://developer.apple.com/app-store/product-page/"),

    dict(id="screenshot-specifications", vendor="apple", strategy="apple_html",
         title="Screenshot specifications",
         url="https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications",
         substituted_from="https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications",
         note="Moved under /reference/app-information/."),

    dict(id="age-ratings", vendor="apple", strategy="apple_html",
         title="Age ratings values and definitions",
         url="https://developer.apple.com/help/app-store-connect/reference/age-ratings",
         substituted_from="https://developer.apple.com/help/app-store-connect/reference/age-ratings-definitions",
         note="Original 404s. Apple restructured age ratings (13+/16+/18+ tiers)."),

    dict(id="set-age-rating", vendor="apple", strategy="apple_html",
         title="Set an app age rating",
         url="https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating",
         note="Added alongside age-ratings: covers the questionnaire that drives mismatches."),

    dict(id="export-compliance", vendor="apple", strategy="apple_html",
         title="Overview of export compliance",
         url="https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance"),

    dict(id="submit-for-review", vendor="apple", strategy="apple_html",
         title="Overview of submitting for review",
         url="https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review",
         substituted_from="https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-for-review"),

    dict(id="account-deletion", vendor="apple", strategy="apple_html",
         title="Offering account deletion in your app",
         url="https://developer.apple.com/support/offering-account-deletion-in-your-app/"),

    dict(id="expo-apple-privacy", vendor="apple", strategy="generic",
         title="Expo: Apple privacy manifests",
         url="https://docs.expo.dev/guides/apple-privacy/"),

    dict(id="expo-submit-ios", vendor="apple", strategy="generic",
         title="Expo: Submit to the App Store",
         url="https://docs.expo.dev/submit/ios/"),

    # --------------------------------------------------------------- GOOGLE
    dict(id="policy-center-index", vendor="google", strategy="index_only",
         title="Google Play Developer Policy Center (section index)",
         url="https://play.google/developer-content-policy/",
         note="JS SPA. Section routes are not server-rendered, so only the "
              "table of contents is recoverable. Policy text comes from the "
              "support.google.com pages below."),

    dict(id="policy-center-hub", vendor="google", strategy="google_help", primary=True,
         title="Play Console Help: Policy Center hub",
         url="https://support.google.com/googleplay/android-developer/topic/9858052",
         note="Added in Phase 0: navigable, server-rendered index of the "
              "Developer Program Policies."),

    dict(id="prepare-and-roll-out-a-release", vendor="google", strategy="google_help",
         title="Prepare and roll out a release",
         url="https://support.google.com/googleplay/android-developer/answer/9859348",
         note="Listed in the brief as 'Developer Program Policies' but this ID is "
              "actually release rollout. Kept for testing-track rules; policy text "
              "is under policy-center-hub."),

    dict(id="data-safety", vendor="google", strategy="google_help", primary=True,
         title="Provide information for Google Play's Data safety section",
         url="https://support.google.com/googleplay/android-developer/answer/10787469"),

    dict(id="user-data-policy", vendor="google", strategy="google_help", primary=True,
         title="User Data policy",
         url="https://support.google.com/googleplay/android-developer/answer/10144311",
         substituted_from="https://support.google.com/googleplay/android-developer/answer/16810878",
         note="Original answer ID is dead (bounces to support.google.com root)."),

    dict(id="target-api-level", vendor="google", strategy="google_help",
         title="Meet Google Play's target API level requirement",
         url="https://support.google.com/googleplay/android-developer/answer/11926878"),

    dict(id="subscriptions-policy", vendor="google", strategy="google_help",
         title="Play subscriptions policy",
         url="https://support.google.com/googleplay/android-developer/answer/10281818"),

    dict(id="payments-policy", vendor="google", strategy="google_help",
         title="Payments policy / Play Billing",
         url="https://support.google.com/googleplay/android-developer/answer/9858738"),

    dict(id="account-deletion-play", vendor="google", strategy="google_help",
         title="App account deletion requirements",
         url="https://support.google.com/googleplay/android-developer/answer/13327111"),

    dict(id="testing-requirements", vendor="google", strategy="google_help",
         title="App testing requirements for new personal developer accounts",
         url="https://support.google.com/googleplay/android-developer/answer/14151465",
         note="The 12-tester / 14-day closed-testing gate for new personal accounts."),

    dict(id="permissions-policy", vendor="google", strategy="google_help", primary=True,
         title="Permissions and APIs that Access Sensitive Information",
         url="https://support.google.com/googleplay/android-developer/answer/16558241",
         substituted_from="https://support.google.com/googleplay/android-developer/answer/9888170",
         note="Google redirected the old permissions answer ID here."),

    dict(id="prepare-for-release", vendor="google", strategy="android_dev",
         title="Prepare your app for release",
         url="https://developer.android.com/studio/publish/preparing",
         substituted_from="https://developer.android.com/distribute/best-practices/launch/launch-checklist",
         note="The launch-checklist page is retired; it 302s to a Play Console stub."),

    dict(id="publish-your-app", vendor="google", strategy="android_dev",
         title="Publish your app",
         url="https://developer.android.com/studio/publish"),

    dict(id="target-sdk", vendor="google", strategy="android_dev",
         title="Meet Google Play's target API level requirement (Android Developers)",
         url="https://developer.android.com/google/play/requirements/target-sdk"),

    dict(id="expo-submit-android", vendor="google", strategy="generic",
         title="Expo: Submit to Google Play",
         url="https://docs.expo.dev/submit/android/"),
]


def by_id(sid):
    for s in SOURCES:
        if s["id"] == sid:
            return s
    return None
