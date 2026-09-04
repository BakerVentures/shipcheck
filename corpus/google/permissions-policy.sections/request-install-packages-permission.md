<!-- source=permissions-policy clause=request-install-packages-permission url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T16:10:09+00:00 -->

## Request Install Packages Permission

**Policy Summary**

`REQUEST_INSTALL_PACKAGES` permission allows apps to request the installation of other app packages. This permission is restricted to the app's core functionality, specifically when the primary purpose directly involves sending, receiving, or enabling user-initiated installation of app packages. Using this permission to update your app, change its functionality or bundle other APKs for silent or unauthorized installation (except enterprise management) is prohibited. All installations must be a direct, active choice by the user. Apps targeting Android 8+ must hold this permission in order to use `Intent.ACTION_INSTALL_PACKAGE`. Please review the full policy to ensure compliance.

**Full Policy**

The [``REQUEST_INSTALL_PACKAGES``](https://developer.android.com/reference/android/Manifest.permission#<code>REQUEST_INSTALL_PACKAGES</code>) permission allows an application to request the installation of app packages. To use this permission, your app’s core functionality must include:

- Sending or receiving app packages; and
- Enabling user-initiated installation of app packages.

Permitted functionalities include:

- Web browsing or search
- Communication services that support attachments
- File sharing, transfer, or management
- Enterprise device management
- Backup and restore
- Device Migration/Phone Transfer
- Companion app to sync phone to wearable or IoT device (for example, smart watch or smart TV)

Core functionality is defined as the main purpose of the app. The core functionality, as well as any core features that comprise this core functionality, must all be prominently documented and promoted in the app's description.

The ``REQUEST_INSTALL_PACKAGES`` permission may not be used to perform self updates, modifications, or the bundling of other APKs in the asset file unless for device management purposes. All updates or installing of packages must abide by Google Play’s [Device and Network Abuse policy](https://support.google.com/googleplay/android-developer/answer/9888379?hl=en&ref_topic=9877467) and must be initiated and driven by the user.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Clearly and prominently document the core functionality requiring this permission in your app’s Google Play description and when you submit a [declaration form](https://goo.gle/play-permission-decl-form) in your Play Console. | Don't request this permission for a functionality that is not directly related to the primary purpose of your app. This includes Peer-to-Peer (P2P) sharing. P2P must be the primary purpose of the app in order to qualify as a permitted use. |
| Adhere strictly to the permitted functionalities including web browsing/search, file sharing / transfer / management, enterprise device management, backup/restore, device migration / phone transfer, companion app to sync phone to wearable or IoT device. | Don't request this permission when the required task can be done with a less intrusive method. |
| Ensure your app prevents background or unintended installations. All app package installations must be explicitly initiated by the user. | Don't change how your app uses this permission without first revising your Play Console declaration with updated and accurate information. Deceptive and undeclared uses of this permission are prohibited. |

---
