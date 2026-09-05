---
shipcheck_source_id: age-ratings
title: "Age ratings values and definitions"
url: https://developer.apple.com/help/app-store-connect/reference/age-ratings
final_url: https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions
fetched_at: 2026-09-05T02:02:33+00:00
sha256: 20d6e65811ae8ee3b1294ccfb41f89ea5b2fdcaa62ad6576a7c49953501773c9
vendor: apple
substituted_from: https://developer.apple.com/help/app-store-connect/reference/age-ratings-definitions
note: "Original 404s. Apple restructured age ratings (13+/16+/18+ tiers)."
---

[App Store Connect Help](/help/app-store-connect/)

[App Store Connect](/help/app-store-connect/) Reference [App information](/help/app-store-connect/reference/app-information/) Age ratings values and definitions

Reference

# Age ratings values and definitions

The *age rating* is a required [app information](/help/app-store-connect/reference/app-information/app-information) field used for property used by the parental controls. These controls enable parents and guardians to establish a safe online environment for children. As a developer, you can deliver age-appropriate experiences tailored for users across all age groups.

In App Store Connect, you'll find a list of content descriptors, in-app controls, and capabilities that allow you to specify the frequency or presence of each in your app. Apple generates appropriate ratings based on your answer to the age rating questionnaire. [Learn how to set an app age rating.](/help/app-store-connect/manage-app-information/set-an-app-age-rating)

The tables below provide detailed information about the different age rating categories and age rating values by region.

**Notes:**

- An Unrated app can't be published on the App Store. It may be published on alternative app marketplaces or websites.
- Age ratings for an app may vary based on the OS version. [View age range value details](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-values) for Apple devices running a minimum of iOS 26, iPadOS 26, macOS Tahoe 26, tvOS 26, visionOS 26, and watchOS 26. [View details](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-ratings-on-os-versions-earlier-than-26) for Apple devices running an earlier OS version.

## Age rating categories

| Category | Examples of included features and content |
| --- | --- |
| In-App Controls |  |
| Capabilities |  |
| Mature Themes |  |
| Medical or Wellness |  |
| Sexuality or Nudity |  |
| Violence |  |
| Chance-Based Activities |  |

### Age rating values

These ratings apply to all regions that don’t have any additional regional requirements.

Learn about age rating values with region-specific requirements for [Australia](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#australia-age-rating-values), [Brazil](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#brazil-age-rating-values), and [Korea](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#republic-of-korea-age-rating-values).

| Rating | Definition |
| --- | --- |
| 4+ | Apps with this rating contain no objectionable material but may contain instances of the following content that may not be suitable for children under the age of 4: **In-App Controls:** **Capabilities:** **Chance-Based Activities:** |
| 9+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 9: **Mature Themes** **Medical or Wellness** **Sexuality or Nudity** **Violence** **Chance-Based Activities** |
| 13+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 13: **Capabilities:** **Mature Themes:** **Medical or Wellness:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| 16+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 16: **Capabilities:** **Medical or Wellness:** **Sexuality or Nudity:** |
| 18+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 18: **Mature Themes:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| Unrated | Apps with this rating may contain instances of the following content that can’t be published on the App Store. It may be published on alternative app marketplaces or websites: **Sexuality or Nudity:** **Violence:** |

### Australia age rating values

As required by [Australia’s guidelines for the classification of computer games](https://www.legislation.gov.au/F2023L01424/latest/text), apps that have at least one of the following content descriptors will display the regional region-specific age rating.

**Note:** Only the age rating values listed below differ from the [age rating values](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-values).

| Rating | Definition |
| --- | --- |
| 16+ | Apps that contain: **Capabilities:** **Chance-Based Activities:** |
| R 18+ | Apps that contain: **Chance-Based Activities:** |

If we’re notified by the regulator that your app doesn’t meet their guidelines or requires a region-specific rating, you’ll receive a message from App Review. If you receive this message, follow the instructions and [re-submit your app for review](/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review).

### Brazil age rating values

As required by the Brazilian Ministry of Justice and Public Security (MJSP), the App Store uses a different set of region-specific rating pictograms and descriptors for self-rated apps, than for ratings officially issued by the MJSP.

Official Brazil region-specific ratings and descriptors apply to apps that were issued an official rating by the MJSP. If a rating or descriptor has been issued to your app by the MJSP, Apple will update your regional rating and/or descriptors on your behalf and it'll display on the App Store in Brazil.

Apps that include fixed-odds betting (gambling) features require a valid Brazilian fixed-odds betting license from the [Secretariat of Prizes and Bets (SPA)](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/lista-de-empresas) to be distributed on the App Store in Brazil. When submitting a new app update, provide your license details and any supporting documentation in the App Review Information section in App Store Connect. Enter your license details in the Notes field and attach any supporting documents using the file attachment field.

[Review App Review Guideline 5.3.4. to ensure gambling app compliance.](/app-store/review/guidelines/#legal)

Possible values for official Brazil age pictograms are:

Possible values for self-rated Brazil age pictograms are:

| Rating | Definition |
| --- | --- |
| AL | Apps that contain no objectionable material but may contain instances of the following content: **In-App Controls:** |
| A6 | Apps that contain: **Capabilities:** **Violence:** **Chance-Based Activities:** |
| A10 | Apps that contain: **Mature Themes:** **Medical or Wellness:** **Violence:** |
| A12 | Apps that contain: **Capabilities:** **Mature Themes:** **Medical or Wellness:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| A14 | Apps that contain: **Mature Themes:** |
| A16 | Apps that contain: **Capabilities:** **Mature Themes:** **Medical or Wellness:** |
| A18 | Apps that contain: **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |

### Republic of Korea age rating values

For all apps made available in Korea, the following region-specific rating values will display:

**Note:** Apps and games with Frequent or Intense simulated gambling content are only available on the App Store in Korea if you provide a Rating Classification Number (RCN).

| Rating | Definition |
| --- | --- |
| All | Apps that contain: **In-App Controls:** **Capabilities:** **Mature Themes:** **Medical or Wellness:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| 12+ | Apps that contain: **Mature Themes:** **Medical or Wellness:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| 15+ | Apps that contain: **Capabilities:** **Medical or Wellness:** |
| 19+ | Apps that contain: **Mature Themes:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |

**Note:** You’ll receive a message from App Review if the [Korean Games Rating and Administration Committee(GRAC)](https://www.grac.or.kr/english/) issues an official rating for your app that is different from your app’s age rating. If you receive this notice, follow the instructions in the [override age rating for Korea](/help/app-store-connect/manage-app-information/set-an-app-age-rating/#override-region-specific-ratings) section and re-submit your app for review.

### Vietnam age rating values

As required by Article 38 of Vietnam Decree 147, apps that have at least one of the following content descriptors will display the region-specific age rating.

| Rating | Definition |
| --- | --- |
| 00+ | Apps with this rating contain no objectionable material but may contain instances of the following content: **In-App Controls:** **Capabilities:** **Chance-Based Activities:** |
| 12+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 12: **Mature Themes:** **Medical or Wellness:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| 16+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 16: **Capabilities:** **Medical or Wellness:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |
| 18+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 18: **Mature Themes:** **Sexuality or Nudity:** **Violence:** **Chance-Based Activities:** |

## Age ratings on OS versions earlier than 26

The age rating is a required [app information](/help/app-store-connect/reference/app-information/app-information) field used for parental controls. These controls enable parents and guardians to establish a safe online environment for children. As a developer, you can deliver age-appropriate experiences tailored for users across all age groups. [Learn more about how parents approve what kids buy with ask to buy.](https://support.apple.com//105055)

View the age ratings that'll be displayed for Apple devices running an earlier OS version than 26 in the Operating Systems Earlier than Version 26 section under Age Ratings in App Store Connect.

[View age range value details](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-values) for Apple devices running a minimum of iOS 26, iPadOS 26, macOS Tahoe 26, tvOS 26, visionOS 26, and watchOS 26.

## Global age ratings

| Rating | Definition |
| --- | --- |
| 4+ | Apps with this rating contain no objectionable material. |
| 9+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 9: |
| 12+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 12: |
| 17+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 17: |
| Unrated | Apps with this rating may contain instances of the following content that can’t be published on the App Store. It may be published on alternative app marketplaces or websites: |

### Australia regional ratings

As required by [Australia’s guidelines for the classification of computer games](https://www.legislation.gov.au/F2023L01424/latest/text.), apps with Games as the primary or secondary category that have at least one of the following content descriptions will display an additional regional rating along with their Apple global age rating. The relevant regional rating will display on the App Store in Australia for iOS 18, macOS 15, tvOS 18, watchOS 11, and visionOS 2 or later.

| Content description | Region-specific rating |
| --- | --- |
| App that contains purchasable loot boxes |  |
| App with any instances of simulated gambling |  |

If we’re notified by the regulator that your app doesn’t meet their guidelines or requires a regional rating, you’ll receive a message from App Review. If you receive this message, follow the instructions and [re-submit your app for review](/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review).

### Brazil regional ratings

As required by the Brazilian Ministry of Justice and Public Security (MJSP), the App Store uses a different set of regional rating pictograms and descriptors for self-rated apps, than for ratings officially issued by the MJSP.

Official Brazil regional ratings apply to apps that were issued an official rating and/or descriptors by the MJSP. If a rating or descriptor has been issued to your app by the MJSP, Apple will update your regional rating and/or descriptors on your behalf. The updated regional rating will display on the App Store in Brazil for iOS 16.2, iPadOS 16.2, macOS 13.1, and tvOS 16.2, or later.

Possible values for official Brazil age pictograms are:

Possible values for self-rated Brazil age pictograms are:

### France regional rating

As required by the Agence Nationale des Fréquences ("ANFR"), apps with a 17+ Apple global age rating will display an additional regional rating of 18+ on the App Store in France for iOS 18, macOS 15, tvOS 18, watchOS 11, and visionOS 2 or later.

### Republic of Korea regional ratings

[As required by the Korean Games Rating and Administration Committee(GRAC)](https://www.grac.or.kr/english/), apps in the Games or Entertainment categories (primary or secondary) and/or apps with Frequent/Intense instances of Simulated Gambling will display an additional regional rating along with their Apple global age rating. The relevant regional rating will display on the App Store in Republic of Korea for iOS 18, macOS 15, tvOS 18, watchOS 11, and visionOS 2 or later.

Possible values for Korea regional ratings are:

| Apple global age ratings | Region-specific rating |
| --- | --- |
| 4+ |  |
| 9+ |  |
| 12+* |  |

* The GRAC may issue a KR-15 regional rating with an updated pictogram, or text that indicates KR-19 regional age rating for some apps.

**Note:** You’ll receive a message from App Review if the [Korean Games Rating and Administration Committee(GRAC)](https://www.grac.or.kr/english/) issues an official rating for your app that is different from your app’s age rating. If you receive this notice, follow the instructions in the [override age rating for Korea](/help/app-store-connect/manage-app-information/set-an-app-age-rating/#override-region-specific-ratings) section and re-submit your app for review.

**Related** [Set an app age rating](/help/app-store-connect/manage-app-information/set-an-app-age-rating) [App information](/help/app-store-connect/reference/app-information/app-information) [Platform version information](/help/app-store-connect/reference/app-information/platform-version-information)
