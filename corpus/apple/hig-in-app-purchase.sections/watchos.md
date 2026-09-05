<!-- source=hig-in-app-purchase clause=watchos url=https://developer.apple.com/design/human-interface-guidelines/in-app-purchase fetched=2026-09-05T02:02:31+00:00 -->

### watchOS

The sign-up screen in your watchOS app needs to display the same set of information about your subscription options that you display in other versions of your app. For the complete list of required items, see [Making signup effortless](https://developer.apple.com/design/human-interface-guidelines/in-app-purchase#Making-signup-effortless). The following guidelines can help you design a sign-up screen that feels at home on Apple Watch.

**Clearly describe the differences between versions of your app that run on different devices.** If your watchOS app supports different functionality or provides a subset of the content that’s available on other devices, be sure to clarify these differences in your description. Be straightforward about the advantages of accessing subscription content through your watchOS app without implying that the experience is identical to the ones in other versions of your app.

**Consider using a modal sheet to display the required information.** After people respond to your call to action to learn more about your subscription offers, you can use a modal sheet to present all required items in a single view. Even though people must scroll the view to access all the information, displaying it in a modal sheet helps your app UI remain streamlined and concise. Also, a modal sheet’s default Close button makes it easy for people to return to your free content with one tap. If you create a custom sign-up view instead of using a modal sheet, design a complete, efficient flow and include a Close or Cancel button that lets people return to your free content.

**Make subscription options easy to compare on a small screen.** People need to understand the terms of each subscription option before they can choose one. Aim to display the duration and discount information for each option in a compact way that’s easy to scan and compare. Here are two ways you might present subscription options in your watchOS app:

- Display each option in a separate button. Using one button per payment option lets people start the signup process with one tap. In this design, it’s important to lock up each button with its description so that people can see how these elements are related, especially while scrolling.
- Display a list of options, followed by a button people tap to start the signup process. Using a list to display one option per row gives you a compact design that minimizes scrolling while making subscription choices easy to scan and understand. In this design, the button’s title can update to reflect the chosen option.
