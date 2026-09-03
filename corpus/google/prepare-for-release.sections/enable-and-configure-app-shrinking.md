<!-- source=prepare-for-release clause=enable-and-configure-app-shrinking url=https://developer.android.com/studio/publish/preparing fetched=2026-09-03T19:54:40+00:00 -->

### Enable and configure app shrinking

Many of the following optimizations can be automated by enabling [shrinking](/studio/build/shrink-code) for your release build. For
example, you can add ProGuard rules to remove log statements, and the shrinker
will identify and remove unused code and resources. The shrinker can also
replace class and variable names with shorter names to further reduce DEX
size.
