#!/usr/bin/env python3
"""ShipCheck submission gate -- evidence from a real build and a real run.

WHY THIS EXISTS, in one line: *the config is not the artifact.*

ShipCheck's scanner (scan.py) reads app.json, package.json and the source tree.
That was enough to be useful and is not enough to be trusted, because nearly
every rejection and nearly every real defect in this portfolio existed only in
the built binary or in the running app. The evidence for that is not an opinion:

  * scan.py:collect_info_plist() walks `ios/` and skips any path containing
    "build" -- so the one file that actually ships, the built Info.plist, is the
    one file it has never read.
  * `ios/` is gitignored CNG output in every one of these repos, so the
    scanner's view of the plist depends on whether someone happened to run
    `expo prebuild` on that machine. The same commit scans differently in CI.
    That yields false findings in BOTH directions, and both have happened:
      - FALSE MISSING: FlirtGym was reported missing three usage descriptions.
        All three are in the built binary, written at prebuild time by the
        expo-image-picker and expo-tracking-transparency config plugins. A
        worker spent a commit pinning a non-problem.
      - FALSE PRESENT: TentClock's scene manifest exists only in an untracked
        `ios/` directory on one Mac. Any config-or-source read calls it adopted.
        No build on any other machine reproduces it.
  * The 2026-10-13 portfolio sweep: 61 findings across 27 repos, "True
    positives: 0" by its own closing line -- while the apps were being rejected
    for things in the binary and in the running app.

So this module reads the ARTIFACT, and requires PROOF OF A RUN. Four kinds of
evidence, none of which a config file can satisfy:

  1. BINARY FACTS      -- the built Info.plist, the Mach-O load commands, the
                          embedded privacy manifests, the bundled icon.
  2. PROVENANCE        -- would a build from TRACKED config reproduce this
                          artifact's safety-relevant plist? This is the check
                          that catches TentClock, and the one the existing
                          ios27-upload-gate.sh does not make.
  3. A LAUNCH PROOF    -- installed and launched on a simulator, process alive,
                          no crash report, and a first frame that actually has
                          pixels in it. Bound to the binary, not to a version
                          string (see RECEIPT BINDING below).
  4. A STRESS PASS and HUMAN ATTESTATIONS -- the six abuse patterns that each
                          caught a real defect here in the last two days, plus
                          the two things a tool cannot do and must therefore
                          require were done and recorded.

RECEIPT BINDING -- the bug this fixes, found by running the old gate
---------------------------------------------------------------------
ios27-upload-gate.sh keys receipts on `bundleid@version+build`, and defends that
choice at length: you launch a simulator build and you upload a device build, so
they are different binaries of the same app. That reasoning is correct and the
key is still not sound, because version+build does not identify a binary. Run
against the real receipt store on this machine:

    receipt com.bakerventures.vocabdrift@1.0.1+3 was earned on
      /Users/ryanbaker/vocabdrift-ios27-scene/.../Vocabdrift.app   (FIXED,
      scene_delegate EXExpoAppSceneDelegate)
    and the gate applied it to
      /Users/ryanbaker/lockscreen-learn/.../Vocabdrift.app          (BROKEN,
      no UIApplicationSceneManifest at all)

Same version, same build number, different binary, opposite safety. The scene
half of that gate re-reads the artifact so it caught this one; but anything a
receipt is the ONLY evidence of -- "it drew a first frame", "the stress pass
ran" -- is transferable by accident between two binaries that differ in exactly
the way that matters.

The fix keeps the sim-build/device-build case working without keying on a
version string. A receipt records the launched binary's LC_UUID *and* a
fingerprint of the gate-relevant Info.plist keys. Matching is then three-valued:

    exact    same LC_UUID                      -> accepted
    sibling  same bundle+version+build, other
             UUID, and the gate-relevant plist
             fingerprint AGREES                -> accepted (sim -> device)
    expired  version/build moved, or the
             fingerprint disagrees             -> rejected, loudly

The Vocabdrift pair is a `sibling` whose fingerprint disagrees, so it is
rejected. A simulator and device build of the same commit agree on every key in
the fingerprint, so that case still passes. A build number bump still expires
everything, which is the existing behaviour and is correct.

CRYING WOLF IS THE FAILURE MODE THAT MATTERS
--------------------------------------------
A gate that blocks a good submission teaches everyone to skip it, which is worse
than no gate. So every rule here is written against a real must-not-fire case
from this portfolio, and selftest.py asserts them:

  * FlirtGym links SDK 26.5 and has no scene manifest. It is CORRECT and must
    not be flagged -- UIKit's requirement applies only to SDK >= 27 binaries.
  * FlirtGym's three usage descriptions are absent from config and present in
    the binary. The binary wins. No finding.
  * IOLTAlign's manifest comes from `enableSceneSupport` in tracked app.json at
    expo ~57.0.21 -- below the 57.0.23 floor the Brain documents, and it
    demonstrably worked. So provenance checks for the OPT-IN, and does not
    impose a version floor it cannot verify. A floor would block IOLTAlign.
  * A bare React Native repo that legitimately TRACKS ios/Info.plist has real
    provenance and must not be flagged.

"Cannot evaluate" never reads the same as "fine". It blocks, and it says which
tool was missing, because a gate that silently passes what it failed to measure
is the thing being replaced here.

Standard library only. Python 3.9+.
"""
import glob
import hashlib
import json
import os
import plistlib
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import zlib

RECEIPT_DIRNAME = ".shipcheck-receipts"
HOME_RECEIPTS = os.path.expanduser("~/.config/shipcheck/receipts")

# The iOS SDK major at which UIKit begins requiring UIScene adoption. A binary
# linked against anything lower launches normally and is exempt -- this is the
# FlirtGym must-not-fire case and the reason the check is gated on the linked
# SDK read from the Mach-O rather than on the deployment target or the OS.
SCENE_REQUIRED_SDK_MAJOR = 27

# ===================================================== Apple's reason codes ===
# WHY A TABLE AND NOT A FLAT ALLOW-LIST: Apple's ITMS-91055 does not object to
# unknown codes. It objects to codes that are valid *somewhere else*. Verbatim,
# from the rejection that bounced Nearvo 1.0.0 build 1 twice on 2026-09-07:
#
#   "ITMS-91055: Invalid API reason declaration - The PrivacyInfo.xcprivacy file
#    at the "PrivacyInfo.xcprivacy" path contains "E174.1" as the value for a
#    NSPrivacyAccessedAPITypeReasons key instead of a valid reason code for
#    using an API in the NSPrivacyAccessedAPICategorySystemBootTime category.
#    Values for NSPrivacyAccessedAPITypeReasons keys in your app's privacy
#    manifests must be valid reason codes for the corresponding API category."
#
# ...and the same text again for "35F9.1" under ...CategoryDiskSpace. Those two
# codes had been written under each other's categories. BOTH ARE INDIVIDUALLY
# VALID CODES. A check that asked "is this one of Apple's 17 codes?" would have
# been GREEN on the exact binary Apple refused. The category is the check.
#
# PROVENANCE -- fetched 2026-10-15, not recalled. Apple's rendered HTML pages
# are JS shells; these come from the DocC JSON that backs them:
#   https://developer.apple.com/tutorials/data/documentation/bundleresources/
#     app-privacy-configuration/nsprivacyaccessedapitypes/
#       nsprivacyaccessedapitype.json          (categories, each listing its
#                                               own permitted codes)
#       nsprivacyaccessedapitypereasons.json   (all 17 codes, with prose)
#   https://developer.apple.com/tutorials/data/documentation/bundleresources/
#     describing-use-of-required-reason-api.json
# Raw responses kept at ~/privacy-rules-work/apple-docs/.
# The per-category grouping below was read off the FIRST url. The SECOND was
# then used as an independent cross-check: same 17 codes, and each code's prose
# names its own subject ("access the system boot time..." for 35F9.1, "check
# whether there is sufficient disk space..." for E174.1). Two Apple pages, same
# partition. The fix commit relationship-app@2f4fd26 agrees from a third angle.
#
# Apple's own caveat, verbatim from the article: "Apple continually reviews the
# list of required reason APIs and reasons for usage, and will update this
# article from time to time." Hence APPLE_REASON_CODES_FETCHED: a stale table
# and a wrong manifest are different failures and must not read the same. An
# UNRECOGNISED code is therefore reported differently from a MISFILED one --
# from the outside, "Apple added a code" and "this code is in the wrong
# category" look identical, and guessing between them is what this exists to
# stop.
APPLE_REASON_CODES_FETCHED = "2026-10-15"
APPLE_REASON_CODES_SOURCE = (
    "developer.apple.com/documentation/bundleresources/"
    "app-privacy-configuration/nsprivacyaccessedapitypes/"
    "nsprivacyaccessedapitype (DocC JSON, fetched %s)"
    % APPLE_REASON_CODES_FETCHED)
APPLE_REASON_CODES = {
    "NSPrivacyAccessedAPICategoryFileTimestamp":
        ("DDA9.1", "C617.1", "3B52.1", "0A2A.1"),
    "NSPrivacyAccessedAPICategorySystemBootTime":
        ("35F9.1", "8FFB.1", "3D61.1"),
    "NSPrivacyAccessedAPICategoryDiskSpace":
        ("85F4.1", "E174.1", "7D9E.1", "B728.1"),
    "NSPrivacyAccessedAPICategoryActiveKeyboards":
        ("3EC4.1", "54BD.1"),
    "NSPrivacyAccessedAPICategoryUserDefaults":
        ("CA92.1", "1C8F.1", "C56D.1", "AC6B.1"),
}
# code -> the one category it belongs to, so a misfiled code can be NAMED as
# misfiled ("E174.1 belongs to DiskSpace") rather than merely rejected. Built
# from the table above so the two can never drift apart.
APPLE_CODE_HOME = {c: cat for cat, codes in APPLE_REASON_CODES.items()
                   for c in codes}

# Info.plist keys a launch receipt is allowed to vouch for across two binaries
# of the same app at the same version+build (the sim-build/device-build case).
# If any of these differs between the launched binary and the one being gated,
# the receipt is not evidence about this artifact. Keep this list to keys whose
# value is a property of the BUILD CONFIGURATION rather than of the platform:
# a sim build and a device build of one commit agree on all of them.
FINGERPRINT_KEYS = (
    "CFBundleIdentifier",
    "CFBundleShortVersionString",
    "CFBundleVersion",
    "ITSAppUsesNonExemptEncryption",
    "UIApplicationSceneManifest",
)

# Linked system framework -> the purpose string(s) Apple's delivery check wants
# if any of them satisfies it. THIS IS THE CHECK THAT CATCHES A RECORDED, REAL
# REJECTION: MileTruth build 3 was rejected at delivery with ITMS-90683 for a
# missing NSMotionUsageDescription. The app config said motionUsagePermission:
# false, which deleted the key -- and could not remove the linkage.
# Config said no. The Mach-O said yes. Apple reads the Mach-O.
#
# WHERE THE LINKAGE ACTUALLY COMES FROM, measured 2026-10-15 and corrected:
# this comment used to blame expo-location's precompiled XCFramework. That is
# too narrow, and it sends the next worker to delete the wrong dependency.
# Four of the five apps found carrying this defect -- Steadychart, PolicyReady,
# MoveWitness, DenialDesk -- have no location or sensor package of any kind,
# and their app executables link CoreMotion anyway. The mechanism is Swift
# autolinking: object files that import the Expo modules runtime emit
# `LC_LINKER_OPTION -framework CoreMotion` (and CoreLocation), so the linkage
# lands on the app's own executable in essentially every Expo SDK 57 app. In
# one MoveWitness build, 26 of the static libraries carried that linker option.
# Consequence: the purpose string is the only reliable fix.
#
# The map is deliberately SHORT. Every entry is a framework whose presence Apple
# treats as requiring a string, and nothing else gets in. AVFoundation is the
# instructive omission: any app that plays a sound links it, so requiring
# camera/microphone strings from AVFoundation linkage would fire on half this
# portfolio and teach everyone to ignore the gate. A rule that cries wolf is
# worse than no rule.
FRAMEWORK_PURPOSE_STRINGS = {
    "CoreMotion": ("NSMotionUsageDescription",),
    "CoreLocation": ("NSLocationWhenInUseUsageDescription",
                     "NSLocationAlwaysAndWhenInUseUsageDescription",
                     "NSLocationUsageDescription"),
    "Contacts": ("NSContactsUsageDescription",),
    "EventKit": ("NSCalendarsUsageDescription",
                 "NSCalendarsFullAccessUsageDescription",
                 "NSRemindersUsageDescription",
                 "NSRemindersFullAccessUsageDescription"),
    "Speech": ("NSSpeechRecognitionUsageDescription",),
    "HealthKit": ("NSHealthShareUsageDescription",
                  "NSHealthUpdateUsageDescription"),
    "CoreBluetooth": ("NSBluetoothAlwaysUsageDescription",
                      "NSBluetoothPeripheralUsageDescription"),
    "Photos": ("NSPhotoLibraryUsageDescription",
               "NSPhotoLibraryAddUsageDescription"),
    "LocalAuthentication": ("NSFaceIDUsageDescription",),
}

# The six abuse patterns. Each one caught a real defect in this portfolio in the
# last two days, and the note says which -- a required checklist item with no
# story attached is the kind of item people learn to tick without doing.
STRESS_PATTERNS = [
    ("double-tap",
     "Double-tap every create, save and delete control",
     "A second tap landed before the first finished: one app surfaced a raw "
     "database error to the user, another wrote a duplicate record."),
    ("kill-while-typing",
     "Type into a text field and kill the app with the field still focused",
     "An evidence app silently lost typed notes when it was interrupted "
     "mid-entry -- no error, no draft, the text was simply gone."),
    ("no-network",
     "Launch and use the primary flow with no network at all",
     "A flow that assumes a reachable backend hangs or dies on a plane, and "
     "that is the first thing a reviewer on hotel wifi hits."),
    ("empty-state",
     "Open every screen with no data in it",
     "First-run empty screens are guideline 2.1 rejections. Several apps here "
     "shipped a screen that was blank rather than explained."),
    ("volume",
     "Load the app to realistic volume and use it",
     "Lists that are fine at three records are not always fine at three "
     "hundred; one save path degraded into a visible stall."),
    ("decline-permissions",
     "Decline every permission the app asks for, then use it",
     "A denied permission that the app treats as granted crashes or dead-ends. "
     "A first-render permission wall is itself a 5.1.1(ii) rejection."),
    # --- the three added from Nearvo's recovered rejection history ----------
    # Every Nearvo rejection whose cause was ever established was a runtime
    # defect. Not one was a config fact. These three are those defects turned
    # into patterns.
    ("repeat-onboarding",
     "Finish onboarding, then relaunch, background, and relaunch again",
     "This is the only verbatim App Review citation that survives anywhere in "
     "the corpus: \"the app repeatedly prompt user to go through onboarding "
     "after onboarding.\" A related defect let a settled-but-empty profile row "
     "read as still-loading, so a fresh account SKIPPED onboarding entirely -- "
     "including the Terms acceptance and the 18-plus age gate."),
    ("demo-credential",
     "Sign in with the exact demo credentials written in the review notes",
     "Nearvo was rejected over a demo account that existed and was confirmed "
     "-- the password given to Apple simply was not that account's password. "
     "Nothing but an actual sign-in attempt with the exact string you pasted "
     "into App Store Connect finds that."),
    ("account-switch",
     "Sign out, then sign in as a different account",
     "Nearvo's sign-out never cleared the cache, so the previous account's "
     "data rendered for the next user. A single-account walkthrough cannot "
     "see this, and it is a privacy incident, not a cosmetic bug."),
]

# A recorded result. 'n/a' is allowed and requires a note, because demanding
# an account-switch pass from an app with no accounts is the cry-wolf failure
# this gate is trying not to commit. 'n/a' with a reason is honest; silently
# dropping the requirement is not.
STRESS_RESULTS = ("pass", "fail", "n/a")

# The two things this tool genuinely cannot do. It requires that they were done
# and that a human put their name to it, which is worth more than a check that
# silently passes.
ATTEST_ITEMS = [
    ("device-render",
     "Installed and used on real hardware",
     "A simulator does not render like a device. The grey-patch rendering bug "
     "in this portfolio could not be reproduced or confirmed on any simulator; "
     "it needed hardware in hand."),
    ("reviewer-walkthrough",
     "A human followed the primary flow end to end as a reviewer would",
     "Whether a reviewer can finish the flow is judgement, not a predicate. "
     "Nearvo's is a two-person flow a solo reviewer cannot complete at all, "
     "which no scan of its code would ever tell you. If you ever read an "
     "App Review citation, paste the VERBATIM text into the app's decision "
     "log in the same hour -- see RED THEN GREEN below for why."),
    ("regression-red-then-green",
     "Every fix in this build has a test shown to FAIL against the pre-fix tree",
     "A green suite is not evidence. 2,115 Nearvo tests passed while the "
     "onboarding loop that Apple rejected was live and shipping -- and the "
     "FIRST regression test written for that bug passed against the UNFIXED "
     "code. It was vacuous, and only stashing the fix and re-running revealed "
     "it. So a test that has only ever been seen passing proves nothing. "
     "Record the red output, then the green."),
]

# Required ONLY when the bundle actually embeds an app extension, which is read
# from the artifact. Vocabdrift is live with a Lock Screen widget as its
# headline feature and nobody has ever exercised it -- a simulator cannot
# produce a real long-press Lock Screen widget, so this is hardware work, and
# the gate's job is to require that it was done rather than to pretend.
EXTENSION_ATTEST = (
    "extension-exercised",
    "Every app extension in the bundle was installed and used",
    "An extension is a separate binary with its own entry point. It does not "
    "run when you launch the app, so a launch proof says nothing about it. "
    "Vocabdrift ships PlugIns/LockLearnWidget.appex as its core feature and it "
    "has never been exercised on anything.")


# ===================================================================== helpers
def _tool(name):
    return shutil.which(name)


def _run(cmd, timeout=120):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except (OSError, subprocess.SubprocessError):
        return 127, "", "could not execute %s" % (cmd[0] if cmd else "?")


class GateError(Exception):
    """Raised when the gate cannot evaluate. Never the same as a pass."""


# ================================================================== artifact
class Artifact:
    """The built thing, read as the built thing.

    Everything on this object comes out of the artifact. Nothing is inferred
    from app.json, package.json or the source tree -- those belong to the
    scanner, and mixing them in here is precisely the mistake being corrected.
    """

    def __init__(self, path):
        self.given = path
        self._tmp = None
        self.app = self._resolve(path)
        self.plist_path = os.path.join(self.app, "Info.plist")
        self.plist = self._read_plist(self.plist_path)
        if not self.plist:
            raise GateError("no readable Info.plist in %s" % self.app)
        self.bundle_id = self.plist.get("CFBundleIdentifier") or ""
        self.version = str(self.plist.get("CFBundleShortVersionString") or "0")
        self.build = str(self.plist.get("CFBundleVersion") or "0")
        if not self.bundle_id:
            raise GateError("artifact has no CFBundleIdentifier: %s" % self.app)
        exe = self.plist.get("CFBundleExecutable") or os.path.basename(
            self.app)[:-4]
        self.exe = os.path.join(self.app, exe)
        if not os.path.isfile(self.exe):
            raise GateError("no Mach-O executable at %s" % self.exe)

    # --------------------------------------------------------------- plumbing
    def _resolve(self, path):
        if not os.path.exists(path):
            raise GateError("no such artifact: %s" % path)
        if path.endswith(".app") and os.path.isdir(path):
            return path
        if path.endswith(".xcarchive"):
            hits = sorted(glob.glob(os.path.join(
                path, "Products", "Applications", "*.app")))
            if not hits:
                raise GateError("no .app inside %s" % path)
            return hits[0]
        if path.endswith(".ipa"):
            # An .ipa is a zip from somewhere else. Expand it into its own
            # empty directory, never into a working tree.
            self._tmp = tempfile.mkdtemp(prefix="shipgate-ipa-")
            rc, _o, err = _run(["unzip", "-q", "-o", path, "-d", self._tmp])
            if rc != 0:
                raise GateError("could not expand %s: %s" % (path, err.strip()))
            hits = sorted(glob.glob(os.path.join(self._tmp, "Payload", "*.app")))
            if not hits:
                raise GateError("no Payload/*.app inside %s" % path)
            return hits[0]
        raise GateError("not an .app, .ipa or .xcarchive: %s" % path)

    def cleanup(self):
        if self._tmp and os.path.isdir(self._tmp):
            shutil.rmtree(self._tmp, ignore_errors=True)
            self._tmp = None

    @staticmethod
    def _read_plist(path):
        # A built Info.plist is usually binary. plistlib reads both formats;
        # PlistBuddy and a text grep read only one, which is how a binary plist
        # gets misreported as "key absent".
        try:
            with open(path, "rb") as f:
                return plistlib.load(f)
        except Exception:                                      # noqa: BLE001
            return None

    # ---------------------------------------------------------- Mach-O facts
    def load_versions(self):
        """(linked_sdk, minos) from LC_BUILD_VERSION. Raises if unreadable."""
        if not _tool("vtool"):
            raise GateError(
                "vtool is not on PATH, so the linked SDK cannot be read. "
                "Install Xcode command line tools. This blocks: the whole "
                "iOS-27 scene rule turns on the linked SDK, and guessing it "
                "from the deployment target is how this was got wrong before.")
        rc, out, _e = _run(["vtool", "-show-build", self.exe])
        if rc != 0:
            raise GateError("vtool could not read %s" % self.exe)
        sdk = minos = None
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 2 and parts[0] == "sdk" and sdk is None:
                sdk = parts[1]
            if len(parts) >= 2 and parts[0] == "minos" and minos is None:
                minos = parts[1]
        if not sdk:
            raise GateError(
                "no LC_BUILD_VERSION in %s -- cannot tell which SDK linked it"
                % self.exe)
        return sdk, minos

    def uuids(self):
        """{arch: uuid} from LC_UUID. This is the binary's identity."""
        if not _tool("dwarfdump"):
            raise GateError("dwarfdump is not on PATH; cannot read LC_UUID")
        rc, out, _e = _run(["dwarfdump", "--uuid", self.exe])
        if rc != 0:
            raise GateError("dwarfdump could not read %s" % self.exe)
        found = {}
        for line in out.splitlines():
            m = re.match(r"\s*UUID:\s*([0-9A-Fa-f-]{36})\s*\(([^)]+)\)", line)
            if m:
                found[m.group(2).strip()] = m.group(1).upper()
        if not found:
            raise GateError("no LC_UUID in %s" % self.exe)
        return found

    def identity(self):
        """One stable id for this binary. Prefers arm64, the slice that ships."""
        u = self.uuids()
        for arch in ("arm64", "arm64e", "x86_64"):
            if arch in u:
                return u[arch]
        return sorted(u.values())[0]

    # -------------------------------------------------------- plist readings
    def scene(self):
        """(manifest_present, delegate_class, config_count).

        A UIApplicationSceneManifest whose UISceneConfigurations is EMPTY looks
        adopted to anyone skimming a plist and is NOT adoption to UIKit -- the
        trap still fires. A worker shipped exactly that and reported it as proof
        the fix does not work. So adoption means a NAMED DELEGATE CLASS.
        """
        man = self.plist.get("UIApplicationSceneManifest")
        if not isinstance(man, dict):
            return False, None, 0
        cfgs = man.get("UISceneConfigurations")
        if not isinstance(cfgs, dict):
            return True, None, 0
        roles = cfgs.get("UIWindowSceneSessionRoleApplication")
        if not isinstance(roles, list) or not roles:
            return True, None, 0
        deleg = None
        for entry in roles:
            if isinstance(entry, dict) and entry.get("UISceneDelegateClassName"):
                deleg = entry["UISceneDelegateClassName"]
                break
        return True, deleg, len(roles)

    def usage_descriptions(self):
        return {k: v for k, v in self.plist.items()
                if k.startswith("NS") and k.endswith("UsageDescription")
                and isinstance(v, str) and v.strip()}

    def privacy_manifests(self):
        """(app_level_manifest_or_None, [sdk manifest relpaths]).

        Read from the bundle. The scanner reads node_modules for this and then
        says so in its own evidence string -- "node_modules is absent, so
        ShipCheck cannot tell" appeared on 9 of 27 apps in the portfolio sweep.
        In the bundle there is nothing to be unsure about.
        """
        app_level, sdk = None, []
        top = os.path.join(self.app, "PrivacyInfo.xcprivacy")
        if os.path.isfile(top):
            app_level = self._read_plist(top) or {}
        for root, _dirs, files in os.walk(self.app):
            for fn in files:
                if fn != "PrivacyInfo.xcprivacy":
                    continue
                p = os.path.join(root, fn)
                if os.path.abspath(p) == os.path.abspath(top):
                    continue
                sdk.append(os.path.relpath(p, self.app))
        return app_level, sorted(sdk)

    def privacy_manifest_contents(self):
        """[(relpath, parsed_dict_or_None, read_error_or_None), ...]

        Every embedded PrivacyInfo.xcprivacy, PARSED. privacy_manifests() above
        returns the SDK ones as bare paths, which is all a presence check needs
        -- and a presence check is exactly what missed ITMS-91055 and
        ITMS-91064. Both of those rejections fired on manifests that were
        present and wrong inside, so the rules below need the contents.

        A manifest that cannot be parsed is returned with its error rather than
        skipped. "I could not read it" must not read the same as "it is fine";
        that confusion is the house failure mode.

        The app-level manifest sorts first and is marked by a relpath of exactly
        "PrivacyInfo.xcprivacy", because Apple validates the app's own manifest
        independently of its SDKs' -- established the hard way on FlirtGym,
        where every bundled SDK manifest was individually consistent and the
        app's own was not (RizzMaxx@c86f432, from the build-25 .ipa).
        """
        out = []
        top = os.path.abspath(os.path.join(self.app, "PrivacyInfo.xcprivacy"))
        found = []
        for root, _dirs, files in os.walk(self.app):
            for fn in files:
                if fn == "PrivacyInfo.xcprivacy":
                    found.append(os.path.join(root, fn))
        for p in sorted(found, key=lambda q: (os.path.abspath(q) != top, q)):
            rel = os.path.relpath(p, self.app)
            try:
                with open(p, "rb") as fh:
                    d = plistlib.load(fh)
                if not isinstance(d, dict):
                    out.append((rel, None, "top level is not a dictionary"))
                else:
                    out.append((rel, d, None))
            except Exception as exc:                  # noqa: BLE001
                out.append((rel, None, "%s: %s" % (type(exc).__name__, exc)))
        return out

    def icon(self):
        """(ok, detail) -- is there a real app icon IN the bundle?"""
        names = [n for n in os.listdir(self.app)
                 if re.match(r"AppIcon.*\.png$", n)]
        car = os.path.isfile(os.path.join(self.app, "Assets.car"))
        pbi = (self.plist.get("CFBundleIcons") or {}) if isinstance(
            self.plist.get("CFBundleIcons"), dict) else {}
        declared = bool(pbi) or bool(self.plist.get("CFBundleIconName"))
        if names or (car and declared):
            bits = []
            if names:
                bits.append("%d AppIcon png(s) in the bundle" % len(names))
            if car:
                bits.append("Assets.car present")
            if declared:
                bits.append("CFBundleIconName/CFBundleIcons declared")
            return True, "; ".join(bits)
        return False, ("no AppIcon*.png in the bundle, and no Assets.car with a "
                       "declared CFBundleIconName")

    def extensions(self):
        """[(name, appex_path)] from PlugIns/. Read from the bundle."""
        plugins = os.path.join(self.app, "PlugIns")
        if not os.path.isdir(plugins):
            return []
        out = []
        for n in sorted(os.listdir(plugins)):
            if n.endswith(".appex"):
                out.append((n, os.path.join(plugins, n)))
        return out

    def _macho_paths(self):
        """Just the EXECUTABLES: the app binary and each extension's binary.

        Deliberately NOT the bundled dynamic frameworks, and that restriction
        was measured rather than guessed. Scanning everything flagged
        Photos.framework on 2 of the 4 Expo apps here, every time linked by
        Frameworks/ExpoFileSystem.framework -- expo-file-system links Photos in
        essentially every Expo app, whether or not the app touches the photo
        library. A rule that fires on half the portfolio for a reason nobody
        can act on is how a gate gets ignored.

        The app's OWN executable is the signal, and it is the one that catches
        the real case: Expo modules link statically and Swift autolinking emits
        a `-framework CoreMotion` linker option from anything that imports the
        Expo modules runtime, so the MileTruth ITMS-90683 linkage lands on the
        app binary. Verified on five apps, 2026-10-14 and 2026-10-15:
        Steadychart, PolicyReady, Nearvo, MoveWitness and DenialDesk all show
        CoreMotion on their own executable, which is exactly the shape Apple
        refused -- and four of the five have no location or sensor dependency.
        """
        paths = [self.exe]
        for _name, appex in self.extensions():
            d = Artifact._read_plist(os.path.join(appex, "Info.plist")) or {}
            exe = d.get("CFBundleExecutable")
            if exe and os.path.isfile(os.path.join(appex, exe)):
                paths.append(os.path.join(appex, exe))
        return paths

    def linked_system_frameworks(self):
        """{framework name: [which executable linked it]} from LC_LOAD_DYLIB.

        Read with otool, because this is the fact Apple's delivery check reads
        and it is not in any config file. MileTruth's ITMS-90683 is the proof:
        the app config had deleted NSMotionUsageDescription and CoreMotion was
        still linked, by a precompiled XCFramework nobody had looked inside.
        """
        if not _tool("otool"):
            raise GateError("otool is not on PATH; cannot read linked frameworks")
        found = {}
        for p in self._macho_paths():
            rc, out, _e = _run(["otool", "-L", p])
            if rc != 0:
                continue
            for m in re.finditer(
                    r"/System/Library/Frameworks/([A-Za-z0-9_+]+)\.framework", out):
                found.setdefault(m.group(1), [])
                rel = os.path.relpath(p, self.app)
                if rel not in found[m.group(1)]:
                    found[m.group(1)].append(rel)
        return found

    def binary_short(self):
        try:
            return self.identity()
        except GateError:
            return None

    def fingerprint(self):
        """Digest of the gate-relevant plist keys. See RECEIPT BINDING."""
        payload = {}
        for k in FINGERPRINT_KEYS:
            v = self.plist.get(k)
            payload[k] = _stable(v)
        blob = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]

    def facts(self):
        sdk = minos = None
        err = None
        try:
            sdk, minos = self.load_versions()
        except GateError as e:
            err = str(e)
        present, deleg, n = self.scene()
        app_pm, sdk_pm = self.privacy_manifests()
        icon_ok, icon_detail = self.icon()
        ident = None
        try:
            ident = self.identity()
        except GateError as e:
            err = err or str(e)
        return dict(
            app=self.app, bundle_id=self.bundle_id, version=self.version,
            build=self.build, linked_sdk=sdk, minos=minos,
            binary_uuid=ident, fingerprint=self.fingerprint(),
            scene_manifest=present, scene_delegate=deleg,
            scene_config_count=n,
            usage_descriptions=sorted(self.usage_descriptions()),
            app_privacy_manifest=bool(app_pm),
            sdk_privacy_manifests=len(sdk_pm),
            icon_ok=icon_ok, icon_detail=icon_detail,
            export_compliance=self.plist.get("ITSAppUsesNonExemptEncryption"),
            read_error=err)


def _stable(v):
    """JSON-safe, order-stable rendering of a plist value."""
    if isinstance(v, dict):
        return {str(k): _stable(v[k]) for k in sorted(v)}
    if isinstance(v, (list, tuple)):
        return [_stable(x) for x in v]
    if isinstance(v, (bytes, bytearray)):
        return hashlib.sha256(bytes(v)).hexdigest()[:16]
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return str(v)


# ================================================================ provenance
def git_tracked(root, pattern=None):
    rc, out, _e = _run(["git", "-C", root, "ls-files"] +
                       ([pattern] if pattern else []))
    if rc != 0:
        return None
    return [l for l in out.splitlines() if l.strip()]


def scene_provenance(project_root, artifact):
    """Would a build from TRACKED config reproduce this artifact's manifest?

    This is the check the existing upload gate does not make, and the one that
    catches TentClock -- whose manifest lives only in an untracked ios/
    directory on one Mac, and which that gate therefore passes with exit 0.

    Returns (status, detail). status is one of:
      n/a           the artifact has no manifest, so there is nothing to explain
      config        tracked app config opts in, or declares the manifest
      tracked-plist a tracked ios/**/Info.plist carries it (bare RN, legitimate)
      tracked-plugin a tracked config plugin writes it
      unexplained   the artifact has it and nothing tracked accounts for it
      unknown       not a git repo, or git unavailable -- blocks, does not pass
    """
    present, _deleg, _n = artifact.scene()
    if not present:
        return "n/a", "artifact declares no UIApplicationSceneManifest"
    if not project_root or not os.path.isdir(project_root):
        return "unknown", "no project root given, so tracked config was not read"
    rc, _o, _e = _run(["git", "-C", project_root, "rev-parse", "--git-dir"])
    if rc != 0:
        return "unknown", "%s is not a git repository" % project_root

    tracked = git_tracked(project_root) or []
    tset = set(tracked)

    # (a) a tracked ios Info.plist that carries the manifest. A bare React
    #     Native project tracks ios/ for real, and that is genuine provenance.
    for rel in tracked:
        if rel.endswith("Info.plist") and rel.startswith("ios/"):
            d = Artifact._read_plist(os.path.join(project_root, rel))
            if isinstance(d, dict) and isinstance(
                    d.get("UIApplicationSceneManifest"), dict):
                return ("tracked-plist",
                        "%s is tracked and declares UIApplicationSceneManifest"
                        % rel)

    # (b) the app config. Read the tracked file as text and as JSON -- a
    #     dynamic app.config.ts cannot be evaluated here, but the opt-in is a
    #     literal either way, so a text match is the honest test.
    #
    #     NOTE: this checks for the OPT-IN ONLY and imposes no expo version
    #     floor. The Brain documents enableSceneSupport as needing
    #     expo >= 57.0.23, but IOLTAlign generates a working manifest from
    #     expo ~57.0.21, so a floor here would block a good submission. The
    #     floor belongs in a warning, not in a gate.
    cfg_files = [r for r in tracked
                 if r in ("app.json", "app.config.js", "app.config.ts",
                          "app.config.mjs", "app.config.cjs")]
    for rel in cfg_files:
        try:
            with open(os.path.join(project_root, rel), encoding="utf-8",
                      errors="replace") as f:
                text = f.read(2 * 1024 * 1024)
        except OSError:
            continue
        # The quote matters: in JSON the key is "enableSceneSupport" and the
        # colon comes AFTER the closing quote. The first version of this regex
        # omitted it and silently reported IOLTAlign's tracked opt-in as
        # unexplained -- a false CRITICAL on a correctly configured app, which
        # is the exact failure mode this gate must not have. Caught by
        # selftest_gate.py's IOLTAlign must-not-fire case.
        if re.search(r"enableSceneSupport[\"']?\s*[:=]\s*true", text):
            return ("config",
                    "%s (tracked) sets expo-build-properties "
                    "ios.enableSceneSupport = true" % rel)
        if "UIApplicationSceneManifest" in text:
            return ("config",
                    "%s (tracked) declares UIApplicationSceneManifest directly"
                    % rel)

    # (c) a tracked config plugin that writes the manifest.
    for rel in tracked:
        if not re.search(r"(^|/)(plugins?|config-plugins?)/.*\.(js|ts|cjs|mjs)$",
                         rel):
            continue
        try:
            with open(os.path.join(project_root, rel), encoding="utf-8",
                      errors="replace") as f:
                if "UIApplicationSceneManifest" in f.read(1024 * 1024):
                    return ("tracked-plugin",
                            "%s is a tracked config plugin that writes "
                            "UIApplicationSceneManifest" % rel)
        except OSError:
            continue

    untracked_hint = ""
    ios_plists = glob.glob(os.path.join(project_root, "ios", "*", "Info.plist"))
    for p in ios_plists:
        rel = os.path.relpath(p, project_root)
        if rel in tset:
            continue
        d = Artifact._read_plist(p)
        if isinstance(d, dict) and isinstance(
                d.get("UIApplicationSceneManifest"), dict):
            untracked_hint = (" The manifest IS present in %s, which is NOT "
                              "tracked by git -- so it exists on this machine "
                              "and nowhere else." % rel)
            break
    return ("unexplained",
            "the artifact declares UIApplicationSceneManifest but nothing "
            "tracked in %s accounts for it: no enableSceneSupport opt-in, no "
            "manifest in tracked app config, no tracked ios Info.plist, no "
            "tracked config plugin that writes one.%s"
            % (project_root, untracked_hint))


# =================================================================== receipts
def receipt_dirs(project_root=None, artifact_path=None):
    """Where receipts live, most-portable first.

    Repo-local and committable is the one that matters: the machine that builds
    and the machine that uploads are not the same machine here, and a receipt
    that lives only in ~/.config on the mini would block every legitimate
    upload from the laptop.
    """
    out = []
    for start in (project_root, os.path.dirname(artifact_path or "") or None):
        if not start:
            continue
        rc, o, _e = _run(["git", "-C", start, "rev-parse", "--show-toplevel"])
        if rc == 0 and o.strip():
            d = os.path.join(o.strip(), RECEIPT_DIRNAME)
            if d not in out:
                out.append(d)
    if HOME_RECEIPTS not in out:
        out.append(HOME_RECEIPTS)
    return out


def receipt_name(artifact, kind):
    return "%s@%s+%s.%s.json" % (artifact.bundle_id, artifact.version,
                                 artifact.build, kind)


def load_receipt(artifact, kind, project_root=None):
    for d in receipt_dirs(project_root, artifact.app):
        p = os.path.join(d, receipt_name(artifact, kind))
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    r = json.load(f)
                r["_path"] = p
                return r
            except (OSError, ValueError):
                continue
    return None


def save_receipt(artifact, kind, payload, project_root=None):
    written = []
    for d in receipt_dirs(project_root, artifact.app):
        try:
            os.makedirs(d, exist_ok=True)
            p = os.path.join(d, receipt_name(artifact, kind))
            with open(p, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, sort_keys=True)
            written.append(p)
        except OSError:
            continue
    if not written:
        raise GateError("could not write a %s receipt anywhere" % kind)
    return written


LEDGER_NAME = "gated-builds.jsonl"


def ledger_path(project_root=None, artifact_path=None):
    return os.path.join(receipt_dirs(project_root, artifact_path)[0],
                        LEDGER_NAME)


def ledger_lookup(artifact, project_root=None):
    """An earlier, DIFFERENT binary at this same version+build, or None."""
    try:
        ident = artifact.identity()
    except GateError:
        return None
    for d in receipt_dirs(project_root, artifact.app):
        p = os.path.join(d, LEDGER_NAME)
        if not os.path.isfile(p):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if (row.get("bundle_id") == artifact.bundle_id
                            and str(row.get("version")) == artifact.version
                            and str(row.get("build")) == artifact.build
                            and row.get("binary_uuid")
                            and row.get("binary_uuid") != ident):
                        return row
        except OSError:
            continue
    return None


def ledger_append(artifact, project_root=None):
    """Record that this binary was evaluated. Append-only, best effort."""
    try:
        row = dict(bundle_id=artifact.bundle_id, version=artifact.version,
                   build=artifact.build, binary_uuid=artifact.identity(),
                   fingerprint=artifact.fingerprint(),
                   app_path=os.path.abspath(artifact.app),
                   when=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    except GateError:
        return None
    p = ledger_path(project_root, artifact.app)
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
        return p
    except OSError:
        return None


def match_receipt(artifact, receipt):
    """('exact'|'sibling'|'expired'|'absent', why). See RECEIPT BINDING."""
    if not receipt:
        return "absent", "no receipt found"
    if receipt.get("bundle_id") != artifact.bundle_id:
        return "expired", "receipt is for a different bundle id"
    if (str(receipt.get("version")) != artifact.version
            or str(receipt.get("build")) != artifact.build):
        return ("expired",
                "receipt is for %s+%s, this artifact is %s+%s -- a receipt "
                "stops being valid the moment the build number moves"
                % (receipt.get("version"), receipt.get("build"),
                   artifact.version, artifact.build))
    try:
        ident = artifact.identity()
    except GateError as e:
        return "expired", "cannot read this binary's LC_UUID: %s" % e
    if receipt.get("binary_uuid") == ident:
        return "exact", "receipt was earned on this exact binary (%s)" % ident
    rf, af = receipt.get("fingerprint"), artifact.fingerprint()
    if rf and rf == af:
        return ("sibling",
                "receipt was earned on a different binary of the same build "
                "(%s vs %s) whose gate-relevant Info.plist keys are identical "
                "-- the simulator-build/device-build case"
                % (receipt.get("binary_uuid"), ident))
    return ("expired",
            "receipt was earned on a DIFFERENT BINARY (%s) of the same "
            "version+build whose gate-relevant Info.plist keys DISAGREE with "
            "this one (fingerprint %s vs %s). It is not evidence about this "
            "artifact. This is the exact shape of the Vocabdrift receipt that "
            "vouched for a fixed binary while a broken one was being checked."
            % (receipt.get("binary_uuid"), rf, af))


# ================================================================ screenshots
def png_pixels(path, sample=20000):
    """(w, h, distinct_sampled_colors, dominant_fraction).

    Enough to answer "did it draw a first frame, or is this a blank window".
    Stdlib only: PNG is zlib plus five filter types, and simctl writes 8-bit
    non-interlaced, so a full decoder is not needed.
    """
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise GateError("%s is not a PNG" % path)
    i, w, h, bd, ct, inter, idat = 8, None, None, None, None, 0, []
    while i + 8 <= len(raw):
        ln = struct.unpack(">I", raw[i:i + 4])[0]
        typ = raw[i + 4:i + 8]
        body = raw[i + 8:i + 8 + ln]
        i += 12 + ln
        if typ == b"IHDR":
            w, h, bd, ct, _c, _f, inter = struct.unpack(">IIBBBBB", body)
        elif typ == b"IDAT":
            idat.append(body)
        elif typ == b"IEND":
            break
    if w is None:
        raise GateError("%s has no IHDR" % path)
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if ch is None or bd != 8 or inter != 0:
        raise GateError("unsupported PNG (bit depth %s, colour type %s, "
                        "interlace %s)" % (bd, ct, inter))
    data = zlib.decompress(b"".join(idat))
    stride = w * ch
    prev = bytearray(stride)
    counts, p = {}, 0
    total = w * h
    step = max(1, total // max(1, sample))
    idx = 0
    for _y in range(h):
        if p >= len(data):
            break
        f = data[p]
        p += 1
        line = bytearray(data[p:p + stride])
        p += stride
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                b = prev[x]
                c = prev[x - ch] if x >= ch else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        for x in range(0, w):
            if idx % step == 0:
                o = x * ch
                counts[bytes(line[o:o + 3])] = counts.get(
                    bytes(line[o:o + 3]), 0) + 1
            idx += 1
        prev = line
    n = sum(counts.values()) or 1
    dom = max(counts.values()) / float(n) if counts else 1.0
    return w, h, len(counts), dom


# A first frame that is one flat colour after the settle delay is a blank
# window, not a rendered app. The thresholds are deliberately loose: real first
# frames on this machine sampled 217-1852 distinct colours, so anything under a
# dozen is a uniform field, and a human can still overrule with an attestation.
# Loose on purpose -- blocking a good submission is the failure that matters.
FRAME_MIN_COLORS = 8
FRAME_MAX_DOMINANT = 0.995


# ===================================================================== checks
# WHICH SEVERITIES FAIL THE GATE -- ONE DEFINITION, AND WHY IT IS NOT "critical"
#
# Until 2026-10-15 every exit status in the gate was computed inline from
# `severity == "critical"`, in four separate places. `BIN-FRAMEWORK-PURPOSE-
# STRING-*` is severity `high`, so:
#
#     $ shipcheck gate sweep ~/steadychart-ios27-verify ~/policyready-ios27-scene
#       ... eight `high` ITMS-90683 findings printed ...
#       exit 0
#
# A sweep over two genuinely defective binaries printed the finding built from
# THE ONLY REJECTION APPLE HAS EVER PUT IN WRITING and returned shell status 0.
# Any CI step or script reading $? called it clean. It went unnoticed because
# every published sweep so far also happened to contain a GATE-NO-ARTIFACT or a
# critical BIN-SCENE-NOT-ADOPTED, so the 1 was always being earned by something
# else. `gate check` had the same bug: on that binary it exits 1 only because
# the launch and stress receipts are missing -- the same binary with its
# receipts in order was REVIEW, exit 0, with the ITMS-90683 defect intact.
#
# The fix is not to promote one rule to critical. The severity vocabulary in
# this gate already means something specific, and the mapping to exit status
# should follow that meaning rather than one rule's importance:
#
#   critical  this build cannot work or cannot be evaluated -- it will not
#             launch (BIN-SCENE-NOT-ADOPTED), it drew a blank first frame, or
#             the gate could not read it / has no artifact / has no run proof.
#   high      Apple will REFUSE this upload, or the gate could not establish
#             something it needs:
#               BIN-FRAMEWORK-PURPOSE-STRING-*  ITMS-90683, refused at delivery
#               BIN-BUILD-NUMBER-REUSED         refused at upload processing
#               BIN-ICON-ABSENT                 refused at upload
#               BIN-PRIVACY-MANIFEST-ABSENT     refused at upload
#               GATE-CANNOT-READ-LINKAGE        "I could not check" -- and its
#                                               own fix text already said
#                                               "This blocks rather than
#                                               passing", which it did not
#               GATE-SCENE-PROVENANCE-UNKNOWN   could not establish
#               GATE-STRESS-MISSING-*           no proof for a required pattern
#               GATE-ATTEST-MISSING-*           no proof for a required item
#   medium    a nuisance, not a refusal: BIN-EXPORT-COMPLIANCE-MISSING makes
#             App Store Connect ask a question on every upload. It does not
#             stop one.
#
# Every `high` in that list is either a rejection or an unanswered question.
# None of them is a style note. So the gate fails on critical AND high, and
# reports medium and below. This is the whole of the mapping, in one place, so
# that a fifth caller cannot quietly reintroduce the inline version.
#
# The one place `high` was being used to mean "report, do not block" was
# _pm_sev() for an SDK's own embedded privacy manifest, whose docstring says so
# in as many words. That is now `medium`, which is what this mapping makes that
# sentence mean -- rather than leaving one rule whose severity contradicts the
# policy. It costs nothing in detection: the SDK manifests were measured across
# 216 embedded files in six repos and produced zero findings.
#
# `shipcheck scan` is deliberately NOT changed. It reads config, not the
# artifact, and it has a user-facing, documented `fail-on` knob (action.yml,
# README) that defaults to critical. The gate has no knob: it is the last thing
# before an upload, and nothing it calls critical or high should pass it.
BLOCKING_SEVERITIES = ("critical", "high")


def blocking_findings(findings):
    """The findings that must make the process exit non-zero.

    Used by `gate check`, by `gate sweep`, and by the --json exit status of
    both. One function, so there is one answer.
    """
    return [f for f in findings
            if f.get("severity") in BLOCKING_SEVERITIES]


def _f(fid, severity, title, evidence, fix, clause=None, confidence="high"):
    return dict(id=fid, severity=severity, title=title, evidence=evidence,
                fix=fix, clause=clause, confidence=confidence,
                platform="ios", source="gate")


# ============================ the contents of a privacy manifest ============
# Two rejection reasons Apple has actually sent this portfolio, and the only
# two of the four that no check had ever looked at. The nearest existing rule,
# BIN-PRIVACY-MANIFEST-ABSENT, asks "is there a PrivacyInfo.xcprivacy?" -- and
# BOTH of these fired on manifests that were present. A check that cannot see
# its subject; the subject is the contents.

def _pm_sev(relpath):
    """Severity by whose manifest it is.

    The app's own manifest is the one the developer writes and the one Apple
    cited in both rejections, so it blocks. An SDK's embedded manifest is still
    validated -- Apple checks every manifest in the bundle -- but the only fix
    is to upgrade or drop the dependency, so it is reported rather than
    blocking. Including SDK manifests was not free-by-assumption: it was
    measured first across 216 embedded manifests in six repos on this machine,
    and produced ZERO findings, so it costs no false positives. (The precedent
    is the Photos.framework noise that the purpose-string rule had to be
    narrowed to remove.)

    "Reported rather than blocking" is `medium`, not `high`. It was `high`
    until 2026-10-15, when `high` meant nothing to any exit status; now that
    BLOCKING_SEVERITIES includes high, `high` here would contradict this
    docstring and block on a finding whose only fix is someone else's release.
    """
    return "critical" if relpath == "PrivacyInfo.xcprivacy" else "medium"


def _pm_whose(relpath):
    return ("the app's own manifest" if relpath == "PrivacyInfo.xcprivacy"
            else "an embedded SDK manifest at %s" % relpath)


def privacy_reason_code_findings(manifests):
    """BIN-PRIVACY-REASON-CODE-INVALID -- every code against ITS OWN category.

    manifests: [(relpath, parsed_or_None, read_error_or_None)] from
    Artifact.privacy_manifest_contents(). Taken as an argument rather than read
    from an Artifact so the selftest can hand it the exact bytes Apple refused.

    Apple: "Values for NSPrivacyAccessedAPITypeReasons keys in your app's
    privacy manifests must be valid reason codes for the corresponding API
    category." The words "for the corresponding API category" are the rule. A
    global allow-list of Apple's 17 codes passes Nearvo build 1.
    """
    out = []
    for rel, man, err in manifests:
        if err is not None:
            out.append(_f(
                "BIN-PRIVACY-MANIFEST-UNREADABLE", _pm_sev(rel),
                "A privacy manifest in the bundle could not be parsed, so its "
                "contents were not checked",
                "%s could not be read as a property list: %s. Apple validates "
                "this file at upload; an unparseable one is not a passing one, "
                "and 'I could not check' must never read as 'it is fine'."
                % (_pm_whose(rel), err),
                "Open the file and fix the plist syntax, then rebuild.",
                clause="apple:required-reason-api"))
            continue
        types = man.get("NSPrivacyAccessedAPITypes")
        if types is None:
            continue                      # nothing declared; not this rule's
        if not isinstance(types, list):
            out.append(_f(
                "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                "NSPrivacyAccessedAPITypes is not an array",
                "In %s, NSPrivacyAccessedAPITypes is %s, not an array of "
                "dictionaries." % (_pm_whose(rel), type(types).__name__),
                "Make NSPrivacyAccessedAPITypes an array of dictionaries.",
                clause="apple:required-reason-api"))
            continue
        for i, ent in enumerate(types):
            where = "%s, NSPrivacyAccessedAPITypes[%d]" % (_pm_whose(rel), i)
            if not isinstance(ent, dict):
                out.append(_f(
                    "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                    "A required-reason API declaration is not a dictionary",
                    "%s is %s." % (where, type(ent).__name__),
                    "Each entry must be a dictionary with "
                    "NSPrivacyAccessedAPIType and "
                    "NSPrivacyAccessedAPITypeReasons.",
                    clause="apple:required-reason-api"))
                continue
            cat = ent.get("NSPrivacyAccessedAPIType")
            reasons = ent.get("NSPrivacyAccessedAPITypeReasons")
            known_cat = cat in APPLE_REASON_CODES
            if not known_cat:
                out.append(_f(
                    "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                    "Unrecognised required-reason API category %r" % (cat,),
                    "%s declares the category %r, which is not one of Apple's "
                    "%d categories as of %s: %s. Either it is a typo or Apple "
                    "has added a category since that date -- those look "
                    "identical from here, so this is reported rather than "
                    "guessed at."
                    % (where, cat, len(APPLE_REASON_CODES),
                       APPLE_REASON_CODES_FETCHED,
                       ", ".join(sorted(APPLE_REASON_CODES))),
                    "Re-read %s and use a listed category, or update "
                    "APPLE_REASON_CODES if Apple has changed the list."
                    % APPLE_REASON_CODES_SOURCE,
                    clause="apple:required-reason-api"))
            if reasons is None or (isinstance(reasons, list) and not reasons):
                out.append(_f(
                    "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                    "A declared API category carries no reason codes",
                    "%s declares category %r with %s. Apple requires the "
                    "reasons your app uses the API, so an empty or absent "
                    "NSPrivacyAccessedAPITypeReasons declares the category "
                    "without declaring any reason for it."
                    % (where, cat,
                       "no NSPrivacyAccessedAPITypeReasons key" if
                       reasons is None else "an empty reasons array"),
                    "Add at least one reason code valid for %r: %s."
                    % (cat, ", ".join(APPLE_REASON_CODES.get(cat, ("--",)))),
                    clause="apple:required-reason-api"))
                continue
            if not isinstance(reasons, list):
                out.append(_f(
                    "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                    "NSPrivacyAccessedAPITypeReasons is not an array",
                    "%s has NSPrivacyAccessedAPITypeReasons as %s."
                    % (where, type(reasons).__name__),
                    "Make it an array of reason-code strings.",
                    clause="apple:required-reason-api"))
                continue
            for code in reasons:
                if not isinstance(code, str):
                    out.append(_f(
                        "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                        "A reason code is not a string",
                        "%s lists %r (%s) as a reason code."
                        % (where, code, type(code).__name__),
                        "Reason codes are strings such as \"CA92.1\".",
                        clause="apple:required-reason-api"))
                    continue
                home = APPLE_CODE_HOME.get(code)
                if not known_cat:
                    continue              # already reported; don't double up
                if home == cat:
                    continue              # valid FOR THIS CATEGORY
                if home is not None:
                    # THE NEARVO CASE. Apple's exact objection.
                    out.append(_f(
                        "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                        "Reason code %s is valid, but not in the %s category"
                        % (code, cat.replace(
                            "NSPrivacyAccessedAPICategory", "")),
                        "%s declares %r under %s. %s is a valid code -- it "
                        "belongs to %s. Valid codes for %s are: %s. This is "
                        "the exact shape of ITMS-91055, which bounced Nearvo "
                        "1.0.0 build 1 twice on 2026-09-07 with: \"contains "
                        "%r as the value for a NSPrivacyAccessedAPITypeReasons "
                        "key instead of a valid reason code for using an API "
                        "in the %s category\". Because the code is valid "
                        "elsewhere, a check against a flat list of Apple's %d "
                        "codes passes this manifest."
                        % (where, code, cat, code, home, cat,
                           ", ".join(APPLE_REASON_CODES[cat]), code, cat,
                           len(APPLE_CODE_HOME)),
                        "Either move %s under %s, or replace it with a code "
                        "that is valid for %s (%s) -- whichever matches what "
                        "the app actually does. Do not guess: picking the "
                        "wrong one reproduces the same rejection. Source: %s."
                        % (code, home, cat,
                           ", ".join(APPLE_REASON_CODES[cat]),
                           APPLE_REASON_CODES_SOURCE),
                        clause="apple:required-reason-api"))
                else:
                    out.append(_f(
                        "BIN-PRIVACY-REASON-CODE-INVALID", _pm_sev(rel),
                        "Unrecognised reason code %r" % (code,),
                        "%s declares %r under %s, and %r is not one of "
                        "Apple's %d reason codes in ANY category as of %s. "
                        "Reported separately from a misfiled code on purpose: "
                        "from here, \"Apple added a code\" and \"this code is "
                        "in the wrong category\" are indistinguishable."
                        % (where, code, cat, code, len(APPLE_CODE_HOME),
                           APPLE_REASON_CODES_FETCHED),
                        "Check %s. If the code is current, update "
                        "APPLE_REASON_CODES and record the new fetch date; if "
                        "not, replace it with a valid code for %s (%s)."
                        % (APPLE_REASON_CODES_SOURCE, cat,
                           ", ".join(APPLE_REASON_CODES[cat])),
                        clause="apple:required-reason-api"))
    return out


def privacy_tracking_findings(manifests):
    """BIN-PRIVACY-TRACKING-INCONSISTENT -- Apple's tracking invariant.

    Apple's ITMS-91064 email states ONE direction, verbatim:

        "NSPrivacyTracking must be true if NSPrivacyTrackingDomains isn't
         empty."

    THAT SENTENCE ALONE WOULD HAVE BEEN GREEN ON THE BUILD IT CAME FROM, and
    that is the whole reason this docstring is long. FlirtGym 1.0.0 build 24
    was rejected on 2026-08-03, and build 25 three hours later with identical
    text. Its manifest violated the OTHER direction: NSPrivacyTracking=true
    with an EMPTY NSPrivacyTrackingDomains array. Established from the shipped
    artifact and from tracked config independently --
      * RizzMaxx@c86f432, from the build-25 .ipa: "the app's own
        Payload/FlirtGym.app/PrivacyInfo.xcprivacy shipped
        NSPrivacyTracking=<true/> with an EMPTY NSPrivacyTrackingDomains
        array";
      * RizzMaxx@c9b152f app.json (buildNumber 24) sets NSPrivacyTracking:true
        and has NO NSPrivacyTrackingDomains key, and @expo/config-plugins
        ios/PrivacyInfo.js mergePrivacyInfo() defaults that key to [] and
        always emits it -- so prebuild wrote true + [].
    So the canary for this rule is the shape Apple rejected, NOT the shape
    Apple's sentence describes.

    Apple documents both directions; only one made it into the email. Fetched
    2026-10-15 from the DocC JSON behind the reference pages:
      * NSPrivacyTracking -- "When set to `true` you need to provide a list of
        internet domains in NSPrivacyTrackingDomains."   (true => non-empty)
      * NSPrivacyTrackingDomains -- "To provide a list of internet domains in
        `NSPrivacyTrackingDomains`, set `NSPrivacyTracking` to `true`."
                                                          (non-empty => true)
    Together: one biconditional. tracking == true  <=>  domains non-empty.
    """
    out = []
    for rel, man, err in manifests:
        if err is not None:
            continue                      # reported by the reason-code rule
        has_t = "NSPrivacyTracking" in man
        tracking = man.get("NSPrivacyTracking")
        domains = man.get("NSPrivacyTrackingDomains")
        if domains is None:
            domains = []
        if not isinstance(domains, list):
            out.append(_f(
                "BIN-PRIVACY-TRACKING-INCONSISTENT", _pm_sev(rel),
                "NSPrivacyTrackingDomains is not an array",
                "%s has NSPrivacyTrackingDomains as %s."
                % (_pm_whose(rel), type(domains).__name__),
                "Make it an array of domain strings.",
                clause="apple:privacy-tracking"))
            continue
        real = [d for d in domains
                if isinstance(d, str) and d.strip()]
        if domains and not real:
            out.append(_f(
                "BIN-PRIVACY-TRACKING-INCONSISTENT", _pm_sev(rel),
                "NSPrivacyTrackingDomains has entries but no usable domain",
                "%s lists %d tracking domain entr%s, none of which is a "
                "non-blank string: %r."
                % (_pm_whose(rel), len(domains),
                   "y" if len(domains) == 1 else "ies", domains),
                "List the real tracking endpoints, or remove the key and set "
                "NSPrivacyTracking to false.",
                clause="apple:privacy-tracking"))
        if has_t and not isinstance(tracking, bool):
            out.append(_f(
                "BIN-PRIVACY-TRACKING-INCONSISTENT", _pm_sev(rel),
                "NSPrivacyTracking is not a boolean",
                "%s has NSPrivacyTracking as %r (%s). Apple requires a "
                "Boolean; a string \"true\" is not one, and a plist will "
                "carry it through as a string."
                % (_pm_whose(rel), tracking, type(tracking).__name__),
                "Set NSPrivacyTracking to a real boolean true or false.",
                clause="apple:privacy-tracking"))
            continue

        is_true = tracking is True
        if bool(real) == is_true:
            continue                      # the invariant holds

        if real and not is_true:
            # Apple's emailed direction.
            out.append(_f(
                "BIN-PRIVACY-TRACKING-INCONSISTENT", _pm_sev(rel),
                "NSPrivacyTrackingDomains is not empty but NSPrivacyTracking "
                "is not true",
                "%s lists %d tracking domain(s) (%s) while NSPrivacyTracking "
                "is %s. Apple, verbatim in ITMS-91064: \"NSPrivacyTracking "
                "must be true if NSPrivacyTrackingDomains isn't empty.\" And "
                "in the NSPrivacyTrackingDomains reference: \"To provide a "
                "list of internet domains in NSPrivacyTrackingDomains, set "
                "NSPrivacyTracking to true.\""
                % (_pm_whose(rel), len(real), ", ".join(real),
                   "absent" if not has_t else repr(tracking)),
                "If the app really does track, set NSPrivacyTracking to true. "
                "If it does not, remove the domains -- but remove them "
                "because the app does not contact them, not to make the "
                "declaration quiet. A declaration is only worth correcting "
                "when it is the declaration that is wrong.",
                clause="apple:privacy-tracking"))
        else:
            # THE FLIRTGYM CASE -- the direction Apple's email does not state.
            out.append(_f(
                "BIN-PRIVACY-TRACKING-INCONSISTENT", _pm_sev(rel),
                "NSPrivacyTracking is true but NSPrivacyTrackingDomains is "
                "empty",
                "%s sets NSPrivacyTracking=true with %s. Apple's "
                "NSPrivacyTracking reference: \"When set to true you need to "
                "provide a list of internet domains in "
                "NSPrivacyTrackingDomains.\" THIS IS THE SHAPE THAT WAS "
                "ACTUALLY REJECTED: FlirtGym 1.0.0 build 24 (2026-08-03 "
                "16:48) and build 25 (19:48, identical text) both died at "
                "upload on ITMS-91064 with exactly this manifest. Note that "
                "Apple's emailed sentence -- \"NSPrivacyTracking must be true "
                "if NSPrivacyTrackingDomains isn't empty\" -- describes the "
                "OTHER direction and is satisfied here, so a rule written "
                "from the email text alone passes this manifest."
                % (_pm_whose(rel),
                   "no NSPrivacyTrackingDomains key" if
                   "NSPrivacyTrackingDomains" not in man else
                   "an empty NSPrivacyTrackingDomains array"),
                "List the tracking endpoints the app actually contacts (for "
                "FlirtGym that was ep1.facebook.com, the domain FBSDKCoreKit "
                "already declares). If the app contacts none, the honest fix "
                "is NSPrivacyTracking=false -- but only if the app genuinely "
                "does not track; do not flip the flag to silence the gate.",
                clause="apple:privacy-tracking"))
    return out


def check_binary(artifact, project_root=None):
    """Binary evidence. Reads the artifact, never the config."""
    out = []
    facts = artifact.facts()

    if facts["read_error"]:
        out.append(_f(
            "GATE-CANNOT-READ-BINARY", "critical",
            "The binary could not be read, so the gate could not evaluate it",
            facts["read_error"],
            "Install the Xcode command line tools and re-run. 'I could not "
            "check' must never read the same as 'it is fine', so this blocks."))
        return out, facts

    sdk = facts["linked_sdk"] or "0"
    try:
        major = int(str(sdk).split(".")[0])
    except ValueError:
        major = 0
    present, deleg, nconf = artifact.scene()

    # --- the iOS 27 scene rule, on the linked SDK read from the Mach-O -------
    if major >= SCENE_REQUIRED_SDK_MAJOR:
        if not deleg:
            if present and nconf == 0:
                ev = ("The binary has a UIApplicationSceneManifest whose "
                      "UISceneConfigurations names no delegate class. That "
                      "LOOKS adopted in a plist and is not adoption to UIKit: "
                      "the SIGTRAP still fires before the first frame.")
            elif present:
                ev = ("The binary's UIApplicationSceneManifest has %d "
                      "configuration entr(ies) and none names a "
                      "UISceneDelegateClassName." % nconf)
            else:
                ev = ("The binary has no UIApplicationSceneManifest at all. "
                      "Read from %s, not from app.json."
                      % os.path.relpath(artifact.plist_path, artifact.app))
            out.append(_f(
                "BIN-SCENE-NOT-ADOPTED", "critical",
                "Linked against iOS SDK %s without UIScene adoption -- this "
                "binary cannot launch for any user on iOS 27" % sdk,
                ev,
                "Add [\"expo-build-properties\", {\"ios\": "
                "{\"enableSceneSupport\": true}}] to the plugins array, then "
                "`expo prebuild --clean` and rebuild. Do not hand-write the "
                "manifest: an empty UISceneConfigurations passes a human "
                "reading and still traps.",
                clause="apple:tn3183"))
    # A binary linked below SDK 27 is exempt and must not be flagged. This is
    # the FlirtGym must-not-fire case: SDK 26.5, no manifest, entirely correct.

    # --- the plist keys, read from the artifact ------------------------------
    if facts["export_compliance"] is None:
        out.append(_f(
            "BIN-EXPORT-COMPLIANCE-MISSING", "medium",
            "ITSAppUsesNonExemptEncryption is absent from the built Info.plist",
            "The key is not in %s. Without it App Store Connect asks the "
            "export-compliance question on every single upload."
            % os.path.relpath(artifact.plist_path, artifact.app),
            "Set expo.ios.infoPlist.ITSAppUsesNonExemptEncryption and rebuild.",
            clause="ASC:export-compliance"))

    ok, detail = artifact.icon()
    if not ok:
        out.append(_f(
            "BIN-ICON-ABSENT", "high",
            "No app icon in the built bundle",
            detail + ". An icon configured in app.json that did not make it "
            "into the bundle is a failed upload, and only the bundle shows it.",
            "Check the icon path in app config, re-run prebuild, and confirm "
            "with `ls <App>.app | grep AppIcon` before uploading.",
            clause="ASC:screenshot-specifications"))

    # --- linked framework vs purpose string: the ITMS-90683 check ------------
    # Config cannot answer this. A precompiled XCFramework links what it links,
    # and deleting the key from app.json does not unlink it.
    try:
        linked = artifact.linked_system_frameworks()
    except GateError as e:
        linked = None
        out.append(_f(
            "GATE-CANNOT-READ-LINKAGE", "high",
            "Could not read which system frameworks this binary links",
            str(e),
            "Install the Xcode command line tools and re-run. This blocks "
            "rather than passing: a missing purpose string for a linked "
            "framework is the ITMS-90683 that bounced MileTruth build 3 at "
            "delivery, and it is invisible in config."))
    if linked is not None:
        have = set(artifact.usage_descriptions())
        for fw, keys in sorted(FRAMEWORK_PURPOSE_STRINGS.items()):
            if fw not in linked:
                continue
            if have.intersection(keys):
                continue
            out.append(_f(
                "BIN-FRAMEWORK-PURPOSE-STRING-%s" % fw, "high",
                "%s.framework is linked but no purpose string for it is in "
                "the built Info.plist" % fw,
                "Linked by: %s. The built Info.plist has none of %s. App "
                "config may well say this permission is off, or say nothing "
                "at all -- that deletes the key and cannot remove the "
                "linkage, which is exactly how MileTruth build 3 was rejected "
                "at delivery with ITMS-90683. Apple reads the Mach-O, not "
                "app.json, and says so in the rejection: \"If you\'re using "
                "external libraries or SDKs, they may reference APIs that "
                "require a purpose string. While your app might not use these "
                "APIs, a purpose string is still required.\""
                % (", ".join(linked[fw]), ", ".join(keys)),
                "Add one of %s to the app config\'s ios.infoPlist with an "
                "honest purpose string. If the app does not use the "
                "capability, say so plainly -- Apple requires the string, not "
                "a use, and inventing a use is worse. Do NOT try to remove "
                "the linkage unless you can prove the removal: setting a "
                "plugin permission option to false is the approach that "
                "already failed, and %s arrives by Swift autolinking from the "
                "Expo modules runtime, not from one named package -- measured "
                "2026-10-15, 26 of the static libraries in a MoveWitness "
                "build carry a `-framework CoreMotion` LC_LINKER_OPTION and "
                "that app has no location or sensor dependency at all. "
                "Confirm the fix with `otool -L` and plutil on the REBUILT "
                "binary, never with app.json."
                % (keys[0], fw),
                clause="5.1.1", confidence="high"))

    # --- build number reuse: the collision that bounces at UPLOAD PROCESSING -
    # One FlirtGym rejection was not a review rejection at all: it was rejected
    # at upload processing over a version-number collision. No review-focused
    # check would ever look for it, and it is cheap to see locally -- the gate
    # already keeps a ledger of every binary it has evaluated, so a second,
    # DIFFERENT binary at the same version+build is exactly the collision shape.
    # It is also the Vocabdrift receipt bug restated: two binaries, 1.0.1+3.
    seen = ledger_lookup(artifact, project_root)
    if seen:
        out.append(_f(
            "BIN-BUILD-NUMBER-REUSED", "high",
            "A different binary has already been gated at %s+%s"
            % (artifact.version, artifact.build),
            "This binary is %s; %s was gated as %s+%s on %s (%s). App Store "
            "Connect refuses a build number it has already accepted, and that "
            "rejection happens at UPLOAD PROCESSING, before review -- which is "
            "how one FlirtGym submission died. It also means any receipt keyed "
            "only on version+build is now ambiguous between two binaries."
            % ((artifact.binary_short() or "?"), seen.get("binary_uuid", "?"),
               seen.get("version"), seen.get("build"), seen.get("when"),
               seen.get("app_path", "?")),
            "Bump CFBundleVersion and rebuild. If this binary is a rebuild of "
            "the same source, bump anyway: the build number is what ASC keys "
            "on, and reusing it fails before anyone looks at the app.",
            clause="ASC:submit-for-review"))

    app_pm, sdk_pm = artifact.privacy_manifests()
    if app_pm is None:
        out.append(_f(
            "BIN-PRIVACY-MANIFEST-ABSENT", "high",
            "No app-level PrivacyInfo.xcprivacy in the built bundle",
            "%d SDK privacy manifest(s) are embedded in the bundle but the app "
            "target ships none. Read from the bundle, so unlike the scanner's "
            "node_modules guess there is nothing here to be unsure about."
            % len(sdk_pm),
            "Add expo.ios.privacyManifests to app config and rebuild. "
            "NSPrivacyTracking and NSPrivacyCollectedDataTypes live in the "
            "app-level manifest and nowhere else.",
            clause="apple:required-reason-api"))

    # The contents of every embedded manifest, not just their presence. The
    # absence rule above and these two are not alternatives: Nearvo build 1 and
    # FlirtGym build 24 both HAD the file.
    pm_contents = artifact.privacy_manifest_contents()
    out.extend(privacy_reason_code_findings(pm_contents))
    out.extend(privacy_tracking_findings(pm_contents))

    return out, facts


# ====================== the previously approved version, as an INPUT ========
# THE GAP THIS CLOSES, in the standard's own words (PRE-SUBMISSION-PROCESS.md
# Gate 2.1): "ITMS-90062 compares against the previously approved version,
# WHICH LIVES IN APP STORE CONNECT, NOT ON THIS MACHINE. A local ledger can
# catch reuse it has witnessed; it cannot know what Apple approved.
# Recommend the gate take the last-approved version as an input rather than
# inferring it. THIS IS THE ONE GATE INPUT THAT IS STILL MISSING."
#
# BIN-BUILD-NUMBER-REUSED above is the local half: it catches a SECOND binary
# at a stamp this machine has already gated. It cannot catch the case that
# actually bounced FlirtGym twice, three weeks apart, because the colliding
# value was never on this machine:
#
#   ITMS-90062: ... the value for key CFBundleShortVersionString [1.0.2] in
#   the Info.plist file must contain a higher version than that of the
#   previously approved version [1.0.2].
#   ITMS-90186: Invalid Pre-Release Train - The train version '1.0.2' is
#   closed for new build submissions.
#
# For any app that has EVER been live, the comparand is free and needs no
# credentials -- which is the same endpoint Apple's refusal is comparing
# against:
#
#   https://itunes.apple.com/lookup?bundleId=<id>
#
# WHY THREE QUERIES AND A CACHE-BUSTER. A single query has handed a stale
# version to three separate workers on this machine (one of them got "1.0"
# for an app that was live at 1.0.2). One query cannot tell you it was stale.
# This asks three times with a unique `_cb=` and `Cache-Control: no-cache`,
# and if the three do not agree it refuses to grant a verdict rather than
# picking one.
#
# WHY resultCount 0 BLOCKS. Five apps in this portfolio have been submitted
# twice each and never approved, so the lookup returns nothing for them -- and
# "nothing" is the answer for an app that was never approved AND the answer
# for an app whose bundle id you typed wrong AND the answer for a storefront
# hiccup. More importantly, it says nothing at all about the BUILD numbers
# already consumed, which are the thing that bounces a re-upload of a
# never-approved app and which exist only in App Store Connect ->
# TestFlight/Activity. So an absent lookup is NOT CHECKED, not clean, exactly
# as Law 3 requires. It is turned into a pass by SUPPLYING the input, which is
# the whole point of this wire:
#
#   --approved-version none            Ryan has looked: nothing approved
#   --approved-version 1.0.2           Ryan has looked: 1.0.2 is approved
#                                      (an app can be APPROVED and not yet
#                                      RELEASED; that state is invisible to
#                                      the public lookup and visible in ASC)
#   --consumed-builds 1,2,3            the build list from ASC, pasted
#
# A positive control is required before any of this is believed, and the one
# used here is in the commit message: in a single session, the same three
# cache-busted queries returned resultCount 1 for com.burbn.instagram,
# com.google.ios.youtube and com.apple.Pages, and resultCount 1 / 1.0.2 for
# com.bakerventures.vocabdrift, while returning 0 for all five of the
# never-approved Baker Ventures bundle ids in four storefronts. The five
# zeroes are a measured absence, not a broken fetch.

LOOKUP_URL = os.environ.get("SHIPGATE_LOOKUP_URL",
                            "https://itunes.apple.com/lookup")
LOOKUP_QUERIES = int(os.environ.get("SHIPGATE_LOOKUP_QUERIES", "3"))


def _version_tuple(v):
    """('1.0.2' -> (1, 0, 2)), or None if it is not a dotted integer.

    Returns None rather than guessing. A version string this cannot parse must
    not silently compare equal to anything -- that is how a rule reports clean
    on an artifact it did not understand.
    """
    if not isinstance(v, str) or not v.strip():
        return None
    parts = v.strip().split(".")
    out = []
    for p in parts:
        if not p.isdigit():
            return None
        out.append(int(p))
    return tuple(out) if out else None


def compare_versions(a, b):
    """-1 / 0 / 1 for a<b, a==b, a>b. None if either is unparseable.

    Zero-pads the shorter one, so 1.0 == 1.0.0 and 1.0.3 > 1.0 -- which is
    what Apple's comparison does and what matters here, because the App Review
    notices in this portfolio record the marketing version as "1.0" while the
    repos write "1.0.0".
    """
    ta, tb = _version_tuple(a), _version_tuple(b)
    if ta is None or tb is None:
        return None
    n = max(len(ta), len(tb))
    ta = ta + (0,) * (n - len(ta))
    tb = tb + (0,) * (n - len(tb))
    return (ta > tb) - (ta < tb)


def lookup_approved_version(bundle_id, queries=None, timeout=10):
    """Ask Apple what version of this bundle id is live. Three times.

    Returns a dict:
        status  "live"        -> version/release_date are Apple's answer
                "absent"     -> every query agreed on resultCount 0
                "unstable"   -> the queries disagreed; no verdict is granted
                "unreachable"-> the endpoint could not be read at all
        version, release_date, track, queries (the per-query raw answers)

    Standard library only, deliberately: this runs on a machine where the
    gate must work with nothing installed.
    """
    import json as _json                                  # noqa: PLC0415
    import random                                         # noqa: PLC0415
    import time as _time                                  # noqa: PLC0415
    import urllib.error                                   # noqa: PLC0415
    import urllib.parse                                   # noqa: PLC0415
    import urllib.request                                 # noqa: PLC0415

    n = queries or LOOKUP_QUERIES
    answers = []
    errors = []
    for i in range(n):
        cb = "%d-%d-%d" % (int(_time.time() * 1000), i,
                           random.randint(0, 10 ** 9))
        url = "%s?%s" % (LOOKUP_URL, urllib.parse.urlencode(
            {"bundleId": bundle_id, "country": "us", "_cb": cb}))
        req = urllib.request.Request(url, headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "shipcheck-gate/1 (+presubmission)",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as fh:
                body = fh.read().decode("utf-8", "replace")
            data = _json.loads(body)
        except Exception as e:                            # noqa: BLE001
            errors.append("query %d: %s" % (i + 1, e))
            answers.append(None)
            continue
        count = data.get("resultCount") or 0
        if count and data.get("results"):
            r = data["results"][0]
            answers.append({
                "resultCount": count,
                "version": r.get("version"),
                "release_date": r.get("currentVersionReleaseDate"),
                "track": r.get("trackName"),
            })
        else:
            answers.append({"resultCount": 0, "version": None,
                            "release_date": None, "track": None})

    got = [a for a in answers if a is not None]
    if not got:
        return {"status": "unreachable", "version": None, "release_date": None,
                "track": None, "queries": answers, "errors": errors}
    keys = {(a["resultCount"] and 1, a["version"]) for a in got}
    if len(keys) > 1:
        return {"status": "unstable", "version": None, "release_date": None,
                "track": None, "queries": answers, "errors": errors}
    a0 = got[0]
    if not a0["resultCount"]:
        return {"status": "absent", "version": None, "release_date": None,
                "track": None, "queries": answers, "errors": errors}
    return {"status": "live", "version": a0["version"],
            "release_date": a0["release_date"], "track": a0["track"],
            "queries": answers, "errors": errors}


def check_store_version(artifact, approved=None, consumed_builds=None,
                        lookup=None):
    """ITMS-90062 / ITMS-90186, against the version Apple actually approved.

    `approved` is the operator's input and OUTRANKS the lookup, because an
    approved-but-unreleased version exists only in App Store Connect:
        None        -> ask Apple's public lookup
        "none"      -> the operator states nothing is approved
        "1.0.2"     -> the operator states this is approved
    `consumed_builds` is the CFBundleVersion list from ASC, if the operator
    has it.

    Returns (findings, state) where state is one of
    "live"/"none-approved"/"absent"/"unstable"/"unreachable".
    """
    out = []
    bundle_id = artifact.bundle_id
    ours = artifact.version
    src = "App Store Connect, supplied by the operator"

    if approved is not None:
        a = str(approved).strip()
        if a.lower() in ("none", "null", "-", ""):
            info = {"status": "none-approved", "version": None,
                    "release_date": None, "queries": [], "errors": []}
        else:
            info = {"status": "live", "version": a, "release_date": None,
                    "queries": [], "errors": []}
    else:
        src = "itunes.apple.com/lookup?bundleId=%s, %d cache-busted queries" \
              % (bundle_id, LOOKUP_QUERIES)
        info = lookup(bundle_id) if lookup else lookup_approved_version(
            bundle_id)

    status = info["status"]
    detail_q = "; ".join(
        "query %d: %s" % (i + 1,
                          "unreadable" if a is None else
                          ("resultCount %s, version %s"
                           % (a["resultCount"], a["version"])))
        for i, a in enumerate(info.get("queries") or [])) or "(not queried)"

    if status == "unreachable":
        out.append(_f(
            "GATE-APPROVED-VERSION-UNREACHABLE", "high",
            "Could not read the previously approved version, so ITMS-90062 "
            "was not evaluated",
            "Source: %s. %s. Errors: %s. This blocks rather than passing: "
            "ITMS-90062 is a comparison against a value that is not on this "
            "machine, and a comparison that did not happen must not read the "
            "same as one that passed."
            % (src, detail_q, "; ".join(info.get("errors") or []) or "none"),
            "Re-run with network, or supply the value from App Store Connect: "
            "`--approved-version 1.0.2`, or `--approved-version none` if ASC "
            "shows nothing approved.",
            clause="ASC:submit-for-review"))
        return out, status

    if status == "unstable":
        out.append(_f(
            "GATE-APPROVED-VERSION-UNSTABLE", "high",
            "Apple's lookup gave different answers to the same question, so "
            "no verdict is granted",
            "Source: %s. %s. A single lookup has returned a stale version to "
            "three separate workers on this machine; that is why this asks "
            "more than once, and why disagreement refuses rather than picks."
            % (src, detail_q),
            "Re-run. If it keeps disagreeing, take the number from App Store "
            "Connect and pass `--approved-version <x>`.",
            clause="ASC:submit-for-review"))
        return out, status

    if status == "absent":
        out.append(_f(
            "GATE-APPROVED-VERSION-UNKNOWN", "high",
            "This app has never been live, so neither the approved version "
            "nor the consumed build numbers can be read from here",
            "Source: %s -> %s. resultCount 0 is a MEASURED absence: in the "
            "same session the same three queries returned resultCount 1 for "
            "com.burbn.instagram, com.google.ios.youtube, com.apple.Pages "
            "and com.bakerventures.vocabdrift. So the method works and this "
            "bundle id is genuinely not on the store.\n"
            "What that does and does not settle: ITMS-90062 cannot fire "
            "(there is no approved version to be lower than), so the "
            "marketing version may stay as it is. What it does NOT settle is "
            "CFBundleVersion reuse -- this binary is %s+%s, the App Review "
            "notices in this portfolio carry a marketing version and no "
            "build number, and the builds already consumed exist only in App "
            "Store Connect -> this app -> TestFlight/Activity. An app "
            "submitted twice at build 1 bounces a third upload at build 1, "
            "before review."
            % (src, detail_q, ours, artifact.build),
            "One glance in App Store Connect, then re-run with "
            "`--approved-version none --consumed-builds 1,2,3` (the build "
            "list, comma separated). That turns this from an unknown into an "
            "input, which is the point. Until then, bump CFBundleVersion with "
            "headroom above anything plausibly consumed.",
            clause="ASC:submit-for-review"))
        return out, status

    if status == "none-approved":
        if consumed_builds and str(artifact.build) in consumed_builds:
            out.append(_f(
                "BIN-BUILD-NUMBER-CONSUMED", "critical",
                "CFBundleVersion %s has already been used for this app"
                % artifact.build,
                "The operator supplied App Store Connect's consumed build "
                "list for this app: %s. This binary is %s+%s. App Store "
                "Connect refuses a build number it has already accepted, and "
                "that refusal happens at UPLOAD PROCESSING, before review."
                % (", ".join(sorted(consumed_builds)), ours, artifact.build),
                "Bump CFBundleVersion above every value in that list and "
                "rebuild. Note that `ios/` is generated: bumping app config "
                "without re-running `expo prebuild` leaves the old value in "
                "the built Info.plist.",
                clause="ASC:submit-for-review"))
        return out, status

    # status == "live": the comparison Apple's refusal actually makes.
    theirs = info["version"]
    cmp = compare_versions(ours, theirs)
    where = "%s%s" % (src, (" (released %s)" % info["release_date"])
                      if info.get("release_date") else "")
    if cmp is None:
        out.append(_f(
            "GATE-APPROVED-VERSION-UNPARSEABLE", "high",
            "Could not compare this build's version with the approved one",
            "This binary is CFBundleShortVersionString %r; the approved "
            "version is %r. One of them is not a dotted integer, so no "
            "ordering is asserted. Source: %s." % (ours, theirs, where),
            "Establish the ordering by hand and pass `--approved-version`.",
            clause="ASC:submit-for-review"))
        return out, status
    if cmp > 0:
        if consumed_builds and str(artifact.build) in consumed_builds:
            out.append(_f(
                "BIN-BUILD-NUMBER-CONSUMED", "critical",
                "CFBundleVersion %s has already been used for this app"
                % artifact.build,
                "Approved version %s per %s; this binary is %s+%s, which is "
                "higher -- but the operator's consumed build list for this "
                "app is %s and it contains %s."
                % (theirs, where, ours, artifact.build,
                   ", ".join(sorted(consumed_builds)), artifact.build),
                "Bump CFBundleVersion above every value in that list and "
                "rebuild.",
                clause="ASC:submit-for-review"))
        return out, status

    # cmp <= 0 -- this upload is refused before anyone looks at the app.
    equal = cmp == 0
    out.append(_f(
        "BIN-VERSION-NOT-ABOVE-APPROVED", "critical",
        "CFBundleShortVersionString %s is %s the approved version %s, so this "
        "upload is refused before review"
        % (ours, "not higher than" if equal else "LOWER than", theirs),
        "Approved version read from %s. This binary's built Info.plist says "
        "%s+%s. Apple's verbatim refusal for exactly this, FlirtGym build 35: "
        "\"ITMS-90062: ... the value for key CFBundleShortVersionString "
        "[1.0.2] in the Info.plist file must contain a higher version than "
        "that of the previously approved version [1.0.2].\"%s\n"
        "This is the one gate input that was missing: the comparand is not on "
        "this machine and the local ledger cannot know it. It is free for any "
        "app that has ever been live."
        % (where, ours, artifact.build,
           ("\nAnd because the two are EQUAL, expect ITMS-90186 as well: "
            "\"Invalid Pre-Release Train - The train version '%s' is closed "
            "for new build submissions.\" FlirtGym took both codes together, "
            "twice, three weeks apart." % ours) if equal else ""),
        "Raise CFBundleShortVersionString above %s in tracked app config, "
        "re-run `expo prebuild` (ios/ is generated -- bumping config alone "
        "leaves the old value in the built plist) and rebuild. Do not upload "
        "this binary." % theirs,
        clause="ASC:submit-for-review"))
    return out, status


def check_provenance(artifact, project_root):
    """Is the artifact's safety reproducible from tracked config?"""
    status, detail = scene_provenance(project_root, artifact)
    if status == "unexplained":
        return [_f(
            "GATE-SCENE-PROVENANCE-UNTRACKED", "critical",
            "This binary's iOS-27 safety is not reproducible from tracked "
            "config -- it exists on this machine and nowhere else",
            detail,
            "Put the opt-in in tracked config: [\"expo-build-properties\", "
            "{\"ios\": {\"enableSceneSupport\": true}}] in app.json, then "
            "`expo prebuild --clean` and rebuild from a clean checkout to "
            "prove it. A hand-edited ios/Info.plist in a gitignored directory "
            "vanishes on the next clean prebuild or fresh clone, and the "
            "binary that replaces it will not launch on iOS 27.")], status
    if status == "unknown":
        return [_f(
            "GATE-SCENE-PROVENANCE-UNKNOWN", "high",
            "Could not establish whether this binary's scene manifest is "
            "reproducible from tracked config",
            detail,
            "Re-run with --project pointing at the git repo this artifact was "
            "built from. The gate blocks rather than passing, because 'I could "
            "not check' is not 'it is fine'.")], status
    return [], status


def check_launch(artifact, project_root):
    r = load_receipt(artifact, "launch", project_root)
    state, why = match_receipt(artifact, r)
    if state in ("exact", "sibling"):
        frame = (r or {}).get("first_frame") or {}
        if frame.get("verdict") == "blank":
            return [_f(
                "GATE-LAUNCH-BLANK-FRAME", "critical",
                "The app launched but drew a blank first frame",
                "Launch receipt records a first frame of %s distinct sampled "
                "colours with %.1f%% of the frame one flat colour, on %s. The "
                "process survived, so a liveness check would have called this a "
                "pass." % (frame.get("colors"),
                           100.0 * float(frame.get("dominant") or 1),
                           (r or {}).get("runtime")),
                "Launch it yourself and look at the screen. If the frame is "
                "genuinely correct (a deliberate flat splash), record "
                "`shipcheck gate attest --item reviewer-walkthrough` saying so, "
                "and the human judgement overrides this measurement.")], state
        return [], state
    sev = "critical"
    if state == "absent":
        ev = ("No launch receipt for %s@%s+%s. A correct-looking plist is not "
              "evidence that the app starts."
              % (artifact.bundle_id, artifact.version, artifact.build))
    else:
        ev = why
    return [_f(
        "GATE-LAUNCH-UNPROVEN", sev,
        "No valid proof that this build was installed, launched and drew a frame",
        ev,
        "Run `shipcheck gate launch <artifact>`. It installs the app on a "
        "simulator, launches it, waits, confirms the process is alive with no "
        "new crash report, and measures the first frame -- then writes a "
        "receipt bound to this binary's LC_UUID, which stops being valid when "
        "the build number or the build-relevant plist changes.")], state


def check_stress(artifact, project_root):
    r = load_receipt(artifact, "stress", project_root)
    state, why = match_receipt(artifact, r)
    runs = (r or {}).get("patterns") or {}
    out = []
    if state not in ("exact", "sibling"):
        detail = why if state != "absent" else (
            "no stress receipt for this build")
        out.append(_f(
            "GATE-STRESS-NOT-RUN", "critical",
            "No stress pass on record for this build",
            "%s. Every one of the six patterns below caught a real defect in "
            "this portfolio in the last two days, and not one of them is "
            "visible to any scan of config or source." % detail,
            "Run `shipcheck gate stress <artifact> --run` for the patterns a "
            "tool can drive, and record the rest with `--record <pattern> "
            "--result pass|fail --note \"...\"` as they are done."))
        return out, state, runs
    for key, title, why_it_matters in STRESS_PATTERNS:
        got = runs.get(key)
        if not got:
            out.append(_f(
                "GATE-STRESS-MISSING-%s" % key, "high",
                "Stress pattern not recorded: %s" % title,
                why_it_matters,
                "Do it, then `shipcheck gate stress <artifact> --record %s "
                "--result pass --note \"what you saw\"`." % key))
        elif got.get("result") == "n/a":
            # Explicitly not applicable, with a reason on the record. Honest.
            continue
        elif got.get("result") == "fail":
            out.append(_f(
                "GATE-STRESS-FAILED-%s" % key, "critical",
                "Stress pattern FAILED: %s" % title,
                "Recorded %s by %s: %s" % (got.get("when"), got.get("by"),
                                           got.get("note") or "(no note)"),
                "Fix the defect and re-record. A recorded failure blocks; it "
                "does not expire on its own."))
    return out, state, runs


def required_attestations(artifact):
    """ATTEST_ITEMS, plus the extension item only if the bundle has one.

    Demanding an extension attestation from an app with no extension is the
    cry-wolf failure in miniature, so the requirement is derived from the
    artifact rather than asked of everybody.
    """
    items = list(ATTEST_ITEMS)
    exts = artifact.extensions()
    if exts:
        key, title, reason = EXTENSION_ATTEST
        items.append((key, title + " (%s)" % ", ".join(n for n, _p in exts),
                      reason))
    return items


def check_attestations(artifact, project_root):
    r = load_receipt(artifact, "attest", project_root)
    state, why = match_receipt(artifact, r)
    items = (r or {}).get("items") or {}
    required = required_attestations(artifact)
    out = []
    if state not in ("exact", "sibling"):
        detail = why if state != "absent" else (
            "no attestation receipt for this build")
        for key, title, reason in required:
            out.append(_f(
                "GATE-ATTEST-MISSING-%s" % key, "high",
                "Not attested: %s" % title,
                "%s %s" % (detail + ".", reason),
                "`shipcheck gate attest <artifact> --item %s --by \"<name>\" "
                "--note \"<what you did and what you saw>\"`. This is a human "
                "putting their name to it, which is worth more than a check "
                "that silently passes." % key))
        return out, state, items
    for key, title, reason in required:
        got = items.get(key)
        if not got:
            out.append(_f(
                "GATE-ATTEST-MISSING-%s" % key, "high",
                "Not attested: %s" % title, reason,
                "`shipcheck gate attest <artifact> --item %s --by \"<name>\" "
                "--note \"...\"`" % key))
        elif got.get("result") == "fail":
            out.append(_f(
                "GATE-ATTEST-FAILED-%s" % key, "critical",
                "Attested as FAILING: %s" % title,
                "Recorded %s by %s: %s" % (got.get("when"), got.get("by"),
                                           got.get("note") or "(no note)"),
                "Fix it and re-attest."))
    return out, state, items


def gate_check(artifact_path, project_root=None, approved=None,
               consumed_builds=None):
    """The whole verdict. Returns a dict; exit code is the caller's business.

    `approved`/`consumed_builds` are the App Store Connect inputs for Gate
    2.1. Left as None, the previously approved version is fetched from
    Apple's public lookup -- see check_store_version for why that is the
    right comparand and why its absence blocks.
    """
    art = Artifact(artifact_path)
    try:
        findings, facts = check_binary(art, project_root)
        store, store_state = check_store_version(
            art, approved=approved, consumed_builds=consumed_builds)
        prov, prov_state = check_provenance(art, project_root)
        launch, launch_state = check_launch(art, project_root)
        stress, stress_state, stress_runs = check_stress(art, project_root)
        attest, attest_state, attest_items = check_attestations(
            art, project_root)
        findings = findings + store + prov + launch + stress + attest
        order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        findings.sort(key=lambda f: order.get(f["severity"], 5))
        # Record that this binary was evaluated, AFTER reading the ledger, so a
        # single run never reports a collision with itself.
        ledger_append(art, project_root)
        blocking = blocking_findings(findings)
        return dict(
            artifact=artifact_path, project=project_root, facts=facts,
            evidence=dict(provenance=prov_state, launch=launch_state,
                          approved_version=store_state,
                          stress=stress_state, attest=attest_state,
                          stress_patterns=stress_runs,
                          attestations=attest_items),
            findings=findings, blocking=len(blocking),
            verdict="BLOCKED" if blocking else (
                "REVIEW" if findings else "CLEARED"))
    finally:
        art.cleanup()


# ======================================================================= sweep
# WHY THIS EXISTS, AND IT IS THE WHOLE LESSON OF THIS PROJECT AGAIN
#
# BIN-FRAMEWORK-PURPOSE-STRING was built from a real, written Apple rejection
# (MileTruth build 3, ITMS-90683, 2026-10-13) and it works: run it against a
# binary with the defect and it fires, every time. On 2026-10-14 it was
# dogfooded against "every real built binary on this machine" and reported the
# defect in Steadychart, PolicyReady and both Nearvo binaries.
#
# It said nothing about MoveWitness or DenialDesk. Both have the defect --
# measured 2026-10-15, CoreMotion linked on the app's own executable with no
# NSMotionUsageDescription in the built plist, and the existing rule fires on
# both the moment it is handed their binaries. It said nothing because THERE
# WAS NO BINARY TO HAND IT. Neither repo had an ios/ directory, so neither app
# was in the corpus, and a table of six apps with two findings reads exactly
# like a portfolio with two defective apps.
#
# That is the same failure as every row in VERIFICATION-LESSON.md -- a check
# that cannot see its subject -- arriving one level up: not a rule that cannot
# read a file, but a correct rule that was never pointed at three of the apps
# it was written for. So the fix is not in the rule. It is a command that
# enumerates the apps, and reports an app with NO ARTIFACT as a BLOCKING
# finding rather than as a quiet omission from a table.
def find_artifacts(project_root):
    """Every Release-iphone*/*.app built under this repo, newest first.

    Walks the repo rather than guessing a path, because the derived-data
    location differs per repo here (ios/build/dd, ios/build/dd-lr, and
    Xcode's own DerivedData). node_modules/Pods/.git are skipped for speed,
    not for correctness -- no .app is built inside them.
    """
    hits = []
    for base, dirs, _files in os.walk(project_root):
        dirs[:] = [d for d in dirs
                   if d not in ("node_modules", ".git", "Pods")
                   and not d.endswith(".app")]
        if os.path.basename(base).startswith("Release-iphone"):
            for d in sorted(os.listdir(base)):
                if d.endswith(".app"):
                    hits.append(os.path.join(base, d))
    hits.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return hits


def gate_sweep(roots):
    """Run the binary rules over every artifact in every repo named.

    One entry per repo, always -- including repos with nothing built, which is
    the point. `artifacts: []` plus a GATE-NO-ARTIFACT finding is the honest
    answer to "is this app clean?", and it is not "yes".
    """
    out = []
    for root in roots:
        root = os.path.abspath(root)
        apps = find_artifacts(root)
        entry = dict(project=root, artifacts=[], findings=[])
        if not apps:
            entry["findings"].append(_f(
                "GATE-NO-ARTIFACT", "critical",
                "No built binary for this app, so the gate has never looked "
                "at it",
                "No Release-iphone*/*.app exists anywhere under %s. Every "
                "binary rule -- the linked-SDK scene check, the ITMS-90683 "
                "purpose-string check, the privacy-manifest contents -- reads "
                "the artifact, so none of them has run for this app. This is "
                "reported as BLOCKING, not skipped: on 2026-10-14 MoveWitness "
                "and DenialDesk were omitted from the dogfood table for "
                "exactly this reason, and both were carrying the ITMS-90683 "
                "defect that bounced MileTruth build 3 at delivery." % root,
                "Build Release for the simulator and re-run: `npx expo "
                "prebuild -p ios` then xcodebuild -configuration Release "
                "-sdk iphonesimulator. An app with no artifact is unevaluated, "
                "not clean."))
            out.append(entry)
            continue
        for app in apps:
            art = None
            try:
                art = Artifact(app)
                findings, facts = check_binary(art, root)
                entry["artifacts"].append(dict(
                    path=app, facts=facts,
                    findings=findings))
                entry["findings"].extend(findings)
            except GateError as e:
                f = _f("GATE-CANNOT-READ-ARTIFACT", "critical",
                       "Could not read a built artifact that exists",
                       "%s: %s" % (app, e),
                       "Fix the artifact or the toolchain. An unreadable "
                       "artifact is not a pass.")
                entry["artifacts"].append(dict(path=app, facts=None,
                                               findings=[f]))
                entry["findings"].append(f)
            finally:
                if art is not None:
                    art.cleanup()
        out.append(entry)
    return out


# ====================================================================== launch
def pick_simulator(runtime_prefix):
    """A booted-or-bootable available device on a matching runtime."""
    if not _tool("xcrun"):
        raise GateError("xcrun is not on PATH")
    rc, out, _e = _run(["xcrun", "simctl", "list", "devices", "available",
                        "-j"], timeout=180)
    if rc != 0:
        raise GateError("could not list simulators")
    try:
        devices = json.loads(out)["devices"]
    except (ValueError, KeyError):
        raise GateError("could not parse simctl device list")
    booted, shutdown = [], []
    for rt, devs in devices.items():
        if runtime_prefix.lower() not in rt.lower():
            continue
        for d in devs:
            if not d.get("isAvailable"):
                continue
            entry = (d["udid"], rt.split(".")[-1], d.get("name", "?"))
            if d.get("state") == "Booted":
                booted.append(entry)
            else:
                shutdown.append(entry)
    # Prefer an already-booted device: booting another one on a machine with 30
    # simulators up and 2GB of disk free is how you take the box down.
    for pool in (booted, shutdown):
        if pool:
            return pool[0]
    raise GateError(
        "no available simulator on a runtime matching %r. The receipt cannot "
        "be earned without one -- and it will not be faked." % runtime_prefix)


def boot_sim(udid):
    """Boot the device and wait for it. `bootstatus -b` alone is not enough.

    Measured: bootstatus returned on a freshly created device that was still
    in state Shutdown, and the next install failed with CoreSimulator 405
    "Unable to lookup in current state: Shutdown". So boot explicitly first
    (tolerating "already booted"), then wait, then verify the state really did
    change -- rather than discovering it from a confusing install error.
    """
    _run(["xcrun", "simctl", "boot", udid], timeout=300)
    _run(["xcrun", "simctl", "bootstatus", udid, "-b"], timeout=600)
    for _ in range(30):
        rc, out, _e = _run(["xcrun", "simctl", "list", "devices", "-j"],
                           timeout=180)
        if rc == 0:
            try:
                for _rt, devs in json.loads(out)["devices"].items():
                    for d in devs:
                        if d.get("udid") == udid:
                            if d.get("state") == "Booted":
                                return True
            except (ValueError, KeyError):
                pass
        time.sleep(2)
    raise GateError(
        "simulator %s would not reach Booted. The launch proof cannot be "
        "earned without it, and it will not be faked." % udid)


def runtime_of(udid):
    rc, out, _e = _run(["xcrun", "simctl", "list", "devices", "-j"],
                       timeout=180)
    if rc != 0:
        return None
    try:
        devices = json.loads(out)["devices"]
    except (ValueError, KeyError):
        return None
    for rt, devs in devices.items():
        for d in devs:
            if d.get("udid") == udid:
                return rt.split(".")[-1]
    return None


def do_launch(artifact_path, udid=None, runtime="iOS-26", settle=10,
              project_root=None, out_dir=None):
    """Install, launch, verify, and write a receipt -- or write nothing."""
    art = Artifact(artifact_path)
    try:
        if not art.app.endswith(".app"):
            raise GateError("launch needs a simulator .app bundle")
        name = "?"
        if udid:
            rt = runtime_of(udid)
            if not rt:
                raise GateError("no such simulator: %s" % udid)
        else:
            udid, rt, name = pick_simulator(runtime)
        print("device  : %s (%s) %s" % (udid, rt, name))
        print("bundle  : %s  %s+%s" % (art.bundle_id, art.version, art.build))
        print("binary  : %s" % art.identity())

        boot_sim(udid)
        rc, _o, err = _run(["xcrun", "simctl", "install", udid, art.app],
                           timeout=300)
        if rc != 0:
            raise GateError("install failed: %s" % err.strip()[:400])

        crashdir = os.path.expanduser("~/Library/Logs/DiagnosticReports")
        pat = os.path.basename(art.app)[:-4]

        def ncrash():
            try:
                return len([n for n in os.listdir(crashdir)
                            if n.startswith(pat + "-")])
            except OSError:
                return 0

        before = ncrash()
        rc, out, err = _run(["xcrun", "simctl", "launch", udid,
                             art.bundle_id], timeout=180)
        print("launch  : %s" % (out.strip() or err.strip()))
        m = re.search(r":\s*(\d+)\s*$", out.strip())
        if rc != 0 or not m:
            print("FAILED TO LAUNCH -- no pid. No receipt written.")
            return 1, None
        pid = m.group(1)

        time.sleep(settle)

        alive = _run(["ps", "-p", pid])[0] == 0
        after = ncrash()
        print("alive   : %s (pid %s)" % ("yes" if alive else "no", pid))
        print("crashes : %d before, %d after" % (before, after))
        if not alive or after > before:
            print("NOT HEALTHY -- process gone and/or a new crash report. "
                  "No receipt written.")
            return 1, None

        shot_dir = out_dir or (receipt_dirs(project_root, art.app)[0])
        os.makedirs(shot_dir, exist_ok=True)
        shot = os.path.join(shot_dir, "%s@%s+%s.launch.png"
                            % (art.bundle_id, art.version, art.build))
        _run(["xcrun", "simctl", "io", udid, "screenshot", shot], timeout=180)

        frame = dict(verdict="unverified", path=shot)
        if os.path.isfile(shot):
            try:
                w, h, colors, dom = png_pixels(shot)
                frame = dict(width=w, height=h, colors=colors,
                             dominant=round(dom, 5), path=shot,
                             verdict=("rendered"
                                      if (colors >= FRAME_MIN_COLORS
                                          and dom <= FRAME_MAX_DOMINANT)
                                      else "blank"))
                print("frame   : %dx%d, %d distinct sampled colours, "
                      "%.1f%% one colour -> %s"
                      % (w, h, colors, 100.0 * dom, frame["verdict"]))
            except GateError as e:
                frame = dict(verdict="unverified", path=shot, why=str(e))
                print("frame   : could not measure (%s)" % e)
        else:
            frame["why"] = "screenshot not written"
            print("frame   : no screenshot; recorded as unverified")

        payload = dict(
            kind="launch", bundle_id=art.bundle_id, version=art.version,
            build=art.build, binary_uuid=art.identity(),
            fingerprint=art.fingerprint(), linked_sdk=art.load_versions()[0],
            scene_delegate=art.scene()[1], runtime=rt, device=udid, pid=pid,
            settle_seconds=settle, first_frame=frame,
            app_path=os.path.abspath(art.app),
            when=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            note=("Written only because the process was alive after %ds with "
                  "no new crash report. Bound to binary_uuid + fingerprint, so "
                  "it cannot vouch for a different binary of the same build."
                  % settle))
        paths = save_receipt(art, "launch", payload, project_root)
        for p in paths:
            print("receipt : %s" % p)
        if frame["verdict"] == "blank":
            print("WARNING: the app survived but drew a flat frame. The receipt "
                  "records that honestly and `gate check` will block on it.")
        return 0, payload
    finally:
        art.cleanup()


# ====================================================================== stress
def _blank_run(art, kind):
    return dict(
        kind=kind, bundle_id=art.bundle_id, version=art.version,
        build=art.build, binary_uuid=art.identity(),
        fingerprint=art.fingerprint(),
        when=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


def _load_or_new(art, kind, project_root):
    r = load_receipt(art, kind, project_root)
    state, _why = match_receipt(art, r)
    if state in ("exact", "sibling") and r:
        r.pop("_path", None)
        return r
    return _blank_run(art, kind)


def record_stress(artifact_path, pattern, result, note, by, project_root=None):
    valid = [k for k, _t, _w in STRESS_PATTERNS]
    if pattern not in valid:
        raise GateError("unknown pattern %r. Known: %s"
                        % (pattern, ", ".join(valid)))
    if result not in STRESS_RESULTS:
        raise GateError("result must be one of %s" % ", ".join(STRESS_RESULTS))
    if result == "n/a" and (not note or len(note.strip()) < 12):
        raise GateError(
            "recording a pattern as n/a requires --note saying WHY it does not "
            "apply to this app. An unexplained n/a is how a required check "
            "quietly becomes optional.")
    if result == "fail" and not note:
        raise GateError("recording a failure requires --note saying what broke")
    art = Artifact(artifact_path)
    try:
        rec = _load_or_new(art, "stress", project_root)
        rec.setdefault("patterns", {})[pattern] = dict(
            result=result, note=note or "",
            by=by or os.environ.get("USER") or "unknown",
            how="recorded",
            when=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        rec["when"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for p in save_receipt(art, "stress", rec, project_root):
            print("receipt : %s" % p)
        missing = [k for k, _t, _w in STRESS_PATTERNS
                   if k not in rec["patterns"]]
        print("recorded: %s = %s" % (pattern, result))
        print("still missing: %s" % (", ".join(missing) or "nothing"))
        return 0
    finally:
        art.cleanup()


def run_stress(artifact_path, udid=None, runtime="iOS-26", project_root=None):
    """Drive the patterns a tool can honestly drive, and say so for the rest.

    This deliberately does NOT claim to automate all six. Three of them need a
    UI driver to be meaningful (you cannot double-tap a button you cannot find,
    and 'kill the app while a field is focused' requires focusing a field), and
    simctl alone cannot take a single simulator off the network. Pretending
    otherwise would produce a receipt that says a pattern ran when nothing
    touched the app -- which is the failure this whole gate exists to stop.
    """
    art = Artifact(artifact_path)
    try:
        if udid:
            rt = runtime_of(udid) or "?"
        else:
            udid, rt, _n = pick_simulator(runtime)
        print("device  : %s (%s)" % (udid, rt))
        rec = _load_or_new(art, "stress", project_root)
        rec.setdefault("patterns", {})
        now = lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        boot_sim(udid)

        # --- empty-state: a genuinely fresh container, then look at the frame
        print("\n[empty-state] uninstall, reinstall, launch cold, measure frame")
        _run(["xcrun", "simctl", "uninstall", udid, art.bundle_id], timeout=180)
        rc, _o, err = _run(["xcrun", "simctl", "install", udid, art.app],
                           timeout=300)
        if rc != 0:
            raise GateError("install failed: %s" % err.strip()[:300])
        rc, out, _e = _run(["xcrun", "simctl", "launch", udid, art.bundle_id],
                           timeout=180)
        m = re.search(r":\s*(\d+)\s*$", out.strip())
        if not m:
            rec["patterns"]["empty-state"] = dict(
                result="fail", how="driven",
                note="cold launch on a fresh container produced no pid",
                by="shipcheck gate stress --run", when=now())
        else:
            time.sleep(8)
            alive = _run(["ps", "-p", m.group(1)])[0] == 0
            shot = os.path.join(tempfile.gettempdir(),
                                "shipgate-empty-%s.png" % art.bundle_id)
            _run(["xcrun", "simctl", "io", udid, "screenshot", shot],
                 timeout=180)
            verdict, detail = "fail", "process died on a cold first launch"
            if alive:
                try:
                    w, h, colors, dom = png_pixels(shot)
                    rendered = (colors >= FRAME_MIN_COLORS
                                and dom <= FRAME_MAX_DOMINANT)
                    verdict = "pass" if rendered else "fail"
                    detail = ("cold first launch on an empty container drew "
                              "%dx%d with %d distinct sampled colours, %.1f%% "
                              "one colour" % (w, h, colors, 100.0 * dom))
                except GateError as e:
                    verdict, detail = "pass", (
                        "cold first launch survived; frame unmeasured (%s). "
                        "A human should confirm the empty screens are "
                        "explained rather than blank." % e)
            rec["patterns"]["empty-state"] = dict(
                result=verdict, how="driven", note=detail,
                by="shipcheck gate stress --run", when=now())
            print("  -> %s: %s" % (verdict, detail))

        # --- decline-permissions: revoke everything, relaunch, must survive
        print("\n[decline-permissions] deny all privacy services, relaunch")
        _run(["xcrun", "simctl", "terminate", udid, art.bundle_id], timeout=120)
        # The action is `revoke`, not `deny`, and there is no `camera`
        # service. The first version of this used "deny" and a made-up service
        # list; every call failed with "Unknown action 'deny'", nothing was
        # revoked, and the app was then recorded as having PASSED a permission
        # denial it never saw. That is this gate's own failure mode committed
        # inside the gate, so: the revoke must succeed or the pattern is
        # recorded as NOT DRIVEN rather than as a pass.
        rc_rev, _o, rev_err = _run(
            ["xcrun", "simctl", "privacy", udid, "revoke", "all",
             art.bundle_id], timeout=180)
        if rc_rev != 0:
            rec["patterns"].pop("decline-permissions", None)
            print("  -> NOT DRIVEN: could not revoke permissions (%s). "
                  "Recording nothing rather than a pass."
                  % rev_err.strip()[:120])
        else:
            rc, out, _e = _run(["xcrun", "simctl", "launch", udid,
                                art.bundle_id], timeout=180)
            m = re.search(r":\s*(\d+)\s*$", out.strip())
            if not m:
                rec["patterns"]["decline-permissions"] = dict(
                    result="fail", how="driven",
                    note="no pid after revoking all privacy permissions",
                    by="shipcheck gate stress --run", when=now())
                print("  -> fail: no pid after revoking all permissions")
            else:
                time.sleep(8)
                alive = _run(["ps", "-p", m.group(1)])[0] == 0
                rec["patterns"]["decline-permissions"] = dict(
                    result="pass" if alive else "fail", how="driven",
                    note=("survived 8s with ALL privacy services revoked "
                          "(simctl privacy revoke all)") if alive
                         else "died after revoking all privacy services",
                    by="shipcheck gate stress --run", when=now())
                print("  -> %s (all privacy services revoked)"
                      % ("pass" if alive else "fail"))

        # --- kill-while-typing, the half a tool can do without a UI driver
        print("\n[kill-while-typing] hard-kill mid-session, relaunch cold")
        rc, out, _e = _run(["xcrun", "simctl", "launch", udid, art.bundle_id],
                           timeout=180)
        time.sleep(4)
        _run(["xcrun", "simctl", "terminate", udid, art.bundle_id], timeout=120)
        rc, out, _e = _run(["xcrun", "simctl", "launch", udid, art.bundle_id],
                           timeout=180)
        m = re.search(r":\s*(\d+)\s*$", out.strip())
        survived = bool(m)
        if survived:
            time.sleep(6)
            survived = _run(["ps", "-p", m.group(1)])[0] == 0
        rec["patterns"]["kill-while-typing"] = dict(
            result="pass" if survived else "fail",
            how="partially-driven",
            note=(("relaunch after a hard kill %s. NOT the whole pattern: "
                   "nothing typed into a field, because that needs a UI "
                   "driver. The data-loss half -- type, kill with the field "
                   "focused, relaunch, is the text still there -- must be "
                   "recorded by whoever drives the UI."
                   % ("succeeded" if survived else "FAILED"))),
            by="shipcheck gate stress --run", when=now())
        print("  -> %s (relaunch-after-kill only; the typing half needs a "
              "driver and is still owed)" % ("pass" if survived else "fail"))

        rec["when"] = now()
        for p in save_receipt(art, "stress", rec, project_root):
            print("\nreceipt : %s" % p)

        drivable = {"empty-state", "decline-permissions"}
        owed = [k for k, _t, _w in STRESS_PATTERNS
                if k not in rec["patterns"] or k not in drivable]
        print("\nNOT driven by this tool, and still required:")
        for k, title, why in STRESS_PATTERNS:
            if k in drivable:
                continue
            have = rec["patterns"].get(k)
            mark = ("partially recorded" if k == "kill-while-typing" and have
                    else ("recorded" if have else "MISSING"))
            print("  %-22s %-12s %s" % (k, mark, title))
        print("\nRecord each with: shipcheck gate stress <artifact> "
              "--record <pattern> --result pass|fail --note \"...\"")
        return 0
    finally:
        art.cleanup()


def record_attest(artifact_path, item, result, note, by, project_root=None):
    # EXTENSION_ATTEST belongs here too: the gate demands it whenever the
    # bundle has an .appex, and the first version of this function validated
    # only against ATTEST_ITEMS -- so the gate asked for an attestation it then
    # refused to accept. An unsatisfiable requirement is the worst kind of
    # cry-wolf: it cannot be cleared at all. Caught by selftest_gate.py.
    valid = [k for k, _t, _w in ATTEST_ITEMS] + [EXTENSION_ATTEST[0]]
    if item not in valid:
        raise GateError("unknown item %r. Known: %s" % (item, ", ".join(valid)))
    if result not in ("pass", "fail"):
        raise GateError("result must be 'pass' or 'fail'")
    if not by:
        raise GateError(
            "--by is required: an attestation is a person putting their name "
            "to something a tool could not check. An anonymous one is a "
            "checkbox, which is what this replaces.")
    if not note or len(note.strip()) < 12:
        raise GateError(
            "--note must say what you actually did and what you saw (at least "
            "a dozen characters). 'ok' is not an attestation.")
    art = Artifact(artifact_path)
    try:
        rec = _load_or_new(art, "attest", project_root)
        rec.setdefault("items", {})[item] = dict(
            result=result, note=note.strip(), by=by,
            when=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        rec["when"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for p in save_receipt(art, "attest", rec, project_root):
            print("receipt : %s" % p)
        print("attested: %s = %s (by %s)" % (item, result, by))
        return 0
    finally:
        art.cleanup()
