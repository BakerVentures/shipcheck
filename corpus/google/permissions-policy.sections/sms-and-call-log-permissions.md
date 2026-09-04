<!-- source=permissions-policy clause=sms-and-call-log-permissions url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T16:10:09+00:00 -->

## SMS and Call Log Permissions

**Policy Summary**

Google Play imposes strict restrictions on accessing highly sensitive SMS and Call Log data. Your app must be the designated default handler for SMS, Phone, or Assistant to request these permissions. Usage is limited *only* to documented core app functionality that is absolutely essential for your app's primary purpose. This data must never be used for advertising or any other unapproved purpose. Please review the full policy to ensure compliance.

**Full Policy**

SMS and Call Log Permissions are regarded as personal and sensitive user data subject to the [Personal and Sensitive Information](/googleplay/android-developer/answer/9888076#personal_sensitive) policy, and the following restrictions:

| Restricted Permission | Requirement |
| --- | --- |
| Call Log permission group (for example, `READ_CALL_LOG`, `WRITE_CALL_LOG`, `PROCESS_OUTGOING_CALLS`) | It must be actively registered as the default Phone or Assistant handler on the device. |
| SMS permission group (for example, `READ_SMS`, `SEND_SMS`, `WRITE_SMS`, `RECEIVE_SMS`, `RECEIVE_WAP_PUSH`, `RECEIVE_MMS`) | It must be actively registered as the default SMS or Assistant handler on the device. |

Apps lacking default SMS, Phone, or Assistant handler capability may not declare use of the above permissions in the manifest. This includes placeholder text in the manifest. Additionally, apps must be actively registered as the default SMS, Phone, or Assistant handler before prompting users to accept any of the above permissions and must immediately stop using the permission when they’re no longer the default handler. The permitted uses and exceptions are available on [this Help Center page](https://support.google.com/googleplay/android-developer/answer/9047303).

Apps may only use the permission (and any data derived from the permission) to provide approved core app functionality Core functionality is defined as the main purpose of the app. This may include a set of core features, which must all be prominently documented and promoted in the app’s description. Without the core feature(s), the app is “broken” or rendered unusable. The transfer, sharing, or licensed use of this data must only be for providing core features or services within the app, and its use may not be extended for any other purpose (for example, improving other apps or services, advertising, or marketing purposes). You may not use alternative methods (including other permissions, APIs, or third-party sources) to derive data attributed to Call Log or SMS related permissions.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Submit a [declaration form](https://goo.gle/play-permission-decl-form) in your Play Console. | Don't request SMS/Call Log permissions without a core need justification. |
| Clearly document the core functionality requiring access to your users. | Don't use this data for advertising or other purposes. |
| Use policy-compliant alternatives like the [SMS Retriever API](https://developers.google.com/identity/sms-retriever/overview) where possible. | Don't store or share unnecessary SMS or Call Log data. |
| Stop accessing data immediately upon losing default handler status. | Don't attempt to derive this data using alternative methods. |
| Review the [permitted uses and exceptions](https://support.google.com/googleplay/android-developer/answer/10208820) of the SMS and Call log permissions. |  |

---
