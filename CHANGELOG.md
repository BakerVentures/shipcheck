# Changelog

## v0.2.22: five false positives from the 27-app portfolio sweep (2026-10-13)

The sweep found 0 true positives and 5 false positives; fixed at the cause.

- Comments no longer count. JS/TS `//` and `/* */` comments are stripped before any
  source search, so "never behind a paywall" in a comment is not a paywall signal
  (Stillmoor; it also cleared a comment-driven `IAP-ATTACH-SUBMISSION`).
- `PROMISE-FREE-BUT-SELLS` now needs an IAP/purchases SDK in `dependencies` AND a
  purchase call (purchasePackage, getOfferings, requestPurchase, Stripe sheet, ...)
  reachable from a routed screen: for expo-router, files under `app/` or `src/app/`
  plus anything they import. `Purchases.configure()` alone is not a sale. A dormant
  `pricing.ts` or unrouted `PaywallScreen` with no SDK (DenialDesk) or an unreached
  wrapper (MileTruth) no longer fires. Where routing cannot be established (not
  expo-router) it still fires but at `low` confidence instead of `medium`.
- `CLAIM-UNBACKED-*` skips a capability phrase when no/never/without/not/doesn't
  precedes it in the same sentence (PlateRamp, Slowbend). A separate un-negated
  mention still fires.
- Selftest: 104 -> 122 offline checks. The old MileTruth positive (a bare
  `Purchases.configure` file, no package.json) was replaced by three reachable-paywall
  positives, since that shape is exactly what is now suppressed.

## v0.2.21: specific promises, checked one at a time (2026-10-13)

v0.2.18's `CLAIM-UNBACKED-*` asks "does the code contain any implementation of
feature X". Several of the nine rejections were promises specific enough to check
against one named thing. New `check_concrete_promises` (all `PROMISE-*` ids) fires
only when it can name the missing thing:

- `PROMISE-TRIAL-UNBACKED` (3.1.2): a trial in the listing or notes that the
  Subscriptions section denies, states with a different length, or that has no
  trial/introductory-offer shape in source (Rigsheet, FlirtGym).
- `PROMISE-FREE-TIER-UNBACKED`, `PROMISE-FREE-BUT-SELLS`: "free plan" against a hard
  paywall; "no in-app purchases" against shipped purchase code (FlirtGym).
- `PROMISE-LIFETIME-UNBACKED`, `PROMISE-PRICE-MISMATCH`: a lifetime purchase no
  product or allowlist in source will sell; a listing price absent from the
  Subscriptions section (Nearvo).
- `PROMISE-UI-MISSING-<name>`: a quoted button/screen the review notes tell the
  reviewer to use that is not a string, route or filename in shipping source
  (DenialDesk).
- `PROMISE-POPULATED-STATE`: notes describe a populated list while the app shows an
  empty state and nothing seeds (TentClock).
- `PROMISE-PROGRESS-NO-WRITER`: "saved progress" whose only writer is a
  screenshot/seed/dev file (Foldbook).
- `PROMISE-SIGNIN-NO-AUTH`: notes say to sign in; the app has no sign-in.

IOLTAlign's sample account was already covered by `CLAIM-PHANTOM-seeded-data`.
Run against the real portfolio repos, it found one true positive (MileTruth's
listing says "no in-app purchases" while a RevenueCat paywall ships) and one false
positive (HormoneLog: "Monthly: no trial" beside "Annual: 14-day free trial"),
fixed and pinned by a regression test. 17 new selftest cases, 7 of them negatives.

## v0.2.19: permission timing (2026-10-13)

Nine apps from one developer's portfolio were rejected by App Review in a single
batch. Three apps from the same portfolio passed review in the same window. One of
those passes, FlipStage, cleared review 81 seconds after one of the rejections,
TentClock, off the same code scaffold. Close enough in time and similar enough in
code that the difference between them was worth reading closely.

The difference: TentClock asked for location permission the moment its one screen
rendered, before the user had tapped anything or been told why. FlipStage asks for
photo library access from inside the button that needs it, with a sentence
explaining what it's for. Guideline 5.1.1 calls this data minimization: ask for what
you need, when you need it, not on the way in the door.

**New check: `PERM-REQUEST-ON-MOUNT`.** Finds a sensitive permission request
(location, notifications, camera, photo library, microphone, contacts, tracking)
called unconditionally inside a `useEffect` with an empty dependency array, React's
"run once, on mount" shape. That is the exact pattern TentClock shipped and FlipStage
didn't. Verified against both real repos at the real commits: fires on TentClock's
code before the fix, silent after, silent on FlipStage.

**New check: `NOTIF-PERMISSION-NEVER-SCHEDULED`.** A notification permission is
requested somewhere in the app, but nothing anywhere in the source ever schedules or
sends one. A reviewer who grants the permission and waits for something that never
arrives has a concrete basis to reject, and it's dead weight even when they don't.

Both checks default to silence on a permission that's declared but never called at
all. A library pulling in an API your code never touches is a different, narrower
problem (there's an existing check for that), and flagging it here would confuse it
with the timing question these two checks actually answer.

Independently re-run against a second batch of the same nine apps, separately from
the work that found the pattern in the first place: one fires, eight don't, and
neither of the two apps that passed review fires either. A rule that flagged a
submission Apple already approved would be worse than no rule.

## v0.2.18: the listing doesn't match the binary (2026-10-13)

Four of those same nine rejections had a different shape: the store listing, or the
notes left for the App Review team, described something the shipped code didn't do.
A push-notification feature with the code to register for one but nothing that ever
sent it. A review note pointing the reviewer at a seeded demo account that no code
anywhere created. A privacy policy page that still called the product "a working
name, the final app name is not yet chosen," written before launch, never updated,
sitting on the live listing weeks after a rejection that should have prompted someone
to re-read it.

None of that is visible to a tool that only reads code, because none of it is a code
defect. It's a mismatch between two things that are supposed to agree: what you told
Apple, and what you shipped.

**New checks:** `CLAIM-UNBACKED-*` (ten categories: notifications, background
location, import/export, cloud sync, biometric lock, camera, and others, each tied to
a real example from this batch) matches a claim in your store listing against the
source that would have to back it up. `CLAIM-PHANTOM-*` does the same against your
App Review notes specifically, for claims made to the reviewer rather than the buyer.
`LISTING-URL-PLACEHOLDER-*` fetches the privacy/support/marketing pages linked from
your listing and checks the page content itself, not just whether the link resolves.
The placeholder-name page above is a real example of a dead-link check missing a live
one.

**A bug found while building this, not by looking for one.** Running the new checks
against a real `shipcheck.metadata.md` turned up a page that answers with HTTP 308
Permanent Redirect, the normal way Cloudflare and most static-site hosts handle an
apex-to-www address. Python's standard library has never followed 308 redirects. The
dead-link check shipped before this release read that redirect as a confirmed-dead
URL and would have raised a critical finding against a page that opens fine in any
browser. Fixed for every app, not just the one that found it: any project behind a
normal redirect was at risk of this false positive before today.

## Earlier releases

- **v0.2.17.** Stopped flagging a correctly-configured privacy manifest as missing
  when it's declared in config but not yet generated on disk.
- **v0.2.16.** A truncated source search no longer compounds into a false critical
  finding.
- **v0.2.15.** A dead network response is no longer treated the same as a confirmed
  HTTP error when deciding whether a URL is actually dead.
- **v0.2.14.** Applied the v0.2.13 call-site detection fix to the in-app-purchase
  restore-purchases check.
- **v0.2.13.** Stopped flagging an auth SDK as a live obligation just because it's a
  dependency. Now looks for a real call site.
- **v0.2.12.** Fixed a false-critical bug in the metadata parser.
- **v0.2.11.** Fixed a content-duplication bug in the HTML-to-markdown converter,
  added a verified judgment pattern.
- **v0.2.10 and earlier.** Initial checks for privacy manifests, required-reason
  APIs, usage-description strings, Sign in with Apple, subscription terms, account
  deletion, and the Android equivalents. The policy corpus fetcher and its weekly
  refresh. The GitHub Action. Full history in `git log`.
