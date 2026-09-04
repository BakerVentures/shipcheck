# shipcheck launch kit

Status as of 2026-09-04 (a second, much longer session on top of the first):
the repo is live, installable, CI is green, and the plugin has been through
ten version bumps (v0.2.2 → v0.2.10) fixing real bugs found by dogfooding
against a genuinely clean fixture and a headless plugin session, not just
code review. See below for what changed and why "is it launch-ready" now
splits cleanly into "yes, for free-tier use" and "no, not for paid" -- and
every remaining item under 'Still needs you' traces back to the same two
root blockers: Lemon Squeezy isn't set up, and `server/validate.js` isn't
deployed.

## Done, this second session

- [x] **Four real bugs in htmlmd.py/docc.py** (the corpus HTML→Markdown
      renderer) that were corrupting real report citations -- a sentence-
      splitting bug (found via visually QA-ing new SEO pages, confirmed
      already live in `examples/bad-expo-app/shipcheck-report.md`), a
      decorative Apple icon rendering as broken `![alt]` markdown, a
      regression the first fix introduced, and 69 more bare-image instances
      across the corpus. v0.2.2 → v0.2.4.
- [x] **Four bugs in the "app is actually fine" scan/report path**, which had
      zero test coverage anywhere (every fixture that existed was
      deliberately violation-seeded): a dangling separator in the terminal
      summary, a report referencing a section that never rendered, and
      missing pass-on-success entries for four checks the README's own
      example already claimed existed. v0.2.5 → v0.2.7 (iOS + Android).
- [x] **`/shipcheck:refresh` was a complete no-op** -- it re-fetched policy
      text correctly but no scan ever read it back, because
      `${CLAUDE_PLUGIN_DATA}` (where refresh writes) is markdown-level text
      substitution, not a real environment variable a Python subprocess can
      read -- confirmed against Claude Code's own docs. First fix attempt
      (v0.2.8) didn't actually work; caught that with a marker-injection
      test against the real installed plugin, traced the real cause, and
      shipped the actual fix (v0.2.9 + v0.2.10, judgment-layer reads too).
      Verified with `--output-format stream-json` against a real session --
      every one of 29 corpus-related tool calls hit the refreshed path.
- [x] **Added `examples/clean-expo-app`** -- a genuinely compliant fixture,
      the first one in the repo. Wired into `selftest.py` and a new
      `clean-scan` CI job that runs the real tagged Action and asserts a
      genuine pass with real outputs, closing the same test-coverage gap at
      the CI layer too.
- [x] **The real comparison SEO page** (`docs/guidelines/vs-free-claude-code-checkers.html`),
      built from `competitive-analysis.md`'s actual measured data against
      greenlight, not the speculative "vs. AcceptMyApp" page the original
      pre-launch research suggested -- linked from the homepage right before
      pricing.
- [x] Landing page: dark mode, a sourced stat-band ("9.1M submissions
      evaluated, 2M+ rejected, 443K+ for privacy" -- verified against Apple's
      actual May 2026 Newsroom release, not just the research doc's
      citation), the missing "why not just ask Claude" FAQ entry, the agency
      pricing card de-emphasized per the UX research, `--json` on the CLI.
- [x] **Fixed the unverified launch-post anecdote** in `show-hn.md`,
      `x-thread.md`, and `product-hunt.md` -- all three opened with a
      first-person rejection story that couldn't be verified. Replaced with
      the real, sourced story already found this session (RizzMaxx's own
      fake-discount-paywall rejection). Also added the Product Hunt
      gallery's "3 PNGs of report sections," which never existed.
- [x] A `git stash` between `git add` and `git commit` silently dropped
      several files' staged changes once during this session -- caught it by
      checking the real CI run, not by trusting the commit message, and
      recovered with a follow-up commit. Worth knowing if a future commit
      here looks incomplete relative to what was intended.

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

## Done, this session (in addition to the "Done" list above)

- [x] Community catalog submission completed via platform.claude.com/plugins/submit
      (your Console session was already authenticated) — status: submitted for
      review, no ETA given
- [x] `awesome-claude-skills` PR opened and live:
      https://github.com/travisvn/awesome-claude-skills/pull/1211
- [x] `awesome-claude-code` **deliberately skipped** — their own
      CONTRIBUTING.md forbids PRs entirely ("Do not open a PR... not possible
      to submit via the gh CLI"), requires 14+ days of history or 100+ stars
      (this repo has neither yet), and states a paid/signup product is a
      review blocker. Submit later via their issue form once those clear:
      https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
- [x] Demo GIF recorded (`docs/demo/shipcheck-scan.gif`, via `vhs` against the
      synthetic `examples/bad-expo-app` fixture — not a real customer's app)
      and wired into both the README and the landing page's CLI section
- [x] Render blueprint (`render.yaml`) added for one-click `validate.js` deploy

## Still needs you — this is the actual blocker on taking money

Everything below needs your identity or banking. I did not attempt any of it —
account creation and entering financial/tax info are hard lines I don't cross
even on request.

1. **Lemon Squeezy.** No existing account on this machine. Per
   `lemon-squeezy-setup.md`: create the store, the three products (one-time
   $29 / yearly $49 / yearly $149), and license keys.
2. **Paste the three checkout URLs** into `docs/index.html`
   (`REPLACE_CHECKOUT_SINGLE/YEARLY/AGENCY`) — the only placeholders left in
   the file (confirmed live on the deployed page).
3. **Deploy `server/validate.js`.** Render Dashboard → New → Blueprint →
   connect this repo → Apply. It'll prompt for `LEMONSQUEEZY_API_KEY` first;
   the three `VARIANT_*` ids come after you create the products in step 1.
   **Until `VARIANT_SINGLE/UNLIMITED/AGENCY` are set, every valid key resolves
   to `unlimited` — the $29 single-app tier restricts nothing.** Deliberate
   fail-safe, not a bug — but step 1 has to finish before $29 means one app.
4. Point the plugin at your deployed endpoint: change `DEFAULT_ENDPOINT` in
   `scripts/license.py` to your Render URL and commit it, or tell early users
   to `export SHIPCHECK_VALIDATE_URL=...`.
5. Set F5Bot keywords per `reddit-playbook.md`.
6. **The landing page promises a 14-day no-questions refund** (`docs/index.html`,
   the "Refunds?" FAQ line). That's a real commitment to customers, not just
   copy — set the matching refund window in Lemon Squeezy's store settings so
   the policy is actually true the moment someone buys, and decide who
   monitors the receipt-reply inbox for refund requests.

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
