---
shipcheck_source_id: prepare-and-roll-out-a-release
title: "Prepare and roll out a release"
url: https://support.google.com/googleplay/android-developer/answer/9859348
final_url: https://support.google.com/googleplay/android-developer/answer/9859348?hl=en
fetched_at: 2026-09-05T02:02:35+00:00
sha256: 3e0303cf06a9d2731f1e1775e0de18b3d80614fad58bc386aac1c674ff48908f
vendor: google
note: "Listed in the brief as 'Developer Program Policies' but this ID is actually release rollout. Kept for testing-track rules; policy text is under policy-center-hub."
---

# Prepare and roll out a release

Releases allow Android developers to manage [Android App Bundles](https://developer.android.com/guide/app-bundle/) (or APKs for apps created before August 2021) and roll out updates to specific testing tracks or production on Google Play. This guide helps developers create, prepare, and launch app versions. Before you begin, ensure you have set up your app's [store listing](https://support.google.com/googleplay/android-developer/answer/9859152#store_listing), [prepared your app for review](https://support.google.com/googleplay/android-developer/answer/9859455), and [configured app pricing](https://support.google.com/googleplay/android-developer/answer/6334373).

## Step 1: Create a release

A release is a combination of one or more app versions that you prepare to launch an app or roll out an app update. You can create a release across three testing tracks or in production:

- **Open testing:** Open testing releases are available to testers on Google Play. Users can join tests directly from your store listing.
- **Closed testing:** Closed testing releases are available to a limited number of chosen testers who test a pre-release version of your app and submit feedback.
- **Internal testing:** Internal testing releases are available to up to 100 chosen testers.
- **Production:** Production releases are available to all Google Play users in your chosen countries and regions.

To create a release, keep the following requirements in mind:

- You must have the [Release apps to testing tracks](https://support.google.com/googleplay/android-developer/answer/9844686#release_testing) account permission to create a new release.
- Developers with personal accounts created after November 13, 2023, must meet specific testing requirements before making their app available on Google Play. To learn more, read about [personal account testing requirements](https://support.google.com/googleplay/android-developer/answer/14151465).
- You cannot create a new release when you have outstanding releases. Roll out any staged releases to 100%, or remove changes on the [**Publishing overview**](https://play.google.com/console/developers/app/publishing) page and discard any unpublished releases first.

To start your release, follow these steps:

1. Sign in to Play Console, select your app, and go to the track where you want to start your release:
  [**Open testing**](https://play.google.com/console/developers/app/tracks/open-testing)(**Test and release > Testing > Open testing**)
  [**Closed testing**](https://play.google.com/console/developers/app/closed-testing)(**Test and release > Testing > Closed testing**)
  **Note:** To create a release on an existing closed testing track, click **Manage track**. To create a new track, click **Create track**.
  [**Internal testing**](https://play.google.com/console/developers/app/tracks/internal-testing)(**Test and release > Testing > Internal testing**)
  [**Production**](https://play.google.com/console/developers/app/tracks/production) (**Test and release > Production**)
2. Near the top right of the page, click **Create new release**.

To edit an existing release, go to the corresponding release page and click **Edit release**.

**Tip:** For more information on testing options, see [Set up an open, closed, or internal test](https://support.google.com/googleplay/android-developer/answer/9845334).

## Step 2: Prepare your app's release

To prepare your release, follow these steps:

1. Follow the on-screen instructions to prepare your release:
  If this is your first release for this app, follow the instructions to [configure Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756).
  Add your app bundles. Legacy apps (created before August 2021) can add app bundles or APKs for app updates.
  **Optional:** If you are creating a release for the first time, you can change your app signing key. In the 'App integrity' section, click **Change app signing key**. Before changing your key, understand that:
  - Internal and closed track users who already installed your app will no longer receive updates. These users must uninstall and reinstall the app to receive updates.
  - You cannot use previously uploaded app versions. You must re-upload app versions.
  **Optional:** To add the Play Games Sidekick to your app bundle, click **Add Play Games Sidekick** to new app bundles you upload**.**
  - To upload an app bundle for your game, click **Upload**.
  - To use a previously uploaded app version, click **Add from library**.
  Name your release.
  Enter your localized release notes.
  - For more information on any of these data fields, select the matching section heading in the following section.
2. To save changes to your release, click **Save as draft**.
3. When you finish preparing your release, click **Next**.

**Note:** Once you publish an app to an open track, its signing key is fixed.

#### Configure release options

Review the following section details when configuring your release settings:

App bundle enhancements

In this section, you can manage and configure various app bundle enhancements, including [Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756), [Automatic protection](https://support.google.com/googleplay/android-developer/answer/10183279), and [Play Games Sidekick](https://developer.android.com/games/pgs/play-games-sidekick).

App bundles

Upload new app bundles or add them from your library. Click **More** to perform the following actions:

- Upload a ReTrace mapping file (.txt)
- Upload native debug symbols (.zip)
- Upload an expansion file (.obb)
- Remove an app bundle

**Note:** Legacy apps (created before August 2021) can use app bundles or APKs in releases.

To learn more about ReTrace mapping files and native debug symbols, see [Deobfuscate or symbolicate crash stack traces](https://support.google.com/googleplay/android-developer/answer/9848633).

Included

View details about app bundles from your previous release that will be included in this release.

To remove the app bundle from the current release, click **Remove**. You can find the app bundle or APK again in **[All app bundles](https://play.google.com/console/developers/app/bundle-explorer-selector)**.

Not included

View details about app bundles from your previous release that will not be included in this release.

To add the excluded app bundle back to this release, click **Include**.

Declare permissions for your app (optional)

Permission requests are evaluated during the release process after adding your app bundles or APKs. If your app requests [high-risk or sensitive permissions](https://support.google.com/googleplay/android-developer/answer/16558241) (for example, SMS or Call Log), you might need to [complete the Permissions Declaration Form](https://support.google.com/googleplay/android-developer/answer/9214102) and receive approval from Google Play.

Release name

The release name is used only in Play Console and is not visible to users.

Play Console auto-populates this field with the version name of the first app bundle or APK added to the release.

To make your release easier to identify, add a meaningful release name, such as the build version ("3.2.5-RC2") or an internal code name ("Banana").

What's new in this release?

#### **Overview**

Inform users about recent updates made in your release. Do not use release notes for promotional purposes or to solicit user actions.

#### **Add release notes and manage translations**

Add descriptions for your release between the relevant language tags. Language tags appear in the text box for each language your app supports.

To change your app's supported languages, you must first [add translations](https://support.google.com/googleplay/android-developer/answer/9844778). When you return to the **Prepare release** page, the latest set of languages appears.

Place language tags on separate lines from release notes using the following format:

<en-US>

The release notes description can take up multiple lines.

</en-US>

**Note:** You can enter release notes using up to 500 Unicode characters per language.

#### **Copy from previous release**

To copy release notes from a previous release, click **Copy from a previous release**. Selecting a release copies the release notes and translations into the text box for editing, replacing existing entries.

## Step 3: Review and roll out your release

When preparing your release, options to **Save** or **Publish** appear depending on whether your changes require review. Clicking **Publish** pushes changes live immediately. Clicking **Save** adds your changes to the 'Changes ready to send for review' section on the **Publishing overview** page, where you can decide when to submit them. Learn more about [managing when changes go live](https://support.google.com/googleplay/android-developer/answer/9859654).

To roll out your app, follow these steps:

1. Sign in to Play Console, select your app, and go to the appropriate track ([**Open testing**](https://play.google.com/console/developers/app/tracks/open-testing)or [**Closed testing**](https://play.google.com/console/developers/app/closed-testing)).
2. Select the **Releases** tab, then click **Edit** under the release you want to roll out.
3. Review your draft release, make any necessary changes, and click **Next** to proceed to the **Preview and confirm** screen.
4. If you see 'Errors summary' at the top of the page, click **Show more** to review details and resolve any problems.
5. If updating an existing app, select a rollout percentage.
  Rollout percentage options are unavailable for a first release.
  For details on targeting staged rollouts to specific countries or regions, see [Release app updates with staged rollouts](https://support.google.com/googleplay/android-developer/answer/6346149#staged_country).
6. Click **Start rollout**.
  If rolling out a first production release, clicking **Start rollout to production** publishes your app to all Google Play users in your selected [countries or regions](https://support.google.com/googleplay/android-developer/answer/7550024).

## Step 4: Review release details

After creating a release, view release information under 'Latest releases' on the **Latest releases and bundles** page (**Test and release > Latest releases and bundles**).

- **Release:** Name identifying the release in Play Console, such as an internal code name or build version.
- **Track:** The track where the release was rolled out.
- **Release status:** The current status of your release.
- **Last updated:** Date and timestamp of the last rollout event.
- **Countries/regions:** The number of targeted countries and regions. After rolling out to production, open testing, or closed testing, you can target specific countries. For details, read about [distributing app releases to specific countries](https://support.google.com/googleplay/android-developer/answer/7550024).

Click the right arrow to open the **Release details** page for deeper insights:

- **Release overview:** Metrics for installs, updates, performance issues, and ratings compared to previous releases.
- **App bundles and APKs:** A list of new, retained, and deactivated app bundles and APKs associated with your release.
- **Release notes:** A list of previous release notes.
- **Rollout history:** Timeline displaying timestamps when releases were halted, resumed, or served to new user percentages.

## Optional: Discard a release

To discard a release during setup, use the procedure corresponding to your release state:

- **Draft:** Click **Discard draft release** near the top right of the page. This action removes changes made in the release.
- **Ready to send for review:** Click **Discard release** on the release summary. Your release is removed from the [**Publishing overview**](https://play.google.com/console/developers/app/publishing) page and excluded from review submissions.
- **In review** or **Ready to publish:** Remove changes from the **Publishing overview** page first. Once removed, click **Discard release** on the release summary.
- **Rejected:** Click **Discard release** on the rejected release summary.

**Note:** You can only discard the latest release on a track, including draft releases and recently rejected releases.

## Track releases on the Latest releases and bundles page

If you roll out multiple releases, your app's [**Latest releases and bundles**](https://play.google.com/console/developers/app/releases/overview) page (**Test and release > Latest releases and bundles**) helps you monitor releases in one location. Use this page to monitor app availability across tracks, view country and region availability, and select individual releases to view details.

## Manage app changes on the Publishing overview page

Use the **[Publishing overview](https://play.google.com/console/developers/app/publishing)** page to control when changes are sent for review and published. To learn more, read about [managing when changes go live](https://support.google.com/googleplay/android-developer/answer/9859654).

## Related content

- Learn more about managing country availability across production, open, and closed releases in [Distribute app releases to specific countries](https://support.google.com/googleplay/android-developer/answer/7550024).
- Learn more about testing options in [Set up an open, closed, or internal test](https://support.google.com/googleplay/android-developer/answer/9845334).
- Learn about releasing updates progressively with staged rollouts in the [training modules found within the Academy for App Success](https://playacademy.exceedlms.com/student/collection/260728-prepare).

## Was this helpful?

How can we improve it?
