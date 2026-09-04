<!-- source=app-privacy-details clause=additional-guidance url=https://developer.apple.com/app-store/app-privacy-details/ fetched=2026-09-04T15:48:25+00:00 -->

## Additional guidance

#### Your app has web views.

Data collected via web traffic must be declared, unless you are enabling the user to navigate the open web.

#### You collect and store IP address from your users.

Declare the relevant data types based on how you use IP address, such as precise location, coarse location, device ID, or diagnostics.

#### You offer in-app private messaging between users that are not SMS text messages.

Declare emails or text messages on your label. Text messages refer to both SMS and non-SMS messages.

#### Your app includes game saves, multiplayer matching, or gameplay logic.

Declare Gameplay Content on your label.

#### You collect different types of data from users depending on whether the user is a child, whether they are a free or paid user, whether they opt in, where they live, or for some other reason.

Please disclose all data collected from your app, unless it meets all of the criteria outlined in the Optional Disclosure section. You may use the Privacy Choices or Privacy Policy links to provide additional detail about how your data collection practices may vary.

#### You use Apple frameworks or services, such as MapKit, CloudKit, or App Analytics.

If you collect data about your app from Apple frameworks or services, you should indicate what data you collect and how you use it. You are not responsible for disclosing data collected by Apple.

#### You use location, device identifiers, and other sensitive data, but only on device, and the data is never sent to a server.

Data that is processed only on device is not “collected” and does not need to be disclosed in your answers. If you derive anything from that data and send it off device, the resulting data should be considered separately.

#### You collect precise location, but immediately de-identify and coarsen it before storing.

Disclose that you collect Coarse Location, since the precise location data is immediately coarsened and precise location is not stored.

#### Your app includes free-form text fields or voice recordings, and users can save any type of information they want through those mediums, including names and health data.

Mark "Other User Content" to represent generic free form text fields and "Audio Data" for voice recordings. You’re not responsible for disclosing all possible data that users may manually enter in the app through free-form fields or voice recordings. However, if you ask a user to input a specific data type into a text field, such as their name or email, or if you have a feature that enables users to upload a particular media type, such as photos or videos, then you’ll need to disclose the specific type of data.

#### You collect data to service a request but do not retain it after servicing the request.

"Collect" refers to transmitting data off the device and storing it in a readable form for longer than the time it takes you and/or your third-party partners to service the request. For example, if an authentication token or IP address is sent on a server call and not retained, or if data is sent to your servers then immediately discarded after servicing the request, you do not need to disclose this in your answers in App Store Connect.
