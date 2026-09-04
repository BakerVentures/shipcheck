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
| `VARIANT_SINGLE` | no | variant id(s) for the $29 one-time product |
| `VARIANT_UNLIMITED` | no | variant id(s) for the $49/yr product |
| `VARIANT_AGENCY` | no | variant id(s) for the $149/yr product |
| `SINGLE_APP_SEATS` | no | apps a `single` licence may bind (default 1) |
| `BINDING_FILE` | no | where app bindings persist (default `./bindings.json`) |
| `PORT` | no | default 3000 |
| `CACHE_TTL_MS` | no | default 7 days |
| `LS_VALIDATE_URL` | no | overrides the upstream Lemon Squeezy endpoint; defaults to the real one. For pointing at a local mock during testing -- see "Testing this locally" below. |

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

**Per-app binding.** A `single` licence pins to the first `app_token` it sees.
That token is a hash the client computes from the licence key and the bundle id,
so this server enforces "one app" without ever learning which app. Bindings
persist to `BINDING_FILE`; if you scale past one instance, move them to Postgres
or Redis, otherwise each instance keeps its own file and a customer can bind
more apps than they paid for. That errs in the customer's favour, which is the
right direction to be wrong at this price, but fix it before it matters.

**Variant mapping.** If you set none of the `VARIANT_*` vars, every valid licence
resolves to `unlimited`. That is deliberate: an unmapped variant should not lock
out someone who paid. Set them once your Lemon Squeezy products exist.

Node 18+ (uses global `fetch`).

## Testing this locally, without a real Lemon Squeezy account

Point `LS_VALIDATE_URL` at a local stand-in that mimics Lemon Squeezy's actual
`/v1/licenses/validate` response shape (`valid`, `license_key.status`,
`meta.store_id`/`meta.variant_id`):

```js
// mock-ls.js -- minimal stand-in, not part of the shipped server
const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: true }));
app.post('/v1/licenses/validate', (req, res) => {
  const key = req.body.license_key;
  if (key === 'SINGLE-KEY') {
    return res.json({ valid: true, license_key: { status: 'active' },
      meta: { store_id: 999, variant_id: 111 } });
  }
  return res.status(400).json({ valid: false, error: 'license_key not found.' });
});
app.listen(8956);
```

```bash
node mock-ls.js &
LS_VALIDATE_URL=http://localhost:8956/v1/licenses/validate \
  LEMONSQUEEZY_API_KEY=fake LEMONSQUEEZY_STORE_ID=999 \
  VARIANT_SINGLE=111 VARIANT_UNLIMITED=222 VARIANT_AGENCY=333 \
  SINGLE_APP_SEATS=1 PORT=8955 node validate.js &

curl -s -X POST http://localhost:8955/validate -H "Content-Type: application/json" \
  -d '{"license_key":"SINGLE-KEY","app_token":"AAA"}'
# {"valid":true,"tier":"single","bound_app":"AAA"}
```

This is how tier mapping, per-app binding (bind, re-validate the same app,
correctly refuse a second app), disabled/unknown keys, and rate limiting were
all actually verified before this shipped -- not just reviewed.
