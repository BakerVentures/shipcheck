# Lemon Squeezy setup (no monthly fee; 5% + 50¢ per sale)

## Status as of 2026-09-06

Configured in the dashboard. Account "Baker Ventures LLC"; storefront
<https://bakerventures.lemonsqueezy.com> (not yet activated):

| Step | State |
| --- | --- |
| 1. Create store | done |
| 2. Store settings (logo, contact email) | done |
| 3. Verify identity / activate store | **you** — personal ID details |
| 4. Two-factor authentication | **you** — your own device |
| 5. Products (all three) | done, published |
| 6. Discount code LAUNCH | done, active |
| 7. Connect a bank account | **you** — banking details |

Products as actually created (product id in parentheses):

| Product | Price | License keys | Length | Activation limit |
| --- | --- | --- | --- | --- |
| ShipCheck · One App (1341681) | $29 one-time | on | unlimited (never expires) | 1 |
| ShipCheck · Unlimited (1341682) | $49/year | on | tied to subscription | 10 |
| ShipCheck · Agency (1341687) | $149/year | on | tied to subscription | 50 |

Each product's email receipt carries the thank-you note
"Run /shipcheck:unlock in Claude Code and paste this key."

Discount code (id 1122711): **LAUNCH**, $10 fixed amount off, scoped to One App
and Unlimited only (not Agency), limited to 100 redemptions across all
customers, currently Active.

### Test mode, and what it means for the above

All of the above was created while the dashboard's *Test mode* toggle was on.
Lemon Squeezy keeps test data completely separate from live data, and the
toggle **cannot be switched off until the store is activated** (step 3) — so
test mode was not a choice, it is where a not-yet-activated store puts you.

The fix was applied: every product and the discount was pushed across with the
"Copy to Live Mode" item in each row's `...` menu. Lemon Squeezy confirmed
"Your product is now in live mode!" for ShipCheck · One App and "Your discount
is now in live mode!" for LAUNCH. The same menu item was clicked for Agency and
Unlimited but their toasts had already faded before they could be read, so
those two are **probable, not confirmed** — verify after activation rather than
assuming, and do not simply click Copy to Live Mode again, which would create
duplicate live products.

Verification is blocked until activation: with test mode locked on, the live
list is not viewable in the dashboard, and the public storefront
<https://bakerventures.lemonsqueezy.com> answers "This store has not been
activated."

**After you finish step 3, do these in order:**

1. Switch *Test mode* off.
2. Confirm the live list holds exactly three products — One App $29, Unlimited
   $49/yr, Agency $149/yr — and one LAUNCH discount. Recreate anything missing
   from the tables above; delete any duplicate.
3. Open the live LAUNCH code and confirm it is still scoped to One App and
   Unlimited only. A copied discount's product scoping points at the products
   it was built against, and the live products are new records with new ids, so
   this is the most likely thing to have come across wrong.
4. Collect the three live checkout URLs (row `...` → Share → Checkout Link) and
   paste them into `docs/index.html` over `REPLACE_CHECKOUT_SINGLE` (line 168),
   `REPLACE_CHECKOUT_YEARLY` (line 174) and `REPLACE_CHECKOUT_AGENCY` (line
   177).

A checkout link looks like
`https://bakerventures.lemonsqueezy.com/checkout/buy/<variant-uuid>`. **The
test-mode URLs are not reusable** — a copied product gets a new id, so its
checkout URL differs from its test-mode twin. Take the URLs from live mode.

## Original plan

1. Create store "shipcheck". Enable license keys under Settings → Licensing.

2. Products (three, all with "Generate license keys" on):
   - shipcheck · one app — one-time, $29, key never expires. (Binding is enforced
     by our server, so the LS activation limit is informational; set it to 1 anyway.)
   - shipcheck · unlimited — yearly subscription, $49, activation limit 10, key expires with subscription.
   - shipcheck · agency — yearly subscription, $149, activation limit 50, key expires with subscription.
   Launch variant: add a 100-use discount code LAUNCH for $10 off the first two.

   **A toggle-able cheaper price, for driving subscriptions up and down at
   will:** this is a Lemon Squeezy discount code, not a fourth product --
   nothing to build, no code changes, no separate ShipCheck tier. Products →
   your product → Discounts → New discount:
   - Percentage or flat amount off (e.g. 40% off the $49/yr tier, or a flat
     $20 off), scoped to one product or all of them.
   - Optional start/end dates for a scheduled window, or leave them off and
     just toggle the code's own Active/Inactive switch whenever you want it
     on or off -- that's the actual "cycle on/off" control, no scheduling
     needed.
   - Optional max redemptions (e.g. "first 50") if you want it to also self-
     expire by volume, not just by date.
   - The license key it issues is identical either way -- server/validate.js
     and the plugin only ever see the variant_id (which tier), never the
     price paid, so a discounted sale needs zero changes anywhere in
     ShipCheck to unlock the right tier correctly.

   On the "will it be too expensive" question: there's no compute or
   infrastructure cost to worry about here, discounted or not -- the whole
   reason $29/$49 undercuts subscription competitors is that a scan runs in
   the *buyer's own* Claude session, so shipcheck's marginal cost per sale
   is already ~$0 regardless of price. The only real cost of a discount is
   the revenue given up on that sale plus Lemon Squeezy's normal 5%+50¢ cut
   (proportionally larger the deeper the discount) -- there's no scenario
   where turning a discount on costs money beyond that. The one thing worth
   deciding deliberately: price it low enough to actually move the needle on
   conversions, but not so low it reads as the "real" price and makes $29/$49
   look inflated by comparison the next time someone sees it at full price --
   the existing pricing research flags exactly this anchoring risk. A 30-50%
   off code, toggled on for a specific push (a launch week, a slow month,
   answering a Reddit thread) rather than left on indefinitely, avoids that.

3. Checkout: turn on "Buy now" overlay links; paste each product's checkout URL into docs/index.html where it says REPLACE_CHECKOUT_*.

4. Receipt email: the default includes the license key. Add one line: "Run /shipcheck:unlock in Claude Code and paste this key."

5. Plugin validation: `server/validate.js` (deploy it yourself; nothing is hosted).
   It calls POST https://api.lemonsqueezy.com/v1/licenses/validate with the license_key,
   reads `meta.variant_id` from the response, and maps it to a tier via env vars:

       LEMONSQUEEZY_API_KEY=...
       LEMONSQUEEZY_STORE_ID=<your store id>     # rejects keys from other stores
       VARIANT_SINGLE=<variant id of the $29 product>
       VARIANT_UNLIMITED=<variant id of the $49/yr product>
       VARIANT_AGENCY=<variant id of the $149/yr product>

   Set these before you sell. With none set, every valid key resolves to `unlimited`
   and the $29 tier restricts nothing.

   Per-app binding is enforced by our server, not by Lemon Squeezy activations.
   The plugin sends an opaque `app_token` = sha256(license_key + ":" + bundle_id);
   the server binds a `single` licence to the first token it sees and refuses a
   second. That is why the server never learns which app you scanned. Lemon
   Squeezy activation limits are belt-and-braces and are not read by the plugin.

   Validation caches for 7 days client-side and 7 days server-side, and fails
   OPEN on any endpoint error — never answer `valid:false` on an outage, or a
   downtime locks out every paying customer at once.

   Point the plugin at your deployment:  export SHIPCHECK_VALIDATE_URL=https://your-host/validate
   (or change DEFAULT_ENDPOINT in scripts/license.py).

6. Webhook (optional, for analytics): Settings → Webhooks → order_created → your Render endpoint or a PostHog capture URL. Nothing else needs to run for fulfillment.

7. Tax and payouts: Lemon Squeezy is merchant of record; nothing to configure. Payouts every two weeks after the first sale clears.
