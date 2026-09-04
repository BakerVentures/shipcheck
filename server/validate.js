/**
 * ShipCheck license validation endpoint.
 *
 * A single Express route. Deploy it anywhere that can hold env vars and a
 * writable directory.
 *
 * Contract with the plugin (scripts/license.py):
 *   POST /validate  { "license_key", "plugin_version", "app_token"? }
 *     -> 200 { "valid": true,  "tier": "single|unlimited|agency", "bound_app": "..." }
 *     -> 200 { "valid": false, "error": "..." }   client downgrades to free
 *     -> 5xx / timeout / anything else            client FAILS OPEN as paid
 *
 * That last line is deliberate. A paying customer must never be blocked because
 * this box is down. Only a well-formed, explicit `valid: false` downgrades them.
 *
 * PRIVACY. `app_token` is sha256(license_key + ":" + bundle_id), computed on the
 * client. It is stable per (licence, app) so a $29 single-app licence can be
 * bound to one app, and it is opaque: you cannot recover a bundle id from it
 * without already knowing the bundle id. Do not add project telemetry to this
 * route. "We never see your code" is the product's privacy guarantee and it is
 * only true while this file stays this small.
 *
 * Env:
 *   LEMONSQUEEZY_API_KEY        required
 *   LEMONSQUEEZY_STORE_ID       optional; rejects licences from other stores
 *   VARIANT_SINGLE              variant id(s) for $29 one-time, comma separated
 *   VARIANT_UNLIMITED           variant id(s) for $49/yr
 *   VARIANT_AGENCY              variant id(s) for $149/yr
 *   SINGLE_APP_SEATS            apps a "single" licence may bind (default 1)
 *   BINDING_FILE                default ./bindings.json
 *   PORT                        default 3000
 *   CACHE_TTL_MS                default 7 days
 */

const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json({ limit: '4kb' }));

// Malformed JSON otherwise falls through to Express's default HTML error
// page, which includes the full server filesystem path and a stack trace --
// harmless to the plugin (license.py fails open on any non-JSON response
// either way) but a real information leak to anyone who sends a bad body on
// purpose. Clean JSON, no internals, same shape as every other response here.
app.use((err, _req, res, next) => {
  if (err instanceof SyntaxError && 'body' in err) {
    return res.status(200).json({ valid: false, error: 'malformed request body' });
  }
  return next(err);
});

// Overridable for local testing against a mock upstream; defaults to the
// real Lemon Squeezy endpoint in every real deployment.
const LS_VALIDATE = process.env.LS_VALIDATE_URL || 'https://api.lemonsqueezy.com/v1/licenses/validate';
const CACHE_TTL_MS = Number(process.env.CACHE_TTL_MS || 7 * 24 * 60 * 60 * 1000);
const STORE_ID = process.env.LEMONSQUEEZY_STORE_ID || '';
const SINGLE_APP_SEATS = Number(process.env.SINGLE_APP_SEATS || 1);
const BINDING_FILE = process.env.BINDING_FILE || path.join(__dirname, 'bindings.json');

const ids = (v) => String(v || '').split(',').map((s) => s.trim()).filter(Boolean);
const VARIANTS = {
  single: ids(process.env.VARIANT_SINGLE),
  unlimited: ids(process.env.VARIANT_UNLIMITED),
  agency: ids(process.env.VARIANT_AGENCY),
};

/**
 * Which apps each single-app licence is bound to.
 * File-backed so a redeploy does not silently unbind every customer.
 * Swap for Postgres/Redis if you run more than one instance -- with several
 * instances each would keep its own file and a customer could bind more apps
 * than they paid for. That errs in the customer's favour, which is the right
 * direction to be wrong for a $29 product, but it is worth fixing at scale.
 */
let bindings = {};
try {
  bindings = JSON.parse(fs.readFileSync(BINDING_FILE, 'utf8'));
} catch {
  bindings = {};
}
let writeQueued = false;
function persistBindings() {
  if (writeQueued) return;
  writeQueued = true;
  setTimeout(() => {
    writeQueued = false;
    try {
      fs.writeFileSync(BINDING_FILE, JSON.stringify(bindings), 'utf8');
    } catch (err) {
      console.error('[shipcheck] could not persist bindings:', err.message);
    }
  }, 250);
}

/** key -> { valid, tier, error, at } */
const cache = new Map();
const cacheGet = (k) => {
  const hit = cache.get(k);
  if (!hit) return null;
  if (Date.now() - hit.at > CACHE_TTL_MS) { cache.delete(k); return null; }
  return hit;
};
const cacheSet = (k, v) => {
  if (cache.size > 50000) cache.clear();
  cache.set(k, { ...v, at: Date.now() });
};

/** Rough per-key rate limit so a leaked key cannot hammer Lemon Squeezy. */
const hits = new Map();
function rateLimited(key) {
  const now = Date.now();
  const recent = (hits.get(key) || []).filter((t) => now - t < 60_000);
  recent.push(now);
  hits.set(key, recent);
  return recent.length > 30;
}

function tierFor(variantId) {
  const v = String(variantId || '');
  for (const [tier, list] of Object.entries(VARIANTS)) {
    if (list.includes(v)) return tier;
  }
  // No variant mapping configured, or an unrecognised product. Be generous:
  // a paying customer with an unmapped variant should not be locked out.
  return VARIANTS.single.length || VARIANTS.unlimited.length || VARIANTS.agency.length
    ? 'unlimited'
    : 'unlimited';
}

async function validateWithLemonSqueezy(licenseKey) {
  const apiKey = process.env.LEMONSQUEEZY_API_KEY;
  if (!apiKey) throw new Error('LEMONSQUEEZY_API_KEY is not set');

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  let res;
  try {
    res = await fetch(LS_VALIDATE, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Bearer ${apiKey}`,
      },
      body: new URLSearchParams({ license_key: licenseKey }),
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timer);
  }

  // 400 is Lemon Squeezy's answer for "no such key" -- a real negative, not an outage.
  if (!res.ok && res.status !== 400) throw new Error(`lemonsqueezy responded ${res.status}`);

  const data = await res.json();
  if (data.valid !== true) {
    return { valid: false, error: data.error || 'license key not valid' };
  }

  const lk = data.license_key || {};
  if (lk.status && !['active', 'inactive'].includes(lk.status)) {
    return { valid: false, error: `license is ${lk.status}` };
  }

  const meta = data.meta || {};
  if (STORE_ID && meta.store_id && String(meta.store_id) !== String(STORE_ID)) {
    return { valid: false, error: 'license belongs to a different store' };
  }

  return { valid: true, tier: tierFor(meta.variant_id) };
}

app.post('/validate', async (req, res) => {
  const body = req.body || {};
  const key = String(body.license_key || '').trim();
  const appToken = String(body.app_token || '').trim().slice(0, 64);

  if (!key || key.length > 200) {
    return res.status(200).json({ valid: false, error: 'missing or malformed license key' });
  }

  let result = cacheGet(key);
  if (!result) {
    if (rateLimited(key)) {
      // 429 is not an explicit negative, so the client fails open. Intended.
      return res.status(429).json({ error: 'rate limited' });
    }
    try {
      result = await validateWithLemonSqueezy(key);
      cacheSet(key, result);
    } catch (err) {
      console.error('[shipcheck] upstream failure:', err.message);
      // Do NOT answer `valid: false` here. An outage must not downgrade a payer.
      return res.status(503).json({ error: 'validation temporarily unavailable' });
    }
  }

  if (!result.valid) {
    return res.status(200).json({ valid: false, error: result.error });
  }

  // Unlimited and agency tiers are not app-bound.
  if (result.tier !== 'single') {
    return res.status(200).json({ valid: true, tier: result.tier });
  }

  // A single-app licence with no token yet (scan of a project with no bundle id)
  // still validates -- we just cannot bind it.
  if (!appToken) {
    return res.status(200).json({ valid: true, tier: 'single', bound_app: null });
  }

  const bound = bindings[key] || [];
  if (bound.includes(appToken)) {
    return res.status(200).json({ valid: true, tier: 'single', bound_app: appToken });
  }
  if (bound.length < SINGLE_APP_SEATS) {
    bindings[key] = [...bound, appToken];
    persistBindings();
    return res.status(200).json({ valid: true, tier: 'single', bound_app: appToken });
  }
  return res.status(200).json({
    valid: false,
    error: `this licence is already bound to ${bound.length} app(s). `
      + 'Upgrade to the $49/year unlimited plan to scan more apps.',
  });
});

app.get('/health', (_req, res) =>
  res.json({ ok: true, cached: cache.size, bound_licenses: Object.keys(bindings).length }));

if (require.main === module) {
  const port = Number(process.env.PORT || 3000);
  app.listen(port, () => console.log(`shipcheck validate listening on :${port}`));
}

module.exports = app;
