# Changelog

## Unreleased: `gate app <repo>` — one command per app (2026-10-15)

`gate check` answers "is THIS artifact fit to submit?" and needs the `.app`
path, which means the caller has to find it first. A caller who guesses wrong
gets a confident verdict on the wrong binary, and that is not hypothetical:
running the published per-app command at the root of the `rigsheet` monorepo
made `expo prebuild` treat the root as an Expo app and would have produced a
binary called `rigsheet.app` **that is not Rigsheet**. A verdict would have
been published for an app that does not exist.

`gate app <repo>` takes the repo, finds every artifact under it, and renders
`check` for each. It adds **no new rule** — the rules stay in `shipgate.py`
and the exit status comes from `shipgate.blocking_findings`, the single
definition added below. A fifth inline `severity == "critical"` comparison in
a new entry point would have reintroduced the exact bug that fix exists for.

Three states, three exit codes, because collapsing any two of them is how
"not checked" gets read as "clean":

| | |
|---|---|
| `0` | evaluated and fit |
| `1` | evaluated and blocked |
| **`2`** | **NOT CHECKED — nothing is built, so no binary rule ran at all** |

It does not build for you. A gate that silently builds changes its own
subject, and on 2026-10-15 a session rebuilt an app mid-task and destroyed the
binary a finding rested on.

**Two binaries, one version+build.** If a repo holds more than one artifact,
all of them are evaluated and none is chosen, and the output is keyed on
`LC_UUID`. Two binaries have carried the identical version and build stamp on
this machine twice in one day, and a launch proof earned on one was accepted
for the other. There is an assertion for exactly this: one version+build, two
UUIDs, and the defective twin drags the exit status to 1 so a fit sibling
cannot vouch for it.

**Proven by mutation, not by inspection.** Ten new assertions in
`scripts/selftest_gate.py::test_gate_app_entrypoint`, every one of which runs
`bin/shipcheck` **as a subprocess** and asserts on nothing but the return code.
Both directions were run:

- revert the no-artifact branch to `return 0` → **2 assertions fail, suite
  exits 1**.
- revert `BLOCKING_SEVERITIES` to `("critical",)` → **7 assertions fail**, two
  of them the new `gate app` ones, suite exits 1.
- restore either → **131 checks, all pass, exit 0**.

The must-not-fire case is there too: a fit binary with its receipts in order
exits 0, so "always fail" would not have passed.

### Note on branches, since the rules briefly lived on two

`fix/gate-purpose-string-coverage-2026-10-15` and
`fix/gate-exit-status-2026-10-15` both carry the privacy-manifest and
purpose-string rules, after a session swept the first branch's work into the
second's commit. They are **not** divergent: verified with
`git merge-base --is-ancestor`, the purpose-string branch is a strict ancestor
of the exit-status branch, which is 8 commits ahead of `master` and 0 behind.
So `fix/gate-exit-status-2026-10-15` is the superset and the only one that
needs landing; this work is branched from it rather than from `master`, so
landing it brings the exit-status fix with it. Landing the purpose-string
branch separately afterwards would be a no-op, not a revert.

## Unreleased: the gate's exit status, which read only `critical` (2026-10-15)

**A sweep over two genuinely defective repos printed six `high`
`BIN-FRAMEWORK-PURPOSE-STRING` findings and returned shell status 0.** Measured
on `~/steadychart-ios27-verify` and `~/policyready-ios27-scene`, whose binaries
link CoreLocation/CoreMotion with no purpose string — the ITMS-90683 that
bounced MileTruth build 3 at delivery, and the only rejection Apple has ever put
in writing. Every exit status in the gate was computed inline from
`severity == "critical"`, in four places, and that rule is `high`. Any CI step
or script reading `$?` called those repos clean. It went unnoticed because every
published sweep so far also contained a `GATE-NO-ARTIFACT` or a critical
`BIN-SCENE-NOT-ADOPTED`, so the 1 was always being earned by something else.

`gate check` had the same bug from the other side: on that binary it exits 1
only because its launch and stress receipts are missing. With the receipts in
order it was `REVIEW`, exit 0, with the defect intact — reproduced as a fixture
in `selftest_gate.py`.

- **`shipgate.BLOCKING_SEVERITIES = ("critical", "high")`**, with
  `blocking_findings()`, used by `gate check`, `gate sweep` and the `--json`
  exit status of both. One definition instead of four inline comparisons. The
  fix is the mapping, not a promotion: every `high` in this gate is either a
  refusal at upload (ITMS-90683, a reused build number, a missing icon or
  app privacy manifest) or an "I could not check" —
  `GATE-CANNOT-READ-LINKAGE`'s own fix text already said *"This blocks rather
  than passing"*, which it did not. `medium` and below are reported.
- **An SDK's own embedded privacy manifest drops from `high` to `medium`.** Its
  docstring already said "reported rather than blocking", and `high` would now
  contradict that and block on a finding whose only fix is someone else's
  release. Costs nothing: measured across 216 embedded manifests in six repos,
  zero findings.
- **`shipcheck scan` is unchanged.** It reads config, not the artifact, and has
  a documented `fail-on` knob defaulting to `critical`. The gate has no knob.
- **Regression test, and it runs `bin/shipcheck` as a subprocess.** Every
  existing assertion in `selftest_gate.py` called `gate_sweep()` / `gate_check()`
  in process and asserted on the returned dict; all 104 were green while the
  CLI exited 0. The exit status was never the subject of a test. The new
  `test_exit_status_mapping` asserts on nothing but `returncode`, on a fixture
  whose findings are deliberately high-only (SDK 26, so the critical scene rule
  is exempt and cannot earn the 1), and on a clean fixture that still carries a
  `medium` finding, so exit 0 is not merely "nothing was found".

## v0.3.0: the submission gate — binary evidence, a launch proof, a stress pass (2026-10-14)

ShipCheck was run across 27 of Ryan's repos on 2026-10-13. It produced 61 findings
and, by that sweep's own closing line, **0 true positives** — while eight of those
apps sat rejected. This release is the answer to why, and it is not a new rule.

**The config is not the artifact.** `scan.py:collect_info_plist()` walks `ios/` and
skips any path containing `build`, so the one file that actually ships — the built
`Info.plist` — is the one file the scanner had never read. And `ios/` is gitignored
CNG output in every one of these repos, so the scanner's view of the plist depended
on whether someone had run `expo prebuild` on that machine. That produced false
findings in both directions, and both happened:

- **False MISSING.** FlirtGym was reported missing `NSCameraUsageDescription`,
  `NSPhotoLibraryUsageDescription` and `NSUserTrackingUsageDescription`. All three
  are in the built binary, written at prebuild time by the `expo-image-picker` and
  `expo-tracking-transparency` config plugins. A worker spent a commit pinning a
  non-problem. A permission string is a property of the plugin graph, and only the
  build resolves the plugin graph.
- **False PRESENT.** TentClock's scene manifest exists only in an untracked `ios/`
  directory on one Mac. Every config-or-source read calls it adopted. No build on
  any other machine reproduces it.

### New: `shipcheck gate` (scripts/shipgate.py)

`scan` still reads config and source. `gate` reads the **built artifact** and requires
**proof it was run**. Nothing should be submitted until `gate check` passes.

- `gate inspect` — what the binary actually says: linked SDK and minos from
  `LC_BUILD_VERSION`, `LC_UUID`, the real scene delegate, embedded privacy manifests,
  bundled icon, `PlugIns/*.appex`.
- `gate check` — the verdict. Exit 1 blocked, 3 unevaluable, 0 cleared. "I could not
  check" never reads the same as "it is fine".
- `gate launch` — installs and launches on a simulator and **measures the first
  frame** (a stdlib PNG decoder over the screenshot). "It launched" is not "it drew
  something": a flat frame after the settle delay is a blank window, and a liveness
  check calls that a pass.
- `gate stress` — nine abuse patterns, each one a defect that really happened here.
  `--run` drives what simctl alone honestly can and prints the rest as still owed.
- `gate attest` — what no tool can do, required and signed: real hardware, a reviewer
  walkthrough, red-then-green on every fix, and each app extension exercised.

New binary rules, each from a real case:

- `BIN-SCENE-NOT-ADOPTED` — linked SDK ≥ 27 with no *named* scene delegate. An empty
  `UISceneConfigurations` is not adoption. **Nearvo's shipped 1.0.0+9 binary has
  exactly that**: the manifest is present and configures nothing.
- `BIN-FRAMEWORK-PURPOSE-STRING-*` — `otool -L` against the built plist's purpose
  strings. This is MileTruth build 3, rejected at delivery with **ITMS-90683**:
  `expo-location`'s precompiled XCFramework links CoreMotion unconditionally, so
  `motionUsagePermission: false` deleted the key and could not remove the linkage.
- `BIN-BUILD-NUMBER-REUSED` — a second, different binary at the same version+build.
  One FlirtGym submission died at **upload processing**, not review, over exactly
  this, and no review-focused check looks for it.
- `GATE-SCENE-PROVENANCE-UNTRACKED` — the artifact's safety is not reproducible from
  tracked config. This is the TentClock hole, and the existing
  `ios27-upload-gate.sh` passes TentClock with exit 0.
- `BIN-PRIVACY-MANIFEST-ABSENT`, `BIN-ICON-ABSENT`, `BIN-EXPORT-COMPLIANCE-MISSING`
  — all read from the bundle. The scanner's `node_modules` guess said "ShipCheck
  cannot tell" on 9 of 27 apps; in the bundle there is nothing to be unsure about.

### Receipts name the binary, not just the build number

`ios27-upload-gate.sh` keys receipts on `bundleid@version+build` and defends that at
length (you launch a sim build and upload a device build). The reasoning is right and
the key is not sound, as running it showed: a receipt earned on Vocabdrift's **fixed**
binary was applied to a **different** binary, same `1.0.1+3`, with no scene manifest
at all. Receipts now carry the launched binary's `LC_UUID` and a fingerprint of the
gate-relevant plist keys, and matching is three-valued — `exact`, `sibling` (different
binary, same build, keys agree: the legitimate sim→device case), `expired`. A build
number bump still expires everything.

### Tests: 57 checks, and red-then-green is enforced rather than advised

`scripts/selftest_gate.py`. Every rule has a **must-not-fire** case from a real app,
because a gate that blocks a good submission teaches everyone to skip it.

A green suite is not evidence: 2,115 Nearvo tests passed while the onboarding loop
App Review rejected was live and shipping, and the *first* regression test written for
that bug passed against the unfixed code. So for every rule this suite also builds the
fixture the rule is meant to **pass** and asserts silence — a rule that fires on both
is indistinguishable from one that always fires. The centrepiece is a real red/green
pair: `clang` builds a genuine Mach-O linked once against SDK 26 and once against
SDK 27, same absent manifest in both, and the scene rule must be silent on one and
fire on the other. Mocking `vtool` would have tested the mock.

Four bugs the tests found in the gate itself, each the gate's own failure mode:
a false CRITICAL on IOLTAlign (the provenance regex did not match JSON quoting); an
**unsatisfiable** requirement (`extension-exercised` demanded and then refused);
a **pass recorded for a permission denial that never happened** (`simctl privacy`
takes `revoke`, not `deny`, and every call had been failing silently); and fixtures
that were testing their own error path because a fixture salt was not a valid C
identifier.

### Honest about scope

`BIN-FRAMEWORK-PURPOSE-STRING-*` is `high`, not blocking: it fires on linkage, which
is what bounced MileTruth, but a linked framework is not proof of use. It was also
tightened by measurement — scanning every Mach-O in the bundle flagged
`Photos.framework` on half the Expo apps, always via `ExpoFileSystem`, so the rule now
reads only the app's own executable and each extension's. The gate cannot see App
Store Connect (Nearvo's one recorded rejection, 2.1(b), is a submission-assembly
fact), cannot see uploaded screenshots, and cannot take a single simulator off the
network. Those are required and recorded, not automated.

**A correction to this changelog's own record.** The v0.2.19 and v0.2.21 entries below
say "nine rejections". No file in the company enumerates nine apps. The accurate
figures are **eight apps currently in a rejected state** and **at least thirteen
distinct rejection events** once Nearvo's five-or-more and FlirtGym's two are counted
separately. Apple's notices for the batch of eight carried an **empty issues block**:
no guideline, no reason text. Seven of those reasons are unrecorded and unrecoverable
without Ryan's Apple sign-in, so this release makes no claim about which of them the
gate would have caught. What it catches is stated above and was measured. Standing
rule going with it: if an App Review citation is ever read, paste the **verbatim** text
into that app's decision log the same hour — the single surviving verbatim citation in
the whole corpus survives only because a human pasted it into a commit message.

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
