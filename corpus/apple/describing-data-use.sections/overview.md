<!-- source=describing-data-use clause=overview url=https://developer.apple.com/documentation/bundleresources/describing-data-use-in-privacy-manifests fetched=2026-09-03T19:56:58+00:00 -->

## Overview

Record the categories of data that your app or third-party SDK collects about the person using the app, and the reasons it collects the data. App developers can use Xcode to create a privacy report, summarizing the information about collected data in their app and the third-party SDKs the app links to.

> **Important:** Third-party SDKs need to provide their own privacy manifest files that record the types of data they collect. Your app’s privacy manifest file doesn’t need to cover data collected by third-party SDKs that your app links to.
