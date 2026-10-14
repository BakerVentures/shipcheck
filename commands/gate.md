---
name: gate
description: The pre-submission gate. Reads the BUILT binary, requires a launch proof and a stress pass, and blocks a submission that has no evidence behind it.
---

Run the ShipCheck submission gate on a built artifact.

`/shipcheck:scan` reads config and source. That is useful and it is not
sufficient: a 27-repo sweep of this portfolio produced 61 findings and zero true
positives while eight of those apps sat rejected, because nearly every real
defect lived in the **built binary** or in the **running app**. **The config is
not the artifact.**

Arguments: `$ARGUMENTS` — a path to a built `.app`, `.ipa` or `.xcarchive`. If
none is given, look for the newest one under the project (commonly
`ios/build/**/Build/Products/*-iphonesimulator/*.app`) and say which you picked.

## Steps

1. **Inspect the artifact.** Run:
   `python3 ${CLAUDE_PLUGIN_ROOT}/bin/shipcheck gate inspect <artifact> --project .`
   Report the linked SDK, the real scene delegate, the usage descriptions and any
   app extensions. Note out loud where these differ from `app.json` — that
   difference is the whole point, and it is where the false findings came from.

2. **Earn the launch proof** if there is none:
   `… gate launch <artifact> --project .`
   Build and launch for **iOS 26.5**, not 27: a binary built on this machine
   traps on launch on iOS 27 unless the app carries the UIScene fix. The gate
   confirms the process survived, that no crash report appeared, and that the
   first frame actually has pixels in it.

3. **Run the stress pass:** `… gate stress <artifact> --run --project .`
   It drives what `simctl` alone honestly can and then prints the patterns it
   did **not** drive. Those are still required. Drive them yourself — with
   Maestro if the project has flows, otherwise by hand — and record each:
   `… gate stress <artifact> --record <pattern> --result pass|fail|n/a --note "…"`
   An `n/a` needs a real reason. Do not record a pass for something you did not
   do; that is the failure this gate exists to stop, and it has already happened
   once inside the gate itself.

4. **Attestations.** `… gate attest <artifact> --item <item> --by "<name>" --note "…"`
   These are the things no tool can check: real hardware, a reviewer
   walkthrough, red-then-green on every fix in the build, and each app extension
   exercised. If you cannot honestly attest one, say so and leave it — an
   unearned attestation is worse than a missing one. **Only a human can sign
   these.** If you are an agent, report which remain and stop; do not sign for
   Ryan.

5. **The verdict:** `… gate check <artifact> --project . -v`
   Exit 0 cleared, 1 blocked, 3 could not evaluate. Report the verdict and every
   blocking item. **Do not submit anything while this is non-zero**, and do not
   route around it by editing config — no blocking item in this gate can be
   cleared that way, by design.

## On red-then-green

If this build contains a fix, its regression test must have been **seen to fail
against the pre-fix tree**. A green suite is not evidence: 2,115 tests passed
while an onboarding loop App Review had rejected was live and shipping, and the
first regression test written for that bug passed against the unfixed code. If
you cannot show the red, you do not have a test.

## If you ever read an App Review citation

Paste the **verbatim** text into that app's decision log in the same hour. In
this whole company exactly one verbatim citation survives, and only because
someone pasted it into a commit message. Apple's notices for the batch of eight
rejections carried an empty issues block — no guideline, no reason text — so
seven of those reasons are gone for good.
