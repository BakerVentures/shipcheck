<!-- source=permissions-policy clause=full-screen-intent-permission url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-05T02:02:40+00:00 -->

## Full-Screen Intent Permission

**Policy Summary**

On Android 14+, the ``USE_FULL_SCREEN_INTENT`` permission is auto-granted *only* for apps whose core function is setting alarms or handling calls. For any other use case, you must obtain explicit user consent and clearly explain your need. This policy prevents the misuse of full-screen intents for non-critical purposes and requires that your use does not interfere with or disrupt the user's device, other apps, or overall usability. Please review the full policy to ensure compliance.

**Full Policy**

For apps targeting Android 14 (API target level 34) and above, [``USE_FULL_SCREEN_INTENT``](https://developer.android.com/reference/android/app/Notification.Builder#setFullScreenIntent(android.app.PendingIntent,%20boolean)) is a [special apps access permission](https://developer.android.com/training/permissions/requesting-special). Apps will only be automatically granted to use the ``USE_FULL_SCREEN_INTENT`` permission if the core functionality of their app falls under one of the below categories that require high priority notifications:

- setting an alarm
- receiving phone or video calls

Apps that request this permission are subject to review, and those that do not meet the above criteria will not be automatically granted this permission. In that case, apps must request permission from the user to use ``USE_FULL_SCREEN_INTENT``.

As a reminder, any usage of the ``USE_FULL_SCREEN_INTENT`` permission must comply with all [Google Play Developer Policies](https://play.google.com/about/developer-content-policy/?authuser=0#!?modal_active=none), including our [Mobile Unwanted Software](https://support.google.com/googleplay/android-developer/answer/9970222), [Device and Network Abuse](https://support.google.com/googleplay/android-developer/answer/9888379?hl=en), and [Ads](https://support.google.com/googleplay/android-developer/answer/9857753?hl=en&sjid=11744761627827448774-NA) policies. Full-screen intent notifications cannot interfere with, disrupt, damage, or access the user’s device in an unauthorized manner. Additionally, apps should not interfere with other apps or the usability of the device.

Learn more about the ``USE_FULL_SCREEN_INTENT`` permission in our [Help Center](https://support.google.com/googleplay/android-developer/answer/13392821#full_screen_intent).

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Request user consent for the permission and provide a clear explanation for the request if not auto-granted. | Don't use this permission for non-core or low-priority features. |
| Limit use to necessary high-priority notifications/alerts. | Don't use this permission to interfere with devices or other apps. |
| Submit a [declaration form](https://goo.gle/play-permission-decl-form) in your Play Console to establish pre-grant eligibility for the full-screen intent permission if targeting Android 14+ | Don't use this permission for disruptive ads or disruptive notifications. |
| Learn more about the [``USE_FULL_SCREEN_INTENT`` permission](https://support.google.com/googleplay/android-developer/answer/13392821?sjid=7274498547371890152-NC#full_screen_intent) and its requirements. |  |

---
