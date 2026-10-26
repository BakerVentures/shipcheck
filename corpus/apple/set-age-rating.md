---
shipcheck_source_id: set-age-rating
title: "Set an app age rating"
url: https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating
final_url: https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating
fetched_at: 2026-10-26T13:10:14+00:00
sha256: ad2656cb2ed5e3cafeb15ac0d0c4da77141b32a8c51b92b7ab2b27bd1ffd5fd5
vendor: apple
note: "Added alongside age-ratings: covers the questionnaire that drives mismatches."
---

[App Store Connect Help](/help/app-store-connect/)

[App Store Connect](/help/app-store-connect/) Manage app information Set an app age rating

Manage app information

# Set an app age rating

An age rating is a required [app information](/help/app-store-connect/reference/app-information/app-information) property that helps users assess the content and any potentially objectionable material within your app or game. This rating supports the functionality of parental controls, allowing parents and guardians to establish a safe online environment for children. As a developer, you can deliver age-appropriate experiences tailored for users across all age groups.

To determine the age rating of your app, respond to the age rating questionnaire in App Store Connect. This questionnaire includes a list of content descriptors, in-app controls, and capabilities that allow you to specify the frequency of each content type in your app. Your selections are then translated into an Apple global age rating, as well as additional region-specific ratings if required. [Learn about age rating values and definitions.](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions)

This process helps you understand how different types of content can impact your app’s rating across various regions, enabling you to make informed declarations of frequency of the content and features in your app.

Depending on your responses, an age rating is assigned to each country or region based on their specific age suitability standards. This rating will be displayed on the App Store for that country or region and will remain consistent across all platforms. Learn about age rating values with region-specific requirements for [Australia](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#australia-age-rating-values), [Brazil](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#brazil-age-rating-values), and [Korea](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#republic-of-korea-age-rating-values).

**Notes:**

- Age ratings for an app may vary based on the OS version. [View age range value details](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-values) for Apple devices running a minimum of iOS 26, iPadOS 26, macOS Tahoe 26, tvOS 26, visionOS 26, and watchOS 26. [View details](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-ratings-on-os-versions-earlier-than-26) for Apple devices running an earlier OS version.
- An Unrated app can’t be published on the App Store. It may be published on alternative app marketplaces or websites.

[Learn how to manage app age ratings with the App Store Connect API.](https://developer.apple.com/documentation/appstoreconnectapi/app_store/app_metadata/age_rating_declarations)

**Required role:** Account Holder, Admin, App Manager, or Marketing. [View role permissions.](/help/app-store-connect/reference/account-management/role-permissions)

## Set an app age rating

1. In Apps, select the app you want to view.
2. In the sidebar, under General, click App Information. **Tip:** To learn more about and view examples of the features and content used to determine age ratings, select a category from the panel of examples on the App Information Page. You can also browse [Age rating categories](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-categories).
3. Below Age Ratings, click the Set Up Age Ratings button. ![App Information page showing the 'Set Up Age Ratings' button in the Age Ratings section.](/help/app-store-connect/manage-app-information/set-an-app-age-rating/images/set-an-app-age-rating-1_2x.png)
4. When the dialog box appears, review the list of in-app controls and capabilities options, and select any that your app includes that can restrict content, then click Next.
5. Navigate through each section of the progress bar, answering the questions and selecting the appropriate level of frequency for each content description, then click Next. ![Step 5: Chance-Based Activities in the Age Ratings questionnaire, with frequency options for simulated gambling and contests, and yes or no options for gambling and loot boxes.></figure>

### Override to higher age rating

To increase the rating of your app to a rating that exceeds the rating assigned by Apple, choose Override to Higher Age Rating and select the appropriate rating from the menu. App Store will display this specified age rating, and the content descriptions will still reflect your questionnaire answers.

If your app will be distributed through alternative app marketplaces or your website in the European Union and you believe your app is Unrated, select Unrated from the menu options under Override to Higher Age Rating.

**Note:**

- If your app has a EULA with minimum age requirements that exceed the rating that Apple calculated, you must override to a rating that adheres to the requirements.
- The override will apply in all regions where your app is available and may override to a different rating value per region based on region-specific requirements. Learn about age rating values with region-specific requirements for [Australia](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#australia-age-rating-values), [Brazil](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#brazil-age-rating-values), and [Korea](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#republic-of-korea-age-rating-values).

If your app has a dedicated website with details on age suitability, you can provide the URL in the field provided under Age Suitability URL (Optional).

Click Save. The dialog box will close, returning you to the App Information page. Here, you can view your global and region-specific ratings . Click on each panel for details on the age ratings and the specific countries and regions they apply to.

To edit your age rating, click App Information in the sidebar, then click Edit at the top of the page.

**Note:** You can view the age ratings for Apple devices running an earlier OS version than 26 under the Operating Systems Earlier than Version 26 section. [Learn more.](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-ratings-on-os-versions-earlier-than-26)

### Override region-specific ratings

### Override age rating for the Republic of Korea

App Review may contact you if the Korean [Games Rating and Administration Committee](https://www.grac.or.kr/english/) (GRAC) issues a region-specific rating that differs from your app's existing age rating. If you receive this notice, you need to update your app's age rating for the App Store in Korea by providing your Rating Classification Number (RCN) and submitting a new version of your app to App Review.

1. In Apps, select your app.
2. In the sidebar, under General, click App Information.
3. In the Age Ratings section, next to Republic of Korea, click Add RCN.
4. In the dialog that appears, enter your RCN and select the rating you received from GRAC.
5. Select the checkbox confirming that this is the official rating issued by GRAC for your app, then click Save. **Note:** If an error appears after clicking Save, address the error message and click Save again.

You can edit your RCN or override at any time before submitting your app for review by clicking Edit RCN next to Republic of Korea. From there, you can select a new rating, or clear your RCN and rating together by clicking Remove. While your app is in review, you can only view your RCN and rating by clicking View RCN. Once your app is approved, your RCN and rating are locked and can no longer be edited.

**Related** [Age ratings values and definitions](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions) [Platform version information](/help/app-store-connect/reference/app-information/platform-version-information) [Required, localizable, and editable properties](/help/app-store-connect/reference/app-information/required-localizable-and-editable-properties)
