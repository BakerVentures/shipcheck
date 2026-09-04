<!-- source=permissions-policy clause=restricted-permissions url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T16:10:09+00:00 -->

## Restricted Permissions

**Policy Summary**

To safeguard user privacy, Google Play defines restricted permissions, subjecting them to additional requirements and mandates apps to responsibly use these permissions and not to manipulate users into granting access. Respect user choices when they decline permission requests and provide alternatives. Be aware that certain restricted permissions might have further additional requirements. Please review the full policy to ensure compliance.

**Full Policy**

In addition to the above, restricted permissions are permissions that are designated as [Dangerous](https://developer.android.com/guide/topics/permissions/overview#dangerous_permissions), [Special](https://developer.android.com/guide/topics/permissions/overview#special_permissions), [Signature](https://developer.android.com/guide/topics/permissions/overview#signature_permissions), or as documented below. These permissions are subject to the following additional requirements and restrictions:

- User or device data accessed through Restricted Permissions is considered as personal and sensitive user data. The requirements of the [User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?) apply.
- Respect users’ decisions if they decline a request for a Restricted Permission, and users may not be manipulated or forced into consenting to any non-critical permission. You must make a reasonable effort to accommodate users who do not grant access to sensitive permissions (for example, allowing a user to manually enter a phone number if they’ve restricted access to Call Logs).
- Use of permissions in violation of Google Play [malware policies](https://support.google.com/googleplay/android-developer/answer/9888380) (including [Elevated Privilege Abuse](https://support.google.com/googleplay/android-developer/answer/9888380)) is expressly prohibited.

Certain Restricted Permissions may be subject to additional requirements as detailed below. The objective of these restrictions is to safeguard user privacy. We may make limited exceptions to the requirements below in very rare cases where apps provide a highly compelling or critical feature and where there is no alternative method available to provide the feature. We evaluate proposed exceptions against the potential privacy or security impacts on users.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| If a user denies a restricted permission, your app must honor that decision without manipulation. | Don't use permissions to violate Google Play's [Malware](https://support.google.com/googleplay/android-developer/answer/9888380) policy, including [Elevated Privilege Abuse](https://support.google.com/googleplay/android-developer/answer/9888380#elevated-privilege-abuse). |
| Offer a different way to perform a function if a user denies a permission, such as allowing manual data entry. | Don't manipulate or deceive users. Never pressure or trick users into granting permissions. |
| Follow the [User Data](https://support.google.com/googleplay/android-developer/answer) policy, because all data accessed through these permissions is sensitive. | Don't deny a user a reasonable alternative if they decline a Restricted Permission; ensure the app remains functional. |
| Request dangerous permissions (for example, `READ_CALENDAR`) with a runtime request and a clear explanation. | Don't request without justification. Only request a restricted permission for a compelling, critical feature that has no alternative. |
| Direct users to the system settings page for approval of special permissions (for example, `SYSTEM_ALERT_WINDOW`). |  |

---
