<!-- source=prepare-for-release clause=clean-up-your-project-directories url=https://developer.android.com/studio/publish/preparing fetched=2026-09-04T15:48:37+00:00 -->

### Clean up your project directories

Clean up your project and make sure it conforms to the directory structure
described in [Projects overview](/tools/projects#ApplicationProjects).
Leaving stray or orphaned files in your project can prevent your app from
compiling and cause your app to behave unpredictably. At a minimum, perform the
following cleanup tasks:

- Review the contents of your `cpp/`, `lib/`, and
- Check your project for private or proprietary data files that your app
- Check your `lib/` directory for test libraries and remove them if they are no
- Review the contents of your `assets/` directory and your
