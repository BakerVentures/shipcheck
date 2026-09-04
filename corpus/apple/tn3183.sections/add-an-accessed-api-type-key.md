<!-- source=tn3183 clause=add-an-accessed-api-type-key url=https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest fetched=2026-09-04T07:14:03+00:00 -->

## Add an accessed API type key

The `NSPrivacyAccessedAPIType` key uses the following format:

```xml
<key>NSPrivacyAccessedAPIType</key>
<string>NS_PRIVACY_ACCESSED_API_CATEGORY_VALUE</string>
```

The `NS_PRIVACY_ACCESSED_API_CATEGORY_VALUE` string represents a privacy accessed API category. For more information, see [Select an accessed API category](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Select-an-accessed-API-category).

To add the `NSPrivacyAccessedAPIType` key to a privacy accessed API type and reasons dictionary:

1. Select the dictionary in the property list editor.
2. Click the disclosure triangle to the left of the dictionary to reveal it.
3. Click the Add button (+) beside the dictionary to add a new item.
4. In the pop-up menu that appears, choose `NSPrivacyAccessedAPIType`.
5. Confirm the value is `String` in the Type column.
6. Select a privacy accessed API category from the pop-up menu in the Value column. For possible values, see [Select an accessed API category](https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest#Select-an-accessed-API-category).
7. Confirm that the value exactly matches the category of required reason API that your app or third-party SDK uses.
