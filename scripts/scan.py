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


CORPUS_DIR = os.path.abspath(os.path.join(HERE, "..", "corpus"))


def corpus_text(rel):
    try:
        with open(os.path.join(CORPUS_DIR, rel), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def target_api_floors():
    """Read Play's current target-API floors out of the cached policy page.

    Hardcoding "API 35" would be stale the moment Google moves the deadline,
    which is the whole reason the corpus exists. Returns
    (new_app_floor, existing_app_floor, deadline) with None for anything the
    page no longer states in a recognisable form.
    """
    txt = corpus_text("google/target-api-level.md")
    if not txt:
        return None, None, None
    new = existing = deadline = None
    m = re.search(r"New apps and app updates must target Android\s+\d+\s*"
                  r"\(API level (\d+)\)", txt)
    if m:
        new = int(m.group(1))
    m = re.search(r"Existing apps must target Android\s+\d+\s*\(API level (\d+)\)", txt)
    if m:
        existing = int(m.group(1))
    m = re.search(r"Starting\s+([A-Z][a-z]+ \d{1,2},\s*\d{4})", txt)
    if m:
        deadline = m.group(1)
    return new, existing, deadline


PERMISSION_REMEDY = {
    "android.permission.QUERY_ALL_PACKAGES":
        "replace with a <queries> element naming the packages or intents you "
        "actually need. Keep the permission only with an approved declaration — "
        "broad package visibility is reserved for launchers, antivirus and "
        "accessibility tools.",
    "android.permission.ACCESS_BACKGROUND_LOCATION":
        "reviewed individually, and it needs a demo video of the in-app flow plus "
        "user-facing consent. Confirm foreground location genuinely is not enough; "
        "if it is, remove this. Budget several review rounds if you keep it.",
    "android.permission.MANAGE_EXTERNAL_STORAGE":
        "use the Storage Access Framework or scoped storage instead unless you are "
        "a file manager or backup app.",
    "android.permission.SCHEDULE_EXACT_ALARM":
        "use setInexactRepeating or WorkManager unless the app is an alarm clock or "
        "calendar; otherwise you must justify it.",
    "android.permission.USE_FULL_SCREEN_INTENT":
        "restricted to calling and alarm apps; anything else should use a normal "
        "high-priority notification.",
    "android.permission.REQUEST_INSTALL_PACKAGES":
        "only for app stores and file managers; remove it if a library pulled it in.",
}

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
        self.passes = []
        self.gaps = []
        self.facts = {"project_root": self.root}

    # ------------------------------------------------------------ utilities
    def p(self, *parts):
        """Join onto the project root, clamped so a config-derived path (an
        icon field, say) can never resolve outside it.

        This matters because the GitHub Action runs on `pull_request`: an
        external contributor's app.json can contain anything, and
        "assets/../../../../../../etc/passwd" resolves and reads cleanly --
        os.path.exists() honors embedded ".." through real directories
        regardless of where the string started. A single choke point here
        protects every caller (self.exists, self.read, and direct self.p()
        callers like png_info) without auditing each config-derived field.
        """
        real_root = os.path.realpath(self.root)
        candidate = os.path.realpath(os.path.join(self.root, *parts))
        if candidate != real_root and not candidate.startswith(real_root + os.sep):
            # Escapes the project. Return a path that cannot exist, so
            # exists() is False and open() raises the OSError callers
            # already handle -- no new exception shape for anyone to miss.
            return os.path.join(real_root, ".shipcheck-blocked-path-escape")
        return os.path.join(self.root, *parts)

    def exists(self, *parts):
        return os.path.exists(self.p(*parts))

    def read(self, *parts):
        # Every config file this reads (app.json, package.json, eas.json,
        # build.gradle, shipcheck.metadata.md) is legitimately a few KB.
        # Bounded at the one shared helper so every caller gets the limit
        # for free, same reasoning as the cap in grep_source: this runs
        # against a PR's own files in CI, and nothing here should trust
        # "small config file" without enforcing it.
        try:
            with open(self.p(*parts), encoding="utf-8", errors="replace") as f:
                return f.read(5 * 1024 * 1024)
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
        self.sdk_declared = {}
        self.node_modules_present = os.path.isdir(nm)
        if self.node_modules_present:
            count = 0
            for dirpath, dirs, files in os.walk(nm):
                depth = dirpath[len(nm):].count(os.sep)
                if depth > 4:
                    dirs[:] = []
                    continue
                # a manifest inside a library's own example/test app is not
                # that library's manifest
                dirs[:] = [x for x in dirs if x.lower() not in
                           ("example", "examples", "__tests__", "test", "tests",
                            "docs", "fixtures", "__fixtures__", "demo")]
                for fn in files:
                    if fn != "PrivacyInfo.xcprivacy":
                        continue
                    full = os.path.join(dirpath, fn)
                    sdk_manifests.append(os.path.relpath(full, self.root))
                    count += 1
                    rel = os.path.relpath(full, nm).split(os.sep)
                    pkg = os.sep.join(rel[:2]) if rel and rel[0].startswith("@") else rel[0]
                    try:
                        with open(full, "rb") as fh:
                            d = plistlib.load(fh)
                        cats = {e.get("NSPrivacyAccessedAPIType")
                                for e in d.get("NSPrivacyAccessedAPITypes") or []
                                if e.get("NSPrivacyAccessedAPIType")}
                    except Exception:            # noqa: BLE001
                        cats = set()
                    self.sdk_declared.setdefault(pkg, set()).update(cats)
                if count > 400:
                    break
        # CocoaPods is where a React Native wrapper's real native SDK lives, so
        # for a prebuilt project it is the authoritative source. RevenueCat,
        # FBSDK and AppsFlyer all ship their manifest in the pod, not in npm.
        self.pod_declared = {}
        pods = self.p("ios", "Pods")
        self.pods_present = os.path.isdir(pods)
        if self.pods_present:
            for dirpath, dirs, files in os.walk(pods):
                dirs[:] = [x for x in dirs if x not in
                           ("Headers", "Target Support Files", "Local Podspecs")]
                for fn in files:
                    if not fn.endswith(".xcprivacy"):
                        continue
                    full = os.path.join(dirpath, fn)
                    pod = os.path.relpath(full, pods).split(os.sep)[0]
                    try:
                        with open(full, "rb") as fh:
                            d = plistlib.load(fh)
                        cats = {e.get("NSPrivacyAccessedAPIType")
                                for e in d.get("NSPrivacyAccessedAPITypes") or []
                                if e.get("NSPrivacyAccessedAPIType")}
                    except Exception:            # noqa: BLE001
                        cats = set()
                    self.pod_declared.setdefault(pod, set()).update(cats)

        if not self.node_modules_present:
            self.gap("SDK privacy manifests",
                     "node_modules is not installed, so ShipCheck could not read which "
                     "privacy manifests your SDKs actually ship. Run `npm install` and "
                     "re-scan — this is the difference between guessing and knowing.")
        self.facts["pods_present"] = self.pods_present
        self.facts["pod_manifest_count"] = len(self.pod_declared)
        return app_manifest, sdk_manifests

    def has_native_ios(self, pkg):
        """Does this npm package contain native iOS code?

        Returns None when the package is not installed -- "not on disk" is not
        evidence that it ships no privacy manifest, it just means we cannot say.
        """
        base = self.p("node_modules", *pkg.split("/"))
        if not os.path.isdir(base):
            return None
        if os.path.isdir(os.path.join(base, "ios")):
            return True
        try:
            return any(f.endswith(".podspec") for f in os.listdir(base))
        except OSError:
            return None

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

    def find_appiconset_1024(self):
        """The Xcode asset-catalog icon (bare RN and prebuilt Expo ios/ both use
        this). Contents.json names the 1024x1024 marketing-icon filename; older
        Expo bare templates instead ship a single non-Contents.json PNG folder,
        which this also handles by falling back to any square PNG >= 1024px."""
        ios_dir = self.p("ios")
        if not os.path.isdir(ios_dir):
            return None
        for dirpath, dirs, files in os.walk(ios_dir):
            if "Pods" in dirpath or ".xcodeproj" in dirpath or ".xcworkspace" in dirpath:
                dirs[:] = []
                continue
            if os.path.basename(dirpath) != "AppIcon.appiconset":
                continue
            contents = os.path.join(dirpath, "Contents.json")
            if os.path.exists(contents):
                try:
                    with open(contents, encoding="utf-8") as f:
                        c = json.load(f)
                    for img in c.get("images") or []:
                        if img.get("size") == "1024x1024" and img.get("filename"):
                            fp = os.path.join(dirpath, img["filename"])
                            if os.path.exists(fp):
                                return os.path.relpath(fp, self.root)
                except (OSError, json.JSONDecodeError):
                    pass
            for fn in os.listdir(dirpath):
                if fn.lower().endswith(".png"):
                    fp = os.path.join(dirpath, fn)
                    info = png_info(fp)
                    if info and info["width"] >= 1024 and info["width"] == info["height"]:
                        return os.path.relpath(fp, self.root)
        return None

    def _icon_candidates(self, cfg):
        """Return {variant_label: relative_path}, in priority order.

        Expo SDK 53+ supports per-appearance icons as an object:
            "ios": {"icon": {"light": "...", "dark": "...", "tinted": "..."}}
        Older config and most bare RN projects just have a plain string. Both
        shapes have to be handled or a config that predates this feature
        crashes the whole scan -- which is what happened on a real project.
        """
        out = {}
        ios_icon = (cfg.get("ios") or {}).get("icon")
        if isinstance(ios_icon, dict):
            for variant in ("light", "dark", "tinted"):
                v = ios_icon.get(variant)
                if isinstance(v, str) and v:
                    out["ios.icon.%s" % variant] = v.lstrip("./")
        elif isinstance(ios_icon, str) and ios_icon:
            out["ios.icon"] = ios_icon.lstrip("./")
        top_icon = cfg.get("icon")
        if isinstance(top_icon, str) and top_icon and "icon" not in out:
            out["icon"] = top_icon.lstrip("./")
        for fallback in ("assets/icon.png", "assets/images/icon.png"):
            if not out and self.exists(fallback):
                out["(default location)"] = fallback
        return out

    def check_icon(self, cfg):
        candidates = self._icon_candidates(cfg)
        path = None
        primary_label = None
        for label, rel in candidates.items():
            if self.exists(rel):
                path = rel
                primary_label = label
                break
        if not path:
            path = self.find_appiconset_1024()
            primary_label = "AppIcon.appiconset"
        if not path:
            self.add("ICON-MISSING", "critical",
                     "App icon not found",
                     clause="ASC:screenshot-specifications",
                     evidence="No icon at %s, and no AppIcon.appiconset with a "
                              "1024x1024 entry under ios/"
                              % (", ".join(candidates.values()) or "any configured path"),
                     fix="Add a 1024x1024 PNG with no alpha channel and point "
                         "`expo.icon` (or `expo.ios.icon`) at it.")
            return
        info = png_info(self.p(path))
        self.facts["icon"] = dict(path=path, label=primary_label, **(info or {}))
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
                     evidence="%s (%s) is %dx%d" % (path, primary_label, w, h),
                     fix="Export a 1024x1024 PNG. App Store Connect rejects the "
                         "upload outright at any other size.")
        if info["has_alpha"]:
            self.add("ICON-ALPHA", "critical",
                     "App icon contains an alpha channel",
                     clause="ASC:screenshot-specifications",
                     evidence="%s (%s) has color type %d%s"
                              % (path, primary_label, info["color_type"],
                                 " and a tRNS chunk" if info["trns"] else ""),
                     fix="Flatten the icon onto an opaque background and re-export "
                         "without transparency (color type 2, no tRNS). App Store "
                         "Connect rejects icons with alpha at upload time.")

        # dark/tinted variants must independently satisfy the same rules --
        # Apple validates each icon asset in the catalog, not just the primary.
        for label, rel in candidates.items():
            if rel == path or not self.exists(rel):
                continue
            vi = png_info(self.p(rel))
            if not vi:
                continue
            if vi["has_alpha"]:
                self.add("ICON-ALPHA-%s" % label.split(".")[-1], "critical",
                         "%s icon contains an alpha channel" % label,
                         clause="ASC:screenshot-specifications",
                         evidence="%s has color type %d%s"
                                  % (rel, vi["color_type"],
                                     " and a tRNS chunk" if vi["trns"] else ""),
                         fix="Flatten the %s icon variant onto an opaque background "
                             "and re-export without transparency." % label)
            if (vi["width"], vi["height"]) != (1024, 1024):
                self.add("ICON-SIZE-%s" % label.split(".")[-1], "medium",
                         "%s icon is %dx%d, not 1024x1024"
                         % (label, vi["width"], vi["height"]),
                         clause="ASC:screenshot-specifications",
                         evidence="%s is %dx%d" % (rel, vi["width"], vi["height"]),
                         fix="Export the %s variant at 1024x1024 to match the "
                             "others." % label,
                         confidence="medium")

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

        call_sites = self.map.get("usage_description_call_sites", {})
        for key, pkgs in sorted(needed.items()):
            val = plist.get(key)
            if val in (None, ""):
                pattern = call_sites.get(key)
                used_in = self.grep_source(pattern) if pattern else None
                if used_in:
                    self.add("PLIST-MISSING-%s" % key, "critical",
                             "Missing %s" % key,
                             clause="5.1.1",
                             evidence="%s calls this API (%s) and %s is not set in %s"
                                      % (used_in, ", ".join(pkgs), key,
                                         " / ".join(self.facts.get("info_plist_sources")
                                                    or ["app config"])),
                             fix='Add to app.json under expo.ios.infoPlist:\n'
                                 '  "%s": "<specific reason this app needs it>"\n'
                                 "Without the key iOS terminates the app the moment the "
                                 "permission is requested, which reviewers hit "
                                 "immediately and reject under 2.1." % key)
                else:
                    self.add("PLIST-UNUSED-%s" % key, "low",
                             "%s pulls in %s but nothing calls it"
                             % (", ".join(pkgs), key.replace("UsageDescription", "")),
                             clause="5.1.1",
                             evidence="No call site found for %s, and %s is not set. "
                                      "The dependency looks unused."
                                      % (", ".join(pkgs), key),
                             fix="Either remove the unused dependency, or add %s "
                                 "before you ship the feature. Do not add the key "
                                 "speculatively — shipping a permission you never use "
                                 "widens your privacy surface and invites questions at "
                                 "review." % key,
                             confidence="medium")
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
        """Required-reason API coverage.

        Apple's rule, verbatim in corpus/apple/required-reason-api.md: an SDK
        reports its own API use in its own manifest, and "your third-party SDK
        can't rely on the privacy manifest files for apps that link" it. The
        converse matters just as much and is where a naive checker goes wrong:
        if a package ships a manifest declaring a category, the APP does not
        also have to declare it.

        So node_modules is the authority when it is there. The static map only
        says "this package touches required-reason API at all"; what it actually
        declares is read off disk.
        """
        touches = {}
        for pkg in deps:
            entry = self.map["packages"].get(pkg)
            if entry and entry.get("required_reason_api"):
                touches[pkg] = set(entry["required_reason_api"])
        self.facts["packages_touching_required_reason"] = sorted(touches)

        if not touches:
            return

        if not self.node_modules_present:
            # Do not guess. Guessing here produces a critical finding on a
            # correctly-configured app, which is worse than saying nothing.
            if not app_manifest:
                self.add("PRIVACY-MANIFEST-MISSING", "high",
                         "No PrivacyInfo.xcprivacy in the app target",
                         clause="apple:required-reason-api",
                         evidence="Packages that touch required-reason API: %s. "
                                  "node_modules is absent, so ShipCheck cannot tell "
                                  "which of these already declare it themselves."
                                  % ", ".join(sorted(touches)),
                         fix="Install dependencies and re-scan for an exact answer. "
                             "If your app's own native code touches these APIs you "
                             "need ios/<App>/PrivacyInfo.xcprivacy (or "
                             "`expo.ios.privacyManifests` in app.json); if only your "
                             "SDKs do, they must each ship their own.",
                         confidence="medium",
                         corpus="apple/required-reason-api.md",
                         itms="ITMS-91053")
            return

        uncovered, covered, unverifiable = {}, {}, {}
        not_installed = []
        for pkg, cats in touches.items():
            native = self.has_native_ios(pkg)
            if native is None:
                not_installed.append(pkg)
                continue
            if not native:
                # A JS-only package cannot call a required-reason API itself; its
                # storage goes through AsyncStorage / expo-file-system, which
                # declare their own. Flagging it is noise.
                continue
            declared = self.sdk_declared.get(pkg)
            if declared:
                covered[pkg] = sorted(declared)
                continue
            pod_names = (self.map["packages"].get(pkg) or {}).get("pods") or []
            if pod_names:
                if not self.pods_present:
                    unverifiable[pkg] = pod_names
                    continue
                if any(p in self.pod_declared for p in pod_names):
                    covered[pkg] = sorted(
                        {c for p in pod_names for c in self.pod_declared.get(p, ())})
                    continue
            uncovered[pkg] = sorted(cats)

        if not_installed:
            self.gap("Uninstalled dependencies",
                     "These are in package.json but not under node_modules, so their "
                     "privacy manifests could not be checked: %s. Run a full install "
                     "and re-scan." % ", ".join(sorted(not_installed)))
        if unverifiable:
            self.gap("Pod-delivered privacy manifests",
                     "These packages ship their native SDK through CocoaPods, and "
                     "ios/Pods is not present, so ShipCheck cannot confirm the pod "
                     "carries its privacy manifest: %s. Run `npx expo prebuild` (or "
                     "`pod install`) and re-scan."
                     % ", ".join(sorted(unverifiable)))
        self.facts["sdk_self_declared"] = {k: sorted(v) for k, v in
                                           sorted(self.sdk_declared.items())}
        self.facts["packages_without_own_manifest"] = sorted(uncovered)

        for pkg, cats in sorted(uncovered.items()):
            self.add("SDK-NO-MANIFEST-%s" % pkg.replace("/", "-").replace("@", ""),
                     "high",
                     "%s uses required-reason API but ships no privacy manifest" % pkg,
                     clause="apple:required-reason-api",
                     evidence="No PrivacyInfo.xcprivacy found under node_modules/%s. "
                              "Expected it to declare: %s" % (pkg, ", ".join(cats)),
                     fix="Upgrade %s to a version that ships its own "
                         "PrivacyInfo.xcprivacy. If no such version exists, declare "
                         "the categories in your app's manifest as a stopgap and open "
                         "an issue upstream — Apple emails ITMS-91053/91061 on upload "
                         "and, since 1 May 2024, blocks the build." % pkg,
                     confidence="medium",
                     corpus="apple/required-reason-api.md",
                     itms="ITMS-91061")

        if not app_manifest:
            self.add("PRIVACY-MANIFEST-MISSING", "high",
                     "No PrivacyInfo.xcprivacy in the app target",
                     clause="apple:required-reason-api",
                     evidence="%d SDK manifest(s) found under node_modules, but the "
                              "app target has none. An app manifest is also where "
                              "NSPrivacyTracking and NSPrivacyCollectedDataTypes live."
                              % len(sdk_manifests),
                     fix="Add `expo.ios.privacyManifests` to app.json (Expo SDK 50+) "
                         "or ios/<App>/PrivacyInfo.xcprivacy, declaring any "
                         "required-reason API your own native code uses plus your "
                         "data-collection and tracking posture.",
                     confidence="medium",
                     corpus="apple/required-reason-api.md",
                     itms="ITMS-91053")
        elif covered:
            self.passes.append(dict(
                title="Required-reason API declarations",
                clause="apple:required-reason-api",
                note="%d package(s) ship their own privacy manifest and declare their "
                     "own API use (%s), so your app manifest does not need to repeat "
                     "them." % (len(covered), ", ".join(sorted(covered)))))

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
        if not self.node_modules_present:
            self.gap("Apple-listed SDK manifests",
                     "These dependencies bundle SDKs on Apple's published list (%s), "
                     "which must ship a privacy manifest and signature. Without "
                     "node_modules ShipCheck cannot check whether the resolved "
                     "versions do." % ", ".join(sorted(n for n, _ in listed)))
            return

        def sdk_covered(pkg):
            if pkg in self.sdk_declared:
                return True
            pods = (self.map["packages"].get(pkg) or {}).get("pods") or []
            return any(p in self.pod_declared for p in pods)

        missing = sorted({p for _, p in listed if not sdk_covered(p)})
        ok = sorted({p for _, p in listed if sdk_covered(p)})
        if missing and not self.pods_present:
            self.gap("Apple-listed SDK manifests",
                     "%s deliver their SDK through CocoaPods and ios/Pods is absent, "
                     "so ShipCheck cannot confirm the pod ships a manifest and "
                     "signature. Run `npx expo prebuild` and re-scan."
                     % ", ".join(missing))
            missing = []
        if ok:
            self.passes.append(dict(
                title="Apple-listed SDKs ship privacy manifests",
                clause="apple:third-party-sdk-requirements",
                note=", ".join(ok)))
        if not missing:
            return
        names = sorted({n for n, p in listed if p in missing})
        self.add("SDK-MANIFEST-REQUIRED", "high",
                 "%s bundles SDK(s) on Apple's list but ships no privacy manifest"
                 % (missing[0] if len(missing) == 1
                    else "%d packages bundle" % len(missing)),
                 clause="apple:third-party-sdk-requirements",
                 evidence="No PrivacyInfo.xcprivacy under node_modules/%s. Bundles: %s"
                          % (", node_modules/".join(missing), ", ".join(names)),
                 fix="Upgrade %s to a version that ships its own privacy manifest and "
                     "signature. Patching the pod by hand does not satisfy the "
                     "signature requirement. This is the most common cause of the "
                     "ITMS-91061 upload rejection in Expo projects."
                     % ", ".join(missing),
                 confidence="high",
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
                         "rejected.\n\n%s"
                         % "\n".join("- **%s** — %s" % (p.split(".")[-1],
                                      PERMISSION_REMEDY.get(p, "declare the use case "
                                      "in Play Console > App content, or remove it."))
                                      for p in needs_form),
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

        new_floor, existing_floor, deadline = target_api_floors()
        self.facts["play_target_api"] = dict(new_apps=new_floor,
                                             existing_apps=existing_floor,
                                             deadline=deadline)
        floor = new_floor or existing_floor
        if tgt is not None and floor and tgt < floor:
            below_existing = existing_floor and tgt < existing_floor
            self.add("TARGET-SDK",
                     "critical" if below_existing else "high",
                     "targetSdkVersion is %d, below Play's floor of API %d"
                     % (tgt, floor),
                     clause="play:target-api-level",
                     evidence="android/build.gradle sets targetSdkVersion = %d. "
                              "Play requires API %s for new apps and updates%s, and "
                              "API %s for an existing app to stay available to users "
                              "on newer Android versions."
                              % (tgt, new_floor,
                                 " (from %s)" % deadline if deadline else "",
                                 existing_floor),
                     fix="Set `targetSdkVersion = %d` in android/build.gradle (or "
                         "`expo.android.targetSdkVersion` / the expo-build-properties "
                         "plugin) and re-test. %s"
                         % (new_floor or floor,
                            "Below API %d the Play Console rejects the upload "
                            "outright." % existing_floor if below_existing else
                            "Updates are blocked until you raise it."),
                     platform="android",
                     corpus="google/target-api-level.md")
        elif tgt is not None and not floor:
            self.gap("Play target API floor",
                     "Could not parse the current target-API requirement out of "
                     "corpus/google/target-api-level.md — Google may have reworded "
                     "the page. Run /shipcheck:refresh and check that section.")

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
                            # A legitimate .ts/.tsx source file is rarely more
                            # than a few hundred KB; 4 MB is generous headroom
                            # for a real file and a hard stop for a maliciously
                            # huge one committed to a PR this scans in CI.
                            if rx.search(f.read(4 * 1024 * 1024)):
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
            if not self.facts["bundle_id"]:
                self.facts["bundle_id"] = plist.get("CFBundleIdentifier")
            if not self.facts["app_name"]:
                self.facts["app_name"] = plist.get("CFBundleDisplayName") or plist.get("CFBundleName")
            if not self.facts["version"]:
                self.facts["version"] = plist.get("CFBundleShortVersionString")
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
        return dict(facts=self.facts, findings=self.findings,
                    passes=self.passes, gaps=self.gaps)


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
