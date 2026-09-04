<!-- source=user-privacy-and-data-use clause=asking-permission-to-track url=https://developer.apple.com/app-store/user-privacy-and-data-use/ fetched=2026-09-04T15:48:26+00:00 -->

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
