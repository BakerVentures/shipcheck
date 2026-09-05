<!-- source=hig-sign-in-with-apple clause=using-the-system-provided-buttons url=https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple fetched=2026-09-05T02:02:32+00:00 -->

### Using the system-provided buttons

When you use the system-provided APIs to create a Sign in with Apple button, you get the following advantages.

- A button that’s guaranteed to use an Apple-approved appearance
- Assurance that the button’s contents maintain ideal proportions as you change its style
- Automatic translation of the button’s title into the language specified by the device
- Support for configuring the button’s corner radius to match the style of your UI (iOS, macOS, and web)
- A system-provided alternative text label that lets VoiceOver describe the button

For developer guidance, see [ASAuthorizationAppleIDButton](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidbutton) (iOS, macOS, and tvOS), [WKInterfaceAuthorizationAppleIDButton](https://developer.apple.com/documentation/watchkit/wkinterfaceauthorizationappleidbutton) (watchOS), and [Displaying Sign in with Apple buttons on the web](https://developer.apple.com/documentation/signinwithapple/displaying-sign-in-with-apple-buttons-on-the-web). You can also visit [Sign in with Apple button](https://appleid.apple.com/signinwithapple/button) to view and adjust live previews of web-based buttons and get the code.

The system provides several variants of the button title. Depending on the platform on which your content runs, choose the variant that fits the terminology of your sign-in experience and use it consistently throughout your interfaces.

The following button titles are available for iOS, macOS, tvOS, and the web:

For watchOS, the system provides one title:  Sign in.

![An illustration of a button for watchOS, that includes the Apple logo and text that reads 'Sign in'.](https://developer.apple.com/images/com.apple.HIG/apple-account-watch-44mm-no-background@2x.png)

Depending on the platform, the system provides up to three options for the appearance of the Sign in with Apple button: white, white with an outline, and black. Choose the appearance that works best with the background on which the button displays.

#### White

The white style is available on all platforms and the web. Use this style on dark backgrounds that provide sufficient contrast.

#### White with outline

The white outlined style is available in iOS, macOS, and the web. Use this style on white or light-color backgrounds that don’t provide sufficient contrast with the white button fill. Avoid using this style on a dark or saturated background, because the black outline can add visual clutter; instead, use the [white](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple#White) style to contrast with a dark background.

#### Black

The black style is available on all platforms and the web. Use this style on white or light-color backgrounds that provide sufficient contrast; don’t use it on black or dark backgrounds.

Unlike the black Sign in with Apple button for other platforms, the watchOS button uses a fill color that’s not fully black. To contrast with the pure black background of Apple Watch, the watchOS button uses the system-defined dark gray appearance.

![An illustration of a dark shaded button for watchOS on a black background, that includes the Apple logo and text that reads 'Sign in'.](https://developer.apple.com/images/com.apple.HIG/apple-account-watch-44mm@2x.png)

#### Button size and corner radius

**Adjust the corner radius to match the appearance of other buttons in your app.** By default, the Sign in with Apple button has rounded corners. In iOS, macOS, and the web, you can change the corner radius to produce a button with square corners or a capsule-shape button. For developer guidance, see [cornerRadius](https://developer.apple.com/documentation/authenticationservices/asauthorizationappleidbutton/cornerradius) (iOS and macOS) and [Displaying Sign in with Apple buttons on the web](https://developer.apple.com/documentation/signinwithapple/displaying-sign-in-with-apple-buttons-on-the-web).

**Maintain the minimum button size and margin around the button in iOS, macOS, and the web.** Be mindful that the button title may vary in length depending on the locale. Use the following values for guidance.

| Minimum width | Minimum height | Minimum margin |
| --- | --- | --- |
| 140pt (140px @1x, 280px @2x) | 30pt (30px @1x, 60px @2x) | 1/10 of the button’s height |
