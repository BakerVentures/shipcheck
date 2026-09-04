<!-- source=prepare-and-roll-out-a-release clause=step-2-prepare-your-app-s-release url=https://support.google.com/googleplay/android-developer/answer/9859348 fetched=2026-09-04T07:14:09+00:00 -->

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
