<!-- source=tn3183 clause=add-an-accessed-api-type-reasons-key url=https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest fetched=2026-09-04T15:48:24+00:00 -->

## Add an accessed API type reasons key

The `NSPrivacyAccessedAPITypeReasons` key uses the following format:

```xml
<key>NSPrivacyAccessedAPITypeReasons</key>
<array>
    <string>NS_PRIVACY_ACCESSED_API_TYPE_REASON_VALUE</string>
    ...
</array>
```

Each `NS_PRIVACY_ACCESSED_API_TYPE_REASON_VALUE` string in the array identifies a reason why your app or third-party SDK uses a required reason API. All the values in the array are associated with a `NSPrivacyAccessedAPIType` key you provide when you create a privacy accessed API type and reasons dictionary.

To add the `NSPrivacyAccessedAPITypeReasons` key to a privacy accessed API type and reasons dictionary:

1. Select the dictionary in the property list editor.
2. Click the disclosure triangle to the left of the dictionary to reveal it.
3. Confirm the dictionary contains a `NSPrivacyAccessedAPIType` key with a value as described in [Select an accessed API category](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Select-an-accessed-API-category).
4. Click the Add button (+) beside the dictionary to add a new item.
5. In the pop-up menu that appears, choose `NSPrivacyAccessedAPITypeReasons`.
6. Confirm the value is `Array` in the Type column.
7. Click the disclosure triangle to the left of `NSPrivacyAccessedAPITypeReasons` to reveal it.
8. Click the Add button (+) beside `NSPrivacyAccessedAPITypeReasons` to add a reason.
9. Choose a reason from the pop-up menu in the Value column. For possible values, see [Describing use of required reason API](https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api).
10. Confirm that the value exactly matches a reason for the `NSPrivacyAccessedAPIType` key you use in step 3.
