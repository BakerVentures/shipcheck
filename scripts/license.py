#!/usr/bin/env python3
"""ShipCheck license check.

Tiers, matching how the product is sold:
  free       no key. Score + top 3 findings.
  single     $29 one-time, bound to ONE app. Unlimited scans of that app forever.
  unlimited  $49/yr, any number of apps.
  agency     $149/yr, any number of apps + seats.

Per-app binding without leaking which app
-----------------------------------------
A "single" licence has to be pinned to one app, which normally means telling the
server your bundle identifier. We don't. The client sends

    app_token = sha256(license_key + ":" + bundle_id)[:32]

which is stable for that (licence, app) pair and opaque to us: the server cannot
recover a bundle id from it without already knowing the bundle id. So binding
works and the privacy guarantee survives.

Read _payload(). That is the entire request body: a key, a version string, and
that opaque token. No project path, no dependency list, no metadata, no
findings.

Fails OPEN on any network or endpoint error, so a paying user is never blocked
by our downtime. Only an explicit, well-formed "invalid" downgrades to free.
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request

VERSION = "0.2.11"
HOME = os.path.expanduser("~/.shipcheck")
LICENSE_FILE = os.path.join(HOME, "license")
CACHE_FILE = os.path.join(HOME, "cache.json")
CACHE_TTL = 7 * 24 * 3600
# A "no, that licence is not valid" answer is cached for minutes, not days.
# These two must not share a TTL. A positive answer is safe to hold for a week
# -- the worst case is a lapsed subscription staying usable a little longer.
# A negative answer held for a week is the opposite: the realistic way to get
# one is a transient fault at our end (a VARIANT_* env var wrong for an hour, a
# captive portal answering JSON, a bad deploy), and with a 7-day TTL every
# customer who happened to scan during that window stays locked out for a week
# *after* the fault is fixed, with no way for us to reach into their machine
# and undo it. Re-asking a few minutes later costs one HTTP request.
NEG_CACHE_TTL = 10 * 60
DEFAULT_ENDPOINT = os.environ.get(
    "SHIPCHECK_VALIDATE_URL", "https://api.shipcheck.dev/validate")
FREE_FINDING_LIMIT = 3
PAID_TIERS = ("single", "unlimited", "agency")


def read_key():
    k = os.environ.get("SHIPCHECK_LICENSE_KEY", "").strip()
    if k:
        return k
    try:
        with open(LICENSE_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except (OSError, UnicodeDecodeError):
        # A garbled license file (partial write, binary garbage) must read as
        # "no key", not crash. This whole module exists so a paying user is
        # never blocked; an uncaught exception here is the one failure mode
        # that actually blocks them.
        return ""


def app_token(key, app_id):
    """Opaque, stable per-(licence, app) identifier. Not reversible to app_id."""
    if not app_id:
        return ""
    return hashlib.sha256(("%s:%s" % (key, app_id)).encode()).hexdigest()[:32]


def _cache_key(key, token):
    return hashlib.sha256(("%s|%s" % (key, token)).encode()).hexdigest()[:24]


def _cache_get(ck):
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            c = json.load(f)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(c, dict):
        # Malformed cache structure (truncated write, disk issue, whatever)
        # is a cache miss, not a crash -- falls through to a live check.
        return None
    e = c.get(ck)
    if not isinstance(e, dict):
        return None
    ttl = CACHE_TTL if e.get("valid", True) else NEG_CACHE_TTL
    if time.time() - e.get("checked_at", 0) > ttl:
        return None
    return e


def _cache_put(ck, entry):
    # Caching is an optimization, not a correctness requirement. Any failure
    # here -- corrupt file, disk full, wrong permissions, whatever -- must be
    # swallowed rather than propagate, or a caching bug becomes the thing that
    # blocks a paying user.
    try:
        os.makedirs(HOME, exist_ok=True)
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                c = json.load(f)
            if not isinstance(c, dict):
                c = {}
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            c = {}
        entry["checked_at"] = time.time()
        c[ck] = entry
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(c, f)
        os.chmod(CACHE_FILE, 0o600)
    except (OSError, TypeError, ValueError):
        pass


def _payload(key, token):
    """The complete outbound request body. Nothing identifying the project."""
    body = {"license_key": key, "plugin_version": VERSION}
    if token:
        body["app_token"] = token
    return body


def _free(reason):
    return dict(tier="free", valid=False, reason=reason, limit=FREE_FINDING_LIMIT)


def check(app_id=None, endpoint=None, timeout=8):
    key = read_key()
    if not key:
        return _free("no license key found")

    token = app_token(key, app_id)
    ck = _cache_key(key, token)
    cached = _cache_get(ck)
    if cached:
        tier = cached.get("tier", "unlimited")
        valid = cached.get("valid", True)
        when = time.strftime("%Y-%m-%d", time.localtime(cached["checked_at"]))
        if valid:
            reason = "cached (%s)" % when
        else:
            # Say plainly that this is a remembered refusal and that it expires
            # shortly -- "cached (2026-09-06)" on its own reads like a check
            # that succeeded, which is exactly wrong for someone who has paid
            # and is staring at a free-tier report.
            reason = ("cached refusal from %s; re-checked automatically within "
                      "%d minutes, or run `shipcheck-license --clear-cache` now"
                      % (when, NEG_CACHE_TTL // 60))
        return dict(tier=tier if valid else "free", valid=valid,
                    reason=reason,
                    limit=None if valid else FREE_FINDING_LIMIT,
                    bound_app=cached.get("bound_app"))

    url = endpoint or DEFAULT_ENDPOINT
    try:
        req = urllib.request.Request(
            url, data=json.dumps(_payload(key, token)).encode(), method="POST",
            headers={"Content-Type": "application/json",
                     "User-Agent": "ShipCheck/%s" % VERSION})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())

        if data.get("valid") is True:
            tier = data.get("tier") or "unlimited"
            if tier not in PAID_TIERS:
                tier = "unlimited"
            entry = dict(tier=tier, valid=True, bound_app=data.get("bound_app"))
            _cache_put(ck, entry)
            return dict(tier=tier, valid=True, reason="validated", limit=None,
                        bound_app=data.get("bound_app"))

        if data.get("valid") is False:
            _cache_put(ck, dict(tier="free", valid=False))
            return _free(data.get("error") or "license not valid")

        raise ValueError("unexpected response shape")
    except Exception as e:                            # noqa: BLE001
        # Fail open. Our downtime must never block someone who paid.
        return dict(tier="unlimited", valid=True, limit=None, degraded=True,
                    reason="endpoint unreachable (%s) — failing open"
                           % type(e).__name__)


def clear_cache():
    """Drop every cached verdict. The remedy of last resort for a customer
    stuck behind a stale refusal -- it has to be a real flag, because telling
    someone in a support email to delete a JSON file by hand does not scale and
    a prose instruction in a command's markdown only runs if a model follows
    it. Returns True if a cache file was actually removed."""
    try:
        os.remove(CACHE_FILE)
        return True
    except OSError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app-id", default="",
                    help="bundle identifier, for per-app licence binding")
    ap.add_argument("--require-pro", action="store_true",
                    help="exit 1 if this is not a paid tier")
    ap.add_argument("--clear-cache", action="store_true",
                    help="forget every cached verdict, then re-check live")
    args = ap.parse_args()
    if args.clear_cache:
        removed = clear_cache()
        print(json.dumps({"cleared": removed, "cache_file": CACHE_FILE},
                         indent=2), file=sys.stderr)
    res = check(args.app_id or None)
    print(json.dumps(res, indent=2))
    if args.require_pro and not res.get("valid"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
