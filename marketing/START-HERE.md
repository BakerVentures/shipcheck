# shipcheck launch kit

Status as of this session: the repo is live, installable, and CI is green.

## Done

- [x] Pushed to `github.com/BakerVentures/shipcheck` (public)
- [x] GitHub Pages live at `https://bakerventures.github.io/shipcheck/`
      (served from `/docs` on `master` — the repo's default branch, not `main`)
- [x] `v1.0.0` tagged and released; plugin's own `shipcheck--v0.1.0` tag also cut
- [x] Repo topics + About + homepage set
- [x] Installed via the **real** path end to end: `/plugin marketplace add
      BakerVentures/shipcheck` from a clean session, not a local path — 7
      components discovered, ~369 tokens always-on
- [x] CI green on GitHub's own runner (not just locally): `scripts/selftest.py`
      covers 26 seeded violations, 5 false-positive regressions from dogfooding
      two real apps, and 6 bare-React-Native regressions from a third
- [x] Standalone CLI (`bin/shipcheck`) verified from a genuinely fresh clone,
      correct exit codes for CI gating
- [x] GitHub Action (`action.yml`) — usable today via `uses:
      BakerVentures/shipcheck@v1`, no separate Marketplace listing needed for
      that to work
- [x] Landing page has a CLI/CI section now (it didn't before)
- [x] `render.yaml` added so `server/validate.js` deploys as a Render Blueprint
      with all five Lemon Squeezy env vars pre-declared

## Still needs you — this is the actual blocker on taking money

1. **Lemon Squeezy.** No existing account on this machine, and creating one
   needs your identity/banking, so this has to be you. Per
   `lemon-squeezy-setup.md`: create the store, the three products (one-time
   $29 / yearly $49 / yearly $149), and license keys.
2. **Paste the three checkout URLs** into `docs/index.html`
   (`REPLACE_CHECKOUT_SINGLE/YEARLY/AGENCY`) — the only placeholders left in
   the file.
3. **Deploy `server/validate.js`.** Render Dashboard → New → Blueprint →
   connect this repo → Apply. It'll prompt for `LEMONSQUEEZY_API_KEY` first;
   the three `VARIANT_*` ids come after you create the products in step 1.
   **Until `VARIANT_SINGLE/UNLIMITED/AGENCY` are set, every valid key resolves
   to `unlimited` — the $29 single-app tier restricts nothing.** That's
   deliberate fail-safe behavior, not a bug, but it means step 1 has to
   actually finish before you charge $29 and expect it to mean one app.
4. Point the plugin at your deployed endpoint: change `DEFAULT_ENDPOINT` in
   `scripts/license.py` to your Render URL and commit it (so users don't need
   an env var), or tell early users to `export SHIPCHECK_VALIDATE_URL=...`.
5. Submit to the Anthropic community catalog: **clau.de/plugin-directory-submission**
   (confirmed URL). Run `claude plugin validate .` first — already passes.
6. Open the awesome-list PRs per `directory-submissions.md`.
7. Set F5Bot keywords per `reddit-playbook.md`.
8. **Record one GIF of `/shipcheck:scan`.** Run it against `examples/bad-expo-app`
   — 34 findings, 100/100 risk score, demos well. `examples/bare-rn-app` is a
   second good demo if you want to show RN (not just Expo) support explicitly.

## Launch order

Reddit r/SideProject + r/ClaudeCode → Show HN (Tue–Thu, 9am–12pm ET) → X thread
same day → Product Hunt two weeks later.

Total cash outlay: $0 until Lemon Squeezy's cut of the first sale.

## Competitive reality check

Read `competitive-analysis.md` before writing launch copy. The free field is
bigger than early research assumed — greenlight (2.4k★, MIT) does binary
analysis and Android specifics we don't. Our edge is the store-listing
judgment layer (guideline 2.3, paywall disclosure, category rules) that no
code scanner — free or paid — can reach, because none of them collect the
store listing at all. Lead launch copy with that, not with "we scan your code
too," because on code scanning alone we're one of ~7 free options.

## A deliberate non-feature: seat counting

The agency tier is sold as "unlimited apps, shareable across your team," not a
fixed seat count. Enforcing seats needs a device/user identifier on every
licence check, which conflicts with "your code never leaves your machine."
If you want per-seat pricing later, do it as separate Lemon Squeezy keys per
teammate, not plugin telemetry.
