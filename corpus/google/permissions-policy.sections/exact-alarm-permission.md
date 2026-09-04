<!-- source=permissions-policy clause=exact-alarm-permission url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T15:48:35+00:00 -->

## Exact Alarm Permission

**Policy Summary**

`USE_EXACT_ALARM` permission on Android 13+ is a highly restricted permission used only for apps whose core, user-facing functionality genuinely requires precise timing, like dedicated alarm, timer, or calendar applications with event notifications. If your app does *not* have this specific core need, consider using ``SCHEDULE_EXACT_ALARM`` permission instead. It provides the same functionality but access must be granted by the user. This policy prevents misuse that impacts system resources. Please review the full policy to ensure compliance.

**Full Policy**

A new permission, ``USE_EXACT_ALARM``, will be introduced that will grant access to [exact alarm functionality](https://developer.android.com/about/versions/13/features#use-exact-alarm-permission) in apps starting with Android 13 (API target level 33).

``USE_EXACT_ALARM`` is a restricted permission and apps must only declare this permission if their core functionality supports the need for an exact alarm. Apps that request this restricted permission are subject to review, and those that do not meet the acceptable use case criteria will be disallowed from publishing on Google Play.

**Acceptable use cases for using the Exact Alarm Permission**

Your app must use the ``USE_EXACT_ALARM`` functionality only when your app’s core, user facing functionality requires precisely-timed actions, such as:

- The app is an alarm or timer app.
- The app is a calendar app that shows event notifications.

If you have a use case for exact alarm functionality that’s not covered above, you should evaluate if using ``SCHEDULE_EXACT_ALARM`` as an alternative is an option.

For more information on exact alarm functionality, please see this [developer guidance](https://developer.android.com/about/versions/13/features#use-exact-alarm-permission).

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Request the auto granted version of the permission, `USE_EXACT_ALARM`, only if your app's core functionality is of alarm or calendar. | Don't use this permission for non-critical features that do not directly contribute to the app's main purpose. |
| Use `SCHEDULE_EXACT_ALARM` instead if the above criteria is not met. |  |
| Complete Play Console [declaration](https://goo.gle/play-permission-decl-form) to indicate app functionality. |  |
| Review the [new permission to use exact alarms](https://developer.android.com/about/versions/13/features#use-exact-alarm-permission) for more information on exact alarm functionality. |  |

---
