<!-- source=expo-apple-privacy clause=what-is-a-privacy-manifest url=https://docs.expo.dev/guides/apple-privacy/ fetched=2026-09-04T16:10:03+00:00 -->

## What is a privacy manifest?

A privacy manifest is a file named PrivacyInfo.xcprivacy that is included in your iOS native project. This file is used to declare why the app includes native code that calls into certain APIs that Apple considers sensitive.

These APIs currently include accessing UserDefaults, file timestamp, system boot time, disk space, and active keyboard. Apple considers it an open list that can be expanded in the future.
