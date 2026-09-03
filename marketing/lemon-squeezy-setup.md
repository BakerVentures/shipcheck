# Lemon Squeezy setup (no monthly fee; 5% + 50¢ per sale)

1. Create store "shipcheck". Enable license keys under Settings → Licensing.

2. Products (three, all with "Generate license keys" on):
   - shipcheck · one app — one-time, $29, key never expires. (Binding is enforced
     by our server, so the LS activation limit is informational; set it to 1 anyway.)
   - shipcheck · unlimited — yearly subscription, $49, activation limit 10, key expires with subscription.
   - shipcheck · agency — yearly subscription, $149, activation limit 50, key expires with subscription.
   Launch variant: add a 100-use discount code LAUNCH for $10 off the first two.

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
