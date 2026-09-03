<!-- source=user-privacy-and-data-use clause=using-the-apptrackingtransparency-framework url=https://developer.apple.com/app-store/user-privacy-and-data-use/ fetched=2026-09-03T19:54:29+00:00 -->

### Using the AppTrackingTransparency framework

To request permission to track the user and access the device’s advertising identifier, use the AppTrackingTransparency framework. You must also include a purpose string in the system prompt that explains why you’d like to track the user. Unless you receive permission from the user to enable tracking, the device’s advertising identifier value will be all zeros and you may not track them as described above.

While you can display the AppTrackingTransparency prompt whenever you choose, the device’s advertising identifier value will only be returned once you present the prompt and the user grants permission. Use the purpose string to explain what this data will be used for to help the user understand what they’re opting in to share. If the user allows apps to request to track, but has turned tracking off for your app, you can ask the user to change their preference for your app by providing a [shortcut to Settings](/documentation/uikit/uiapplication/1623042-opensettingsurlstring/) where they can change the tracking permission.

The [ID for Vendors (IDFV)](/documentation/uikit/uidevice/1620059-identifierforvendor/), may be used for analytics across apps from the same content provider. In this case, the use of the AppTrackingTransparency framework is not required. The IDFV may not be combined with other data to track a user across apps and websites owned by other companies. You remain fully responsible to ensure that your collection and use of the IDFV complies with applicable law.

For more information, visit:

- [App Tracking Transparency](/documentation/apptrackingtransparency/)
- [Human Interface Guidelines: Privacy](/design/human-interface-guidelines/privacy/)
- [AdSupport Framework](/documentation/adsupport/)
