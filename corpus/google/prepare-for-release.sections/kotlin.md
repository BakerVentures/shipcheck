<!-- source=prepare-for-release clause=kotlin url=https://developer.android.com/studio/publish/preparing fetched=2026-09-05T02:02:42+00:00 -->

### Kotlin

```
android{ ... buildTypes{ release{ isDebuggable=false ... } debug{ isDebuggable=true ... } } ... }
```
