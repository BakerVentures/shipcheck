<!-- source=user-data-policy clause=account-deletion-requirement url=https://support.google.com/googleplay/android-developer/answer/10144311 fetched=2026-09-04T15:48:32+00:00 -->

## Account Deletion Requirement

**Policy Summary**

To comply with Google Play policy and respect user data control, apps that allow account creation must provide a clear option for account deletion. This option must be available both from within your app and externally through a designated web resource. When a user requests account deletion, you are required to delete *all* associated user data; merely freezing the account is not sufficient. Ensure the deletion process is clear and free of obstacles, and accurately disclose any necessary data retention practices in your privacy policy.

**Full Policy**

If your app allows users to create an account from within your app, then it must also allow users to request for their account to be deleted. Users must have a readily discoverable option to initiate app account deletion from within your app and outside of your app (for example, by visiting your website). A link to this web resource must be entered in the designated URL form field within Play Console.

When you delete an app account based on a user's request, you must also delete the user data associated with that app account. Temporary account deactivation, disabling, or “freezing” the app account does not qualify as account deletion. If you need to retain certain data for legitimate reasons such as security, fraud prevention, or regulatory compliance, you must clearly inform users about your data retention practices (for example, within your privacy policy).

To learn more about account deletion policy requirements, please review this [Help Center](https://support.google.com/googleplay/android-developer/answer/13327111) article. For additional information on updating your Data safety form, visit this [article](https://support.google.com/googleplay/android-developer/answer/10787469).

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Offer a clear account deletion option within your app. | Don't fail to provide both an in-app and external deletion method. |
| Provide an accessible external web resource for account deletion. | Don't create any hidden patterns or undue rigor in the deletion process. |
| Ensure the user process for deletion is straightforward and free of obstacles. | Don't use account freezing as a substitute for deletion. |
| Upon user request, delete *all* data associated with their account. | Don't fail to delete *all* associated user data upon account deletion request. |
| Clearly disclose any necessary (e.g. regulatory compliance) data retention in your privacy policy. | Don't provide broken or outdated links to the external deletion resource page. |
| Ensure your deletion resources clearly reference your app/service. | Don't omit necessary data retention information from your privacy policy. |

---
