<!-- source=permissions-policy clause=vpn-service url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T07:14:14+00:00 -->

## VPN Service

**Policy Summary**

The VpnService base class allows developers to create secure VPN solutions. Google Play permits its use only for apps with core VPN functionality or those requiring a remote server for essential features such as parental control, app usage tracking, device security, network tools, web browsers, or carrier services. It is paramount that VpnService is never used to collect personal or sensitive user data without prominent disclosure and explicit consent. Furthermore, redirecting or manipulating user traffic from other apps for monetization is strictly prohibited. All apps using VpnService must clearly document this in their Google Play listing and encrypt all data from the device to the VPN tunnel endpoint. Please review the full policy to ensure compliance.

**Full Policy**

The [VpnService](https://developer.android.com/reference/android/net/VpnService) is a base class for applications to extend and build their own VPN solutions. Only apps that use the VpnService and have VPN as their core functionality can create a secure device-level tunnel to a remote server. Exceptions include apps that require a remote server for core functionality such as:

- Parental control and enterprise management apps
- App usage tracking
- Device security apps (for example, anti-virus, mobile device management, firewall)
- Network related tools (for example, remote access)
- Web browsing apps
- Carrier apps that require the use of VPN functionality to provide telephony or connectivity services

The VpnService cannot be used to:

- Collect personal and sensitive user data without prominent disclosure and consent.
- Redirect or manipulate user traffic from other apps on a device for monetization purposes (for example, redirecting ads traffic through a country different than that of the user).

Apps that use the VpnService must:

- Document use of the VpnService in the Google Play listing, and
- Must encrypt the data from the device to VPN tunnel end point, and
- Abide by all [Developer Program Policies](https://support.google.com/googleplay/android-developer/topic/9858052?hl=en)including the [Ad Fraud](https://support.google.com/googleplay/android-developer/answer/9969955#zippy=%2Cexamples-of-common-violations), [Permissions](https://support.google.com/googleplay/android-developer/answer/9888170), and [Malware](https://support.google.com/googleplay/android-developer/answer/9888380#1&2&3&4&5&6&7&87&9) policies.

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Document use of the [VpnService](https://developer.android.com/reference/android/net/VpnService) clearly in the Google Play listing. | Don't use [VpnService](https://developer.android.com/reference/android/net/VpnService) for purposes other than core VPN or specified exceptions. |
| Must encrypt the data from the device to the VPN tunnel end point. | Don't collect personal and sensitive user data without prominent disclosure and consent. |
| Ensure your app's core functionality aligns with VPN use or permitted exceptions. | Don't redirect or manipulate user traffic from other apps on a device for monetization purposes (for example, redirecting ads traffic through a country different than that of the user). |
| Provide prominent in-app disclosure and obtain explicit consent for any sensitive data collection. |  |

---
