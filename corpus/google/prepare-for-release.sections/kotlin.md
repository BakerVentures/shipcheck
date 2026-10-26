<!-- source=prepare-for-release clause=kotlin url=https://developer.android.com/studio/publish/preparing fetched=2026-10-26T13:10:23+00:00 -->

### Kotlin

```
android{ ... buildTypes{ release{ isDebuggable=false ... } debug{ isDebuggable=true ... } } ... }
```
