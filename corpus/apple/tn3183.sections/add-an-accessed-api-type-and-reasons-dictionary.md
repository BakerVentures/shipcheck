<!-- source=tn3183 clause=add-an-accessed-api-type-and-reasons-dictionary url=https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest fetched=2026-09-04T07:14:03+00:00 -->

## Add an accessed API type and reasons dictionary

A privacy accessed API type and reasons dictionary includes a category of required reason APIs and a list of related reasons. The dictionary contains exactly two keys: `NSPrivacyAccessedAPIType` and `NSPrivacyAccessedAPITypeReasons`. It uses the following format:

```xml
<dict>
    <!— Add an accessed API type key. -->
    <key>NSPrivacyAccessedAPIType</key>
    <string>NS_PRIVACY_ACCESSED_API_CATEGORY_VALUE</string>

    <!— Add an accessed API type reasons key. -->
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
        <string>NS_PRIVACY_ACCESSED_API_TYPE_REASON_VALUE</string>
        ...
    </array>
</dict>
```

To add a privacy accessed API type and reasons dictionary to the `NSPrivacyAccessedAPITypes` key in your privacy manifest:

1. Select `PrivacyInfo.xcprivacy` in the Project navigator.
2. Find the `NSPrivacyAccessedAPITypes` key in the property list editor.
3. Click the disclosure triangle to the left of `NSPrivacyAccessedAPITypes` to reveal it.
4. Click the Add button (+) beside `NSPrivacyAccessedAPITypes` to insert a new item.
5. Confirm the value is `Dictionary` in the Type column.
6. To add the `NSPrivacyAccessedAPIType` key to the dictionary, see [Add an accessed API type key](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Add-an-accessed-API-type-key).
7. To add the `NSPrivacyAccessedAPITypeReasons` key to the dictionary, see [Add an accessed API type reasons key](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Add-an-accessed-API-type-reasons-key).
