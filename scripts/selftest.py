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
import shutil
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

# 2026-10-13, found pre-flighting Rigsheet: LIVE_AUTH_WRAPPER's
# signInWithPassword is plain email/password, not a third-party/social login
# -- Apple 4.8 verbatim is about "a third-party or social login service (such
# as Facebook Login, Google Sign-In...)", and a BaaS used for your own
# email/password system is neither. Rigsheet's actual deployed shape
# (resetPasswordForEmail, no OAuth anywhere) was getting SIWA-MISSING
# asserted as a false CRITICAL from AUTH_CALL_PATTERN alone. This fixture
# is the true-positive control: an actual OAuth/social call through the
# same SDK, which still must assert SIWA-MISSING.
LIVE_OAUTH_WRAPPER = """\
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(process.env.EXPO_PUBLIC_SUPABASE_URL, process.env.EXPO_PUBLIC_SUPABASE_ANON_KEY);

export async function signInWithGoogle() {
  return supabase.auth.signInWithOAuth({ provider: 'google' });
}
"""


def run_auth_confirmation_checks():
    fails = []
    print("\nAuth call-site confirmation (regression for the MoveWitness "
          "false-CRITICAL bug, and the Rigsheet plain-email/password "
          "false-CRITICAL on SIWA-MISSING)")
    cases = [
        ("dead wrapper (MoveWitness's actual shape) must NOT assert CRITICAL",
         DEAD_AUTH_WRAPPER, {"SIWA-UNCONFIRMED", "ACCOUNT-DELETE-UNCONFIRMED"},
         {"SIWA-MISSING", "ACCOUNT-DELETE-MISSING"}),
        ("live OAuth/social sign-in call site must still assert SIWA-MISSING",
         LIVE_OAUTH_WRAPPER, {"SIWA-MISSING", "ACCOUNT-DELETE-MISSING"},
         {"SIWA-UNCONFIRMED", "ACCOUNT-DELETE-UNCONFIRMED"}),
        ("plain email/password (Rigsheet's real shape) must assert "
         "ACCOUNT-DELETE-MISSING but NOT SIWA-MISSING -- 4.8 is about "
         "third-party/social login, not every account system a BaaS hosts",
         LIVE_AUTH_WRAPPER, {"ACCOUNT-DELETE-MISSING"},
         {"SIWA-MISSING", "SIWA-UNCONFIRMED", "ACCOUNT-DELETE-UNCONFIRMED"}),
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
    # head_ok now returns (ok, detail, confirmed, blocked); blocked marks a
    # 403/405-on-every-method bot block (F4).
    cases = [
        ("a real HTTP 404 response must still assert CRITICAL",
         lambda url, timeout=12: (False, "HTTP 404", True, False),
         {"URL-DEAD-privacy-policy-url"},
         {"URL-UNCONFIRMED-privacy-policy-url", "URL-BOT-BLOCKED-privacy-policy-url"}),
        ("a DNS/timeout failure with no HTTP response must NOT assert CRITICAL",
         lambda url, timeout=12: (False, "URLError", False, False),
         {"URL-UNCONFIRMED-privacy-policy-url"},
         {"URL-DEAD-privacy-policy-url", "URL-BOT-BLOCKED-privacy-policy-url"}),
        ("F4: a 403/405 bot block (answered on every method) must be low, "
         "NOT a CRITICAL dead link",
         lambda url, timeout=12: (False, "HTTP 403 (bot-blocked)", True, True),
         {"URL-BOT-BLOCKED-privacy-policy-url"},
         {"URL-DEAD-privacy-policy-url", "URL-UNCONFIRMED-privacy-policy-url"}),
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
                too_severe = [f["id"] for f in s.findings
                              if f["id"].startswith("URL-BOT-BLOCKED")
                              and scan.SEV.get(f["severity"], 0) > scan.SEV["low"]]
            missing = want_ids - ids
            unwanted = forbid_ids & ids
            if not missing and not unwanted and not too_severe:
                print("  ok     %s" % desc)
            else:
                bits = []
                if missing:
                    bits.append("missing %s" % sorted(missing))
                if unwanted:
                    bits.append("should not have fired %s" % sorted(unwanted))
                if too_severe:
                    bits.append("bot-blocked finding above low severity %s" % too_severe)
                fdesc = "%s (%s)" % (desc, "; ".join(bits))
                print("  FAIL   %s" % fdesc); fails.append(fdesc)
    finally:
        scan.head_ok = real_head_ok
    return fails


def run_redirect_following_checks():
    fails = []
    print("\n308 Permanent Redirect must be followed, not read as dead "
          "(regression: dogfooding v0.2.18 against Nearvo's real privacy "
          "URL found head_ok reading a live, 308-redirecting page as a "
          "CONFIRMED DEAD LINK -- Python's urllib has never followed 308, "
          "and Cloudflare/most static-site hosts issue it routinely)")
    import http.server
    import threading

    class _Handler(http.server.BaseHTTPRequestHandler):
        def _respond(self):
            if self.path == "/redirect":
                self.send_response(308)
                self.send_header("Location", "/final")
                self.end_headers()
            elif self.path == "/final":
                body = b"<html>real page, reached after a 308</html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command == "GET":
                    self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()

        def do_HEAD(self):
            self._respond()

        def do_GET(self):
            self._respond()

        def log_message(self, *a):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), _Handler)
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    try:
        url = "http://127.0.0.1:%d/redirect" % port
        ok, detail, confirmed, blocked = scan.head_ok(url)
        if ok and detail == "HTTP 200" and confirmed and not blocked:
            print("  ok     head_ok follows a 308 to the real 200 page "
                  "instead of reporting the redirect itself as dead")
        else:
            print("  FAIL   head_ok((ok, detail, confirmed, blocked)) = "
                  "%r, want (True, 'HTTP 200', True, False)"
                  % ((ok, detail, confirmed, blocked),))
            fails.append("redirect-following: head_ok on a 308")

        body = scan.fetch_text(url)
        if body and "real page, reached after a 308" in body:
            print("  ok     fetch_text follows a 308 and reads the real "
                  "page's content")
        else:
            print("  FAIL   fetch_text(url with a 308) = %r, want the "
                  "final page's body" % (body,))
            fails.append("redirect-following: fetch_text on a 308")
    finally:
        server.shutdown()
        t.join(timeout=5)
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


# ---------------------------------------------------------------------------
# PRIVACY-MANIFEST-MISSING false positive (found 2026-09-27, PolicyReady): the
# check only ever looked for a generated ios/<App>/PrivacyInfo.xcprivacy file
# on disk. For a managed Expo app, ios/ is CNG output -- gitignored, absent on
# a fresh checkout or in CI -- so a project with a fully correct
# `expo.ios.privacyManifests` in app.json (which is exactly ShipCheck's own
# suggested fix, and what generates that file on every prebuild) still got
# flagged. Copies bad-expo-app (which seeds this finding on purpose, and
# already has node_modules installed) rather than mutating the checked-in
# fixture, adds the config, and re-scans.
# ---------------------------------------------------------------------------

def run_privacy_manifest_config_checks():
    fails = []
    print("\nPRIVACY-MANIFEST-MISSING false positive (config-declared, no ios/)")
    with tempfile.TemporaryDirectory() as tmp:
        dest = os.path.join(tmp, "app")
        shutil.copytree(FIXTURE, dest, symlinks=True)
        app_json_path = os.path.join(dest, "app.json")
        with open(app_json_path, encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["expo"]["ios"]["privacyManifests"] = {
            "NSPrivacyTracking": False,
            "NSPrivacyTrackingDomains": [],
            "NSPrivacyCollectedDataTypes": [],
            "NSPrivacyAccessedAPITypes": [],
        }
        with open(app_json_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        # bad-expo-app has no ios/ directory at all (it seeds the finding via
        # node_modules + no app manifest), so nothing needs deleting here --
        # this is exactly the managed-Expo, fresh-checkout shape.
        res = scan.Scan(dest, platform="ios", offline=True).run()

    ids = {f["id"] for f in res["findings"]}
    titles = {(p.get("title"), p.get("clause")) for p in res.get("passes") or []}
    checks = [
        ("PRIVACY-MANIFEST-MISSING must NOT fire when app.json declares "
         "expo.ios.privacyManifests, even with no ios/ on disk",
         "PRIVACY-MANIFEST-MISSING" not in ids),
        ("a pass is recorded naming the config declaration",
         ("App-level privacy manifest declared in config",
          "apple:required-reason-api") in titles),
        ("SDK-NO-MANIFEST-expo-file-system must STILL fire -- an app-level "
         "declaration does not cover a specific SDK that ships no manifest "
         "of its own; this fix must not become a blanket suppression",
         "SDK-NO-MANIFEST-expo-file-system" in ids),
    ]
    for desc, ok in checks:
        if ok:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s" % desc); fails.append(desc)
    return fails


# ---------------------------------------------------------------------------
# Adversarial-review regressions (2026-09-23). These are the false-PASS bugs
# that would have let a Nearvo-class app through: obligations detected ONLY from
# a ~6-package allowlist, and no model of the "IAP attached to the review
# submission" gap. Each fixture must FAIL on the pre-fix code and PASS now.
# ---------------------------------------------------------------------------

# F1 fixture: a custom-fetch-auth + direct-StoreKit-paywall app with NO mapped
# auth/IAP SDK, NO account deletion, NO restore, NO demo account. On the pre-fix
# code this scored 0 findings / 0 gaps ("Nothing blocking found"). It must now
# raise the 5.1.1(v) and 3.1.1/3.1.2 obligations as gaps -- NEVER 0/0.
F1_AUTH_LIB = """\
const API = 'https://api.example.com';
export async function register(email, password) {
  return fetch(`${API}/register`, { method: 'POST',
    body: JSON.stringify({ email, password }) });
}
export async function login(email, password) {
  return fetch(`${API}/login`, { method: 'POST',
    body: JSON.stringify({ email, password }) });
}
"""
F1_INDEX = """\
import { login } from '../lib/auth';
export default function Index() {
  async function onLogin() { await login('a@b.com', 'pw'); }
  return null;
}
"""
F1_PAYWALL = """\
import StoreKit from 'expo-storekit-shim';
// Real hard paywall: direct StoreKit, no mapped IAP SDK, no restore control.
export default function Paywall() {
  async function buy(product /* SKProduct */) {
    await SKPaymentQueue.default().addPayment(product);
  }
  return null; // renders "Subscribe Now" / "Unlock Premium"
}
"""
F1_METADATA = """\
# ShipCheck metadata
## App name
Custom Auth App
## Description
An app that signs people in against a custom backend and sells a subscription.
## Privacy policy URL
https://example.com/privacy
## Support URL
https://example.com/support
## Accounts
## Subscriptions
## Demo account
"""


def _write(tmp, rel, content):
    path = os.path.join(tmp, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def run_f1_source_signal_checks():
    fails = []
    print("\nF1 (adversarial review): auth/purchase obligations detected from "
          "SOURCE, not just a package allowlist -- a custom-fetch-auth + "
          "StoreKit-paywall app must NEVER score 0 findings / 0 gaps")
    with tempfile.TemporaryDirectory() as tmp:
        _write(tmp, "package.json", json.dumps({
            "name": "custom-auth-app",
            "dependencies": {"expo": "~56.0.0", "react": "18.3.1",
                             "react-native": "0.76.0", "expo-router": "~4.0.0"}}))
        _write(tmp, "app.json", json.dumps({"expo": {
            "name": "Custom Auth App", "slug": "custom-auth",
            "version": "1.0.0",
            "ios": {"bundleIdentifier": "com.example.customauth"}}}))
        _write(tmp, "lib/auth.ts", F1_AUTH_LIB)
        _write(tmp, "app/index.tsx", F1_INDEX)
        _write(tmp, "app/paywall.tsx", F1_PAYWALL)
        _write(tmp, "shipcheck.metadata.md", F1_METADATA)
        res = scan.Scan(tmp, platform="ios", offline=True).run()
    findings, gaps = res["findings"], res["gaps"]
    fid = {f["id"] for f in findings}
    signals = " ".join(g["what"] + " " + g["why"] for g in gaps) + " " + \
              " ".join(f["id"] + " " + (f["clause"] or "") for f in findings)

    checks = [
        ("must NOT be silent (0 findings AND 0 gaps is the exact false PASS)",
         bool(findings) or bool(gaps)),
        ("account-deletion 5.1.1(v) obligation is surfaced (finding or gap)",
         "5.1.1(v)" in signals or "5.1.1v" in signals or
         any(f.startswith("ACCOUNT-DELETE") for f in fid)),
        ("purchase 3.1.1/3.1.2 obligation is surfaced (finding or gap)",
         "3.1.1" in signals or "3.1.2" in signals or
         "IAP-ATTACH-SUBMISSION" in fid),
    ]
    for desc, ok in checks:
        if ok:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s" % desc); fails.append("F1: " + desc)
    return fails


def run_f2_submission_structure_checks():
    fails = []
    print("\nF2 (adversarial review): the 'IAP attached to THIS version's "
          "submission' gap that rejected Nearvo 4/5/6 is modeled as a blocking "
          "checklist item whenever a paywall is plausibly present")
    cases = [
        ("mapped IAP SDK + wired purchase call -> IAP-ATTACH-SUBMISSION",
         "react-native-purchases", LIVE_IAP_WRAPPER, {},
         ["react-native-purchases"]),
        ("metadata 'Subscriptions: yes' with no SDK -> IAP-ATTACH-SUBMISSION",
         None, None, {"subscriptions": "yes\nPro monthly $9.99"}, []),
    ]
    for desc, subdir_pkg, src, md, deps in cases:
        with tempfile.TemporaryDirectory() as tmp:
            if src is not None:
                _write(tmp, "src/lib/purchases.ts", src)
            s = scan.Scan(tmp)
            if deps:
                s.check_iap(deps, None)
            s.check_submission_structure(deps, md)
            ids = {f["id"] for f in s.findings}
        if "IAP-ATTACH-SUBMISSION" in ids:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s (IAP-ATTACH-SUBMISSION not raised)" % desc)
            fails.append("F2: " + desc)
    return fails


def run_f3_metadata_reconcile_checks():
    fails = []
    print("\nF3 (adversarial review): a metadata self-report is cross-checked "
          "against code -- 'Accounts: no' + a real sign-in call must reconcile, "
          "not sail through")
    with tempfile.TemporaryDirectory() as tmp:
        _write(tmp, "lib/auth.ts", F1_AUTH_LIB)  # fetch('.../login') sign-in
        s = scan.Scan(tmp)
        s.check_accounts_reconcile({"accounts": "no"})
        ids = {f["id"] for f in s.findings}
    if "META-ACCOUNTS-RECONCILE" in ids:
        print("  ok     code shows sign-in but metadata says Accounts: no -> "
              "reconcile finding")
    else:
        print("  FAIL   META-ACCOUNTS-RECONCILE not raised for Accounts:no + "
              "sign-in call"); fails.append("F3: reconcile finding")

    # accounts=yes but no delete-account code path must be flagged regardless
    # of SDK (no mapped auth SDK here at all).
    with tempfile.TemporaryDirectory() as tmp:
        _write(tmp, "lib/auth.ts", F1_AUTH_LIB)
        s = scan.Scan(tmp)
        s.check_accounts_reconcile({"accounts": "yes"})
        ids = {f["id"] for f in s.findings}
    if "ACCOUNT-DELETE-METADATA" in ids:
        print("  ok     Accounts: yes + no delete-account code -> 5.1.1(v) "
              "finding regardless of SDK")
    else:
        print("  FAIL   ACCOUNT-DELETE-METADATA not raised for Accounts:yes + "
              "no deletion"); fails.append("F3: accounts=yes deletion")
    return fails


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Permission-request hygiene (2026-10-13): a worker diffed the one rejected
# app in a review window against its sibling that passed 81 seconds later,
# off the same scaffold, and found exactly one hard behavioural difference:
# requesting a sensitive permission unconditionally on mount (TentClock)
# versus from a tap handler with an explanation first (FlipStage). Fixtures
# below are each modeled on the REAL code at the REAL commit -- not a
# paraphrase -- verified directly against ~/iphone-duo/TentClock's actual
# pre-fix commit (f9d11cf~1) and ~/iphone-duo/FlipStage's actual shipped
# DeckSetup.tsx before writing these, so the regression fixture is provably
# the same shape as the real rejection and the real pass.
# ---------------------------------------------------------------------------
TENTCLOCK_PREFIX_USEWEATHER = """\
import * as Location from 'expo-location';
import { useEffect, useState } from 'react';

export function useWeather() {
  const [status, setStatus] = useState('loading');
  const [snapshot, setSnapshot] = useState(null);

  useEffect(() => {
    let cancelled = false;

    const fetchForCurrentPosition = async (lat, lon) => {
      // ... bounded fetch against Open-Meteo, omitted ...
    };

    (async () => {
      const permission = Location.requestForegroundPermissionsAsync();
      let permStatus;
      try {
        ({ status: permStatus } = await permission);
      } catch {
        if (!cancelled) setStatus('error');
        return;
      }
      if (permStatus !== 'granted') {
        if (!cancelled) setStatus('denied');
        return;
      }
      await fetchForCurrentPosition();
    })();

    return () => { cancelled = true; };
  }, []);

  return { status, snapshot };
}
"""

FLIPSTAGE_DECKSETUP_IMPORT = """\
import * as ImagePicker from 'expo-image-picker';
import { Alert, Linking, Pressable } from 'react-native';

export function DeckSetup({ onImport }) {
  const importPhotos = async () => {
    const perm = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!perm.granted) {
      Alert.alert(
        'Photos access needed',
        'FlipStage needs access to your photo library to import slides.',
        [
          { text: 'Not now', style: 'cancel' },
          { text: 'Open Settings', onPress: () => Linking.openSettings() },
        ]
      );
      return;
    }
    const result = await ImagePicker.launchImageLibraryAsync({ allowsMultipleSelection: true });
    onImport(result.assets);
  };

  return <Pressable onPress={importPhotos}><Text>Import</Text></Pressable>;
}
"""

NEARVO_DECLARED_UNUSED_CONFIG = """\
export const config = {
  ios: {
    infoPlist: {
      // ITMS-90683 statically scans every transitive dependency for API
      // usage; expo-image-picker and expo-secure-store reference the
      // Camera/FaceID APIs even though this app's own code never calls
      // them, and Apple's static scan does not know the difference.
      // Removing these strings fails the upload, not the review.
      NSCameraUsageDescription: 'Not used by this app directly.',
      NSFaceIDUsageDescription: 'Not used by this app directly.',
    },
  },
};
"""

MOUNT_EFFECT_WITH_REAL_DEPS = """\
import { useEffect } from 'react';
import * as Location from 'expo-location';

export function useLocationOnRefresh(refreshToken) {
  useEffect(() => {
    Location.requestForegroundPermissionsAsync();
  }, [refreshToken]);
}
"""

NOTIF_PERMISSION_NO_SCHEDULE = """\
import * as Notifications from 'expo-notifications';

export async function askForPermission() {
  await Notifications.requestPermissionsAsync();
}
"""

NOTIF_PERMISSION_WITH_SCHEDULE = """\
import * as Notifications from 'expo-notifications';

export async function askForPermission() {
  await Notifications.requestPermissionsAsync();
}

export async function remind() {
  await Notifications.scheduleNotificationAsync({
    content: { title: 'Reminder' }, trigger: null,
  });
}
"""


def run_permission_hygiene_checks():
    fails = []
    print("\nPermission-request hygiene (2026-10 rejection cause: a sensitive "
          "permission requested unconditionally on mount, or requested and "
          "never followed through)")

    cases = [
        ("real TentClock pre-fix code (commit f9d11cf~1): "
         "requestForegroundPermissionsAsync inside a mount-only useEffect "
         "-> must fire",
         TENTCLOCK_PREFIX_USEWEATHER, "PERM-REQUEST-ON-MOUNT", True),

        ("real FlipStage code: requestMediaLibraryPermissionsAsync inside a "
         "plain async function wired to onPress -- must NOT fire",
         FLIPSTAGE_DECKSETUP_IMPORT, "PERM-REQUEST-ON-MOUNT", False),

        ("Nearvo's documented shape: a usage string declared for a library "
         "that statically references the API, with NO call site at all -- "
         "must NOT fire (nothing to find the timing of)",
         NEARVO_DECLARED_UNUSED_CONFIG, "PERM-REQUEST-ON-MOUNT", False),

        ("a permission request inside a useEffect with a REAL (non-empty) "
         "dependency array -- not the unconditional-on-mount shape -- must "
         "NOT fire",
         MOUNT_EFFECT_WITH_REAL_DEPS, "PERM-REQUEST-ON-MOUNT", False),

        ("notification permission requested, no scheduling call anywhere "
         "(MileTruth's shape per claim-truth-2026-10-13.md) -> must fire",
         NOTIF_PERMISSION_NO_SCHEDULE, "NOTIF-PERMISSION-NEVER-SCHEDULED", True),

        ("notification permission requested AND a real scheduleNotificationAsync "
         "call exists -- must NOT fire",
         NOTIF_PERMISSION_WITH_SCHEDULE, "NOTIF-PERMISSION-NEVER-SCHEDULED", False),
    ]
    for desc, src, fid, must_fire in cases:
        with tempfile.TemporaryDirectory() as tmp:
            _write(tmp, "src/lib/feature.ts", src)
            s = scan.Scan(tmp)
            s.check_permission_request_hygiene()
            ids = {f["id"] for f in s.findings}
        fired = fid in ids
        if fired == must_fire:
            print("  ok     %s" % desc)
        else:
            want = "to fire" if must_fire else "NOT to fire"
            print("  FAIL   %s (expected %s -> %s, got ids=%s)"
                  % (desc, fid, want, sorted(ids)))
            fails.append("permission-hygiene: " + desc)

    # Real-world validation, not a synthetic fixture: run the actual checker
    # against the actual repos at their actual commits, read-only.
    real_cases = [
        ("/Users/ryan/iphone-duo/TentClock", False, "TentClock, current (post-fix)"),
        ("/Users/ryan/iphone-duo/FlipStage", False, "FlipStage, current (the control that passed)"),
    ]
    for path, want_hit, label in real_cases:
        if not os.path.isdir(path):
            print("  skip   %s (repo not present on this machine)" % label)
            continue
        s = scan.Scan(path)
        hit = s._find_permission_request_in_mount_effect()
        got_hit = hit is not None
        if got_hit == want_hit:
            print("  ok     %s: mount-effect permission check %s"
                  % (label, "fired" if got_hit else "silent"))
        else:
            print("  FAIL   %s: expected %s, got %r"
                  % (label, "a hit" if want_hit else "no hit", hit))
            fails.append("permission-hygiene real-world: " + label)
    return fails


# Listing-vs-binary claim checks (2026-10-13): derived from the 2026-10
# rejection batch, where 4 of 9 apps were rejected for a shape no earlier
# check here looked for -- the LISTING or the App Review notes promise a
# behaviour the reviewed binary's source does not perform. Each fixture
# below is modeled on one real labelled example (Nearvo's dead push-token
# registration, MileTruth's never-scheduled notification permission,
# Steadychart's backup with no restore path, IOLTAlign's review notes
# pointing at a seeded account that was never seeded) and each has a
# matching "must NOT fire" case so a real, wired-up feature never gets
# flagged as a phantom one.
# ---------------------------------------------------------------------------
def run_listing_claim_checks():
    fails = []
    print("\nListing-vs-binary claims (2026-10 rejection batch: listing/review "
          "notes promise a feature the binary does not have -- table-driven "
          "from data/rn_sdk_map.json's listing_claims/review_notes_claims)")

    # check_listing_claims(md) cases: (desc, metadata dict, source or None,
    # finding id, must it fire).
    listing_cases = [
        ("notifications claim, no library at all, no call site "
         "(Nearvo: 'love notes that land on their phone')",
         {"description": "Love notes that land right on their phone, any time."},
         None,
         "CLAIM-UNBACKED-notifications", True),

        ("notifications claim with the library present but never scheduled "
         "(MileTruth: permission requested, nothing ever scheduled)",
         {"description": "We'll remind you the moment a trip is detected."},
         "import * as Notifications from 'expo-notifications';\n"
         "export async function askForPermission() {\n"
         "  await Notifications.requestPermissionsAsync();\n"
         "}\n",
         "CLAIM-UNBACKED-notifications", True),

        ("notifications claim backed by a real schedule call -- must NOT fire",
         {"description": "We'll remind you the moment a trip is detected."},
         "import * as Notifications from 'expo-notifications';\n"
         "export async function remind() {\n"
         "  await Notifications.requestPermissionsAsync();\n"
         "  await Notifications.scheduleNotificationAsync({\n"
         "    content: { title: 'Trip detected' }, trigger: null });\n"
         "}\n",
         "CLAIM-UNBACKED-notifications", False),

        ("notifications claim hard-wrapped across a line break in real prose "
         "-- a real shipcheck.metadata.md file wraps at ~90 cols, and Nearvo's "
         "own actual listing splits exactly on 'land on / their phone.'",
         {"description": "Shared photo memories. Love notes that land on\n"
                         "their phone. A daily mood check-in."},
         None,
         "CLAIM-UNBACKED-notifications", True),

        ("import/restore claim with no picker/reader anywhere "
         "(Steadychart: 'a full JSON backup' with no way back in)",
         {"description": "Restore from a backup any time you switch phones."},
         "export function exportJson() { return JSON.stringify({}); }\n"
         "// there is no restore from a backup -- not implemented\n",
         "CLAIM-UNBACKED-import-restore", True),

        ("import/restore claim with a real DocumentPicker call -- must NOT fire",
         {"description": "Restore from a backup any time you switch phones."},
         "import * as DocumentPicker from 'expo-document-picker';\n"
         "export async function restoreBackup() {\n"
         "  const f = await DocumentPicker.getDocumentAsync();\n"
         "  return JSON.parse(f.assets[0].text);\n"
         "}\n",
         "CLAIM-UNBACKED-import-restore", False),

        ("biometric-lock claim with no LocalAuthentication call anywhere "
         "(Nearvo: NSFaceIDUsageDescription declared, never called)",
         {"description": "Lock the app behind Face ID so only you can open it."},
         "export const config = { ios: { infoPlist: {\n"
         "  NSFaceIDUsageDescription: 'Unlock the app' } } };\n",
         "CLAIM-UNBACKED-biometric-lock", True),

        ("biometric-lock claim with a real LocalAuthentication call -- "
         "must NOT fire",
         {"description": "Lock the app behind Face ID so only you can open it."},
         "import * as LocalAuthentication from 'expo-local-authentication';\n"
         "export async function unlock() {\n"
         "  return LocalAuthentication.authenticateAsync();\n"
         "}\n",
         "CLAIM-UNBACKED-biometric-lock", False),
    ]
    for desc, md, src, fid, must_fire in listing_cases:
        with tempfile.TemporaryDirectory() as tmp:
            if src is not None:
                _write(tmp, "src/lib/feature.ts", src)
            s = scan.Scan(tmp)
            s.check_listing_claims(md)
            ids = {f["id"] for f in s.findings}
        fired = fid in ids
        if fired == must_fire:
            print("  ok     %s" % desc)
        else:
            want = "to fire" if must_fire else "NOT to fire"
            print("  FAIL   %s (expected %s -> %s, got ids=%s)"
                  % (desc, fid, want, sorted(ids)))
            fails.append("listing-claims: " + desc)

    # check_review_notes_claims(md) cases.
    notes_cases = [
        ("review notes point at a seeded account that is never seeded "
         "(IOLTAlign: 'open the seeded/sample trust account')",
         {"review notes": "To review: launch the app, open the seeded/sample "
                          "trust account (or create one via Accounts > New)."},
         "export function createAccount(name) { return { name }; }\n",
         "CLAIM-PHANTOM-seeded-data", True),

        ("review notes mention sample data, and the app really seeds it "
         "-- must NOT fire",
         {"review notes": "The app ships with sample data pre-loaded on first "
                          "launch; no login required."},
         "export function init() {\n"
         "  if (count === 0) { seedDatabase(); }\n"
         "}\n",
         "CLAIM-PHANTOM-seeded-data", False),
    ]
    for desc, md, src, fid, must_fire in notes_cases:
        with tempfile.TemporaryDirectory() as tmp:
            _write(tmp, "src/lib/feature.ts", src)
            s = scan.Scan(tmp)
            s.check_review_notes_claims(md)
            ids = {f["id"] for f in s.findings}
        fired = fid in ids
        if fired == must_fire:
            print("  ok     %s" % desc)
        else:
            want = "to fire" if must_fire else "NOT to fire"
            print("  FAIL   %s (expected %s -> %s, got ids=%s)"
                  % (desc, fid, want, sorted(ids)))
            fails.append("review-notes-claims: " + desc)

    # Monorepo shape (2026-10-13, found on the real Rigsheet repo): the Expo
    # project lives at apps/mobile/, two directory levels under the repo
    # root, and the demo-account seeder is a SIBLING of apps/ (supabase/
    # seed.sql), not a child of mobile/ -- grep_source's default roots can
    # never see it, and neither could one level of extra_roots (one level up
    # from apps/mobile is just apps/, which has no supabase/ of its own).
    monorepo_md = {"review notes": "Demo account below has sample customers, "
                                    "services, and jobs already seeded."}
    monorepo_cases = [
        ("Rigsheet's real shape: demo data seeded via a sibling supabase/ "
         "directory two levels up from the Expo project root -- must NOT fire",
         "insert into public.customer (id, business_id, first_name) values "
         "(1, 1, 'Marcus');\n",
         False),
        ("same monorepo layout, but genuinely nothing seeds anywhere "
         "(including the sibling supabase/ directory) -- must still fire",
         "-- no seed data in this project\n",
         True),
    ]
    for desc, seed_sql, must_fire in monorepo_cases:
        with tempfile.TemporaryDirectory() as tmp:
            _write(tmp, "apps/mobile/app.json", json.dumps({"expo": {"name": "x"}}))
            _write(tmp, "supabase/seed.sql", seed_sql)
            s = scan.Scan(os.path.join(tmp, "apps", "mobile"))
            s.check_review_notes_claims(monorepo_md)
            ids = {f["id"] for f in s.findings}
        fid = "CLAIM-PHANTOM-seeded-data"
        fired = fid in ids
        if fired == must_fire:
            print("  ok     %s" % desc)
        else:
            want = "to fire" if must_fire else "NOT to fire"
            print("  FAIL   %s (expected %s -> %s, got ids=%s)"
                  % (desc, fid, want, sorted(ids)))
            fails.append("review-notes-claims: " + desc)

    # check_listing_url_content(md): fetch_text is monkeypatched so this
    # stays offline and deterministic -- it is exercising the regex-match
    # path, not real network reachability (that's check_urls' job).
    print("  (listing URL placeholder content: exercised via monkeypatch, below)")
    real_fetch = scan.fetch_text
    try:
        scan.fetch_text = lambda url, **kw: (
            "DenialDesk (a working name; the final app name is not yet "
            "chosen) is an on-device assistant." if "denialdesk" in url else "")
        with tempfile.TemporaryDirectory() as tmp:
            s = scan.Scan(tmp, offline=False)
            s.check_listing_url_content(
                {"privacy policy url": "https://example.com/denialdesk/privacy/"})
            ids = {f["id"] for f in s.findings}
        if "LISTING-URL-PLACEHOLDER-privacy-policy-url" in ids:
            print("  ok     linked privacy page still says the app name is "
                  "not final (DenialDesk's actual, still-live defect)")
        else:
            print("  FAIL   LISTING-URL-PLACEHOLDER-privacy-policy-url not "
                  "raised for a page with placeholder name text")
            fails.append("listing-url-content: placeholder name text")

        with tempfile.TemporaryDirectory() as tmp:
            s = scan.Scan(tmp, offline=False)
            s.check_listing_url_content(
                {"privacy policy url": "https://example.com/clean/privacy/"})
            ids = {f["id"] for f in s.findings}
        if not any(i.startswith("LISTING-URL-PLACEHOLDER") for i in ids):
            print("  ok     a clean linked page raises nothing")
        else:
            print("  FAIL   clean linked page raised %s" % sorted(ids))
            fails.append("listing-url-content: clean page false positive")
    finally:
        scan.fetch_text = real_fetch
    return fails


def run_concrete_promise_checks():
    """check_concrete_promises: the seven real 2026-10 listing/notes-vs-binary
    rejections as small synthetic projects, plus negatives that must stay
    silent."""
    fails = []
    print("\nConcrete promises vs binary (7 real 2026-10 rejection shapes + negatives)")
    LIST = "src/screens/ListScreen.tsx"
    cases = [
        # (desc, files, metadata, finding-id prefix, must fire)
        ("IOLTAlign: review notes point at a sample account the app never creates",
         {"src/db.ts": "export function createAccount(n){return {n};}\n"},
         {"review notes": "Open the sample account on the home screen to review."},
         "CLAIM-PHANTOM-seeded-data", True),
        ("TentClock: notes promise a populated alarm list; new user sees the empty state",
         {"src/screens/Alarms.tsx":
          "export const A=()=> <FlatList data={[]} ListEmptyComponent={<Text>No alarms yet</Text>}/>;\n"},
         {"review notes": "The Alarms tab already contains three alarms for you to review."},
         "PROMISE-POPULATED-STATE", True),
        ("Foldbook: listing promises saved reading progress; only the screenshot tool writes it",
         {"src/dev/screenshotSeed.ts":
          "import AsyncStorage from '@react-native-async-storage/async-storage';\n"
          "export const seed=()=>AsyncStorage.setItem('progress','42');\n",
          "src/screens/Reader.tsx": "const p = progress; export const R=()=>null;\n"},
         {"description": "Pick up where you left off, with your reading progress saved."},
         "PROMISE-PROGRESS-NO-WRITER", True),
        ("DenialDesk: review notes name two buttons that do not exist",
         {LIST: "export const L=()=> <Button title='Add letter'/>;\n"},
         {"review notes": 'Tap "Generate Appeal" then press the "Send to Insurer" button.'},
         "PROMISE-UI-MISSING-generate-appeal", True),
        ("DenialDesk (second button is also flagged)",
         {LIST: "export const L=()=> <Button title='Add letter'/>;\n"},
         {"review notes": 'Tap "Generate Appeal" then press the "Send to Insurer" button.'},
         "PROMISE-UI-MISSING-send-to-insurer", True),
        ("Nearvo: $129.99 lifetime advertised; the allowlist refuses to sell it",
         {"src/iap.ts": "export const ALLOWED_PRODUCT_IDS = ['nearvo.monthly','nearvo.annual'];\n"
                        "Purchases.purchaseProduct(id);\n"},
         {"description": "Unlock everything with lifetime access for $129.99."},
         "PROMISE-LIFETIME-UNBACKED", True),
        ("Rigsheet: 14-day free trial promised, zero introductory offers configured",
         {"src/paywall.ts": "export const trialDays = 14;\nPurchases.getOfferings();\n"},
         {"description": "Start your 14-day free trial today.",
          "subscriptions": "yes\nMonthly $19.99. Free trial: none (0 introductory offers configured)."},
         "PROMISE-TRIAL-UNBACKED", True),
        ("FlirtGym: copy states a 7-day trial and a free tier; no trial anywhere, hard paywall",
         {"src/paywall.ts": "Purchases.getOfferings();\nexport const P=()=>null;\n"},
         {"description": "Try it with a 7-day free trial, or stay on the free plan.",
          "subscriptions": "yes\nHard paywall, subscription required. No free tier."},
         "PROMISE-TRIAL-UNBACKED", True),
        ("FlirtGym (free tier contradiction)",
         {"src/paywall.ts": "Purchases.getOfferings();\n"},
         {"description": "Stay on the free plan as long as you like.",
          "subscriptions": "yes\nHard paywall, subscription required. No free tier."},
         "PROMISE-FREE-TIER-UNBACKED", True),
        # negatives
        ("NEG: 14-day trial backed by code stating 14 days and metadata saying so",
         {"src/paywall.ts": "export const trialDays = 14;\nPurchases.getOfferings();\n"},
         {"description": "Start your 14-day free trial today.",
          "subscriptions": "yes\nMonthly $19.99 with a 14-day free trial."},
         "PROMISE-TRIAL-UNBACKED", False),
        ("NEG: lifetime advertised and the lifetime product is in the allowlist",
         {"src/iap.ts": "export const ALLOWED_PRODUCT_IDS = ['x.monthly','x.lifetime'];\n"},
         {"description": "Unlock everything with lifetime access for $129.99."},
         "PROMISE-LIFETIME-UNBACKED", False),
        ("NEG: notes name buttons that exist as labels in source",
         {LIST: "export const L=()=> <><Button title='Generate Appeal'/><Text>Send to Insurer</Text></>;\n"},
         {"review notes": 'Tap "Generate Appeal" then press the "Send to Insurer" button.'},
         "PROMISE-UI-MISSING", False),
        ("NEG: populated-list note, and the app seeds on first launch",
         {"src/screens/Alarms.tsx": "export const A=()=> <FlatList ListEmptyComponent={<Text>No alarms yet</Text>}/>;\n",
          "src/seed.ts": "export function seedIfEmpty(){}\n"},
         {"review notes": "The Alarms tab already contains three alarms for you to review."},
         "PROMISE-POPULATED-STATE", False),
        ("NEG: saved-progress promise with a real shipping write",
         {"src/screens/Reader.tsx":
          "import AsyncStorage from '@react-native-async-storage/async-storage';\n"
          "export const save=(p)=>AsyncStorage.setItem('progress',p);\n"},
         {"description": "Pick up where you left off, with your reading progress saved."},
         "PROMISE-PROGRESS-NO-WRITER", False),
        ("NEG: mixed products (Annual has a 14-day trial, Monthly says 'no trial') -- found on HormoneLog",
         {"src/paywall.ts": "export const trialDays = 14;\nPurchases.getOfferings();\n"},
         {"review notes": "Subscribe to Annual to start the 14-day free trial.",
          "subscriptions": "yes\n- Annual: $49.99/yr, 14-day free trial\n- Monthly: $7.99/mo, no trial"},
         "PROMISE-TRIAL-UNBACKED", False),
        ("POS: 'no in-app purchases' listing but a REAL reachable paywall (expo-router screen imports a component that calls purchasePackage)",
         {"package.json": '{"dependencies":{"expo-router":"*","react-native-purchases":"*"}}',
          "src/app/paywall.tsx": "import {Buy} from '../components/Buy';\nexport default function P(){return <Buy/>;}\n",
          "src/components/Buy.tsx": "import Purchases from 'react-native-purchases';\nexport const Buy=()=>{Purchases.purchasePackage(p);return null;};\n"},
         {"description": "Log your drives -- no in-app purchases, nothing to buy."},
         "PROMISE-FREE-BUT-SELLS", True),
        ("POS: same, purchase call directly inside a routed file under app/",
         {"package.json": '{"dependencies":{"expo-router":"*","react-native-purchases":"*"}}',
          "app/upgrade.tsx": "import Purchases from 'react-native-purchases';\nexport default ()=>{Purchases.getOfferings();return null;};\n"},
         {"description": "Completely free."},
         "PROMISE-FREE-BUT-SELLS", True),
        ("POS (low confidence): not expo-router, so reachability is uncertain but SDK + purchase call exist",
         {"package.json": '{"dependencies":{"react-native-purchases":"*"}}',
          "src/Paywall.tsx": "import Purchases from 'react-native-purchases';\nPurchases.purchasePackage(p);\n"},
         {"description": "No in-app purchases."},
         "PROMISE-FREE-BUT-SELLS", True),
        ("NEG (DenialDesk): 'No subscription'; dormant pricing.ts + unrouted PaywallScreen, no IAP SDK",
         {"package.json": '{"dependencies":{"expo-router":"*"}}',
          "src/app/_layout.tsx": "export default function L(){return null;}\n",
          "src/monetization/pricing.ts": "export const planned = {monthly: 9.99, label: 'Upgrade to Pro'};\n",
          "src/screens/PaywallScreen.tsx": "import {planned} from '../monetization/pricing';\nexport const PaywallScreen=()=> <Text>Subscribe now - restore purchases</Text>;\n"},
         {"description": "Free to use. No subscription."},
         "PROMISE-FREE-BUT-SELLS", False),
        ("NEG (Stillmoor): the word paywall appears only in comments of the crisis-support screen",
         {"package.json": '{"dependencies":{"expo-router":"*","react-native-purchases":"*"}}',
          "src/app/support.tsx": "// Crisis support is never behind a paywall.\n/* paywall: never. Upgrade to Pro does not apply here */\nexport default function S(){return null;}\n"},
         {"description": "No subscription, no paywall. Crisis support is always free."},
         "PROMISE-FREE-BUT-SELLS", False),
        ("NEG (MileTruth): react-native-purchases wrapper that no routed screen reaches",
         {"package.json": '{"dependencies":{"expo-router":"*","react-native-purchases":"*"}}',
          "src/app/index.tsx": "export default function H(){return null;}\n",
          "src/lib/purchases.ts": "import Purchases from 'react-native-purchases';\nexport function configurePurchases(){const k=process.env.KEY;if(!k)return;Purchases.configure({apiKey:k});}\nexport const buy=(p)=>Purchases.purchasePackage(p);\n"},
         {"description": "Log your drives -- no in-app purchases, nothing to buy."},
         "PROMISE-FREE-BUT-SELLS", False),
        ("NEG (MileTruth): routed screen only configures the SDK (nothing is offered)",
         {"package.json": '{"dependencies":{"expo-router":"*","react-native-purchases":"*"}}',
          "src/app/_layout.tsx": "import {configurePurchases} from '../lib/purchases';\nconfigurePurchases();\nexport default function L(){return null;}\n",
          "src/lib/purchases.ts": "import Purchases from 'react-native-purchases';\nexport function configurePurchases(){Purchases.configure({apiKey:'k'});}\n"},
         {"description": "No in-app purchases."},
         "PROMISE-FREE-BUT-SELLS", False),
        ("NEG: 'no free trial' wording and an honestly free app with no purchase code",
         {"src/app.ts": "export const x = 1;\n"},
         {"description": "Completely free. There is no free trial because nothing is paid."},
         "PROMISE-", False),
    ]
    for desc, files, md, fid, must_fire in cases:
        with tempfile.TemporaryDirectory() as tmp:
            for rel, content in files.items():
                _write(tmp, rel, content)
            s = scan.Scan(tmp)
            s.check_review_notes_claims(md)
            s.check_concrete_promises(md)
            ids = {f["id"] for f in s.findings}
        fired = any(i == fid or (fid.endswith(("UI-MISSING", "PROMISE-")) and i.startswith(fid))
                    for i in ids)
        if fired == must_fire:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s (want %s %s, got ids=%s)"
                  % (desc, fid, "to fire" if must_fire else "NOT to fire", sorted(ids)))
            fails.append("concrete-promises: " + desc)
    # confidence: reachable -> medium; uncertain routing -> low
    for desc, files, want in (
            ("confidence is medium when reachability is confirmed",
             {"package.json": '{"dependencies":{"expo-router":"*","react-native-purchases":"*"}}', "app/u.tsx": "Purchases.getOfferings();\n"}, "medium"),
            ("confidence is LOW when reachability is uncertain",
             {"package.json": '{"dependencies":{"react-native-purchases":"*"}}',
              "src/P.tsx": "Purchases.getOfferings();\n"}, "low")):
        with tempfile.TemporaryDirectory() as tmp:
            for rel, content in files.items():
                _write(tmp, rel, content)
            s = scan.Scan(tmp)
            s.check_concrete_promises({"description": "No in-app purchases."})
            got = [f["confidence"] for f in s.findings if f["id"] == "PROMISE-FREE-BUT-SELLS"]
        if got == [want]:
            print("  ok     " + desc)
        else:
            print("  FAIL   %s (got %s)" % (desc, got)); fails.append("concrete-promises: " + desc)
    return fails


def run_negated_claim_checks():
    """CLAIM-UNBACKED-health-integration must not fire on a listing line that
    says the app does NOT have the capability (PlateRamp, Slowbend)."""
    fails = []
    print("\nNegated capability claims (PlateRamp, Slowbend false positives)")
    src = {"src/app.ts": "export const x = 1;\n"}
    cases = [
        ("NEG (PlateRamp): 'No location, camera, microphone, photo or Apple Health access.'",
         "Private by design. No location, camera, microphone, photo or Apple Health access.", False),
        ("NEG (Slowbend): 'no HealthKit entitlement' / 'does not read Apple Health'",
         "Slowbend has no HealthKit entitlement and does not read Apple Health data.", False),
        ("NEG: 'without Apple Health' / 'never syncs with Health'",
         "Works without Apple Health. It never syncs to Health.", False),
        ("POS: real unbacked claim still fires ('Syncs with Apple Health.')",
         "Track your meals. Syncs with Apple Health.", True),
        ("POS: negation in a DIFFERENT sentence does not suppress ('No ads. Syncs with Apple Health.')",
         "No ads. Syncs with Apple Health.", True),
        ("POS: one negated mention does not hide a separate positive one",
         "No Apple Health access on the free tier. Pro syncs with Apple Health.", True),
    ]
    for desc, text, must_fire in cases:
        with tempfile.TemporaryDirectory() as tmp:
            for rel, content in src.items():
                _write(tmp, rel, content)
            s = scan.Scan(tmp)
            s.check_listing_claims({"description": text})
            fired = any(f["id"] == "CLAIM-UNBACKED-health-integration" for f in s.findings)
        if fired == must_fire:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s (fired=%s)" % (desc, fired)); fails.append("negated-claims: " + desc)
    return fails


def run_comment_strip_checks():
    fails = []
    print("\nJS comment stripping")
    S = scan.Scan.strip_js_comments
    cases = [
        ("line comment removed", "a // paywall\nb", "paywall", False),
        ("block comment removed", "a /* paywall\n more */ b", "paywall", False),
        ("string containing // kept", "x = 'http://a//paywall'", "paywall", True),
        ("code after a comment kept", "// c\nPurchases.purchasePackage(p)", "purchasePackage", True),
    ]
    for desc, src, needle, kept in cases:
        if (needle in S(src)) == kept:
            print("  ok     %s" % desc)
        else:
            print("  FAIL   %s" % desc); fails.append("comment-strip: " + desc)
    return fails


def run_doc_generator_checks():
    """gen_guideline_pages.py / gen_comparison_pages.py read specific headings and
    filenames out of the cached corpus by hardcoded structure -- a corpus refresh that
    restructures a page can silently crash them, and nothing else in this suite
    exercises either script (found 2026-10-13 on a corpus refresh, see
    rules/lessons.md in the Brain repo). Run them for real and require a clean exit.

    Also checks, when the generated paths were clean going in, that regenerating
    didn't change them -- i.e. the committed docs match what the corpus + script
    produce right now. That half is a real check for a developer running this
    locally after editing the corpus or the generators by hand. It's not a check
    refresh-corpus.yml's own run of this script can ever hit, though: that workflow
    regenerates docs/ itself first specifically so a real corpus change lands as
    "already dirty, skip" here rather than failing the job outright -- for that
    pipeline, the crash check above is what's actually protecting it, and the PR
    peter-evans/create-pull-request opens is what carries the (legitimate) diff."""
    fails = []
    print("\nDoc generators (gen_guideline_pages.py, gen_comparison_pages.py)")
    # Only the paths these two scripts actually write -- docs/index.html (the hand-
    # maintained landing page) and docs/privacy-policy.md live under docs/ too but
    # aren't theirs, so scoping to the whole docs/ dir would let an unrelated WIP
    # edit to either one mask real staleness in docs/guidelines/ or the root sitemap.
    generated_paths = [os.path.join(ROOT, "docs", "guidelines"),
                        os.path.join(ROOT, "docs", "sitemap.xml")]

    def _generated_dirty():
        # --porcelain (not `git diff --quiet`) so a brand-new untracked page a
        # generator just wrote -- `git diff` is blind to those -- still counts.
        return bool(subprocess.run(
            ["git", "status", "--porcelain", "--"] + generated_paths,
            cwd=ROOT, capture_output=True, text=True).stdout.strip())

    tree_was_dirty = _generated_dirty()

    for script in ("gen_guideline_pages.py", "gen_comparison_pages.py"):
        proc = subprocess.run([sys.executable, os.path.join(HERE, script)],
                               cwd=ROOT, capture_output=True, text=True)
        if proc.returncode != 0:
            print("  FAIL   %s crashed (exit %d)" % (script, proc.returncode))
            for line in proc.stderr.strip().splitlines()[-10:]:
                print("    " + line)
            fails.append("doc-generator: %s crashed" % script)
        else:
            print("  ok     %s ran clean" % script)

    if not fails:
        if tree_was_dirty:
            # Can't tell whether any remaining diff is this run's doing or
            # pre-existing uncommitted work -- don't make a call either way.
            print("  skip   stale-docs check (docs/guidelines/ or docs/sitemap.xml "
                  "already had uncommitted changes before this ran)")
        elif _generated_dirty():
            print("  FAIL   docs/guidelines/ or docs/sitemap.xml changed after "
                  "regenerating -- the committed pages are stale relative to the "
                  "current corpus + generator; run the generators and commit the result")
            fails.append("doc-generator: docs/ stale")
        else:
            print("  ok     generated docs/ match what's committed")
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
    fails += run_redirect_following_checks()
    fails += run_grep_truncation_checks()
    fails += run_f1_source_signal_checks()
    fails += run_f2_submission_structure_checks()
    fails += run_f3_metadata_reconcile_checks()
    fails += run_bare_rn_checks()
    fails += run_clean_checks()
    fails += run_privacy_manifest_config_checks()
    fails += run_permission_hygiene_checks()
    fails += run_listing_claim_checks()
    fails += run_concrete_promise_checks()
    fails += run_negated_claim_checks()
    fails += run_comment_strip_checks()
    fails += run_doc_generator_checks()

    print("\n%d findings, %d passes, %d gaps"
          % (len(data["findings"]), len(data.get("passes") or []), len(data["gaps"])))
    if fails:
        print("\nFAILED: %d" % len(fails))
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
