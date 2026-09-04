# ShipCheck

**Find out why Apple will reject your app before Apple tells you.**

![ShipCheck scan demo](docs/demo/shipcheck-scan.gif)

ShipCheck is a Claude Code plugin that scans a React Native or Expo project plus
your store-listing metadata and produces a ranked rejection-risk report — each
finding carrying the exact guideline clause, the text of that clause, what the
reviewer will likely say, and the specific fix.

```
$ /shipcheck:scan

shipcheck · guidelines fetched 2026-09-04 · risk 71/100

HIGH  5.1.1(v)    Account deletion not found
      Reviewer will say: "Your app supports account creation but does not
      include an option to initiate account deletion."
      Fix: add a Delete account action under Settings → Account.

HIGH  ITMS-91053  Privacy manifest does not declare FileTimestamp
      Used by expo-file-system. Upload is rejected before review.
      Fix: add an NSPrivacyAccessedAPITypes entry with reason C617.1.

MED   3.1.2       Paywall shows price but not renewal period
      Fix: "$39.99 / year, renews automatically. Cancel anytime in Settings."

PASS  4.8 Sign in with Apple present · 2.1 no placeholder text ·
      1024px icon has no alpha · export compliance key set
```

![shipcheck:reply drafting a Resolution Center response](docs/demo/shipcheck-reply.gif)

Apple rejects a large share of submissions, and each rejection costs a review
cycle. Most rejections of React Native and Expo apps are configuration problems
you cannot see from JavaScript: a permission string pulled in by a transitive
Expo module, an SDK without a privacy manifest, a paywall that shows the price
but not the renewal period.

---

## Install

```
/plugin marketplace add BakerVentures/shipcheck
/plugin install shipcheck@shipcheck
```

Then, in your Expo/RN project:

```
/shipcheck:scan
```

First run drops a `shipcheck.metadata.md` template in your project root. Fill it
in with what you will actually paste into App Store Connect, then scan again —
roughly half of App Store rejections are metadata problems that cannot be seen
from code.

Requires Python 3.9+ (preinstalled on macOS). No pip packages, no Node
dependencies, no build step.

## Also runs without Claude Code

The deterministic half is a zero-dependency Python CLI, so it works in CI or
from any other agent:

```bash
shipcheck scan .          # terminal report; exits 1 on a critical finding
shipcheck init .          # add the store-listing metadata template
shipcheck report .        # write shipcheck-report.md
shipcheck corpus          # what the cached policy corpus contains
```

In GitHub Actions:

```yaml
- uses: BakerVentures/shipcheck@v1
  with:
    fail-on: critical
```

The judgment checks — store listing, paywall disclosure, category rules,
guideline 4.2 — need a model reading current guideline text, so those live in
the Claude Code plugin where your own Claude does that work.

## Commands

| Command | What it does |
|---|---|
| `/shipcheck:scan` | Full iOS + Android rejection-risk report → `shipcheck-report.md` |
| `/shipcheck:android` | Google Play only: Data safety, permissions, target API, testing gate |
| `/shipcheck:refresh` | Re-fetch Apple/Google policy and print a changelog of what changed |
| `/shipcheck:reply` | Draft a Resolution Center reply to a rejection you received |
| `/shipcheck:unlock` | Add your license key (`/shipcheck:license` is the same command) |

## What it checks

**iOS** — privacy manifest and required-reason API declarations (app and SDK);
`NSUsageDescription` strings for permissions pulled in transitively by Expo
modules, including Expo's generic default strings that reviewers reject;
the Apple-listed SDKs that must ship their own manifest and signature
(**ITMS-91061**) and undeclared required-reason APIs (**ITMS-91053**);
Sign in with Apple when third-party login is present (4.8); subscription terms
and paywall disclosure (3.1.2); restore purchases (3.1.1); in-app account
deletion (5.1.1(v)); demo account behind a login wall (2.1); placeholder text
and broken links in metadata (2.3); screenshots claiming features not in the
build (2.3.3); ATT prompt timing and wording; minimum functionality / web
wrapper risk (4.2); category rules for health, dating, kids and gambling; age
rating mismatches; export compliance; dev-client artifacts in production builds;
1024px icon with an alpha channel.

**Android** — manifest permissions versus Data safety declarations; sensitive
permissions needing a Play Console declaration; prominent disclosure for runtime
permissions; target API level against the current floor; foreground service
types and their permissions; account deletion including the web route Play
requires and Apple does not; Play Billing disclosures; and the closed-testing
gate for new personal developer accounts.

## Why the corpus matters

Apple and Google change these pages constantly. ShipCheck does not hardcode
policy text. It fetches **37 official Apple and Google pages** and caches them
with a fetch date and a SHA-256, chunked so a citation points at an exact clause
— the App Store Review Guidelines are split into **138 numbered clauses**, each
with a deep link back to Apple's page.

`/shipcheck:refresh` re-fetches everything and diffs it against the previous
hash, so you can see exactly what policy text changed and when. Findings quote
the clause **off disk**, which means a citation in your report is text ShipCheck
actually fetched, not text a model remembered.

Only structural facts are hardcoded — file paths, plist key names, permission
strings — because those are stable.

## Privacy guarantee

**Your code never leaves your machine.**

All reasoning runs inside your own Claude Code session. There is no ShipCheck
server that sees your project. The only outbound requests ShipCheck makes are:

1. Fetching public Apple/Google policy pages (`/shipcheck:refresh`).
2. Reachability checks on the URLs *you* put in `shipcheck.metadata.md`
   (skip with `--offline`).
3. A license check containing **only your license key, the plugin version, and
   an opaque per-app token**.

That token is `sha256(license_key + ":" + bundle_id)`. It exists so a one-app
licence can bind to one app — and because it is a hash, the server cannot work
out which app it is without already knowing your bundle id.

That third one is verifiable rather than promised: read `scripts/license.py`.
The function `_payload()` is the entire request body. No project path, no
dependency list, no source, no metadata, no findings.

If the license endpoint is unreachable, ShipCheck fails **open** and treats you
as licensed. An outage on our side never blocks your release.

## Pricing

| | Free | $29 one-time | $49 / year | $149 / year |
|---|---|---|---|---|
| | | **one app** | **unlimited apps** | **agency** |
| Risk score | ✅ | ✅ | ✅ | ✅ |
| Top 3 findings | ✅ | ✅ | ✅ | ✅ |
| Every finding, with clause text + fixes | | ✅ | ✅ | ✅ |
| `/shipcheck:reply` rejection drafter | | ✅ | ✅ | ✅ |
| Unlimited re-scans | | ✅ *(that app)* | ✅ | ✅ |
| Shareable across a team | | | | ✅ |

The $29 tier binds to one bundle identifier the first time you scan, and then
runs forever on that app. Ship more than one app and the yearly plan is cheaper
by the second app.

```
/shipcheck:unlock YOUR-KEY-HERE
```

Stored at `~/.shipcheck/license`, cached for 7 days.

## Layout

```
.claude-plugin/     plugin.json, marketplace.json
skills/shipcheck/   SKILL.md — the reasoning procedure
commands/           six slash commands (license and unlock are the same command,
                    two names — see /shipcheck:license)
scripts/            fetch_corpus.py, scan.py, report.py, license.py
                    htmlmd.py, docc.py, asrg.py  (extractors)
                    selftest.py                  (26 seeded violations + regressions)
                    data/rn_sdk_map.json         (structural rules)
corpus/             cached policy, chunked, + manifest.json
corpus/patterns/    hand-curated RN/Expo rejection patterns
bin/shipcheck       standalone CLI — the deterministic half, no Claude Code needed
action.yml          GitHub Action wrapping the CLI, for CI
.github/workflows/  self-test on every push, weekly corpus refresh, action dogfood
evals/              claude plugin eval case for the judgment half (early-access
                    tooling; see evals/*/README.md for its current limitations)
server/validate.js  license endpoint (deploy yourself)
docs/               landing page + assets/demo GIFs, served by GitHub Pages from /docs
marketing/          launch playbooks: Show HN, Reddit, PH, directories, LS setup
examples/           a deliberately non-compliant Expo app and a bare-RN one, for testing
```

## Not a guarantee

ShipCheck is advisory. App Review outcomes are decided by Apple and Google. A
clean report means the things ShipCheck knows how to check look right — it does
not mean you will be approved. Findings marked *Not checked* are gaps, not
passes; read that section.

Not affiliated with Apple Inc. or Google LLC.

---

© 2026 Ryan Baker. Proprietary — see [LICENSE](LICENSE).
