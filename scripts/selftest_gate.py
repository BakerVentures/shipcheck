#!/usr/bin/env python3
"""Regression tests for the submission gate (scripts/shipgate.py).

Modelled on scripts/selftest.py, and on the same principle: every rule here is
asserted against a real case from Ryan's portfolio, and every rule also has a
MUST-NOT-FIRE case, because a gate that blocks a good submission teaches
everyone to skip it and is worse than no gate at all.

RED THEN GREEN IS ENFORCED HERE, NOT ADVISED
--------------------------------------------
A green suite is not evidence. 2,115 Nearvo tests passed while the onboarding
loop that App Review rejected was live and shipping, and the FIRST regression
test written for that bug passed against the UNFIXED code -- it was vacuous,
and only stashing the fix and re-running revealed it. So this file does not
merely assert that each check fires on a bad fixture. For every must-catch rule
it also builds the fixture the rule is MEANT to pass, and asserts the rule is
silent on it. A rule that fires on both is indistinguishable from a rule that
always fires, which is the shape of a vacuous test.

    python3 scripts/selftest_gate.py [--artifacts]

Fixtures are synthesised: a real .app bundle is a directory with an Info.plist
and a Mach-O, and the plist half can be built from scratch. The Mach-O half
(linked SDK, LC_UUID, otool linkage) cannot be synthesised honestly, so those
are tested against REAL BINARIES on this machine when --artifacts is passed and
reported as skipped when it is not. A test that fakes `vtool` output would be
testing the fake.
"""
import argparse
import json
import os
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shipgate                                            # noqa: E402

PASS, FAIL, SKIP = "ok    ", "FAIL  ", "skip  "

# Which halves of the gate can be tested here at all.
#
# The plist half is pure Python and runs anywhere, including the Linux CI
# runner. The Mach-O half -- linked SDK, LC_UUID, otool linkage -- needs Apple's
# toolchain, and there is no honest way to fake it: a four-byte file with a
# Mach-O magic number is rejected by vtool and dwarfdump, so a "test" against
# one would be exercising the error path and calling it coverage. Those groups
# SKIP when the toolchain is absent and say so, rather than passing quietly or
# crashing the suite.
HAVE_MACHO_TOOLS = all(shutil.which(t) for t in ("vtool", "dwarfdump", "otool"))
HAVE_CLANG = bool(shutil.which("xcrun"))


class Quiet:
    """record_* print their receipt paths, which is right for a human at a
    terminal and noise in a 60-assertion suite."""

    def __enter__(self):
        self._o = sys.stdout
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
        return self

    def __exit__(self, *a):
        sys.stdout.close()
        sys.stdout = self._o
        return False


class Results:
    def __init__(self):
        self.fails = []
        self.n = 0
        self.skipped = 0

    def check(self, desc, ok, detail=""):
        self.n += 1
        if ok:
            print("  %s %s" % (PASS, desc))
        else:
            print("  %s %s%s" % (FAIL, desc, ("  -- " + detail) if detail else ""))
            self.fails.append(desc)

    def skip(self, desc, why):
        self.skipped += 1
        print("  %s %s  (%s)" % (SKIP, desc, why))


# ===================================================================== fixtures
_MACHO_CACHE = {}


def real_macho(sdk="26.0", salt=""):
    """A GENUINE Mach-O linked against `sdk`, with a real LC_UUID.

    Not a mock. A four-byte file with a Mach-O magic number is not a Mach-O:
    vtool and dwarfdump reject it, so every rule that reads the binary would be
    tested against an error path instead of against the thing it checks. One
    `clang` invocation gives a real binary whose LC_BUILD_VERSION sdk field is
    whatever we ask for, which is exactly the fact the scene rule turns on.

    This is what makes the pair of cases below meaningful rather than vacuous:
    the SAME source, linked once against SDK 26 and once against SDK 27, must
    get OPPOSITE verdicts from the scene rule. If a mock produced both, the
    test would prove nothing -- which is the Nearvo lesson.

    Returns bytes, or None when the toolchain is unavailable (then the caller
    skips rather than asserting against a fake).
    """
    key = (sdk, salt)
    if key in _MACHO_CACHE:
        return _MACHO_CACHE[key]
    if not shutil.which("xcrun"):
        _MACHO_CACHE[key] = None
        return None
    try:
        sysroot = subprocess.run(
            ["xcrun", "--sdk", "iphonesimulator", "--show-sdk-path"],
            capture_output=True, text=True, timeout=120).stdout.strip()
        if not sysroot or not os.path.isdir(sysroot):
            _MACHO_CACHE[key] = None
            return None
        with tempfile.TemporaryDirectory() as d:
            csrc = os.path.join(d, "t.c")
            with open(csrc, "w", encoding="utf-8") as f:
                # The salt changes the binary, hence the LC_UUID -- which is
                # how the "two different binaries, same version+build" cases
                # get two genuinely different identities.
                # The salt becomes a C identifier, so it must be sanitised:
                # a salt of "sdk26.0" produced marker_sdk26.0(), clang failed,
                # real_macho() returned None, and the fixture silently fell
                # back to fake bytes -- at which point every Mach-O rule was
                # being tested against its own error path. Caught by this
                # suite failing loudly rather than passing quietly.
                ident = re.sub(r"[^0-9A-Za-z_]", "_", salt or "x")
                f.write("int marker_%s(void){return %d;}\n"
                        % (ident, len(salt or "")))
                f.write("int main(void){return 0;}\n")
            out = os.path.join(d, "bin")
            p = subprocess.run(
                ["xcrun", "--sdk", "iphonesimulator", "clang",
                 "-target", "arm64-apple-ios16.4-simulator",
                 "-isysroot", sysroot, "-mios-simulator-version-min=16.4",
                 "-Wl,-platform_version,ios-simulator,16.4," + sdk,
                 csrc, "-o", out],
                capture_output=True, text=True, timeout=300)
            if p.returncode != 0 or not os.path.isfile(out):
                _MACHO_CACHE[key] = None
                return None
            with open(out, "rb") as f:
                _MACHO_CACHE[key] = f.read()
    except (OSError, subprocess.SubprocessError):
        _MACHO_CACHE[key] = None
    return _MACHO_CACHE[key]


def make_app(tmp, name="Fix", plist=None, exe_bytes=None, plugins=None,
             sdk="26.0", salt=None):
    """A .app directory with a real Info.plist and a real Mach-O."""
    if exe_bytes is None:
        exe_bytes = real_macho(sdk, salt if salt is not None else name)
        if exe_bytes is None:
            exe_bytes = b"\xcf\xfa\xed\xfe fake"
    app = os.path.join(tmp, name + ".app")
    os.makedirs(app, exist_ok=True)
    d = {
        "CFBundleIdentifier": "com.example." + name.lower(),
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1",
        "CFBundleExecutable": name,
        "CFBundleName": name,
    }
    d.update(plist or {})
    with open(os.path.join(app, "Info.plist"), "wb") as f:
        plistlib.dump(d, f)
    with open(os.path.join(app, name), "wb") as f:
        f.write(exe_bytes)
    for pname, pplist in (plugins or {}).items():
        pdir = os.path.join(app, "PlugIns", pname)
        os.makedirs(pdir, exist_ok=True)
        with open(os.path.join(pdir, "Info.plist"), "wb") as f:
            plistlib.dump(pplist or {"CFBundleExecutable": "W"}, f)
    return app


SCENE_ADOPTED = {
    "UIApplicationSceneManifest": {
        "UIApplicationSupportsMultipleScenes": False,
        "UISceneConfigurations": {
            "UIWindowSceneSessionRoleApplication": [
                {"UISceneConfigurationName": "default",
                 "UISceneDelegateClassName": "EXExpoAppSceneDelegate"}]}}}

# The trap that looks like the fix. A worker shipped exactly this and reported
# it as proof the fix does not work.
SCENE_EMPTY = {
    "UIApplicationSceneManifest": {
        "UIApplicationSupportsMultipleScenes": False,
        "UISceneConfigurations": {}}}


def git_init(root, files):
    """A real git repo with real tracked files -- provenance reads git."""
    subprocess.run(["git", "init", "-q", root], check=True,
                   capture_output=True)
    for rel, content in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(content, bytes):
            with open(p, "wb") as f:
                f.write(content)
        else:
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
        subprocess.run(["git", "-C", root, "add", rel], check=True,
                       capture_output=True)
    subprocess.run(["git", "-C", root, "-c", "user.email=t@t", "-c",
                    "user.name=t", "commit", "-qm", "fixture"], check=True,
                   capture_output=True)


# =============================================================== scene / plist
def test_scene_rules(r):
    print("\nScene adoption, read from the artifact's own Info.plist")
    with tempfile.TemporaryDirectory() as tmp:
        cases = [
            ("absent manifest  -> not adopted", {}, False, None),
            ("EMPTY UISceneConfigurations -> NOT adoption (the lookalike trap)",
             SCENE_EMPTY, True, None),
            ("named delegate -> adopted", SCENE_ADOPTED, True,
             "EXExpoAppSceneDelegate"),
        ]
        for desc, extra, want_present, want_deleg in cases:
            a = shipgate.Artifact(make_app(tmp, "S%d" % len(desc), extra))
            present, deleg, _n = a.scene()
            r.check(desc, present == want_present and deleg == want_deleg,
                    "got present=%s delegate=%s" % (present, deleg))
            a.cleanup()


def test_scene_sdk_gate(r):
    """The pair that makes the scene rule non-vacuous.

    ONE source, linked twice: against SDK 26 and against SDK 27. Same absent
    manifest in both. The rule must be SILENT on the 26 build (the FlirtGym
    must-not-fire: it is correct and launches fine) and must FIRE on the 27
    build (the Vocabdrift must-catch: it cannot start for anybody on iOS 27).

    If both verdicts came out the same, the rule would be either always-on or
    always-off, and asserting only the firing half would be the vacuous test
    that let Nearvo's onboarding loop ship behind 2,115 green tests.
    """
    print("\nScene rule vs linked SDK -- one source, two SDKs, opposite "
          "verdicts (this is the red-and-green pair)")
    if real_macho("26.0") is None or real_macho("27.0") is None:
        r.skip("SDK-gated scene rule", "no iphonesimulator clang toolchain")
        return
    with tempfile.TemporaryDirectory() as tmp:
        for sdk, must_fire in (("26.0", False), ("27.0", True)):
            a = shipgate.Artifact(make_app(tmp, "Sdk" + sdk.replace(".", ""),
                                           {}, sdk=sdk, salt="sdk" + sdk))
            got_sdk, _m = a.load_versions()
            fids = {f["id"] for f in shipgate.check_binary(a)[0]}
            fired = "BIN-SCENE-NOT-ADOPTED" in fids
            r.check("SDK %s + no manifest -> scene rule %s  [read %s]"
                    % (sdk, "FIRES" if must_fire else "is SILENT", got_sdk),
                    fired == must_fire and got_sdk.startswith(sdk.split(".")[0]),
                    "fired=%s sdk=%s" % (fired, got_sdk))
            a.cleanup()

        # And the lookalike: SDK 27 WITH an empty UISceneConfigurations still
        # fires, because that is not adoption however good it looks.
        a = shipgate.Artifact(make_app(tmp, "SdkEmpty", SCENE_EMPTY,
                                       sdk="27.0", salt="empty"))
        fids = {f["id"] for f in shipgate.check_binary(a)[0]}
        r.check("SDK 27 + EMPTY UISceneConfigurations still FIRES",
                "BIN-SCENE-NOT-ADOPTED" in fids, str(sorted(fids)))
        a.cleanup()

        # MUST NOT FIRE: SDK 27 with a real named delegate.
        a = shipgate.Artifact(make_app(tmp, "SdkOk", SCENE_ADOPTED,
                                       sdk="27.0", salt="ok"))
        fids = {f["id"] for f in shipgate.check_binary(a)[0]}
        r.check("SDK 27 + a named delegate is SILENT",
                "BIN-SCENE-NOT-ADOPTED" not in fids, str(sorted(fids)))
        a.cleanup()


def test_cannot_read_blocks(r):
    if not HAVE_MACHO_TOOLS:
        r.skip("unreadable-binary blocking", "no vtool/dwarfdump/otool on this machine")
        return
    print("\n'Cannot evaluate' must never read the same as 'fine'")
    with tempfile.TemporaryDirectory() as tmp:
        a = shipgate.Artifact(make_app(tmp, "Junk", SCENE_ADOPTED,
                                       exe_bytes=b"not a mach-o at all"))
        fids = {f["id"] for f in shipgate.check_binary(a)[0]}
        r.check("an unreadable binary raises a CRITICAL, not a pass",
                "GATE-CANNOT-READ-BINARY" in fids, str(sorted(fids)))
        a.cleanup()


def test_plist_checks_fire_and_stay_silent(r):
    """Each plist rule: fires on the bad fixture, SILENT on the good one."""
    if not HAVE_MACHO_TOOLS:
        r.skip("plist rules", "no vtool/dwarfdump/otool on this machine")
        return
    print("\nPlist rules -- each must fire on the bad case AND be silent on "
          "the good one (a rule that fires on both is vacuous)")
    with tempfile.TemporaryDirectory() as tmp:
        matrix = [
            ("BIN-EXPORT-COMPLIANCE-MISSING",
             {}, {"ITSAppUsesNonExemptEncryption": False}),
            ("BIN-PRIVACY-MANIFEST-ABSENT", {}, "privacy"),
            ("BIN-ICON-ABSENT", {}, "icon"),
        ]
        for fid, bad_extra, good in matrix:
            bad = shipgate.Artifact(make_app(tmp, "Bad" + fid[4:10].replace(
                "-", ""), bad_extra))
            bad_ids = {f["id"] for f in shipgate.check_binary(bad)[0]}
            r.check("%s fires on the bad fixture" % fid, fid in bad_ids,
                    "got %s" % sorted(bad_ids))
            bad.cleanup()

            gname = "Good" + fid[4:10].replace("-", "")
            if good == "privacy":
                app = make_app(tmp, gname)
                with open(os.path.join(app, "PrivacyInfo.xcprivacy"), "wb") as f:
                    plistlib.dump({"NSPrivacyTracking": False}, f)
            elif good == "icon":
                app = make_app(tmp, gname)
                open(os.path.join(app, "AppIcon60x60@2x.png"), "wb").close()
            else:
                app = make_app(tmp, gname, good)
            g = shipgate.Artifact(app)
            good_ids = {f["id"] for f in shipgate.check_binary(g)[0]}
            r.check("%s is SILENT on the good fixture" % fid,
                    fid not in good_ids, "got %s" % sorted(good_ids))
            g.cleanup()


# ================================================================== provenance
def test_provenance(r):
    print("\nProvenance -- would a build from TRACKED config reproduce this "
          "artifact's scene manifest? (the TentClock hole)")

    # --- MUST CATCH: TentClock. Manifest in the artifact, nothing tracked.
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "tentclock")
        os.makedirs(repo)
        git_init(repo, {
            "app.json": json.dumps({"expo": {
                "name": "TentClock", "slug": "tentclock",
                "plugins": ["./plugins/withFmtConstevalFix.js"]}}),
            "plugins/withFmtConstevalFix.js": "module.exports = c => c;\n",
            ".gitignore": "ios/\n"})
        # the untracked, hand-written plist that exists on exactly one Mac
        os.makedirs(os.path.join(repo, "ios", "TentClock"))
        with open(os.path.join(repo, "ios", "TentClock", "Info.plist"),
                  "wb") as f:
            plistlib.dump(dict({"CFBundleIdentifier": "x"},
                               **{"UIApplicationSceneManifest": {
                                   "UISceneConfigurations": {
                                       "UIWindowSceneSessionRoleApplication": [
                                           {"UISceneDelegateClassName":
                                            "SceneDelegate"}]}}}), f)
        a = shipgate.Artifact(make_app(tmp, "TentClock", SCENE_ADOPTED))
        status, detail = shipgate.scene_provenance(repo, a)
        r.check("untracked hand-written manifest -> 'unexplained'",
                status == "unexplained", "got %s" % status)
        r.check("the message names the untracked file, so the fix is obvious",
                "not" in detail.lower() and "ios/" in detail,
                detail[:120])
        fids = {f["id"] for f in shipgate.check_provenance(a, repo)[0]}
        r.check("GATE-SCENE-PROVENANCE-UNTRACKED is raised",
                "GATE-SCENE-PROVENANCE-UNTRACKED" in fids, str(fids))
        a.cleanup()

    # --- MUST NOT FIRE 1: IOLTAlign. enableSceneSupport in tracked app.json,
    #     at expo ~57.0.21 -- BELOW the 57.0.23 floor the Brain documents, and
    #     it demonstrably produces a working manifest. A version floor here
    #     would block a good submission, so there is no version floor.
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "iolta")
        os.makedirs(repo)
        git_init(repo, {
            "app.json": json.dumps({"expo": {"name": "IOLTAlign", "plugins": [
                ["expo-build-properties",
                 {"ios": {"enableSceneSupport": True}}]]}}),
            "package.json": json.dumps({"dependencies": {"expo": "~57.0.21"}})})
        a = shipgate.Artifact(make_app(tmp, "IOLTAlign", SCENE_ADOPTED))
        status, _d = shipgate.scene_provenance(repo, a)
        r.check("tracked enableSceneSupport -> 'config' (no version floor: "
                "IOLTAlign ships this at expo 57.0.21)",
                status == "config", "got %s" % status)
        r.check("no provenance finding for IOLTAlign",
                not shipgate.check_provenance(a, repo)[0])
        a.cleanup()

    # --- MUST NOT FIRE 2: a bare RN repo that legitimately TRACKS ios/.
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "barern")
        os.makedirs(repo)
        buf = plistlib.dumps(dict({"CFBundleIdentifier": "com.example.barern"},
                                  **SCENE_ADOPTED))
        git_init(repo, {"ios/BareRN/Info.plist": buf})
        a = shipgate.Artifact(make_app(tmp, "BareRN", SCENE_ADOPTED))
        status, _d = shipgate.scene_provenance(repo, a)
        r.check("tracked ios/Info.plist with the manifest -> 'tracked-plist'",
                status == "tracked-plist", "got %s" % status)
        r.check("no provenance finding for a bare RN repo that tracks ios/",
                not shipgate.check_provenance(a, repo)[0])
        a.cleanup()

    # --- MUST NOT FIRE 3: an app with no manifest at all. Provenance has
    #     nothing to explain; the SCENE rule is what speaks, not this one.
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "plain")
        os.makedirs(repo)
        git_init(repo, {"app.json": "{}"})
        a = shipgate.Artifact(make_app(tmp, "Plain", {}))
        status, _d = shipgate.scene_provenance(repo, a)
        r.check("no manifest -> provenance 'n/a', not a finding",
                status == "n/a", "got %s" % status)
        r.check("no provenance finding when there is no manifest",
                not shipgate.check_provenance(a, repo)[0])
        a.cleanup()

    # --- "cannot evaluate" must never read as "fine".
    with tempfile.TemporaryDirectory() as tmp:
        a = shipgate.Artifact(make_app(tmp, "NoRepo", SCENE_ADOPTED))
        status, _d = shipgate.scene_provenance(os.path.join(tmp, "nope"), a)
        r.check("a missing project root -> 'unknown', and it BLOCKS",
                status == "unknown", "got %s" % status)
        r.check("unknown provenance raises a finding rather than passing",
                bool(shipgate.check_provenance(a, os.path.join(tmp, "x"))[0]))
        a.cleanup()


# ===================================================================== receipts
def test_receipt_binding(r):
    """The bug found by running the old gate: a receipt for another binary.

    ios27-upload-gate.sh keys on bundleid@version+build. The Vocabdrift receipt
    earned on the FIXED binary was applied to a DIFFERENT binary, same 1.0.1+3,
    with no scene manifest at all. These cases are that pair.
    """
    if not HAVE_MACHO_TOOLS:
        r.skip("receipt binding", "no vtool/dwarfdump/otool on this machine")
        return
    print("\nReceipt binding -- a proof must name the build AND the binary")
    with tempfile.TemporaryDirectory() as tmp:
        # Identity keys identical in all three, exactly as the real pair was:
        # com.bakerventures.vocabdrift 1.0.1+3. The fingerprint is computed
        # from the PLIST, so overriding the attribute would not be a fair test
        # -- the fixtures have to really collide.
        ident_keys = {"CFBundleIdentifier": "com.bakerventures.vocabdrift",
                      "CFBundleShortVersionString": "1.0.1",
                      "CFBundleVersion": "3",
                      "CFBundleExecutable": "Vocabdrift"}

        def vd(label, scene, salt):
            d = dict(ident_keys)
            d.update(scene)
            app = os.path.join(tmp, label + ".app")
            os.makedirs(app, exist_ok=True)
            with open(os.path.join(app, "Info.plist"), "wb") as f:
                plistlib.dump(d, f)
            blob = real_macho("27.0", salt) or (b"\xcf\xfa\xed\xfe" + salt.encode())
            with open(os.path.join(app, "Vocabdrift"), "wb") as f:
                f.write(blob)
            return shipgate.Artifact(app)

        fixed = vd("VdFixed", SCENE_ADOPTED, "fixedbuild")
        broken = vd("VdBroken", {}, "brokenbuild")

        base = dict(bundle_id="com.bakerventures.vocabdrift",
                    version="1.0.1", build="3")

        # exact
        rec = dict(base, binary_uuid=fixed.identity(),
                   fingerprint=fixed.fingerprint())
        state, _w = shipgate.match_receipt(fixed, rec)
        r.check("same binary -> 'exact'", state == "exact", state)

        # THE BUG: receipt from the fixed binary, checked against the broken one
        state, why = shipgate.match_receipt(broken, rec)
        r.check("receipt earned on the FIXED binary is REJECTED for the "
                "BROKEN one at the same version+build (the Vocabdrift bug)",
                state == "expired", "%s: %s" % (state, why[:90]))
        r.check("and the message explains that the plist keys disagree",
                "DISAGREE" in why or "disagree" in why, why[:90])

        # MUST NOT FIRE: the legitimate sim-build / device-build case. A
        # different binary of the same build whose gate-relevant keys agree.
        sib = vd("VdDevice", SCENE_ADOPTED, "devicebuild")
        r.check("the sibling fixture really is a different binary",
                sib.identity() != fixed.identity(),
                "%s vs %s" % (sib.identity(), fixed.identity()))
        state, why = shipgate.match_receipt(sib, rec)
        r.check("a DIFFERENT binary whose gate-relevant keys AGREE -> "
                "'sibling', accepted (sim build vouches for device build)",
                state == "sibling", "%s: %s" % (state, why[:90]))

        # expiry on a build bump -- the existing behaviour, and it is correct
        bumped_keys = dict(ident_keys, CFBundleVersion="4")
        bapp = os.path.join(tmp, "VdBump.app")
        os.makedirs(bapp, exist_ok=True)
        with open(os.path.join(bapp, "Info.plist"), "wb") as f:
            plistlib.dump(dict(bumped_keys, **SCENE_ADOPTED), f)
        with open(os.path.join(bapp, "Vocabdrift"), "wb") as f:
            f.write(real_macho("27.0", "bumpbuild") or b"\xcf\xfa\xed\xfeb")
        bumped = shipgate.Artifact(bapp)
        state, why = shipgate.match_receipt(bumped, rec)
        r.check("a build-number bump EXPIRES the receipt",
                state == "expired", state)
        r.check("absent receipt -> 'absent', never a pass",
                shipgate.match_receipt(bumped, None)[0] == "absent")
        for a in (fixed, broken, sib, bumped):
            a.cleanup()


def test_receipt_roundtrip_and_expiry(r):
    if not HAVE_MACHO_TOOLS:
        r.skip("receipts on disk", "no vtool/dwarfdump/otool on this machine")
        return
    print("\nReceipts on disk -- recorded, found, and expiring with the build")
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "proj")
        os.makedirs(repo)
        git_init(repo, {"app.json": "{}"})
        app = make_app(repo, "Round", SCENE_ADOPTED)

        a = shipgate.Artifact(app)
        with Quiet():
            for key in ("double-tap", "kill-while-typing", "no-network",
                        "empty-state", "volume", "decline-permissions",
                        "repeat-onboarding"):
                shipgate.record_stress(app, key, "pass",
                                       "driven in the fixture", "selftest",
                                       project_root=repo)
            shipgate.record_stress(app, "demo-credential", "n/a",
                                   "this app has no accounts at all",
                                   "selftest", project_root=repo)
            shipgate.record_stress(app, "account-switch", "n/a",
                                   "this app has no accounts at all",
                                   "selftest", project_root=repo)
        findings, state, runs = shipgate.check_stress(a, repo)
        r.check("a full stress record satisfies the stress gate",
                not findings and state == "exact",
                "%s %s" % (state, [f["id"] for f in findings]))
        r.check("an n/a WITH A REASON counts as satisfied",
                runs["account-switch"]["result"] == "n/a")

        try:
            with Quiet():
                shipgate.record_stress(app, "volume", "n/a", "", "selftest",
                                       project_root=repo)
            r.check("an n/a with NO reason is refused", False, "it was accepted")
        except shipgate.GateError:
            r.check("an n/a with NO reason is refused", True)

        try:
            with Quiet():
                shipgate.record_stress(app, "not-a-pattern", "pass", "x",
                                       "selftest", project_root=repo)
            r.check("an unknown pattern name is refused", False)
        except shipgate.GateError:
            r.check("an unknown pattern name is refused", True)

        # a recorded FAILURE blocks and does not quietly expire
        with Quiet():
            shipgate.record_stress(app, "double-tap", "fail",
                                   "a second tap surfaced a raw SqliteError",
                                   "selftest", project_root=repo)
        findings, _s, _r = shipgate.check_stress(a, repo)
        r.check("a recorded FAILURE blocks",
                any(f["id"] == "GATE-STRESS-FAILED-double-tap"
                    and f["severity"] == "critical" for f in findings),
                str([f["id"] for f in findings]))
        a.cleanup()

        # the same receipt must NOT satisfy the next build number
        app2 = make_app(repo, "Round2",
                        dict(SCENE_ADOPTED,
                             CFBundleIdentifier="com.example.round",
                             CFBundleVersion="2"),
                        salt="round2")
        a2 = shipgate.Artifact(app2)
        findings, state, _runs = shipgate.check_stress(a2, repo)
        r.check("the stress receipt does not carry over to a new build number",
                state in ("absent", "expired"), state)
        a2.cleanup()


def test_attestations(r):
    if not HAVE_MACHO_TOOLS:
        r.skip("attestations", "no vtool/dwarfdump/otool on this machine")
        return
    print("\nAttestations -- what a tool cannot check, it must require was done")
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "proj")
        os.makedirs(repo)
        git_init(repo, {"app.json": "{}"})

        # MUST NOT FIRE: an app with no extension is not asked about extensions
        plain = shipgate.Artifact(make_app(repo, "Plain", SCENE_ADOPTED))
        req = {k for k, _t, _w in shipgate.required_attestations(plain)}
        r.check("an app with NO extension is not asked to attest one",
                "extension-exercised" not in req, str(sorted(req)))
        r.check("but it IS asked for device-render, reviewer-walkthrough and "
                "regression-red-then-green",
                {"device-render", "reviewer-walkthrough",
                 "regression-red-then-green"}.issubset(req), str(sorted(req)))
        plain.cleanup()

        # MUST CATCH: Vocabdrift's widget. The bundle has it, so it is required.
        widget = shipgate.Artifact(make_app(
            repo, "Vocabdrift", SCENE_ADOPTED,
            plugins={"LockLearnWidget.appex": {"CFBundleExecutable": "W"}}))
        req = {k for k, _t, _w in shipgate.required_attestations(widget)}
        r.check("a bundle WITH an .appex must attest the extension was used "
                "(Vocabdrift's widget is its core feature and has never been "
                "exercised)", "extension-exercised" in req, str(sorted(req)))
        ids = {f["id"] for f in shipgate.check_attestations(widget, repo)[0]}
        r.check("and that becomes a finding until it is recorded",
                "GATE-ATTEST-MISSING-extension-exercised" in ids, str(ids))

        wpath = widget.app
        with Quiet():
            for item in ("device-render", "reviewer-walkthrough",
                         "regression-red-then-green", "extension-exercised"):
                shipgate.record_attest(wpath, item, "pass",
                                       "exercised it by hand in the fixture",
                                       "Ryan", project_root=repo)
        findings, state, _i = shipgate.check_attestations(widget, repo)
        r.check("all attestations recorded -> no findings",
                not findings and state == "exact",
                "%s %s" % (state, [f["id"] for f in findings]))

        # an anonymous or contentless attestation is not an attestation
        for bad_kw, desc in (
                (dict(by=None, note="a real note about what happened"),
                 "an attestation with no --by is refused"),
                (dict(by="Ryan", note="ok"),
                 "an attestation whose note says 'ok' is refused")):
            try:
                with Quiet():
                    shipgate.record_attest(wpath, "device-render", "pass",
                                           bad_kw["note"], bad_kw["by"],
                                           project_root=repo)
                r.check(desc, False, "it was accepted")
            except shipgate.GateError:
                r.check(desc, True)
        widget.cleanup()


def test_build_number_reuse(r):
    if not HAVE_MACHO_TOOLS:
        r.skip("build-number reuse", "no vtool/dwarfdump/otool on this machine")
        return
    print("\nBuild-number reuse -- the collision that bounces at UPLOAD "
          "PROCESSING, before review (one FlirtGym submission died here)")
    with tempfile.TemporaryDirectory() as tmp:
        repo = os.path.join(tmp, "proj")
        os.makedirs(repo)
        git_init(repo, {"app.json": "{}"})
        a = shipgate.Artifact(make_app(repo, "First", SCENE_ADOPTED))

        # MUST NOT FIRE: a first sighting is not a collision.
        ids = {f["id"] for f in shipgate.check_binary(a, repo)[0]}
        r.check("a build seen for the FIRST time is not a collision",
                "BIN-BUILD-NUMBER-REUSED" not in ids, str(sorted(ids)))
        shipgate.ledger_append(a, repo)

        # MUST NOT FIRE: re-checking the SAME binary is not a collision either.
        ids = {f["id"] for f in shipgate.check_binary(a, repo)[0]}
        r.check("re-checking the SAME binary is not a collision",
                "BIN-BUILD-NUMBER-REUSED" not in ids, str(sorted(ids)))

        # MUST CATCH: a different binary at the same version+build.
        b = shipgate.Artifact(make_app(
            repo, "Second",
            dict(SCENE_ADOPTED, CFBundleIdentifier=a.bundle_id),
            salt="second"))
        ids = {f["id"] for f in shipgate.check_binary(b, repo)[0]}
        r.check("a DIFFERENT binary at the same version+build is flagged",
                "BIN-BUILD-NUMBER-REUSED" in ids, str(sorted(ids)))

        # MUST NOT FIRE: bump the build number and the collision is gone.
        c = shipgate.Artifact(make_app(repo, "Third",
                                       dict(SCENE_ADOPTED,
                                            CFBundleIdentifier=a.bundle_id,
                                            CFBundleVersion="2"),
                                       salt="third"))
        ids = {f["id"] for f in shipgate.check_binary(c, repo)[0]}
        r.check("bumping the build number clears it",
                "BIN-BUILD-NUMBER-REUSED" not in ids, str(sorted(ids)))
        for x in (a, b, c):
            x.cleanup()


def test_frame_measurement(r):
    print("\nFirst-frame measurement -- 'it launched' is not 'it drew "
          "something'")
    with tempfile.TemporaryDirectory() as tmp:
        # A flat frame: the shape of a blank window that survives a liveness
        # check. Written as a real PNG so the real decoder is under test.
        flat = os.path.join(tmp, "flat.png")
        _write_png(flat, 64, 64, lambda x, y: (18, 18, 20))
        w, h, colors, dom = shipgate.png_pixels(flat)
        r.check("a flat frame measures as ~1 colour, ~100% dominant",
                colors <= 2 and dom > 0.99, "%d colours, %.3f" % (colors, dom))
        r.check("and is classified blank",
                not (colors >= shipgate.FRAME_MIN_COLORS
                     and dom <= shipgate.FRAME_MAX_DOMINANT))

        # MUST NOT FIRE: a real-looking frame.
        busy = os.path.join(tmp, "busy.png")
        _write_png(busy, 64, 64,
                   lambda x, y: ((x * 4) % 256, (y * 4) % 256, (x + y) % 256))
        w, h, colors, dom = shipgate.png_pixels(busy)
        r.check("a frame with content is classified rendered",
                colors >= shipgate.FRAME_MIN_COLORS
                and dom <= shipgate.FRAME_MAX_DOMINANT,
                "%d colours, %.3f" % (colors, dom))

        # The thresholds must be loose enough for real app screenshots. Real
        # launch frames on this machine sampled 217-1852 distinct colours.
        r.check("the threshold is loose (<= 12 colours) so a dark themed app "
                "is not called blank", shipgate.FRAME_MIN_COLORS <= 12,
                str(shipgate.FRAME_MIN_COLORS))


def _write_png(path, w, h, fn):
    import struct
    import zlib
    raw = b""
    for y in range(h):
        raw += b"\x00"
        for x in range(w):
            rr, gg, bb = fn(x, y)
            raw += bytes((rr, gg, bb))

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)


# =========================================================== real-binary tests
REAL = [
    # (label, artifact, project, what must be true)
    ("FlirtGym (SDK 26.5, no manifest) must NOT be flagged for the scene rule",
     "/Users/ryanbaker/Desktop/Desktop - Ryan’s MacBook Pro/RizzMaxx/ios/build/"
     "Build/Products/Debug-iphonesimulator/FlirtGym.app",
     "/Users/ryanbaker/RizzMaxx", "no-scene-finding"),
    ("FlirtGym's three usage descriptions are read FROM THE BINARY, though "
     "app.json has none of them",
     "/Users/ryanbaker/Desktop/Desktop - Ryan’s MacBook Pro/RizzMaxx/ios/build/"
     "Build/Products/Debug-iphonesimulator/FlirtGym.app",
     "/Users/ryanbaker/RizzMaxx", "usage-from-binary"),
    ("Vocabdrift (SDK 27, no manifest) MUST be flagged",
     "/Users/ryanbaker/lockscreen-learn/ios/build/Build/Products/"
     "Release-iphonesimulator/Vocabdrift.app",
     "/Users/ryanbaker/lockscreen-learn", "scene-finding"),
    ("PolicyReady's manifest is explained by tracked config -> no provenance "
     "finding",
     "/Users/ryanbaker/policyready-ios27-scene/ios/build/dd/Build/Products/"
     "Release-iphonesimulator/PolicyReady.app",
     "/Users/ryanbaker/policyready-ios27-scene", "no-provenance-finding"),
]


def test_real_binaries(r, enabled):
    print("\nReal binaries on this machine (the Mach-O half cannot be "
          "synthesised honestly)")
    if not enabled:
        r.skip("real-binary assertions", "pass --artifacts to run them")
        return
    for label, path, proj, want in REAL:
        if not os.path.exists(path):
            r.skip(label, "artifact not on disk")
            continue
        try:
            a = shipgate.Artifact(path)
        except shipgate.GateError as e:
            r.skip(label, str(e)[:60])
            continue
        try:
            fids = {f["id"] for f in shipgate.check_binary(a)[0]}
            if want == "no-scene-finding":
                sdk, _m = a.load_versions()
                r.check("%s [SDK %s]" % (label, sdk),
                        "BIN-SCENE-NOT-ADOPTED" not in fids, str(sorted(fids)))
            elif want == "scene-finding":
                sdk, _m = a.load_versions()
                r.check("%s [SDK %s]" % (label, sdk),
                        "BIN-SCENE-NOT-ADOPTED" in fids, str(sorted(fids)))
            elif want == "usage-from-binary":
                ud = a.usage_descriptions()
                want3 = {"NSCameraUsageDescription",
                         "NSPhotoLibraryUsageDescription",
                         "NSUserTrackingUsageDescription"}
                r.check(label, want3.issubset(set(ud)), str(sorted(ud)))
            elif want == "no-provenance-finding":
                pf, status = shipgate.check_provenance(a, proj)
                r.check("%s [%s]" % (label, status), not pf,
                        str([f["id"] for f in pf]))
        finally:
            a.cleanup()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", action="store_true",
                    help="also assert against real built binaries on this "
                         "machine")
    args = ap.parse_args()
    if not shutil.which("git"):
        print("git is required for the provenance fixtures")
        return 2
    # NEVER write into the real receipt store from a test run. The first
    # version of this suite wrote nine stress receipts into
    # ~/.config/shipcheck/receipts for a fixture app called "Round".
    sandbox = tempfile.mkdtemp(prefix="shipgate-selftest-receipts-")
    shipgate.HOME_RECEIPTS = sandbox
    r = Results()
    test_scene_rules(r)
    test_scene_sdk_gate(r)
    test_cannot_read_blocks(r)
    test_plist_checks_fire_and_stay_silent(r)
    test_provenance(r)
    test_receipt_binding(r)
    test_receipt_roundtrip_and_expiry(r)
    test_attestations(r)
    test_build_number_reuse(r)
    test_frame_measurement(r)
    test_real_binaries(r, args.artifacts)

    shutil.rmtree(sandbox, ignore_errors=True)
    print("\n%d checks, %d skipped" % (r.n, r.skipped))
    if r.fails:
        print("\nFAILED: %d" % len(r.fails))
        for f in r.fails:
            print("  - %s" % f)
        return 1
    print("\nAll gate checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
