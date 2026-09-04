<!-- source=prepare-for-release clause=turn-off-logging url=https://developer.android.com/studio/publish/preparing fetched=2026-09-04T07:14:15+00:00 -->

### Turn off logging

Deactivate logging before you build your app for release. You can deactivate
logging by removing calls to `[Log](/reference/android/util/Log)` methods in your source
files. Also, remove any log files or static test files that were created in
your project.

Also, remove all `[Debug](/reference/android/os/Debug)`
tracing calls that you added to your code, such as
[`startMethodTracing()`](/reference/android/os/Debug#startMethodTracing())
and
[`stopMethodTracing()`](/reference/android/os/Debug#stopMethodTracing())
method calls.

**Important:** Ensure that you disable
debugging for your app if using [`WebView`](/reference/android/webkit/WebView) to display
paid content or if using JavaScript interfaces, because debugging lets users
inject scripts and extract content using Chrome DevTools. To disable
debugging, use the
[`WebView.setWebContentsDebuggingEnabled()`](/reference/android/webkit/WebView#setWebContentsDebuggingEnabled(boolean))
method.
