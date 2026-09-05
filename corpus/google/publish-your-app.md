---
shipcheck_source_id: publish-your-app
title: "Publish your app"
url: https://developer.android.com/studio/publish
final_url: https://developer.android.com/studio/publish?hl=en
fetched_at: 2026-09-05T02:02:43+00:00
sha256: 9c61acb6fa71afd7d342465f37209acfd43fe96802482f486500bd7ef66395db
vendor: google
---

# Publish your app

Publishing is the general process that makes your Android app available to users. When you
publish an Android app, you do the following:

- **Prepare the app for release.** During the preparation step, you build a release version of your app.
- **Release the app to users.** During the release step, you publicize, sell, and distribute the release version of your

This page provides an overview of the process for preparing to publish
your app. If you plan to publish on Google Play, read
[Release with confidence](/distribute/best-practices/launch/launch-checklist).

If you use a Continuous Integration server, you can configure it to automate the steps outlined
here. You can also configure it to push builds to your
[internal test distribution channel](/studio/publish/upload-bundle#test_with_play).

Prepare your app for release Preparing your app for release is a multistep process involving the following
tasks: You might need to perform several other tasks as part of the preparation process. For example,
you need to create an account on the app marketplace you want to use, if you don't already have
one. You also need to create an icon for your app, and you might want to prepare
an End User License Agreement (EULA) to protect yourself, your organization, and your intellectual
property. To learn how to prepare your app for release, see [Prepare for release](/tools/publishing/preparing) for step-by-step instructions for
configuring and building a release version of your app. When you are finished preparing your app for release, you have a signed
APK file that you can distribute to users. Release your app to users You can release your Android apps several ways. Typically, you release apps
through an app marketplace such as [Google Play](https://play.google.com). You can also
release apps on your own website or by sending an app directly to a user.

Release through an app marketplace If you want to distribute your apps to the broadest possible audience, release them through
an app marketplace. Google Play is the premier marketplace for Android apps and is particularly
useful if you want to distribute your apps to a large global audience.
However, you can distribute your apps through any app marketplace, and
you can use multiple marketplaces. Release your apps on Google Play [Google Play](https://play.google.com) is a robust publishing platform that helps you
publicize, sell, and distribute your Android apps to users around the world. When you
release your apps through Google Play, you have access to a suite of developer tools that let
you analyze your sales, identify market trends, and control who your apps are being
distributed to. Google Play also gives you access to several revenue-enhancing features such as
[in-app billing](/google/play/billing) and
[app licensing](/google/play/licensing). The rich array of tools
and features, coupled with numerous end-user community features, makes Google Play the premier
marketplace for selling and buying Android apps. [Releasing your app on Google Play](/distribute/googleplay) is a
simple process that involves three basic steps: For more information, see [How Google Play works](/distribute/googleplay). Release through a website If you don't want to release your app on a marketplace like Google Play, you
can make the app available for download on your own website or server, including
on a private or enterprise server. To release through a website: When users browse to the download link from their Android-powered devices,
the file is downloaded and the Android system automatically starts installing it on
the device.

**Note:** The installation process will start automatically only if
the user has configured their settings to allow the installation of apps from
unknown sources. Although it is relatively easy to release your app on your own
website, it can be inefficient. For example, if you want to monetize your
app, you need to process and track all financial transactions
yourself, and you can't use Google Play's [in-app billing service](/google/play/billing)
to sell in-app products. You also can't use [app licensing](/google/play/licensing) to
help prevent unauthorized installation and use of your app. User opt-in for unknown apps and sources Android protects users from inadvertent download and installation of apps from
locations other than a trusted, first-party app store, such as Google Play.
Android blocks such installs until the user opts into allowing the
installation of apps from other sources. The opt-in process depends on the
version of Android running on the user's device: ![Screenshot showing the settings screen for accepting install of
unknown apps from different sources.](/static/images/publishing/publishing_unknown_apps_sm.png) **Figure 1.** The **Install unknown apps** system settings screen,
where users grant permission for a particular source to install unknown
apps.
Install unknown apps On devices running Android 8.0 (API level 26) and higher, users must grant
permission to install apps from a source that isn't a first-party app store. To
do so, they must enable the **Allow app installs** setting for that
source within the **Install unknown apps** system settings screen, shown in figure 1. **Note:** Users can change this setting for a particular
source at any time. Therefore, a source that installs unknown apps should always
call `[canRequestPackageInstalls()](/reference/android/content/pm/PackageManager#canRequestPackageInstalls())` to check whether the user has granted that source
permission to install unknown apps. If this method returns `false`,
the source should prompt the user to re-enable the **Allow app installs**
setting for that source. Unknown sources ![Screenshot showing the setting for accepting download and install of
apps from unknown sources.](/static/images/publishing/publishing_unknown_sources_sm.png) **Figure 2.** The **Unknown sources** setting
determines whether users can install apps that aren't downloaded
from Google Play.
To permit the installation of apps from non-first-party
sources on devices running Android 7.1.1 (API level 25) and lower, users
enable the **Unknown sources** setting in
**Settings > Security**, as shown in Figure 2. When users attempt to install an unknown app on a
device running Android 7.1.1 (API level 25) or lower, the system sometimes
shows a dialog that asks the user whether they want to allow only one
particular unknown app to be installed. In most cases, it is recommended that users allow
only one unknown app installation at a time, if the option is available. In either case, users need to make this configuration change before
they can download and install unknown apps onto their devices. **Note:** Some network providers don't let users
install apps from unknown sources.

Content and code samples on this page are subject to the licenses described in the [Content License](/license). Java and OpenJDK are trademarks or registered trademarks of Oracle and/or its affiliates.

Last updated 2023-11-15 UTC.
