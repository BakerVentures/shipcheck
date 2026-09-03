#!/usr/bin/env python3
"""ShipCheck license check.

Privacy guarantee, enforced here rather than promised in a README: the only
things that ever leave this machine are the license key, the plugin version and
the platform string. No project path, no dependency list, no metadata, no
findings. Read _payload() -- that is the entire request body.

Behaviour:
  * result cached in ~/.shipcheck/cache.json for 7 days
  * fails OPEN on any network/endpoint error, so a paying user is never blocked
    by an outage. Only an explicit, well-formed "invalid" from the endpoint
    downgrades to the free tier.
"""
import json
import os
import time
import urllib.error
import urllib.request

VERSION = "0.1.0"
HOME = os.path.expanduser("~/.shipcheck")
LICENSE_FILE = os.path.join(HOME, "license")
CACHE_FILE = os.path.join(HOME, "cache.json")
CACHE_TTL = 7 * 24 * 3600
DEFAULT_ENDPOINT = os.environ.get(
    "SHIPCHECK_VALIDATE_URL", "https://api.shipcheck.dev/validate")
FREE_FINDING_LIMIT = 3


def read_key():
    k = os.environ.get("SHIPCHECK_LICENSE_KEY", "").strip()
    if k:
        return k
    try:
        with open(LICENSE_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def _cache_get(key):
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            c = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    e = c.get(key)
    if not e:
        return None
    if time.time() - e.get("checked_at", 0) > CACHE_TTL:
        return None
    return e


def _cache_put(key, entry):
    try:
        os.makedirs(HOME, exist_ok=True)
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                c = json.load(f)
        except (OSError, json.JSONDecodeError):
            c = {}
        entry["checked_at"] = time.time()
        c[key] = entry
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(c, f)
        os.chmod(CACHE_FILE, 0o600)
    except OSError:
        pass


def _payload(key):
    """The complete outbound request body. Nothing about the project is here."""
    return {"license_key": key, "plugin_version": VERSION}


def check(endpoint=None, timeout=8):
    key = read_key()
    if not key:
        return dict(tier="free", valid=False, reason="no license key found",
                    limit=FREE_FINDING_LIMIT)

    cached = _cache_get(key)
    if cached:
        return dict(tier=cached.get("tier", "pro"), valid=cached.get("valid", True),
                    reason="cached (%s)" % time.strftime(
                        "%Y-%m-%d", time.localtime(cached["checked_at"])),
                    limit=None if cached.get("valid") else FREE_FINDING_LIMIT)

    url = endpoint or DEFAULT_ENDPOINT
    try:
        body = json.dumps(_payload(key)).encode()
        req = urllib.request.Request(
            url, data=body, method="POST",
            headers={"Content-Type": "application/json",
                     "User-Agent": "ShipCheck/%s" % VERSION})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
        if data.get("valid") is True:
            _cache_put(key, dict(tier="pro", valid=True))
            return dict(tier="pro", valid=True, reason="validated", limit=None)
        if data.get("valid") is False:
            _cache_put(key, dict(tier="free", valid=False))
            return dict(tier="free", valid=False,
                        reason=data.get("error") or "license not valid",
                        limit=FREE_FINDING_LIMIT)
        raise ValueError("unexpected response shape")
    except Exception as e:                            # noqa: BLE001
        # Fail open. A paying customer must never be blocked by our downtime.
        return dict(tier="pro", valid=True,
                    reason="endpoint unreachable (%s) — failing open"
                           % type(e).__name__,
                    limit=None, degraded=True)


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
