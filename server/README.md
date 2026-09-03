# shipcheck-validate

One Express route. Not deployed — deploy it yourself.

```bash
npm install
LEMONSQUEEZY_API_KEY=... node validate.js
```

Env:

| var | required | notes |
|---|---|---|
| `LEMONSQUEEZY_API_KEY` | yes | Lemon Squeezy API key |
| `LEMONSQUEEZY_STORE_ID` | no | if set, rejects keys from other stores |
| `PORT` | no | default 3000 |
| `CACHE_TTL_MS` | no | default 7 days |

Then point the plugin at it:

```bash
export SHIPCHECK_VALIDATE_URL=https://your-host/validate
```

`scripts/license.py` in the plugin defaults to `https://api.shipcheck.dev/validate`
— change that constant when you know your real hostname.

**The fail-open contract.** Return an explicit `{"valid": false}` only when Lemon
Squeezy says the key is genuinely bad. On any upstream error return 5xx, which
makes the client treat the user as paid. Getting this backwards means an outage
locks out every paying customer at once.

Node 18+ (uses global `fetch`).
