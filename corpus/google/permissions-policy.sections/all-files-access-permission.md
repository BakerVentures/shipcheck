<!-- source=permissions-policy clause=all-files-access-permission url=https://support.google.com/googleplay/android-developer/answer/16558241 fetched=2026-09-04T15:48:35+00:00 -->

## All Files Access Permission

**Policy Summary**

Google Play policy treats access to user files and directories as sensitive and high risk access, so we restrict use of the ``MANAGE_EXTERNAL_STORAGE`` permission on Android 11+. You must have essential core app functionality that requires broad access to this permission for a user-facing purpose, and never for third parties. This helps prevent unnecessary data collection and protects users' privacy. Apps requesting this permission must clearly prompt users so they can make an informed privacy decision, and get approval through Play’s app review. Please review the full policy to ensure compliance.

**Full Policy**

Files and directory attributes on a user’s device are regarded as personal and sensitive user data subject to the [Personal and Sensitive Information](https://support.google.com/googleplay/android-developer/answer/9888076/) policy and the following requirements:

- Apps should only request access to device storage which is critical for the app to function, and may not request access to device storage on behalf of any third-party for any purpose that is unrelated to critical user-facing app functionality.
- Android devices running R or later, will require the [``MANAGE_EXTERNAL_STORAGE``](https://developer.android.com/reference/android/Manifest.permission#<code>MANAGE_EXTERNAL_STORAGE</code>) permission in order to manage access in shared storage. All apps that target R and request broad access to shared storage (“All files access”) must successfully pass an appropriate access review prior to publishing. Apps allowed to use this permission must clearly prompt users to enable “All files access” for their app under “Special app access” settings. For more information on the R requirements, please see this [help article](https://support.google.com/googleplay/android-developer/answer/9956427).

**Key Considerations**

| **Do** | **Don't** |
| --- | --- |
| Prioritize using privacy-friendly alternatives instead, like [Storage Access Framework](https://developer.android.com/guide/topics/providers/document-provider) or [MediaStore API](https://developer.android.com/training/data-storage/shared/media). | Don't request the `MANAGE_EXTERNAL_STORAGE` permission for non-permitted use-cases like Media Files access or any File selection activity where the user manually selects individual files. |
| [Declare](https://goo.gle/play-permission-decl-form) this permission when you submit a declaration form in your Play Console. | Don't misrepresent the core functionality of your app. |
| Clearly define and document your app's core functionality in your app review. | Don't store or share data beyond essential and disclosed needs. |
| Clearly prompt users to enable “[All files access](https://developer.android.com/about/versions/11/privacy/storage#all-files-access)” for your app under “Special app access” settings. |  |
| Ensure you review the [Android R requirements](https://goo.gle/play-help-all-files-access) for more information. |  |

---
