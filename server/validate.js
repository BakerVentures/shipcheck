/**
 * ShipCheck license validation endpoint.
 *
 * A single Express route. Deploy it anywhere that can hold an env var.
 *
 * Contract with the plugin (scripts/license.py):
 *   POST /validate  { "license_key": "...", "plugin_version": "0.1.0" }
 *     -> 200 { "valid": true,  "tier": "pro" }
 *     -> 200 { "valid": false, "error": "..." }        client downgrades to free
 *     -> 5xx / timeout / anything else                 client FAILS OPEN as paid
 *
 * That last line is deliberate. A paying customer must never be blocked because
 * this box is down. Only a well-formed, explicit `valid: false` downgrades them.
 *
 * The request body is the entire contract: a key and a version string. Do not
 * add project telemetry here. "We never see your code" is the product's privacy
 * guarantee, and it is only true as long as this file stays this small.
 *
 * Env:
 *   LEMONSQUEEZY_API_KEY   required
 *   LEMONSQUEEZY_STORE_ID  optional; if set, licenses from other stores are rejected
 *   PORT                   default 3000
 *   CACHE_TTL_MS           default 7 days
 */

const express = require('express');

const app = express();
app.use(express.json({ limit: '4kb' }));

const LS_API = 'https://api.lemonsqueezy.com/v1/licenses/validate';
const CACHE_TTL_MS = Number(process.env.CACHE_TTL_MS || 7 * 24 * 60 * 60 * 1000);
const STORE_ID = process.env.LEMONSQUEEZY_STORE_ID || '';

/** key -> { valid, tier, error, at }. Swap for Redis if you run more than one instance. */
const cache = new Map();

function cacheGet(key) {
  const hit = cache.get(key);
  if (!hit) return null;
  if (Date.now() - hit.at > CACHE_TTL_MS) {
    cache.delete(key);
    return null;
  }
  return hit;
}

function cacheSet(key, value) {
  if (cache.size > 50000) cache.clear();
  cache.set(key, { ...value, at: Date.now() });
}

/** Rough per-key rate limit so a leaked key cannot be used to hammer Lemon Squeezy. */
const hits = new Map();
function rateLimited(key) {
  const now = Date.now();
  const win = hits.get(key) || [];
  const recent = win.filter((t) => now - t < 60_000);
  recent.push(now);
  hits.set(key, recent);
  return recent.length > 30;
}

async function validateWithLemonSqueezy(licenseKey) {
  const apiKey = process.env.LEMONSQUEEZY_API_KEY;
  if (!apiKey) throw new Error('LEMONSQUEEZY_API_KEY is not set');

  const body = new URLSearchParams({ license_key: licenseKey });
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);

  let res;
  try {
    res = await fetch(LS_API, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Bearer ${apiKey}`,
      },
      body,
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timer);
  }

  // 400 is Lemon Squeezy's answer for "no such key" -- a real negative, not an outage.
  if (!res.ok && res.status !== 400) {
    throw new Error(`lemonsqueezy responded ${res.status}`);
  }

  const data = await res.json();

  if (data.valid !== true) {
    return { valid: false, error: data.error || 'license key not valid' };
  }

  const status = data.license_key && data.license_key.status;
  if (status && !['active', 'inactive'].includes(status)) {
    return { valid: false, error: `license is ${status}` };
  }

  if (STORE_ID) {
    const storeId = data.meta && String(data.meta.store_id || '');
    if (storeId && storeId !== String(STORE_ID)) {
      return { valid: false, error: 'license belongs to a different store' };
    }
  }

  return { valid: true, tier: 'pro' };
}

app.post('/validate', async (req, res) => {
  const key = (req.body && req.body.license_key ? String(req.body.license_key) : '').trim();

  if (!key || key.length > 200) {
    return res.status(200).json({ valid: false, error: 'missing or malformed license key' });
  }

  const cached = cacheGet(key);
  if (cached) {
    return res.status(200).json({ valid: cached.valid, tier: cached.tier, error: cached.error, cached: true });
  }

  if (rateLimited(key)) {
    // 429 is not an explicit negative, so the client fails open. That is intended.
    return res.status(429).json({ error: 'rate limited' });
  }

  try {
    const result = await validateWithLemonSqueezy(key);
    cacheSet(key, result);
    return res.status(200).json(result);
  } catch (err) {
    console.error('[shipcheck] upstream failure:', err.message);
    // Do NOT answer `valid: false` here. An outage must not downgrade a paying user.
    return res.status(503).json({ error: 'validation temporarily unavailable' });
  }
});

app.get('/health', (_req, res) => res.json({ ok: true, cached: cache.size }));

if (require.main === module) {
  const port = Number(process.env.PORT || 3000);
  app.listen(port, () => console.log(`shipcheck validate listening on :${port}`));
}

module.exports = app;
