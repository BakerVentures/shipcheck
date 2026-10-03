<!-- source=prepare-for-release clause=kotlin url=https://developer.android.com/studio/publish/preparing fetched=2026-10-02T03:31:50+00:00 -->

### Kotlin

```
android{ ... buildTypes{ release{ isDebuggable=false ... } debug{ isDebuggable=true ... } } ... }
```
