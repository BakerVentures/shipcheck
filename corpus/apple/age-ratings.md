---
shipcheck_source_id: age-ratings
title: "Age ratings values and definitions"
url: https://developer.apple.com/help/app-store-connect/reference/age-ratings
final_url: https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions
fetched_at: 2026-09-04T16:10:02+00:00
sha256: a7c233f6e11dcf54360c325b548b6bdc80ec8655bdb8e25417611752bf5aaac1
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
| In-App Controls | **Parental Controls:** Settings or tools that allow parents/guardians to monitor, manage, or restrict a child's access to in-app content or features that may not be suitable. *May include: tools to enable content blocking or filtering; setting usage limits; or restrictions on using certain features, such as making purchases or using communication features.* **Age Assurance:** Mechanism to confirm an individual's age meets the age requirement for accessing specific content or services. *May include: declared age range API; age estimation capabilities; age verification via government-issued passport, drivers license, national ID, or other means of age assurance.* |
| Capabilities | **Unrestricted Web Access:** Users can navigate to any webpage within the app or freely browse the web. *May include: embedded browser functionality or browser app.* **User-Generated Content:** Includes the broad distribution of content created by users as a component of the app's intended user experience. *May include: broadly distributed videos, photos, text, and/or audio created by users of the app.* **Social Media:** Redistribution, amplification, or interaction with user-generated content through a social feed or similar discovery method that visibly spreads content to many users. *May include: feeds that allow users to engage with and amplify user-generated content through features such as views, likes, comments, and shares.* **Social Media Disabled for Users Under 13:** Users under 13 don't have access to social media capabilities. At a minimum, the [Declared Age Range API](https://developer.apple.com/documentation/declaredagerange) is called to check users' age ranges before enabling social media features. Only age-appropriate UGC is delivered. **Messaging and Chat:** Users can directly communicate with one another through features within the app. *May include: text, voice and/or video chat, direct and/or group messaging, or public posting.* **Advertising:** Paid promotion of products or services within the app. *May include: banner ads, video and playable ads, rich media ads, or native ad formats.* |
| Mature Themes | **Profanity or Crude Humor:** Offensive or vulgar language that may be considered rude, obscene, or inappropriate. *May include: swearing, derogatory slurs, insult-based humor, or jokes about bodily functions.* **Horror/Fear Themes:** Content or storylines that evoke feelings of anxiety, dread, or terror. *May include: supernatural or psychological elements; body horror; or fear of the unknown, isolation, or death.* **Alcohol, Tobacco, or Drug Use or References:** References to or depictions of the consumption of alcohol, tobacco products, or other licit or illicit substances. *May include: drunken behavior, cigarette smoking, or the taking of illegal drugs.* |
| Medical or Wellness | **Medical or Treatment Information:** Content that provides diagnoses or guidance around the management of medical conditions or health and wellness. *May include: medication guidance, emergency medical care, or treatment information.* **Health or Wellness Topics:** Content that provides self-care or lifestyle recommendations. *May include: calorie tracking, dieting advice, or exercise recommendations.* |
| Sexuality or Nudity | **Mature or Suggestive Themes:** Content that implies or indirectly references sexual or mature topics without being explicit or topics for older audiences due to the complex, intense, or sensitive nature, which may deal with real-world issues or content unsuitable for children. *May include: sexual innuendo, sensual or suggestive imagery, censored or implied nudity, real-world crimes, psychological trauma or abuse, moral or ethical dilemmas, or war or political strife.* **Sexual Content or Nudity:** Non-explicit depictions of sexual behavior, including brief or partial nudity. *May include: mild romantic intimacy, implied sexual activity, or erotic or sensual dialog.* **Graphic Sexual Content and Nudity:** Explicit, detailed depictions of sexual activity or nudity. *May include: uncensored or full-frontal nudity; realistic, illustrative, or pornographic portrayals of sex.* |
| Violence | **Cartoon or Fantasy Violence:** Physical conflict or harm of an exaggerated or fantastical nature that can easily be distinguished from real life. *May include: animated magic used to harm animals or animated human wrestling.* **Realistic Violence:** Aggressive physical conflict or harm involving humans in lifelike situations. *May include: a bloody nose from being punched, a shoot-out, or combat between characters.* **Prolonged Graphic or Sadistic Realistic Violence:** Prolonged detailed or realistic-looking depictions of physical conflict. *May include: realistic and/or extreme depictions of gore, human injury, or death.* **Guns or Other Weapons:** References to or depictions of guns, weapons, or objects that may cause bodily harm. *May include: guns, swords, or knives.* |
| Chance-Based Activities | **Gambling:** Betting or wagering using real money or in-game currency that may be exchanged for real money. *May include: casino or card games, sports and non-sports betting, or lotteries and raffles.* **Simulated Gambling:** Betting or wagering without using real money or in-game currency that can be exchanged for real money. **Contests:** Events that allow users to compete with one another for rankings, rewards, or the achievement of personal goals. *May include: skill-based competitions, trivia quizzes, or sport or fitness contests* **Loot Boxes:** Virtual containers that provide players with randomized virtual items for purchase. *May include: randomized functional cards or cosmetic items for purchase.* |

### Age rating values

These ratings apply to all regions that don’t have any additional regional requirements.

Learn about age rating values with region-specific requirements for [Australia](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#australia-age-rating-values), [Brazil](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#brazil-age-rating-values), and [Korea](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#republic-of-korea-age-rating-values).

| Rating | Definition |
| --- | --- |
| 4+ | Apps with this rating contain no objectionable material but may contain instances of the following content that may not be suitable for children under the age of 4: **In-App Controls:** Parental controls Age assurance **Capabilities:** User-generated content Messaging and chat Advertising **Chance-Based Activities:** Infrequent contests |
| 9+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 9: **Mature Themes** Infrequent profanity and crude humor Infrequent horror or fear themes **Medical or Wellness** Health and wellness topics **Sexuality or Nudity** Infrequent mature or suggestive themes **Violence** Infrequent cartoon or fantasy violence Infrequent guns or other weapons **Chance-Based Activities** Loot boxes |
| 13+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 13: **Capabilities:** Social media Social media disabled for users under 13 **Mature Themes:** Frequent profanity and crude humor Frequent horror or fear themes Infrequent alcohol, tobacco, or drug use or references **Medical or Wellness:** Infrequent medical or treatment information **Sexuality or Nudity:** Infrequent sexual content or nudity **Violence:** Frequent cartoon or fantasy violence Infrequent realistic violence Frequent guns or other weapons **Chance-Based Activities:** Infrequent simulated gambling Frequent contests |
| 16+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 16: **Capabilities:** Unrestricted web access **Medical or Wellness:** Frequent medical or treatment information **Sexuality or Nudity:** Frequent mature or suggestive themes |
| 18+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 18: **Mature Themes:** Frequent alcohol, tobacco, or drug use or references **Sexuality or Nudity:** Frequent sexual content or nudity **Violence:** Frequent realistic violence **Chance-Based Activities:** Gambling Frequent simulated gambling |
| Unrated | Apps with this rating may contain instances of the following content that can’t be published on the App Store. It may be published on alternative app marketplaces or websites: **Sexuality or Nudity:** Infrequent or Frequent graphic sexual content and nudity **Violence:** Infrequent or Frequent prolonged graphic or sadistic realistic violence |

### Australia age rating values

As required by [Australia’s guidelines for the classification of computer games](https://www.legislation.gov.au/F2023L01424/latest/text), apps that have at least one of the following content descriptors will display the regional region-specific age rating.

**Note:** Only the age rating values listed below differ from the [age rating values](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-values).

| Rating | Definition |
| --- | --- |
| 16+ | Apps that contain: **Capabilities:** Social media Social media disabled for users under 13 **Chance-Based Activities:** Loot boxes |
| R 18+ | Apps that contain: **Chance-Based Activities:** Infrequent simulated gambling |

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
| AL | Apps that contain no objectionable material but may contain instances of the following content: **In-App Controls:** Parental controls Age assurance |
| A6 | Apps that contain: **Capabilities:** User-generated content **Violence:** Infrequent cartoon or fantasy violence **Chance-Based Activities:** Infrequent contests |
| A10 | Apps that contain: **Mature Themes:** Infrequent profanity and crude humor Infrequent horror or fear themes **Medical or Wellness:** Health and wellness topics **Violence:** Infrequent guns or other weapons |
| A12 | Apps that contain: **Capabilities:** Advertising Messaging and chat **Mature Themes:** Frequent profanity and crude humor **Medical or Wellness:** Infrequent medical or treatment information **Sexuality or Nudity:** Infrequent mature or suggestive themes Infrequent sexual content or nudity **Violence:** Frequent cartoon or fantasy violence Infrequent realistic violence Frequent guns or other weapons **Chance-Based Activities:** Infrequent simulated gambling |
| A14 | Apps that contain: **Mature Themes:** Frequent horror or fear themes Infrequent alcohol, tobacco, or drug use or references |
| A16 | Apps that contain: **Capabilities:** Unrestricted web access Infrequent guns or other weapons Social media Social media disabled for users under 13 **Mature Themes:** Frequent alcohol, tobacco, or drug use or references **Medical or Wellness:** Frequent medical or treatment information |
| A18 | Apps that contain: **Sexuality or Nudity:** Frequent mature or suggestive themes Frequent sexual content or nudity **Violence:** Frequent realistic violence **Chance-Based Activities:** Frequent gambling Frequent simulated gambling Loot boxes |

### Republic of Korea age rating values

For all apps made available in Korea, the following region-specific rating values will display:

**Note:** Apps and games with Frequent or Intense simulated gambling content are only available on the App Store in Korea if you provide a Rating Classification Number (RCN).

| Rating | Definition |
| --- | --- |
| All | Apps that contain: **In-App Controls:** Parental controls Age assurance **Capabilities:** User-generated content Messaging and chat Advertising **Mature Themes:** Infrequent profanity and crude humor Infrequent horror or fear themes **Medical or Wellness:** Health or wellness topics **Sexuality or Nudity:** Infrequent mature or suggestive themes **Violence:** Infrequent cartoon or fantasy violence Infrequent guns or other weapons **Chance-Based Activities:** Infrequent contests Loot boxes |
| 12+ | Apps that contain: **Mature Themes:** Frequent profanity and crude humor Frequent horror or fear themes Infrequent alcohol, tobacco, or drug use or reference **Medical or Wellness:** Infrequent medical or treatment information **Sexuality or Nudity:** Frequent mature or suggestive themes Infrequent sexual content or nudity **Violence:** Frequent cartoon or fantasy violence Infrequent realistic violence Frequent guns or other weapons **Chance-Based Activities:** Infrequent simulated gambling |
| 15+ | Apps that contain: **Capabilities:** Unrestricted web access Social media Social media disabled for users under 13 **Medical or Wellness:** Frequent medical or treatment information |
| 19+ | Apps that contain: **Mature Themes:** Frequent alcohol, tobacco, or drug use or references **Sexuality or Nudity:** Frequent sexual content or nudity **Violence:** Frequent realistic violence **Chance-Based Activities:** Frequent simulated gambling |

**Note:** You’ll receive a message from App Review if the [Korean Games Rating and Administration Committee(GRAC)](https://www.grac.or.kr/english/) issues an official rating for your app that is different from your app’s age rating. If you receive this notice, follow the instructions in the [override age rating for Korea](/help/app-store-connect/manage-app-information/set-an-app-age-rating/#override-region-specific-ratings) section and re-submit your app for review.

### Vietnam age rating values

As required by Article 38 of Vietnam Decree 147, apps that have at least one of the following content descriptors will display the region-specific age rating.

| Rating | Definition |
| --- | --- |
| 00+ | Apps with this rating contain no objectionable material but may contain instances of the following content: **In-App Controls:** Parental controls Age assurance **Capabilities:** User-generated content Messaging and chat Advertising **Chance-Based Activities:** Infrequent contests |
| 12+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 12: **Mature Themes:** Infrequent profanity and crude humor Frequent profanity and crude humor Infrequent horror or fear themes Frequent horror or fear themes Infrequent alcohol, tobacco, or drug use or reference **Medical or Wellness:** Infrequent medical or treatment information Health and wellness topics **Sexuality or Nudity:** Infrequent mature or suggestive themes Infrequent sexual content or nudity **Violence:** Infrequent cartoon or fantasy violence Frequent cartoon or fantasy violence Infrequent guns or other weapons **Chance-Based Activities:** Frequent contests Loot boxes |
| 16+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 16: **Capabilities:** Unrestricted web access Social media Social media disabled for users under 13 **Medical or Wellness:** Frequent medical or treatment information **Sexuality or Nudity:** Frequent mature or suggestive themes **Violence:** Infrequent realistic violence Frequent guns or other weapons **Chance-Based Activities:** Infrequent simulated gambling |
| 18+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 18: **Mature Themes:** Frequent alcohol, tobacco, or drug use or references **Sexuality or Nudity:** Frequent sexual content or nudity **Violence:** Frequent realistic violence **Chance-Based Activities:** Frequent simulated gambling Gambling |

## Age ratings on OS versions earlier than 26

The age rating is a required [app information](/help/app-store-connect/reference/app-information/app-information) field used for parental controls. These controls enable parents and guardians to establish a safe online environment for children. As a developer, you can deliver age-appropriate experiences tailored for users across all age groups. [Learn more about how parents approve what kids buy with ask to buy.](https://support.apple.com//105055)

View the age ratings that'll be displayed for Apple devices running an earlier OS version than 26 in the Operating Systems Earlier than Version 26 section under Age Ratings in App Store Connect.

[View age range value details](/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions#age-rating-values) for Apple devices running a minimum of iOS 26, iPadOS 26, macOS Tahoe 26, tvOS 26, visionOS 26, and watchOS 26.

## Global age ratings

| Rating | Definition |
| --- | --- |
| 4+ | Apps with this rating contain no objectionable material. |
| 9+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 9: Infrequent or mild cartoon or fantasy violence Infrequent or mild profanity or crude humor Infrequent or mild mature, suggestive, or horror or fear themed |
| 12+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 12: Infrequent or mild medical or treatment-focused content Infrequent or mild references to alcohol, tobacco, or drug use Infrequent or mild sexual content or nudity Frequent or intense contests Frequent or intense profanity or crude humor Frequent or intense horror or fear themed content Frequent or intense cartoon or fantasy violence Infrequent or mild occurrences of realistic violence Infrequent or mild simulated gambling |
| 17+ | Apps with this rating may contain instances of the following content that may not be suitable for children under the age of 17: Unrestricted web access, such as with an embedded browser Gambling Frequent or intense simulated gambling Frequent or intense mature or suggestive content Frequent or intense medical or treatment-focused content Frequent or intense references to alcohol, tobacco, or drug use Frequent or intense sexual content or nudity Frequent or intense realistic violence |
| Unrated | Apps with this rating may contain instances of the following content that can’t be published on the App Store. It may be published on alternative app marketplaces or websites: Infrequent or mild graphic sexual content and nudity Frequent or intense graphic sexual content and nudity Infrequent or mild prolonged graphic or sadistic realistic violence Frequent or intense prolonged graphic or sadistic realistic violence |

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
