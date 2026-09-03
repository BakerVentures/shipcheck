#!/usr/bin/env python3
"""ShipCheck deterministic scanner.

Reads an RN/Expo project and shipcheck.metadata.md and emits JSON:
  { "facts": {...}, "findings": [...], "gaps": [...] }

Deterministic only. Anything requiring judgment (is this description
misleading? does this paywall disclose terms?) is left to the skill, which
reasons over corpus/. Standard library only.

Usage:
  python3 scan.py --project . [--platform ios|android|both] [--offline] [--json]
"""
import argparse
import json
import os
import plistlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

SEV = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


def load_map():
    with open(os.path.join(DATA, "rn_sdk_map.json"), encoding="utf-8") as f:
        return json.load(f)


class Scan:
    def __init__(self, project, platform="both", offline=False):
        self.root = os.path.abspath(project)
        self.platform = platform
        self.offline = offline
        self.map = load_map()
        self.findings = []
        self.gaps = []
        self.facts = {"project_root": self.root}

    # ------------------------------------------------------------ utilities
    def p(self, *parts):
        return os.path.join(self.root, *parts)

    def exists(self, *parts):
        return os.path.exists(self.p(*parts))

    def read(self, *parts):
        try:
            with open(self.p(*parts), encoding="utf-8", errors="replace") as f:
                return f.read()
        except OSError:
            return None

    def add(self, fid, severity, title, clause=None, evidence=None, fix=None,
            confidence="high", platform="ios", corpus=None, itms=None):
        self.findings.append(dict(
            id=fid, severity=severity, title=title, clause=clause,
            evidence=evidence, fix=fix, confidence=confidence,
            platform=platform, corpus=corpus, itms=itms,
            source="deterministic"))

    def gap(self, what, why):
        self.gaps.append(dict(what=what, why=why))

    # ------------------------------------------------------------- discovery
    def load_app_config(self):
        """Prefer `npx expo config` because app.config.js can be dynamic."""
        cfg, how = None, None
        if self.exists("app.config.js") or self.exists("app.config.ts"):
            try:
                out = subprocess.run(
                    ["npx", "--no-install", "expo", "config", "--type", "public", "--json"],
                    cwd=self.root, capture_output=True, text=True, timeout=90)
                if out.returncode == 0 and out.stdout.strip().startswith("{"):
                    cfg, how = json.loads(out.stdout), "expo config"
            except Exception:                       # noqa: BLE001
                pass
        if cfg is None and self.exists("app.json"):
            try:
                cfg = json.loads(self.read("app.json"))
                cfg = cfg.get("expo", cfg)
                how = "app.json"
            except json.JSONDecodeError:
                self.add("CFG-PARSE", "high", "app.json is not valid JSON",
                         evidence="app.json failed to parse",
                         fix="Fix the JSON syntax; EAS Build will fail on this too.")
        if cfg is None and (self.exists("app.config.js") or self.exists("app.config.ts")):
            self.gap("app config",
                     "app.config.js/ts is dynamic and `npx expo config` was unavailable, "
                     "so Info.plist keys declared there could not be read. "
                     "Run `npx expo config --type public --json` and re-scan for full coverage.")
            cfg = {}
        self.facts["app_config_source"] = how
        return cfg or {}

    def load_package_json(self):
        raw = self.read("package.json")
        if not raw:
            self.add("PKG-MISSING", "high", "No package.json found",
                     evidence="package.json missing at project root",
                     fix="Run ShipCheck from your React Native/Expo project root.")
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    # -------------------------------------------------------------- iOS side
    def collect_info_plist(self, cfg):
        """Merge app config infoPlist with a prebuilt ios/ Info.plist."""
        merged, sources = {}, []
        ip = (cfg.get("ios") or {}).get("infoPlist") or {}
        if ip:
            merged.update(ip)
            sources.append(self.facts.get("app_config_source") or "app config")
        ios_dir = self.p("ios")
        if os.path.isdir(ios_dir):
            for dirpath, _dirs, files in os.walk(ios_dir):
                if "Pods" in dirpath or "build" in dirpath.split(os.sep):
                    continue
                for fn in files:
                    if fn == "Info.plist":
                        try:
                            with open(os.path.join(dirpath, fn), "rb") as f:
                                d = plistlib.load(f)
                            if "CFBundleIdentifier" in d or "NSCameraUsageDescription" in d \
                               or "CFBundleName" in d:
                                merged.update({k: v for k, v in d.items() if v not in (None, "")})
                                sources.append(os.path.relpath(
                                    os.path.join(dirpath, fn), self.root))
                        except Exception:            # noqa: BLE001
                            pass
        self.facts["info_plist_sources"] = sources
        return merged

    def find_privacy_manifests(self):
        """App-level PrivacyInfo.xcprivacy plus any shipped by node_modules."""
        app_manifest, sdk_manifests = None, []
        for base in ("ios", "assets", "."):
            d = self.p(base)
            if not os.path.isdir(d):
                continue
            for dirpath, dirs, files in os.walk(d):
                dirs[:] = [x for x in dirs if x not in
                           ("node_modules", "Pods", "build", ".git", ".expo")]
                for fn in files:
                    if fn == "PrivacyInfo.xcprivacy":
                        app_manifest = os.path.relpath(
                            os.path.join(dirpath, fn), self.root)
                        break
                if app_manifest:
                    break
            if app_manifest:
                break

        nm = self.p("node_modules")
        if os.path.isdir(nm):
            count = 0
            for dirpath, dirs, files in os.walk(nm):
                depth = dirpath[len(nm):].count(os.sep)
                if depth > 4:
                    dirs[:] = []
                    continue
                for fn in files:
                    if fn == "PrivacyInfo.xcprivacy":
                        sdk_manifests.append(os.path.relpath(
                            os.path.join(dirpath, fn), self.root))
                        count += 1
                if count > 400:
                    break
        else:
            self.gap("node_modules",
                     "node_modules is not installed, so SDK-shipped privacy manifests "
                     "could not be verified. Run `npm install` and re-scan.")
        return app_manifest, sdk_manifests

    def read_manifest_categories(self, relpath):
        try:
            with open(self.p(relpath), "rb") as f:
                d = plistlib.load(f)
        except Exception:                            # noqa: BLE001
            return None
        cats = set()
        for entry in d.get("NSPrivacyAccessedAPITypes") or []:
            t = entry.get("NSPrivacyAccessedAPIType")
            if t:
                cats.add(t)
        return dict(categories=cats, raw=d)

    def check_icon(self, cfg):
        icon_rel = (cfg.get("ios") or {}).get("icon") or cfg.get("icon")
        candidates = []
        if icon_rel:
            candidates.append(icon_rel.lstrip("./"))
        candidates += ["assets/icon.png", "assets/images/icon.png"]
        path = None
        for c in candidates:
            if self.exists(c):
                path = c
                break
        if not path:
            self.add("ICON-MISSING", "critical",
                     "App icon not found",
                     clause="ASC:screenshot-specifications",
                     evidence="No icon at %s" % ", ".join(candidates),
                     fix="Add a 1024x1024 PNG with no alpha channel and point "
                         "`expo.icon` (or `expo.ios.icon`) at it.")
            return
        info = png_info(self.p(path))
        self.facts["icon"] = dict(path=path, **(info or {}))
        if not info:
            self.add("ICON-UNREADABLE", "medium", "App icon is not a readable PNG",
                     evidence=path,
                     fix="Export the icon as a standard 8-bit PNG.")
            return
        w, h = info["width"], info["height"]
        if (w, h) != (1024, 1024):
            self.add("ICON-SIZE", "high",
                     "App icon is %dx%d, not 1024x1024" % (w, h),
                     clause="ASC:screenshot-specifications",
                     evidence="%s is %dx%d" % (path, w, h),
                     fix="Export a 1024x1024 PNG. App Store Connect rejects the "
                         "upload outright at any other size.")
        if info["has_alpha"]:
            self.add("ICON-ALPHA", "critical",
                     "App icon contains an alpha channel",
                     clause="ASC:screenshot-specifications",
                     evidence="%s has color type %d%s"
                              % (path, info["color_type"],
                                 " and a tRNS chunk" if info["trns"] else ""),
                     fix="Flatten the icon onto an opaque background and re-export "
                         "without transparency (color type 2, no tRNS). App Store "
                         "Connect rejects icons with alpha at upload time.")

    def check_usage_descriptions(self, deps, plist):
        weak_res = [re.compile(p) for p in
                    self.map["usage_description_defaults"]["weak_regexes"]]
        defaults = set(self.map["usage_description_defaults"]["patterns"])
        needed = {}
        for pkg in deps:
            entry = self.map["packages"].get(pkg)
            if not entry:
                continue
            for key in entry.get("ios_usage_descriptions") or []:
                needed.setdefault(key, []).append(pkg)
        self.facts["required_usage_descriptions"] = {
            k: v for k, v in sorted(needed.items())}

        for key, pkgs in sorted(needed.items()):
            val = plist.get(key)
            if val in (None, ""):
                self.add("PLIST-MISSING-%s" % key, "critical",
                         "Missing %s" % key,
                         clause="5.1.1",
                         evidence="Required by: %s. Not present in %s"
                                  % (", ".join(pkgs),
                                     " / ".join(self.facts.get("info_plist_sources")
                                                or ["app config"]) or "app config"),
                         fix='Add to app.json under expo.ios.infoPlist:\n'
                             '  "%s": "<specific reason this app needs it>"\n'
                             "The build will be rejected at review, and on device the "
                             "permission prompt crashes without this key." % key)
                continue
            if val in defaults or any(r.search(str(val)) for r in weak_res):
                self.add("PLIST-WEAK-%s" % key, "medium",
                         "%s uses a generic purpose string" % key,
                         clause="5.1.1",
                         evidence='%s = "%s"' % (key, val),
                         fix="Rewrite it to name the specific feature and benefit, e.g. "
                             '"Used to attach a photo to your progress log." Reviewers '
                             "reject boilerplate and Expo's plugin default strings.",
                         confidence="medium")

    def check_required_reason(self, deps, app_manifest, sdk_manifests):
        needed = {}
        for pkg in deps:
            entry = self.map["packages"].get(pkg)
            if not entry:
                continue
            for cat in entry.get("required_reason_api") or []:
                needed.setdefault(cat, []).append(pkg)
        self.facts["required_reason_categories"] = {
            k: v for k, v in sorted(needed.items())}

        if not needed:
            return
        if not app_manifest:
            self.add("PRIVACY-MANIFEST-MISSING", "critical",
                     "No PrivacyInfo.xcprivacy in the app target",
                     clause="apple:required-reason-api",
                     evidence="Packages using required-reason API: %s"
                              % ", ".join(sorted({p for v in needed.values() for p in v})),
                     fix="Create ios/<YourApp>/PrivacyInfo.xcprivacy (or set "
                         "`expo.ios.privacyManifests` in app.json) declaring "
                         "NSPrivacyAccessedAPITypes for: %s. Since 1 May 2024 App Store "
                         "Connect rejects uploads that use these APIs without it."
                         % ", ".join(sorted(needed)),
                     corpus="apple/required-reason-api.md",
                     itms="ITMS-91053")
            return
        got = self.read_manifest_categories(app_manifest)
        if got is None:
            self.add("PRIVACY-MANIFEST-UNREADABLE", "high",
                     "PrivacyInfo.xcprivacy could not be parsed",
                     evidence=app_manifest,
                     fix="It must be a valid plist. Open it in Xcode to repair.")
            return
        missing = sorted(set(needed) - got["categories"])
        for cat in missing:
            self.add("REASON-MISSING-%s" % cat.replace(
                "NSPrivacyAccessedAPICategory", ""), "critical",
                "Privacy manifest does not declare %s" % cat,
                clause="apple:required-reason-api",
                evidence="Used by %s; %s declares %s"
                         % (", ".join(needed[cat]), app_manifest,
                            ", ".join(sorted(got["categories"])) or "nothing"),
                fix="Add an NSPrivacyAccessedAPITypes entry with "
                    "NSPrivacyAccessedAPIType = %s and an approved reason code "
                    "from corpus/apple/required-reason-codes.md." % cat,
                corpus="apple/required-reason-codes.md",
                itms="ITMS-91053")


    def check_listed_sdks(self, deps, sdk_manifests):
        """SDKs on Apple's published list must ship a manifest and a signature.

        Kept separate from check_required_reason because that one returns early
        when the app has no manifest at all -- which is exactly the project most
        likely to also have this problem.
        """
        listed = set()
        for pkg in deps:
            entry = self.map["packages"].get(pkg) or {}
            for name in entry.get("apple_listed_sdk") or []:
                listed.add((name, pkg))
        self.facts["apple_listed_sdks"] = sorted(n for n, _ in listed)
        if not listed:
            return
        pkgs = sorted({p for _, p in listed})
        names = sorted({n for n, _ in listed})
        self.add("SDK-MANIFEST-REQUIRED", "high",
                 "%d SDK(s) on Apple's list must ship a privacy manifest and "
                 "signature" % len(names),
                 clause="apple:third-party-sdk-requirements",
                 evidence="Pulled in by %s: %s. %d SDK-shipped manifests were found "
                          "under node_modules."
                          % (", ".join(pkgs), ", ".join(names), len(sdk_manifests)),
                 fix="Upgrade each to a version that ships its own "
                     "PrivacyInfo.xcprivacy and signature. Patching the pod by hand "
                     "does not satisfy the signature requirement. This is the most "
                     "common cause of the ITMS-91061 upload rejection in Expo "
                     "projects. Cross-check the current list in "
                     "corpus/apple/third-party-sdk-requirements.md.",
                 confidence="medium",
                 corpus="apple/third-party-sdk-requirements.md",
                 itms="ITMS-91061")

    def check_signin_with_apple(self, deps, cfg, plist):
        third_party, satisfied = [], []
        for pkg in deps:
            entry = self.map["packages"].get(pkg) or {}
            if "sign-in-with-apple" in (entry.get("triggers") or []):
                third_party.append(pkg)
            if "sign-in-with-apple" in (entry.get("satisfies") or []):
                satisfied.append(pkg)
        self.facts["third_party_login_packages"] = third_party
        self.facts["apple_auth_packages"] = satisfied
        if third_party and not satisfied:
            self.add("SIWA-MISSING", "critical",
                     "Third-party login present with no Sign in with Apple",
                     clause="4.8",
                     evidence="Third-party login from: %s. No expo-apple-authentication "
                              "or @invertase/react-native-apple-authentication in "
                              "dependencies." % ", ".join(third_party),
                     fix="Add `expo-apple-authentication`, render an "
                         "`AppleAuthenticationButton` alongside your other login "
                         "buttons, and enable the Sign In with Apple capability "
                         "(`expo.ios.usesAppleSignIn: true`). Guideline 4.8 requires an "
                         "equivalent privacy-preserving login option whenever a "
                         "third-party service sets up the primary account.",
                     corpus="apple/asrg.sections/4.8.md")

    def check_iap(self, deps, cfg):
        iap = [p for p in deps
               if "subscription-terms" in
               ((self.map["packages"].get(p) or {}).get("triggers") or [])]
        self.facts["iap_packages"] = iap
        if not iap:
            return
        src = self.grep_source(r"restorePurchases|restoreTransactions|"
                               r"syncPurchases|restore_purchases")
        if not src:
            self.add("RESTORE-MISSING", "high",
                     "No restore-purchases call found in source",
                     clause="3.1.1",
                     evidence="IAP via %s but no restorePurchases/restoreTransactions/"
                              "syncPurchases call found in app source."
                              % ", ".join(iap),
                     fix="Add a visible \"Restore Purchases\" control that calls "
                         "`Purchases.restorePurchases()` (RevenueCat) or the "
                         "equivalent. Apps selling non-consumables or subscriptions "
                         "must let a returning user restore entitlements.",
                     confidence="medium",
                     corpus="apple/asrg.sections/3.1.1.md")

    def check_account_deletion(self, deps):
        accounts = [p for p in deps
                    if "account-deletion" in
                    ((self.map["packages"].get(p) or {}).get("triggers") or [])]
        self.facts["account_packages"] = accounts
        if not accounts:
            return
        hit = self.grep_source(r"delete[_ ]?account|deleteAccount|deleteUser|"
                               r"account[_ ]?deletion|removeAccount")
        if not hit:
            self.add("ACCOUNT-DELETE-MISSING", "critical",
                     "App creates accounts but no in-app account deletion found",
                     clause="5.1.1v",
                     evidence="Auth via %s; no delete-account code path found in source."
                              % ", ".join(accounts),
                     fix="Add an in-app control that permanently deletes the account "
                         "(not just a link to support, and not sign-out). Apple has "
                         "required this since 30 June 2022 for any app that supports "
                         "account creation.",
                     confidence="medium",
                     corpus="apple/asrg.sections/5.1.1v.md")

    def check_export_compliance(self, plist):
        if "ITSAppUsesNonExemptEncryption" not in plist:
            self.add("EXPORT-COMPLIANCE", "medium",
                     "ITSAppUsesNonExemptEncryption is not declared",
                     clause="ASC:export-compliance",
                     evidence="Key absent from Info.plist / expo.ios.infoPlist",
                     fix='Add "ITSAppUsesNonExemptEncryption": false to '
                         "expo.ios.infoPlist if you only use standard HTTPS. Without "
                         "it every single upload stops and asks you the export "
                         "compliance question before it can be submitted.",
                     corpus="apple/export-compliance.md")

    def check_dev_artifacts(self, deps, cfg):
        eas = None
        if self.exists("eas.json"):
            try:
                eas = json.loads(self.read("eas.json"))
            except json.JSONDecodeError:
                eas = None
        self.facts["eas_json"] = bool(eas)
        if eas:
            prod = ((eas.get("build") or {}).get("production") or {})
            if prod.get("developmentClient"):
                self.add("EAS-DEVCLIENT", "critical",
                         "eas.json production profile sets developmentClient: true",
                         clause="2.2",
                         evidence="build.production.developmentClient = true",
                         fix="Remove `developmentClient` from the production profile. "
                             "A dev-client build shows the Expo dev menu and will be "
                             "rejected as a beta/incomplete app.")
            if str(prod.get("distribution", "store")) == "internal":
                self.add("EAS-INTERNAL", "medium",
                         "eas.json production profile uses internal distribution",
                         evidence="build.production.distribution = internal",
                         fix="Set `\"distribution\": \"store\"` for the profile you "
                             "submit to the App Store.")
        if "expo-dev-client" in deps:
            self.add("DEV-CLIENT-DEP", "medium",
                     "expo-dev-client is a production dependency",
                     clause="2.2",
                     evidence="expo-dev-client present in package.json dependencies",
                     fix="Move it to devDependencies. If it is bundled into the "
                         "release binary the Expo dev menu can surface in the shipped "
                         "app, which reads as a beta build to review.",
                     confidence="medium")

    # ---------------------------------------------------------- Android side
    def scan_android(self, cfg, deps):
        perms, manifest_path = set(), None
        amp = self.p("android", "app", "src", "main", "AndroidManifest.xml")
        if os.path.exists(amp):
            manifest_path = os.path.relpath(amp, self.root)
            try:
                tree = ET.parse(amp)
                ns = "{http://schemas.android.com/apk/res/android}"
                for el in tree.getroot().iter("uses-permission"):
                    n = el.get(ns + "name")
                    if n:
                        perms.add(n)
                for el in tree.getroot().iter("service"):
                    t = el.get(ns + "foregroundServiceType")
                    if t:
                        for part in t.split("|"):
                            need = self.map["android_foreground_service_types"]["map"].get(part)
                            if need and need not in perms:
                                self.add("FGS-PERM-%s" % part, "high",
                                         "Foreground service type '%s' without %s"
                                         % (part, need.split(".")[-1]),
                                         clause="play:permissions-policy",
                                         evidence="%s declares foregroundServiceType=%s"
                                                  % (manifest_path, t),
                                         fix="Add <uses-permission android:name=\"%s\" /> "
                                             "to AndroidManifest.xml. Android 14+ crashes "
                                             "the service without it and Play blocks the "
                                             "release." % need,
                                         platform="android")
            except ET.ParseError:
                self.add("ANDROID-MANIFEST-PARSE", "high",
                         "AndroidManifest.xml could not be parsed",
                         evidence=manifest_path, fix="Repair the XML.",
                         platform="android")
        for p in (cfg.get("android") or {}).get("permissions") or []:
            perms.add(p if "." in p else "android.permission." + p)
        for pkg in deps:
            entry = self.map["packages"].get(pkg) or {}
            for p in entry.get("android_permissions") or []:
                perms.add(p)
        self.facts["android_permissions"] = sorted(perms)
        self.facts["android_manifest"] = manifest_path

        sens = self.map["android_sensitive_permissions"]
        needs_form = sorted(set(perms) & set(sens["declaration_form_required"]))
        needs_disc = sorted(set(perms) & set(sens["prominent_disclosure_required"]))
        self.facts["android_permissions_needing_declaration"] = needs_form
        self.facts["android_permissions_needing_disclosure"] = needs_disc
        if needs_form:
            self.add("PLAY-DECLARATION", "high",
                     "%d sensitive permission(s) require a Play Console declaration"
                     % len(needs_form),
                     clause="play:permissions-policy",
                     evidence="Requested in %s: %s"
                              % (manifest_path or "app config", ", ".join(needs_form)),
                     fix="For each one, either remove the permission or complete the "
                         "matching declaration form in Play Console > App content. "
                         "A release with an undeclared sensitive permission is "
                         "rejected. Most affected here: %s." % needs_form[0],
                     platform="android",
                     corpus="google/permissions-policy.md")
        if needs_disc:
            self.add("PLAY-DISCLOSURE", "medium",
                     "%d runtime permission(s) need prominent in-app disclosure"
                     % len(needs_disc),
                     clause="play:user-data-policy",
                     evidence="Requested via %s: %s"
                              % (manifest_path or "app config / dependencies",
                                 ", ".join(needs_disc)),
                     fix="Before each runtime permission dialog, show an in-app screen "
                         "that names the data, says what it is used for, and is not "
                         "buried in a privacy policy or ToS. Then declare the same "
                         "data in the Data safety form.",
                     confidence="medium", platform="android",
                     corpus="google/user-data-policy.md")

        tgt = None
        gradle = self.read("android", "build.gradle") or ""
        m = re.search(r"targetSdkVersion\s*=?\s*(\d+)", gradle)
        if m:
            tgt = int(m.group(1))
        self.facts["target_sdk"] = tgt
        if tgt is not None and tgt < 35:
            self.add("TARGET-SDK", "high",
                     "targetSdkVersion is %d" % tgt,
                     clause="play:target-api-level",
                     evidence="android/build.gradle targetSdkVersion = %d" % tgt,
                     fix="Raise targetSdkVersion. Play blocks new apps and updates "
                         "below its rolling target-API requirement; check "
                         "corpus/google/target-api-level.md for the current floor "
                         "and deadline.",
                     platform="android",
                     corpus="google/target-api-level.md")

    # ------------------------------------------------------------- shared
    def grep_source(self, pattern, exts=(".ts", ".tsx", ".js", ".jsx")):
        rx = re.compile(pattern, re.I)
        roots = [self.p(d) for d in ("app", "src", "components", "screens", "lib", "features")]
        roots = [r for r in roots if os.path.isdir(r)] or [self.root]
        checked = 0
        for r in roots:
            for dirpath, dirs, files in os.walk(r):
                dirs[:] = [d for d in dirs if d not in
                           ("node_modules", ".git", "ios", "android", ".expo", "build", "dist")]
                for fn in files:
                    if not fn.endswith(exts):
                        continue
                    checked += 1
                    if checked > 4000:
                        return None
                    try:
                        with open(os.path.join(dirpath, fn), encoding="utf-8",
                                  errors="ignore") as f:
                            if rx.search(f.read()):
                                return os.path.relpath(os.path.join(dirpath, fn), self.root)
                    except OSError:
                        pass
        return None

    # --------------------------------------------------------- metadata file
    def load_metadata(self):
        raw = self.read("shipcheck.metadata.md")
        if raw is None:
            self.facts["metadata_present"] = False
            return {}
        self.facts["metadata_present"] = True
        out, key, buf = {}, None, []
        for line in raw.splitlines():
            m = re.match(r"^##\s+(.*)$", line.strip())
            if m:
                if key:
                    out[key] = "\n".join(buf).strip()
                key, buf = m.group(1).strip().lower(), []
            elif key:
                if line.strip().startswith("<!--"):
                    continue
                buf.append(line)
        if key:
            out[key] = "\n".join(buf).strip()
        return {k: re.sub(r"<!--.*?-->", "", v, flags=re.S).strip()
                for k, v in out.items()}

    PLACEHOLDER = re.compile(
        r"lorem ipsum|dolor sit amet|TODO|FIXME|XXX|placeholder|"
        r"your app name here|coming soon|test test|asdf|"
        r"\bTBD\b|example\.com|localhost:\d+", re.I)

    def check_metadata(self, md, cfg):
        if not md:
            self.add("METADATA-MISSING", "critical",
                     "shipcheck.metadata.md not found",
                     evidence="No store-listing metadata to check",
                     fix="Run /shipcheck:scan again after filling in the generated "
                         "shipcheck.metadata.md. Roughly half of App Store rejections "
                         "are metadata problems (guideline 2.3), and none of them can "
                         "be seen from the code alone.")
            return

        limits = {"app name": 30, "subtitle": 30, "short description": 80,
                  "keywords": 100, "promotional text": 170, "description": 4000}
        for field, lim in limits.items():
            v = md.get(field, "")
            if v and len(v) > lim:
                self.add("META-LEN-%s" % field.replace(" ", "-"), "high",
                         "%s is %d chars (limit %d)" % (field.title(), len(v), lim),
                         clause="2.3",
                         evidence="%d characters" % len(v),
                         fix="Trim to %d characters. App Store Connect will not "
                             "accept the listing otherwise." % lim)

        for field in ("app name", "description", "privacy policy url", "support url"):
            if not md.get(field):
                self.add("META-EMPTY-%s" % field.replace(" ", "-"), "high",
                         "%s is empty in shipcheck.metadata.md" % field.title(),
                         clause="2.3" if "url" not in field else "5.1.1",
                         evidence="Field left blank",
                         fix="Fill it in. A missing privacy policy URL is an "
                             "automatic rejection under 5.1.1(i).")

        for field, v in md.items():
            if not v:
                continue
            m = self.PLACEHOLDER.search(v)
            if m:
                self.add("META-PLACEHOLDER-%s" % field.replace(" ", "-"), "critical",
                         "Placeholder text in %s" % field.title(),
                         clause="2.3.1",
                         evidence='%s contains "%s"' % (field.title(), m.group(0)),
                         fix="Replace it with real copy. Placeholder or template text "
                             "in the listing is a guaranteed 2.3 rejection.")

        kw = md.get("keywords", "")
        if kw and ", " in kw:
            self.add("META-KEYWORDS-SPACES", "low",
                     "Keywords contain spaces after commas",
                     clause="2.3.7",
                     evidence='keywords = "%s"' % kw[:80],
                     fix="Use commas with no spaces — each space costs you a character "
                         "of the 100-character budget.")

        accounts = md.get("accounts", "").lower()
        demo = md.get("demo account", "").lower()
        if accounts.startswith("yes") and (not demo or "not required" in demo):
            self.add("DEMO-ACCOUNT-MISSING", "critical",
                     "App has accounts but no demo account for review",
                     clause="2.1",
                     evidence="Accounts = yes, Demo account = %s"
                              % (md.get("demo account") or "(blank)"),
                     fix="Put working credentials in App Review notes. A reviewer who "
                         "hits a login wall with no credentials rejects under 2.1 App "
                         "Completeness, and it costs you a full review cycle.",
                     corpus="apple/asrg.sections/2.1.md")

        return md

    def check_urls(self, md):
        if self.offline or not md:
            return
        for field in ("privacy policy url", "support url", "marketing url"):
            url = (md.get(field) or "").strip().split()[0] if md.get(field) else ""
            if not url.startswith("http"):
                continue
            ok, detail = head_ok(url)
            self.facts.setdefault("url_checks", {})[url] = detail
            if not ok:
                self.add("URL-DEAD-%s" % field.replace(" ", "-"), "critical",
                         "%s is not reachable" % field.title(),
                         clause="2.3.8" if "support" in field else "5.1.1",
                         evidence="%s -> %s" % (url, detail),
                         fix="Fix or replace the URL. Reviewers open every link in the "
                             "listing; a dead privacy policy URL is an automatic "
                             "rejection.")

    # ------------------------------------------------------------------ run
    def run(self):
        cfg = self.load_app_config()
        pkg = self.load_package_json()
        deps = sorted(set(list((pkg.get("dependencies") or {}).keys())))
        devdeps = sorted(set(list((pkg.get("devDependencies") or {}).keys())))
        self.facts["dependencies"] = deps
        self.facts["dependency_count"] = len(deps)
        self.facts["expo_sdk"] = (pkg.get("dependencies") or {}).get("expo")
        self.facts["app_name"] = cfg.get("name")
        self.facts["slug"] = cfg.get("slug")
        self.facts["version"] = cfg.get("version")
        self.facts["bundle_id"] = (cfg.get("ios") or {}).get("bundleIdentifier")
        self.facts["android_package"] = (cfg.get("android") or {}).get("package")
        self.facts["known_packages_detected"] = [
            d for d in deps if d in self.map["packages"]]

        md = self.load_metadata()
        self.facts["metadata"] = md

        if self.platform in ("ios", "both"):
            plist = self.collect_info_plist(cfg)
            self.facts["info_plist_keys"] = sorted(plist.keys())
            app_manifest, sdk_manifests = self.find_privacy_manifests()
            self.facts["app_privacy_manifest"] = app_manifest
            self.facts["sdk_privacy_manifest_count"] = len(sdk_manifests)
            if not self.facts["bundle_id"]:
                self.add("BUNDLE-ID-MISSING", "high",
                         "No iOS bundle identifier configured",
                         evidence="expo.ios.bundleIdentifier is unset",
                         fix="Set `expo.ios.bundleIdentifier`; EAS Build cannot "
                             "produce a submittable binary without it.")
            self.check_icon(cfg)
            self.check_usage_descriptions(deps, plist)
            self.check_required_reason(deps, app_manifest, sdk_manifests)
            self.check_listed_sdks(deps, sdk_manifests)
            self.check_signin_with_apple(deps, cfg, plist)
            self.check_iap(deps, cfg)
            self.check_account_deletion(deps)
            self.check_export_compliance(plist)
            self.check_dev_artifacts(deps + devdeps, cfg)

        if self.platform in ("android", "both"):
            self.scan_android(cfg, deps)

        self.check_metadata(md, cfg)
        self.check_urls(md)

        self.findings.sort(key=lambda f: -SEV.get(f["severity"], 0))
        return dict(facts=self.facts, findings=self.findings, gaps=self.gaps)


# ---------------------------------------------------------------- helpers
def png_info(path):
    try:
        with open(path, "rb") as f:
            data = f.read(2 * 1024 * 1024)
    except OSError:
        return None
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    if data[12:16] != b"IHDR":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    color_type = data[25]
    trns = b"tRNS" in data
    return dict(width=width, height=height, color_type=color_type, trns=trns,
                has_alpha=color_type in (4, 6) or trns)


def head_ok(url, timeout=12):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": "ShipCheck/0.1 (link checker)"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if 200 <= r.status < 400:
                    return True, "HTTP %d" % r.status
                return False, "HTTP %d" % r.status
        except urllib.error.HTTPError as e:
            if e.code in (403, 405) and method == "HEAD":
                continue
            return False, "HTTP %d" % e.code
        except Exception as e:                       # noqa: BLE001
            if method == "GET":
                return False, type(e).__name__
    return False, "unreachable"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=".")
    ap.add_argument("--platform", default="both", choices=["ios", "android", "both"])
    ap.add_argument("--offline", action="store_true",
                    help="skip outbound URL reachability checks")
    ap.add_argument("--out", default="")
    args = ap.parse_args()
    res = Scan(args.project, args.platform, args.offline).run()
    text = json.dumps(res, indent=2, ensure_ascii=False, default=str)
    if args.out:
        d = os.path.dirname(os.path.abspath(args.out))
        os.makedirs(d, exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote %s (%d findings)" % (args.out, len(res["findings"])))
    else:
        print(text)


if __name__ == "__main__":
    sys.exit(main())
