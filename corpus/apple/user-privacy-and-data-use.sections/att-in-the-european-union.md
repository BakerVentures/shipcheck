<!-- source=user-privacy-and-data-use clause=att-in-the-european-union url=https://developer.apple.com/app-store/user-privacy-and-data-use/ fetched=2026-10-05T14:47:04+00:00 -->

## ATT in the European Union

As part of agreements with select European competition authorities, Apple is introducing changes to its App Tracking Transparency framework in the European Union. Beginning with iOS 27.2 and iPadOS 27.2, developers will have the option to use an alternative version of the App Tracking Transparency system prompt in the EU. The requirements for when you must seek permission to track users will remain the same. Due to legal requirements, only the alternative version of the system prompt is available for apps distributed in Germany, France, Italy, Poland, and Romania.

The alternative version of the App Tracking Transparency system prompt has modified formatting and language and provides you the option to use a text button labeled “Additional Information.” This allows you to surface additional information about your request to link user or device data collected from your app with user or device data collected from other companies’ apps, websites, or offline properties for targeted advertising or advertising measurement purposes, or to share user or device data with a data broker.

In addition, for users in the European Union, you can reprompt a user via the App Tracking Transparency system prompt one year after the user’s previous choice in your app’s App Tracking Transparency system prompt, regardless of whether that choice was to accept or reject. A user cannot be re-prompted if they have disabled “Allow Apps to Request to Track” (renamed to “Allow Apps to Request to Link Your Activity Across Companies” in the EU) in their device’s Settings.

For technical details on using the alternative App Tracking Transparency system prompt and optional text button in the European Union, see:

- [Requesting Authorization with Expanded Interface (new)](/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(usingexpandedinterface:additionalinformationaction:completionhandler:))
- [Requesting Authorization](/documentation/apptrackingtransparency/attrackingmanager/requesttrackingauthorization(completionhandler:))
- [Tracking Markdown Usage Description (new)](/documentation/bundleresources/information-property-list/nsusertrackingmarkdownusagedescription)
- [Tracking Usage Description](/documentation/bundleresources/information-property-list/nsusertrackingusagedescription)
