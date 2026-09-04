---
shipcheck_source_id: user-privacy-and-data-use
title: "User privacy and data use (App Tracking Transparency)"
url: https://developer.apple.com/app-store/user-privacy-and-data-use/
final_url: https://developer.apple.com/app-store/user-privacy-and-data-use/
fetched_at: 2026-09-04T15:48:26+00:00
sha256: 9a857cb6d5ff1e28918e22309ad0c69d2b286d8785b26c25541986a6aea91e6a
vendor: apple
---

[Watch the latest videos about privacy](/videos/privacy-security/)

# User privacy and data use

The App Store is designed to be a safe and trusted place for users to discover apps created by talented developers around the world. Apps on the App Store are held to a high standard for privacy, security, and content because nothing is more important than maintaining users’ trust. In order to submit new apps and app updates, you need to provide information about some of your app’s data collection practices on your product page. You’re required to ask users for their permission to track them across apps and websites owned by other companies.

## Describing how your app uses data

The App Store helps users better understand an app’s privacy practices before they download the app. On each app’s product page, users can learn about some of the data types an app may collect, and whether the information is used to track them or is linked to their identity or device.

In order to submit new apps and app updates, you must provide information about your privacy practices in App Store Connect. If you use third-party code — such as advertising or analytics SDKs — you need to describe what data the third-party code collects, how the data may be used, and whether the data is used to track users.

[Learn more](/app-store/app-privacy-details/)

#### What’s new

An important part of submitting your app to the App Store is explaining how your app handles user data. Two new updates make it easier to accurately provide Privacy Nutrition Labels and improve the integrity of the software supply chain: signatures for third-party SDKs and privacy manifests. In addition, we’re adding more data type options to use in your Privacy Nutrition Label when describing what types of data your app collects.

[Read more](/news/?id=av1nevon)

[Watch the latest videos](/videos/privacy-security/)

## Asking permission to track

In iOS 14.5, iPadOS 14.5, and tvOS 14.5 or later, you need to receive the user’s permission through the AppTrackingTransparency (ATT) framework in order to track them or access their device’s advertising identifier. Tracking refers to the act of linking user or device data collected from your app with user or device data collected from other companies’ apps, websites, or offline properties for targeted advertising or advertising measurement purposes. Tracking also refers to sharing user or device data with data brokers.

Examples of tracking include, but are not limited to:

- Displaying targeted advertisements in your app based on user data collected from apps and websites owned by other companies.
- Sharing device location data or email lists with a data broker.
- Sharing a list of emails, advertising IDs, or other IDs with a third-party advertising network that uses that information to retarget those users in other developers’ apps or to find similar users.
- Placing a third-party SDK in your app that combines user data from your app with user data from other developers’ apps to target advertising or measure advertising efficiency, even if you don’t use the SDK for these purposes. For example, using an analytics SDK that repurposes the data it collects from your app to enable targeted advertising in other developers’ apps.

The following use cases are not considered tracking, and do not require user permission through the AppTrackingTransparency framework:

- When user or device data from your app is linked to third-party data solely on the user’s device and is not sent off the device in a way that can identify the user or device.
- When the data broker with whom you share data uses the data solely for fraud detection, fraud prevention, or security purposes. For example, using a data broker solely to prevent credit card fraud.
- When the data broker is a consumer reporting agency and the data is shared with them for purposes of (1) reporting on a consumer’s creditworthiness, or (2) obtaining information on a consumer’s creditworthiness for the specific purpose of making a credit determination.

### Using the AppTrackingTransparency framework

To request permission to track the user and access the device’s advertising identifier, use the AppTrackingTransparency framework. You must also include a purpose string in the system prompt that explains why you’d like to track the user. Unless you receive permission from the user to enable tracking, the device’s advertising identifier value will be all zeros and you may not track them as described above.

While you can display the AppTrackingTransparency prompt whenever you choose, the device’s advertising identifier value will only be returned once you present the prompt and the user grants permission. Use the purpose string to explain what this data will be used for to help the user understand what they’re opting in to share. If the user allows apps to request to track, but has turned tracking off for your app, you can ask the user to change their preference for your app by providing a [shortcut to Settings](/documentation/uikit/uiapplication/1623042-opensettingsurlstring/) where they can change the tracking permission.

The [ID for Vendors (IDFV)](/documentation/uikit/uidevice/1620059-identifierforvendor/), may be used for analytics across apps from the same content provider. In this case, the use of the AppTrackingTransparency framework is not required. The IDFV may not be combined with other data to track a user across apps and websites owned by other companies. You remain fully responsible to ensure that your collection and use of the IDFV complies with applicable law.

For more information, visit:

- [App Tracking Transparency](/documentation/apptrackingtransparency/)
- [Human Interface Guidelines: Privacy](/design/human-interface-guidelines/privacy/)
- [AdSupport Framework](/documentation/adsupport/)

### Frequently asked questions

##### Can I gate functionality on agreeing to allow tracking, or incentivize users to agree to allow tracking in the app tracking transparency prompt?

No, per the [App Review Guidelines: 5.1.2(i)](/app-store/review/guidelines/#5.1.2).

##### Can I explain to users why I would like permission to track them before I show the tracking permission prompt?

Yes, so long as you are transparent to users about your use of the data in your explanation. Per the [App Review Guidelines: 5.1.1 (iv)](/app-store/review/guidelines/#5.1.1), apps must respect the user’s permission settings and not attempt to manipulate, trick, or force people to consent to unnecessary data access.

##### If I have not received permission from a user via the tracking permission prompt, can I use an identifier other than the IDFA (for example, a hashed email address or hashed phone number) to track that user?

No. You will need to receive the user’s permission through the AppTrackingTransparency framework to track that user.

##### If a user provides permission for tracking via a separate process on our website, but declines permission in the app tracking transparency prompt, can I track that user across apps and websites owned by other companies?

Developers must get permission via the app tracking transparency prompt for data that’s collected in the app and used for tracking. Data collected separately, outside of the app and not related to the app, is not in scope.

##### Can I fingerprint or use signals from the device to try to identify the device or a user?

No. Per the Apple Developer Program License Agreement, you may not derive data from a device for the purpose of uniquely identifying it. Examples of user or device data include, but are not limited to: properties of a user’s web browser and its configuration, the user’s device and its configuration, the user’s location, or the user’s network connection. Apps that are found to be engaging in this practice, or that reference SDKs (including but not limited to Ad Networks, Attribution services, and Analytics) that are, may be rejected from the App Store.

##### If I share data with a consumer reporting agency to conduct fraud checks, and separately share data with them as part of a credit check or for credit reporting purposes, do I need permission to track?

No. You do not need permission from the user when a data broker uses the data shared with them solely for fraud detection or prevention or security purposes. You also do not need permission from the user when sharing data with a consumer reporting agency and the data is shared with them for purposes of (1) reporting on a consumer’s creditworthiness, or (2) obtaining information on a consumer’s creditworthiness for the specific purpose of making a credit determination.

##### Do I need to use the AppTrackingTransparency framework to get user permission to use third-party deep-linking or deferred deep-linking tools?

Yes. If your application uses any third-party services that pass unique identifiers or create a shared identity of the user between applications from different companies for ad targeting, ad measurement, or sharing with a data broker, your app will need to request permission from the user using the AppTrackingTransparency framework.

##### I have integrated an SDK from another company. Am I responsible for the data collection and tracking of users of my app by that company?

Yes. Developers are responsible for all code included in their apps. If you are unsure about the data collection and tracking practices of code used in your app that you didn’t write, we suggest contacting the developer of the SDK.

##### I have integrated single sign-on functionality provided by another company. Am I responsible for the data collection and tracking practices of that company?

Yes. Developers are responsible for all code included in their app, including single sign-on (SSO) functionality provided by third parties. If the user will be subject to tracking as a result of SSO functionality included in your app, you must use the app tracking transparency prompt to obtain permission from that user first.

##### What kind of company constitutes a data broker?

Data brokers are defined by law in some jurisdictions. In general, a data broker is a company that regularly collects and sells, licenses, or otherwise discloses to third parties the personal information of particular end-users with whom the business does not have a direct relationship.

##### What identifiers or data are governed by the “tracking” policy?

Any user or device level identifier that is used to join data from your app with data from third parties (including SDKs used in your app) for purposes of advertising or ad measurement or sharing with a data broker. This includes, but is not limited to, the device’s advertising identifier, session ID, fingerprint IDs, and device graph identifiers. If your app receives or shares any of these identifiers for the above listed purposes, you must use the AppTrackingTransparency framework to obtain user consent.

##### If tracking occurs within a webview inside an app, do I need to use the AppTrackingTransparency prompt?

Yes. If you are using a webview for app functionality, it should be treated the same way as native functionality in your app, unless you are enabling the user to navigate the open web.

##### What OS versions require AppTrackingTransparency permission to access the value of the IDFA?

To access the value of the IDFA for users on iOS/iPadOS version 14.5 or later, you will first need to receive permission from the user through the AppTrackingTransparency prompt. For additional guidance on tracking, please refer to [App Review Guidelines: 5.1.1 (iv)](/app-store/review/guidelines/#5.1.1).

##### Can I add other permission requests in order to comply with regulations, such as ePrivacy or GDPR?

Yes, you can choose to include screens in order to comply with government regulations. However, your app must always respect the user’s response to the AppTrackingTransparency prompt, even if their response to other prompts conflicts. [Guideline 5.1.1 (iv)](/app-store/review/guidelines/#5.1.1) states: “Apps must respect the user’s permission settings and not attempt to manipulate, trick, or force people to consent to unnecessary data access.” This includes altering a user’s AppTrackingTransparency response by only respecting their response to other permission requests. You can use third-party Consent Management Platforms to add these permission requests, as long as no tracking takes place from such use. You remain fully responsible to ensure that your collection and use of information linked to users’ identity or to their device, including information used to track users, complies with applicable law.

##### Can I offer a control in my app, separate from ATT, to comply with local privacy laws?

Yes. When offering a separate control to comply with local privacy laws, please consider the following:

- Don’t confuse the user. Be clear that the control doesn’t override their previous ATT choice.
- Provide context. If possible, show the user’s ATT status as part of a separate control so they can understand the choices they've already made.
- Be clear about what the choice is. If the user has not granted ATT permission, and there is no additional data use beyond the scope of ATT, be clear that no further action is required. If the user has granted ATT permission, it should be clear what impact the separate control will have on their ATT choice.

## Attributing app installations

Advertisers can use AdAttributionKit — Apple’s privacy-preserving, industry-leading technology — to attribute in-app ad campaigns and web ads on mobile, while maintaining user privacy.

[Learn more](/app-store/ad-attribution/)
