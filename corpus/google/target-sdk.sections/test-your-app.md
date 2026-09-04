<!-- source=target-sdk clause=test-your-app url=https://developer.android.com/google/play/requirements/target-sdk fetched=2026-09-04T15:48:40+00:00 -->

## Test your app

After you update your app's API level and features as appropriate, you should
test some core use cases. The following suggestions are not exhaustive, but aim
to guide your testing process. We suggest testing:

- That your app compiles to API 29 without errors or warnings.
- That your app has a strategy for cases where the user rejects permission
  Go to your app's App Info screen, and disable each permission.
  Open the app and ensure no crashes.
  - Perform core use case tests and ensure required permissions are
- Handles Doze with expected results and no errors. Using adb, place your test device into Doze while your app is running.
  Using adb, place your test device into Doze while your app is running.
  - Test any use cases that trigger Firebase Cloud Messaging messages.
  - Test any use cases that use Alarms or Jobs.
  - Eliminate any dependencies on background services.
  Set your app into App Standby
  - Test any use cases that trigger Firebase Cloud Messaging messages.
  - Test any use cases that use Alarms.
- Handles new photos / video being taken Check that your app [handles the restricted](/topic/performance/background-optimization#media-broadcasts) [`ACTION_NEW_PICTURE`](/topic/performance/background-optimization#media-broadcasts) [and](/topic/performance/background-optimization#media-broadcasts) [`ACTION_NEW_VIDEO`](/topic/performance/background-optimization#media-broadcasts) broadcasts
  Check that your app [handles the restricted](/topic/performance/background-optimization#media-broadcasts) [`ACTION_NEW_PICTURE`](/topic/performance/background-optimization#media-broadcasts) [and](/topic/performance/background-optimization#media-broadcasts) [`ACTION_NEW_VIDEO`](/topic/performance/background-optimization#media-broadcasts) broadcasts
  correctly (that is, moved to JobScheduler jobs).
  Ensure that any critical use cases that depend on these events still
  work.
- Handles sharing files to other apps
  Test the content is visible in the other app and doesn't trigger
  crashes.
