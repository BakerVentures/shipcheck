<!-- source=data-safety clause=import-or-export-your-form-responses url=https://support.google.com/googleplay/android-developer/answer/10787469 fetched=2026-09-05T02:02:36+00:00 -->

### Import or export your form responses

You can export your form responses to a CSV file. You can also download a sample CSV, complete the form offline, and import your completed form from the CSV.

[Click here to download a sample CSV](//storage.googleapis.com/support-kms-prod/b5v9It2EgwrgyY1gPFVB3jPUypc5lL3oNg2G).

Understand the CSV format

The CSV contains one row per response. Responses for multiple choice and single choice questions span multiple rows, matching the number of available choices. To respond to a question, enter TRUE or FALSE in the corresponding cell in the "Response value" column, or you can leave the cell blank if the question is optional or you're responding to a multiple choice question. The column "Answer requirement" indicates whether or not a response is mandatory, and can contain the following values:

- **OPTIONAL:** Not required — can be left blank.
- **REQUIRED:** Mandatory — you must provide a response value
- **MULTIPLE_CHOICE:** You can provide a response value of TRUE to at least one of the response choices for the corresponding question ID. You can leave other responses blank.
- **SINGLE_CHOICE:** You can provide a response value of TRUE to one of the response choices for the corresponding question ID. You can leave other responses blank.
- **MAYBE_REQUIRED:** You only required when certain conditions are met, e.g. based on the answer to a previous question

The table below provides an example for the “Name” and “Approximate location” sections of the Data safety form. It contains:

- A multiple choice question
- A required question
- An optional question

| **Question ID  (machine readable)** | **Response  (machine readable)** | **Response value** | **Answer requirement** | **Human-friendly question label** |
| --- | --- | --- | --- | --- |
| PSL_DATA_  TYPES_  PERSONAL | PSL_NAME | TRUE | MULTIPLE_  CHOICE | Personal info  Name |
| ... |  |  |  |  |
| PSL_DATA_  TYPES_  LOCATION | PSL_  APPROX_  LOCATION | TRUE | MULTIPLE_  CHOICE | Location  Approximate location |
| ... |  |  |  |  |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  PSL_DATA_USAGE_  COLLECTION_AND_  SHARING | PSL_DATA_  USAGE_ONLY_  COLLECTED | TRUE | MULTIPLE_  CHOICE | Data usage and handling (Name)  Is this data collected, shared, or both?  Collected |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  PSL_DATA_USAGE_  COLLECTION_AND_  SHARING | PSL_DATA_  USAGE_ONLY_  SHARED |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Is this data collected, shared, or both?  Shared |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  PSL_DATA_USAGE_  EPHEMERAL |  | TRUE | MAYBE_  REQUIRED | Data usage and handling (Name)  Is this data processed ephemerally? |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_USER_  CONTROL | PSL_DATA_  USAGE_USER_  CONTROL_  OPTIONAL | TRUE | SINGLE_  CHOICE | Data usage and handling (Name)  Is this data required for your app, or can users choose whether it's collected?  Users can choose whether this data is collected |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_USER_  CONTROL | PSL_DATA_  USAGE_USER_  CONTROL_  REQUIRED |  | SINGLE_  CHOICE | Data usage and handling (Name)  Is this data required for your app, or can users choose whether it's collected?  Data collection is required (users can't turn off this data collection) |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_APP_  FUNCTIONALITY | TRUE | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  App functionality |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_ANALYTICS | TRUE | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  Analytics |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_DEVELOPER_  COMMUNICATIONS |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  Developer communications |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_FRAUD_  PREVENTION_  SECURITY |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  Fraud prevention, security, and compliance |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_ADVERTISING |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  Advertising or marketing |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_  PERSONALIZATION |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  Personalization |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  COLLECTION_  PURPOSE | PSL_ACCOUNT_  MANAGEMENT |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data collected? Select all that apply.  Account management |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_APP_  FUNCTIONALITY |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  App functionality |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_ANALYTICS |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  Analytics |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_DEVELOPER_  COMMUNICATIONS |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  Developer communications |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_FRAUD_  PREVENTION_  SECURITY |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  Fraud prevention, security, and compliance |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_  ADVERTISING |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  Advertising or marketing |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_  PERSONALIZATION |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  Personalization |
| PSL_DATA_USAGE_  RESPONSES:  PSL_NAME:  DATA_USAGE_  SHARING_  PURPOSE | PSL_ACCOUNT_  MANAGEMENT |  | MULTIPLE_  CHOICE | Data usage and handling (Name)  Why is this user data shared? Select all that apply.  Account management |

Export to a CSV file

1. Open Play Console and go to the [**App content**](https://play.google.com/console/app/app-content/summary) page.
2. Under "Data safety," select **Start**.
3. Near the top right of the page, select **Export to CSV**.

Import from a CSV file

**Important:** Answers already entered into your form will be overwritten when you import a CSV.

1. Open Play Console and go to the [**App content**](https://play.google.com/console/app/app-content/summary) page.
2. Under "Data safety," select **Start**.
3. Near the top right of the page, select **Import to CSV**.
