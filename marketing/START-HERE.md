# shipcheck launch kit

Everything here is already wired into the repo. `REPLACE_GITHUB` and
`REPLACE_SITE_URL` are substituted (`BakerVentures`,
`https://bakerventures.github.io/shipcheck/`).

## Done

- [x] Landing page at `docs/index.html`, sample output matches real scanner output
- [x] Repo README with install command and sample scan
- [x] `/shipcheck:unlock` exists, so the Lemon Squeezy receipt line is accurate
- [x] `server/validate.js` maps LS variant ids → tiers and enforces per-app binding

## Still needs you

1. **Push the repo to `github.com/BakerVentures/shipcheck`** (public).
2. **Settings → Pages → Source: `main` branch, `/docs` folder.** Live in a minute.
3. **Lemon Squeezy**: create the three products per `lemon-squeezy-setup.md`, then
   - paste the three checkout URLs into `docs/index.html` (`REPLACE_CHECKOUT_*`)
   - set `VARIANT_SINGLE` / `VARIANT_UNLIMITED` / `VARIANT_AGENCY` on the server.
     **Until these are set every valid key resolves to `unlimited` and the $29
     tier restricts nothing.**
4. **Deploy `server/validate.js`** and either export `SHIPCHECK_VALIDATE_URL` or
   change `DEFAULT_ENDPOINT` in `scripts/license.py` (currently the placeholder
   `https://api.shipcheck.dev/validate`).
5. Repo topics and About per `directory-submissions.md`.
6. Submit to the Anthropic community catalog; open the awesome-list PRs.
7. Set F5Bot keywords per `reddit-playbook.md`.
8. **Record one GIF of `/shipcheck:scan`.** Used in every channel. Run it against
   `examples/bad-expo-app` — it produces 29 findings and a 100/100 score, which
   demos well.

## Launch order

Reddit r/SideProject + r/ClaudeCode → Show HN (Tue–Thu, 9am–12pm ET) → X thread
same day → Product Hunt two weeks later.

Total cash outlay: $0 until the first sale.

## Known gap before you charge

The agency tier advertises **five team seats**. Seats are not implemented —
`server/validate.js` treats `agency` exactly like `unlimited` (any number of
apps, no seat accounting). Either build seats, or sell the tier as "unlimited
apps + priority guideline updates" until you do.
