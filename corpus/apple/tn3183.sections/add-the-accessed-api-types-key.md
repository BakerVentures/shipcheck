<!-- source=tn3183 clause=add-the-accessed-api-types-key url=https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest fetched=2026-09-05T02:02:30+00:00 -->

## Add the accessed API types key

The `NSPrivacyAccessedAPITypes` key is an array of privacy accessed API type and reasons dictionaries. For more information, see [Add an accessed API type and reasons dictionary](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Add-an-accessed-API-type-and-reasons-dictionary). The key uses the following format:

```xml
<key>NSPrivacyAccessedAPITypes</key>
<array>
    <dict>
        <key>NSPrivacyAccessedAPIType</key>
        <string>NS_PRIVACY_ACCESSED_API_CATEGORY_VALUE</string>
        <key>NSPrivacyAccessedAPITypeReasons</key>
        <array>
            <string>NS_PRIVACY_ACCESSED_API_TYPE_REASON_VALUE</string>
            ...
        </array>
    </dict>
    ...
</array>
```

To add the `NSPrivacyAccessedAPITypes` key to your privacy manifest:

1. Select `PrivacyInfo.xcprivacy` in the Project navigator.
2. Click the Add button (+) beside the `App Privacy Configuration` key in the property list editor.
3. In the pop-up menu that appears, choose `NSPrivacyAccessedAPITypes`.
4. Confirm the value is `Array` in the Type column.
5. To add a privacy accessed API type and reasons dictionary to the array, see [Add an accessed API type and reasons dictionary](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Add-an-accessed-API-type-and-reasons-dictionary).

The following example declares disk space required reason API usage in an app named `Sample`:

Repeat step 5 for each additional required reason API your app or third-party SDK uses. The example below additionally declares user defaults required reason API usage in `Sample`:
