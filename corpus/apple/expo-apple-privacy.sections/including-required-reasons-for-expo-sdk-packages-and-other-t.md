<!-- source=expo-apple-privacy clause=including-required-reasons-for-expo-sdk-packages-and-other-t url=https://docs.expo.dev/guides/apple-privacy/ fetched=2026-09-05T02:02:34+00:00 -->

### Including required reasons for Expo SDK packages and other third-party libraries

As of now, Apple does not correctly parse all the PrivacyInfo files included by static CocoaPods dependencies (such as Expo SDK packages and other ecosystem libraries). You may need to include the required reasons for the APIs used by those dependencies in your app's PrivacyInfo.xcprivacy file or the configuration in the app.json.

All Expo SDK packages that use "required reason" APIs file have a PrivacyInfo file included in the package directory. Here's [an example file](https://github.com/expo/expo/blob/main/packages/expo-application/ios/PrivacyInfo.xcprivacy) included with the `expo-application` library.

You can usually identify the required reasons for the APIs used by other third-party libraries by checking if the library you intend to use has a PrivacyInfo.xcprivacy file in the node_modules/package_name/ios directory. If it does, you can check the `NSPrivacyAccessedAPITypes` and `NSPrivacyAccessedAPITypeReasons` values in that file and copy those values to your configuration.

As an alternative, Apple notifies developers after they submit a build with missing privacy manifest files or specific reasons. You can wait until you receive a notification email from Apple and then include the required reasons listed in the email in your app's PrivacyInfo.xcprivacy file (if you don't use [CNG](/workflow/continuous-native-generation)) or the configuration in your app.json file.
