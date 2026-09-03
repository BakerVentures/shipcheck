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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import report                                        # noqa: E402

FIXTURE = os.path.join(ROOT, "examples", "bad-expo-app")

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

    print("Seeded violations")
    for desc, fid, clause in MUST_CATCH:
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

    print("\n%d findings, %d passes, %d gaps"
          % (len(data["findings"]), len(data.get("passes") or []), len(data["gaps"])))
    if fails:
        print("\nFAILED: %d" % len(fails))
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
