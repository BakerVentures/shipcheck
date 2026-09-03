<!-- source=permissions-policy clause=body-sensor-permissions url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-03T19:54:39+00:00 -->

## Body Sensor Permissions

**Policy Summary**

To safeguard user privacy, Google Play mandates that access to highly sensitive body sensor data (such as heart rate, SpO2, and skin temperature) is subject to our [User Data](https://support.google.com/googleplay/android-developer/answer/10144311) policy and [Health apps](https://support.google.com/googleplay/android-developer/answer/12261419#health_apps) policy.

Starting with Android 16, apps must migrate from the general `android.permission.BODY_SENSORS` permission to new, granular health permissions. For example, you will use `android.permission.health.READ_HEART_RATE` to access heart rate data. This change affects all apps that target Android 16 or higher across all form factors, including Wear OS. For a complete list of changes, see [Behavior changes: Apps targeting Android 16 or higher](https://developer.android.com/about/versions/16/behavior-changes-16) page. We review all requests for body sensor permissions—both legacy and new—to ensure your app's use case directly benefits the user and strictly complies with our policies.

**Full Policy**

Access to data from sensors that measure physical parameters of the body (such as heart rate, SpO₂, and skin temperature) is considered personal and sensitive user data**.**Apps requesting access are subject to the requirements outlined in the [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?#personal-sensitive) and the [Health apps policy](https://support.google.com/googleplay/android-developer/answer/12261419?hl=en#:~:text=laws%20and%20regulations.-,Health%20Apps,-If%20your%20app). This applies to requests for `android.permission.BODY_SENSORS` and `android.permission.BODY_SENSORS_BACKGROUND` permissions across all form factors including phones, tablets, and Wear OS devices.

Starting in Android 16, the broad `BODY_SENSORS` permission is being transitioned in favor of granular, more privacy preserving `android.permissions.health.`* permissions for specific data types (for example, `android.permission.health.READ_HEART_RATE`, `android.permission.health.READ_OXYGEN_SATURATION`, `android.permission.health.READ_SKIN_TEMPERATURE`).

Apps targeting Android 16 or higher must use these specific permissions for APIs previously requiring `BODY_SENSORS`. See the [Behavior changes: Apps targeting Android 16 or higher](https://developer.android.com/about/versions/16/behavior-changes-16) page for full details.

All requests for body sensor permissions (both legacy and new granular permissions) will be reviewed so that the intended use of this personal and sensitive data aligns with approved use cases that directly benefit the user.Approved use cases primarily involve features for fitness and wellness tracking (for example, real-time workout monitoring), medical or condition monitoring, health research (with appropriate approvals), or enhancing wearable companion app features.

For comprehensive policy guidance, including prohibited uses, acceptable use cases, and detailed requirements, see the [Android Health Permissions: Guidance & FAQs](https://support.google.com/googleplay/android-developer/answer/12991134?sjid=16523468427823376810-EU).

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Use specific granular health permissions like `android.permission.health.READ_HEART_RATE` instead of the broad ``BODY_SENSORS` permission`. | Don’t declare ``BODY_SENSORS`` when a more specific health permission is available. |
| Ensure your app has a core, user-benefiting feature (for example, for fitness tracking or health monitoring) that strictly requires the data. | Don't access data without a clear, direct user benefit. |
| Comply with the [User Data](https://support.google.com/googleplay/android-developer/answer/10144311?#personal-sensitive)and [Health apps](https://support.google.com/googleplay/android-developer/answer/12261419?hl=en#:~:text=laws%20and%20regulations.-,Health%20Apps,-If%20your%20app) policies. | Don't request or use body sensor data for unapproved purposes, such as for general advertising, analytics, or profiling users based on inferred health conditions. |
| Request only the minimum permissions necessary and the specific data required for your app's intended purpose. | Don't ignore or attempt to bypass the fundamental [User Data](https://support.google.com/googleplay/android-developer/answer/10144311?#personal-sensitive) and [Health apps](https://support.google.com/googleplay/android-developer/answer/12261419?hl=en#:~:text=laws%20and%20regulations.-,Health%20Apps,-If%20your%20app) policies. |
| Consult the [Android Health Permissions: Guidance & FAQs](https://support.google.com/googleplay/android-developer/answer/12991134?sjid=16523468427823376810-EU) for a full list of use cases and requirements. |  |

---
