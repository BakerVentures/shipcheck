#!/usr/bin/env python3
"""ShipCheck self-test.

Runs the scanner against examples/bad-expo-app, whose violations are seeded on
purpose, and asserts each one is caught with the right clause. Also asserts the
false-positive cases that real-project dogfooding turned up, because those are
the failures that actually matter: a wrong CRITICAL on a correctly configured
app is worse than saying nothing.

    python3 scripts/selftest.py [--offline]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import report                                        # noqa: E402
import scan                                          # noqa: E402

FIXTURE = os.path.join(ROOT, "examples", "bad-expo-app")
BARE_RN_FIXTURE = os.path.join(ROOT, "examples", "bare-rn-app")
CLEAN_FIXTURE = os.path.join(ROOT, "examples", "clean-expo-app")

# examples/clean-expo-app has no seeded violations at all -- it exists because
# every other fixture is deliberately broken, so a bug in the "app is actually
# fine" reporting path (a dangling separator, a report referencing a section
# that never renders, a check with no pass entry for the success case) had no
# test coverage until this fixture was added. See git log for "v0.2.5".
CLEAN_MUST_HAVE_ZERO_FINDINGS = True
CLEAN_MUST_PASS = [
    ("1024px icon has no alpha channel", "ASC:screenshot-specifications"),
    ("Export compliance key is set", "ASC:export-compliance"),
    ("Target API level meets Play's floor", "play:target-api-level"),
    ("No placeholder text in metadata", "2.3.1"),
]

# examples/bare-rn-app has no app.json/app.config -- it exists specifically to
# catch the class of bug where a check silently assumes Expo's config shape
# and either crashes or returns nothing useful on a bare React Native project.
BARE_RN_MUST_CATCH = [
    ("bundle id read from Info.plist, no app.json present",
     lambda facts: facts.get("bundle_id") == "com.example.barern"),
    ("app name read from Info.plist CFBundleName",
     lambda facts: facts.get("app_name") == "BareRN"),
    ("icon found via Xcode AppIcon.appiconset, not Expo's assets/icon.png",
     lambda facts: (facts.get("icon") or {}).get("label") == "AppIcon.appiconset"),
]
BARE_RN_MUST_FIND = [
    ("Geolocation.getCurrentPosition called, no NSLocationWhenInUseUsageDescription",
     "PLIST-MISSING-NSLocationWhenInUseUsageDescription"),
]
BARE_RN_MUST_NOT_FIND = [
    ("BUNDLE-ID-MISSING must not fire when Info.plist has CFBundleIdentifier",
     "BUNDLE-ID-MISSING"),
    ("ICON-MISSING must not fire when an AppIcon.appiconset 1024 entry exists",
     "ICON-MISSING"),
]

# seeded violation -> (finding id, expected clause)
MUST_CATCH = [
    ("camera used, no usage string",        "PLIST-MISSING-NSCameraUsageDescription", "5.1.1"),
    ("ATT requested, no usage string",      "PLIST-MISSING-NSUserTrackingUsageDescription", "5.1.1"),
    ("Expo default photo purpose string",   "PLIST-WEAK-NSPhotoLibraryUsageDescription", "5.1.1"),
    ("weak location purpose string",        "PLIST-WEAK-NSLocationWhenInUseUsageDescription", "5.1.1"),
    ("no app privacy manifest",             "PRIVACY-MANIFEST-MISSING", "apple:required-reason-api"),
    ("expo-file-system ships no manifest",  "SDK-NO-MANIFEST-expo-file-system", "apple:required-reason-api"),
    ("expo-device ships no manifest",       "SDK-NO-MANIFEST-expo-device", "apple:required-reason-api"),
    ("third-party login, no SIWA",          "SIWA-MISSING", "4.8"),
    ("accounts, no in-app deletion",        "ACCOUNT-DELETE-MISSING", "5.1.1v"),
    ("IAP, no restorePurchases",            "RESTORE-MISSING", "3.1.1"),
    ("login wall, no demo account",         "DEMO-ACCOUNT-MISSING", "2.1"),
    ("lorem ipsum in description",          "META-PLACEHOLDER-description", "2.3.1"),
    ("TODO in What's New",                  "META-PLACEHOLDER-what's-new", "2.3.1"),
    ("icon has alpha",                      "ICON-ALPHA", "ASC:screenshot-specifications"),
    ("icon is 512x512",                     "ICON-SIZE", "ASC:screenshot-specifications"),
    # network-dependent; skipped under --offline
    ("dead privacy policy URL",             "URL-DEAD-privacy-policy-url", "5.1.1"),
    ("dead support URL",                    "URL-DEAD-support-url", "2.3.8"),
    ("app name over 30 chars",              "META-LEN-app-name", "2.3"),
    ("no export compliance key",            "EXPORT-COMPLIANCE", "ASC:export-compliance"),
    ("eas prod developmentClient",          "EAS-DEVCLIENT", "2.2"),
    ("expo-dev-client in dependencies",     "DEV-CLIENT-DEP", "2.2"),
    ("targetSdkVersion below floor",        "TARGET-SDK", "play:target-api-level"),
    ("sensitive perms need declaration",    "PLAY-DECLARATION", "play:permissions-policy"),
    ("fgs location without permission",     "FGS-PERM-location", "play:permissions-policy"),
    ("runtime perms need disclosure",       "PLAY-DISCLOSURE", "play:user-data-policy"),
    ("keywords have spaces",                "META-KEYWORDS-SPACES", "2.3.7"),
]

# regressions found by scanning real apps. each must NOT be a finding.
MUST_NOT_FIRE = [
    ("posthog-react-native is JS-only, cannot use required-reason API",
     lambda ids: not any("posthog" in i for i in ids)),
    ("async-storage ships its own manifest, so the app need not repeat it",
     lambda ids: not any("async-storage" in i for i in ids)),
    ("pod-delivered SDKs with no ios/Pods are a gap, not a finding",
     lambda ids: not any("fbsdk" in i or "purchases" in i for i in ids)),
    ("a dependency absent from node_modules is a gap, not a finding",
     lambda ids: "SDK-NO-MANIFEST-react-native" not in ids),
    ("microphone with no call site is a cleanup note, not a blocker",
     lambda ids: "PLIST-MISSING-NSMicrophoneUsageDescription" not in ids
                 and "PLIST-UNUSED-NSMicrophoneUsageDescription" in ids),
]


# Real bug, found by the LockScreen worker scanning its own project: a multi-line
# HTML comment under a field header leaked its continuation lines into the field's
# value once the opening "<!--" line was consumed, inflating App Name and Keywords
# to 727 and 238 chars against limits of 30 and 100 -- false criticals in a tool
# whose entire value is trustworthy findings. Root cause was two passes fighting
# each other in load_metadata(): a per-line "skip this line if it starts with
# <!--" filter dropped ONLY the opening line, then the whole-field regex
# (re.sub(r"<!--.*?-->", ...)) that was supposed to strip the rest of the comment
# found no "<!--" left to pair with the trailing "-->" and matched nothing, so the
# continuation lines survived into the value. Fix: let the whole-field regex be
# the only thing that strips comments -- it already handles multi-line ones
# correctly via DOTALL -- and stop pre-filtering lines one at a time.
METADATA_COMMENT_FIXTURE = """# ShipCheck metadata

## App name
<!-- 30 chars max on the App Store, 30 on Play.
     Keep it identical to Info.plist CFBundleDisplayName. -->
Real App Name

## Keywords
<!-- iOS only, 100 chars total, comma separated, no spaces after commas
     do not repeat words already in the app name -->
travel,budget,expenses,split

## Screenshot descriptions
<!-- one line per screenshot describing exactly what is shown, including any
     text overlay. ShipCheck uses this to catch screenshots that show features
     not in the build, or that contain pricing/other-platform references. -->

## Subtitle
Plain value, no comment at all
"""

METADATA_COMMENT_MUST_EQUAL = [
    ("app name", "Real App Name"),
    ("keywords", "travel,budget,expenses,split"),
    ("screenshot descriptions", ""),
    ("subtitle", "Plain value, no comment at all"),
]


def run_metadata_parser_checks():
    fails = []
    print("\nMetadata parser: multi-line HTML comments (regression for the "
          "LockScreen 727/238-char false-critical bug)")
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "shipcheck.metadata.md"), "w", encoding="utf-8") as f:
            f.write(METADATA_COMMENT_FIXTURE)
        md = scan.Scan(tmp).load_metadata()
    for field, want in METADATA_COMMENT_MUST_EQUAL:
        got = md.get(field)
        if got == want:
            print("  ok     %-28s %r" % (field, want))
        else:
            desc = "%s: got %r, want %r" % (field, got, want)
            print("  FAIL   %s" % desc); fails.append(desc)
    return fails


# Real regression, found by scanning an actual app (MoveWitness/rentcheck) during
# the 2026-09-13 outage: SIWA-MISSING and ACCOUNT-DELETE-MISSING fired as CRITICAL
# purely because @supabase/supabase-js was a package.json dependency, even though
# the app's own source explicitly documents the auth client as "CONFIGURED BUT NOT
# YET USED AT RUNTIME" and nothing in the app calls it. Fix (see scan.py's
# AUTH_CALL_PATTERN) requires an actual auth-method call site before asserting the
# CRITICAL; short of that it asserts SIWA-UNCONFIRMED / ACCOUNT-DELETE-UNCONFIRMED
# instead -- a MEDIUM, low-confidence finding that names its own uncertainty
# rather than a CRITICAL asserting something unproven. Both directions are tested:
# an app that genuinely wires up auth must still get the CRITICAL, not just the
# app with the dead wrapper getting spared.
DEAD_AUTH_WRAPPER = """\
import { createClient } from '@supabase/supabase-js';

// CONFIGURED BUT NOT YET USED AT RUNTIME -- nothing in this app calls this yet.
let client = null;
export function getSupabase() {
  if (!client) client = createClient(process.env.EXPO_PUBLIC_SUPABASE_URL, process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY);
  return client;
}
export function isSupabaseConfigured() {
  return true;
}
"""

LIVE_AUTH_WRAPPER = """\
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.EXPO_PUBLIC_SUPABASE_URL, process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY);

export async function signIn(email, password) {
  return supabase.auth.signInWithPassword({ email, password });
}
"""


def run_auth_confirmation_checks():
    fails = []
    print("\nAuth call-site confirmation (regression for the MoveWitness "
          "false-CRITICAL bug)")
    cases = [
        ("dead wrapper (MoveWitness's actual shape) must NOT assert CRITICAL",
         DEAD_AUTH_WRAPPER, {"SIWA-UNCONFIRMED", "ACCOUNT-DELETE-UNCONFIRMED"},
         {"SIWA-MISSING", "ACCOUNT-DELETE-MISSING"}),
        ("live sign-in call site must still assert CRITICAL",
         LIVE_AUTH_WRAPPER, {"SIWA-MISSING", "ACCOUNT-DELETE-MISSING"},
         {"SIWA-UNCONFIRMED", "ACCOUNT-DELETE-UNCONFIRMED"}),
    ]
    for desc, wrapper_src, want_ids, forbid_ids in cases:
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "src", "lib"), exist_ok=True)
            with open(os.path.join(tmp, "src", "lib", "supabase.ts"), "w",
                      encoding="utf-8") as f:
                f.write(wrapper_src)
            s = scan.Scan(tmp)
            s.check_signin_with_apple(["@supabase/supabase-js"], None, None)
            s.check_account_deletion(["@supabase/supabase-js"])
            ids = {f["id"] for f in s.findings}
        missing = want_ids - ids
        unwanted = forbid_ids & ids
        if not missing and not unwanted:
            print("  ok     %s" % desc)
        else:
            bits = []
            if missing:
                bits.append("missing %s" % sorted(missing))
            if unwanted:
                bits.append("should not have fired %s" % sorted(unwanted))
            fdesc = "%s (%s)" % (desc, "; ".join(bits))
            print("  FAIL   %s" % fdesc); fails.append(fdesc)
    return fails


DEAD_IAP_WRAPPER = """\
import Purchases from 'react-native-purchases';

// CONFIGURED BUT NOT YET USED AT RUNTIME -- nothing in this app calls this yet.
export function setupPurchases() {
  Purchases.setLogLevel('DEBUG');
}
"""

LIVE_IAP_WRAPPER = """\
import Purchases from 'react-native-purchases';

export async function buyPro() {
  const offerings = await Purchases.getOfferings();
  return Purchases.purchasePackage(offerings.current.availablePackages[0]);
}
"""


def run_iap_confirmation_checks():
    fails = []
    print("\nIAP call-site confirmation (same bug class as the MoveWitness "
          "false-CRITICAL fix, applied to RESTORE-MISSING)")
    cases = [
        ("dead wrapper (installed, never called) must NOT assert high-severity",
         DEAD_IAP_WRAPPER, {"RESTORE-UNCONFIRMED"}, {"RESTORE-MISSING"}),
        ("live purchase call site with no restore call must still assert high-severity",
         LIVE_IAP_WRAPPER, {"RESTORE-MISSING"}, {"RESTORE-UNCONFIRMED"}),
    ]
    for desc, wrapper_src, want_ids, forbid_ids in cases:
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "src", "lib"), exist_ok=True)
            with open(os.path.join(tmp, "src", "lib", "purchases.ts"), "w",
                      encoding="utf-8") as f:
                f.write(wrapper_src)
            s = scan.Scan(tmp)
            s.check_iap(["react-native-purchases"], None)
            ids = {f["id"] for f in s.findings}
        missing = want_ids - ids
        unwanted = forbid_ids & ids
        if not missing and not unwanted:
            print("  ok     %s" % desc)
        else:
            bits = []
            if missing:
                bits.append("missing %s" % sorted(missing))
            if unwanted:
                bits.append("should not have fired %s" % sorted(unwanted))
            fdesc = "%s (%s)" % (desc, "; ".join(bits))
            print("  FAIL   %s" % fdesc); fails.append(fdesc)
    return fails


def run_url_reachability_checks():
    fails = []
    print("\nURL reachability: confirmed-dead vs network-unconfirmed "
          "(a transient network blip during a scan must not assert the "
          "same CRITICAL as a real HTTP error response)")
    cases = [
        ("a real HTTP 404 response must still assert CRITICAL",
         lambda url, timeout=12: (False, "HTTP 404", True),
         {"URL-DEAD-privacy-policy-url"}, {"URL-UNCONFIRMED-privacy-policy-url"}),
        ("a DNS/timeout failure with no HTTP response must NOT assert CRITICAL",
         lambda url, timeout=12: (False, "URLError", False),
         {"URL-UNCONFIRMED-privacy-policy-url"}, {"URL-DEAD-privacy-policy-url"}),
    ]
    md = {"privacy policy url": "https://example.com/privacy"}
    real_head_ok = scan.head_ok
    try:
        for desc, fake_head_ok, want_ids, forbid_ids in cases:
            scan.head_ok = fake_head_ok
            with tempfile.TemporaryDirectory() as tmp:
                s = scan.Scan(tmp)
                s.check_urls(md)
                ids = {f["id"] for f in s.findings}
            missing = want_ids - ids
            unwanted = forbid_ids & ids
            if not missing and not unwanted:
                print("  ok     %s" % desc)
            else:
                bits = []
                if missing:
                    bits.append("missing %s" % sorted(missing))
                if unwanted:
                    bits.append("should not have fired %s" % sorted(unwanted))
                fdesc = "%s (%s)" % (desc, "; ".join(bits))
                print("  FAIL   %s" % fdesc); fails.append(fdesc)
    finally:
        scan.head_ok = real_head_ok
    return fails


def run_grep_truncation_checks():
    fails = []
    print("\ngrep_source file-cap truncation must not compound with a second "
          "grep into a false CRITICAL (RESTORE-MISSING / ACCOUNT-DELETE-MISSING "
          "from a search that never finished)")

    real_grep_source = scan.Scan.grep_source
    restore_pattern = (r"restorePurchases|restoreTransactions|"
                       r"syncPurchases|restore_purchases")
    delete_pattern = (r"delete[_ ]?account|deleteAccount|deleteUser|"
                      r"account[_ ]?deletion|removeAccount")

    def make_fake_grep_source(truncate_pattern):
        def fake_grep_source(self, pattern, exts=(".ts", ".tsx", ".js", ".jsx")):
            if pattern == truncate_pattern:
                self.facts.setdefault("grep_truncated", set()).add(pattern)
                return None
            return real_grep_source(self, pattern, exts)
        return fake_grep_source

    cases = [
        ("IAP: restore-call search truncated, a real purchase call site "
         "exists -- must NOT assert RESTORE-MISSING",
         "lib", "purchases.ts", LIVE_IAP_WRAPPER, restore_pattern,
         lambda s: s.check_iap(["react-native-purchases"], None),
         {"RESTORE-UNCONFIRMED"}, {"RESTORE-MISSING"}),
        ("Account deletion: delete-code search truncated, a real sign-in "
         "call site exists -- must NOT assert ACCOUNT-DELETE-MISSING",
         "lib", "supabase.ts", LIVE_AUTH_WRAPPER, delete_pattern,
         lambda s: s.check_account_deletion(["@supabase/supabase-js"]),
         {"ACCOUNT-DELETE-UNCONFIRMED"}, {"ACCOUNT-DELETE-MISSING"}),
    ]
    for desc, subdir, fname, src, truncate_pattern, run, want_ids, forbid_ids in cases:
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "src", subdir), exist_ok=True)
            with open(os.path.join(tmp, "src", subdir, fname), "w",
                      encoding="utf-8") as f:
                f.write(src)
            scan.Scan.grep_source = make_fake_grep_source(truncate_pattern)
            try:
                s = scan.Scan(tmp)
                run(s)
            finally:
                scan.Scan.grep_source = real_grep_source
            ids = {f["id"] for f in s.findings}
        missing = want_ids - ids
        unwanted = forbid_ids & ids
        if not missing and not unwanted:
            print("  ok     %s" % desc)
        else:
            bits = []
            if missing:
                bits.append("missing %s" % sorted(missing))
            if unwanted:
                bits.append("should not have fired %s" % sorted(unwanted))
            fdesc = "%s (%s)" % (desc, "; ".join(bits))
            print("  FAIL   %s" % fdesc); fails.append(fdesc)
    return fails


def run_bare_rn_checks():
    fails = []
    subprocess.run([sys.executable, os.path.join(HERE, "scan.py"),
                    "--project", BARE_RN_FIXTURE, "--offline",
                    "--out", "/tmp/shipcheck-selftest-bare-rn.json"],
                   check=True, capture_output=True)
    with open("/tmp/shipcheck-selftest-bare-rn.json", encoding="utf-8") as f:
        data = json.load(f)
    facts = data["facts"]
    ids = {f["id"] for f in data["findings"]}

    print("\nBare React Native project (no app.json)")
    for desc, pred in BARE_RN_MUST_CATCH:
        if pred(facts):
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s" % desc); fails.append(desc)
    for desc, fid in BARE_RN_MUST_FIND:
        if fid in ids:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s (not raised)" % desc); fails.append(desc)
    for desc, fid in BARE_RN_MUST_NOT_FIND:
        if fid not in ids:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s" % desc); fails.append(desc)
    return fails


def run_clean_checks():
    fails = []
    subprocess.run([sys.executable, os.path.join(HERE, "scan.py"),
                    "--project", CLEAN_FIXTURE, "--offline",
                    "--out", "/tmp/shipcheck-selftest-clean.json"],
                   check=True, capture_output=True)
    with open("/tmp/shipcheck-selftest-clean.json", encoding="utf-8") as f:
        data = json.load(f)
    findings = data["findings"]
    passes = data.get("passes") or []

    print("\nGenuinely clean project (no seeded violations)")
    if CLEAN_MUST_HAVE_ZERO_FINDINGS:
        if not findings:
            print("  ok     0 findings on a genuinely clean app")
        else:
            desc = "0 findings on a genuinely clean app"
            got = ", ".join(f["id"] for f in findings)
            print("  FAIL   %s (got: %s)" % (desc, got)); fails.append(desc)

    have = {(p.get("title"), p.get("clause")) for p in passes}
    for title, clause in CLEAN_MUST_PASS:
        if (title, clause) in have:
            print("  ok     %s" % title)
        else:
            desc = "pass: %s" % title
            print("  FAIL   %s (not recorded)" % desc); fails.append(desc)
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    cmd = [sys.executable, os.path.join(HERE, "scan.py"),
           "--project", FIXTURE, "--out", "/tmp/shipcheck-selftest.json"]
    if args.offline:
        cmd.append("--offline")
    subprocess.run(cmd, check=True, capture_output=True)
    with open("/tmp/shipcheck-selftest.json", encoding="utf-8") as f:
        data = json.load(f)

    by = {f["id"]: f for f in data["findings"]}
    ids = list(by)
    fails = []

    needs_network = {"URL-DEAD-privacy-policy-url", "URL-DEAD-support-url"}

    print("Seeded violations")
    for desc, fid, clause in MUST_CATCH:
        if args.offline and fid in needs_network:
            print("  skip   %-44s (needs network)" % desc[:44])
            continue
        f = by.get(fid)
        if not f:
            print("  FAIL   %-44s (not raised)" % desc[:44]); fails.append(desc)
        elif f["clause"] != clause:
            print("  CLAUSE %-44s got %s want %s" % (desc[:44], f["clause"], clause))
            fails.append(desc)
        else:
            print("  ok     %-44s %s" % (desc[:44], clause))

    print("\nFalse positives (found by dogfooding real apps)")
    for desc, pred in MUST_NOT_FIRE:
        if pred(ids):
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s" % desc); fails.append(desc)

    print("\nCitations")
    corpus = os.path.join(ROOT, "corpus")
    unresolved = [c for c in {f["clause"] for f in data["findings"] if f["clause"]}
                  if not report.load_clause(corpus, c)[0]]
    if unresolved:
        print("  FAIL   unresolved: %s" % unresolved); fails.append("citations")
    else:
        print("  ok     all %d clause references resolve to cached corpus files"
              % len({f["clause"] for f in data["findings"] if f["clause"]}))

    fails += run_metadata_parser_checks()
    fails += run_auth_confirmation_checks()
    fails += run_iap_confirmation_checks()
    fails += run_url_reachability_checks()
    fails += run_grep_truncation_checks()
    fails += run_bare_rn_checks()
    fails += run_clean_checks()

    print("\n%d findings, %d passes, %d gaps"
          % (len(data["findings"]), len(data.get("passes") or []), len(data["gaps"])))
    if fails:
        print("\nFAILED: %d" % len(fails))
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
