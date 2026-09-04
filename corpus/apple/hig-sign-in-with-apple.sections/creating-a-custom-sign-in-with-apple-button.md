<!-- source=hig-sign-in-with-apple clause=creating-a-custom-sign-in-with-apple-button url=https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple fetched=2026-09-04T15:48:26+00:00 -->

### Creating a custom Sign in with Apple button

If your interface requires it, you can create a custom Sign in with Apple button for iOS, macOS, or the web. For example, you may want to align logos across multiple sign-in buttons, use buttons that display only a logo, or adjust the button’s font, bezel, or background appearance to coordinate with your UI.

![An illustration that includes two side-by-side partial iPhones showing sign-in screens. The screen on the left includes four stacked buttons: Sign in with Apple, Sign in with X, Sign in with Y, and Sign in with Z. The Sign in with Apple button includes an Apple logo before its title. The Sign in with X button includes a filled circle before its title. The Sign in with Y button includes a filled square before its title. The Sign in with Z button includes a filled triangle before its title. The screen on the right includes a heading that reads 'Sign in with', which appears above a row of four square buttons containing glyphs. The first square button contains the Apple logo. The second square button contains a filled circle. The third square button contains a filled square. The fourth square button contains a filled triangle. The circle, square, and triangle shapes represent a variety of logos.]

Always make sure that people can instantly identify your custom button as a Sign in with Apple button. If your custom button differs too much from the standard one, people may not feel comfortable using it to set up an account or sign in. App Review evaluates all custom Sign in with Apple buttons.

[Apple Design Resources](https://developer.apple.com/design/resources/) provides downloadable Apple logo artwork you can use to create custom Sign in with Apple buttons that display either a logo only or a logo and text. The logo files are available in PNG, SVG, and PDF formats, and the artwork for both types of buttons includes both black and white versions. Here are examples of the black and white logo-only art files, each with a background added for visibility.

All downloadable logo files include padding that simplifies positioning the logo in a button. Logo-only logo files include horizontal and vertical padding that ensures the correct proportion of the logo relative to the button. In addition to padding that keeps the logo and button correctly proportioned, logo files for buttons with text also include horizontal padding that provides a minimum margin between the logo and the button’s leading edge and title.

Use only the logo artwork downloaded from [Apple Design Resources](https://developer.apple.com/design/resources/); never create a custom Apple logo. As you create a custom Sign in with Apple button, follow these guidelines for using the downloadable logo file:

- Use the logo file to position the Apple logo in a button; never use the Apple logo as a button.
- Match the height of the logo file to the height of the button.
- Don’t crop the logo file.
- Don’t add vertical padding.

To make sure that your custom button is visually consistent with the system-provided Sign in with Apple button, don’t change the following attributes.

- Titles. Use only *Sign in with Apple*, *Sign up with Apple*, or *Continue with Apple*.
- General shape. Buttons that combine the logo with text are always rectangular; logo-only buttons can be circular or rectangular.
- Logo and title colors. Within a button, both items must be either black or white; don’t use custom colors.

To coordinate with your app design, you can change:

- Title font. You can also adjust the font’s weight and size.
- Title case. You can capitalize every letter in the title.
- Background appearance. The overall color needs to remain black or white. If necessary, you can include a subtle texture or gradient to help the button harmonize with your interface.
- Button corner radius. You can use a corner radius value that matches the other buttons in your UI.
- Button bezel and shadow. For example, you can use a stroke to emphasize the button bezel or add a drop shadow.

#### Custom buttons with a logo and text

**Choose the format of the logo file based on the height of your button.** Because SVG and PDF are vector-based formats, you can use these files in buttons of any height. Use the PNG files only in buttons that are 44 points tall, which is the default (and recommended) button height in iOS. Logos are available in small, medium, and large sizes, so you can match logo sizes in all the sign-up buttons you display.

**Prefer the system font for the title — that is, Sign in with Apple, Sign up with Apple, or Continue with Apple.** Regardless of the font you choose, the title and button height of your custom button need to use the same proportions that the system uses. Using the system font for example, the title’s font size would be 43% of the button’s height — in other words, the button’s height would be 233% of the title’s font size, rounded to the nearest integer. Here are two examples that show these proportions using different sizes of the system font.

![An illustration of a Sign in with Apple button, with callouts that indicate a button height of 44 points and a font size of 19 points.]

![An illustration of a Sign in with Apple button, with callouts that indicate a button height of 56 points and a font size of 24 points.]

**In general, preserve the capitalization style of the title.** By default, all variants of the button title capitalize the first word — that is, *Sign* or *Continue* — and *Apple*; all other letters are lowercase. Avoid changing this style unless your interface uses only uppercase.

**Keep the title and logo vertically aligned within the button.** To do this, vertically align the title to the middle of the button, then add the logo image, making sure its height matches the height of the button. Because the logo image includes top and bottom padding, vertically aligning the title in the button ensures that the title, the logo, and the button stay properly aligned.

**Inset the logo if necessary.** If you need to horizontally align the Apple logo with other authentication logos, you can adjust the space between the logo and the button’s leading edge.

**Maintain a minimum margin between the title and the right edge of the button.** Ensure the margin measures at least 8% of the button’s width.

**Maintain the minimum button size and margin around the button.** Be mindful that the button title may vary in length depending on the locale. Use the following values for guidance.

| Minimum width | Minimum height | Minimum margin |
| --- | --- | --- |
| 140 pt (140 px @1x, 280 px @2x) | 30 pt (30 px @1x, 60 px @2x) | 1/10 of the button’s height |

#### Custom logo-only buttons

**Choose the format of the logo file based on the size of your button.** The downloadable artwork for logo-only buttons is available in SVG, PDF, and PNG formats. Use the vector-based SVG and PDF formats for buttons of any size; use the PNG format only in buttons that measure 44x44 pt.

**Don’t add horizontal padding to a logo-only image.** A logo-only Sign in with Apple button always has a 1:1 aspect ratio, and the artwork already includes the correct padding on all sides.

**Use a mask to change the default square shape of the logo-only image.** For example, you might want to use a circular or rounded rectangular shape to present all logo-only sign-in buttons. Never crop the Apple-provided artwork to decrease its built-in padding or use the logo by itself, and avoid including additional padding.

**Maintain a minimum margin around the button.** Ensure the margin measures at least 1/10 of the button’s height.
