<!-- source=prepare-for-release clause=prepare-external-servers-and-resources url=https://developer.android.com/studio/publish/preparing fetched=2026-09-04T07:14:15+00:00 -->

## Prepare external servers and resources

If your app relies on a remote server, make sure the server is secure and that
it is configured for production use. This is particularly important if you are
implementing [in-app billing](/google/play/billing) in
your app and you are performing the signature verification step on a remote
server.

Also, if your app fetches content from a remote server or a real-time service
(such as a content feed), be sure the content you are providing is up to date
and production ready.
