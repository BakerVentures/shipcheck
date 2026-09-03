# Competitive analysis (measured, September 2026)

Not vibes. Both tools were run against the same two projects: a real Expo SDK 56
app with `node_modules` and a prebuilt `ios/`, and `examples/bad-expo-app`, whose
violations are seeded on purpose so the ground truth is known.

## The field is bigger and freer than the GTM research assumed

| Tool | Form | Price | Notes |
|---|---|---|---|
| **greenlight** (RevylAI) | CLI + Claude Code plugin | Free, MIT, 2.4k★ | The real competitor. iOS + Play + IPA/APK binary analysis. Guidelines **bundled, not fetched.** |
| **AcceptMyApp** | Web app | $29/app one-time, $149/yr | Reads your GitHub repo read-only. iOS only. |
| **App Store Reject** | `npx skills add` | Free (beta) | Works across 30+ agents, not just Claude Code |
| **appstore-precheck** | Plugin + npm + brew | Free, MIT, 4★ | 55 vectors, **does live guideline drift with pinned quote hashes** |
| **LogicLine Labs checker** | Claude Code skill | Free, MIT | |
| **greenlight, precheck, others** | | | at least six free options in the same install surface |

The GTM doc said AcceptMyApp's €3.99–9.99 pricing was deprecated in favour of
$29/$149. That checks out — acceptmy.app currently states "$29 one-time, per
app" and "$149/year · unlimited apps", first analysis free. So the $29 price
point is validated by the one paid incumbent.

What the doc got wrong is the free field. It described "two free Claude-Code-native
competitors." There are at least six, one with 2.4k stars, and the strongest is
broader than ShipCheck on binary analysis and Android policy specifics.

## Head to head on the seeded fixture

greenlight: 9 findings. ShipCheck: 30 deterministic, plus 6 judgment findings
when the skill runs.

**Both catch:** target API level, foreground service types, missing app privacy
manifest, Sign in with Apple, QUERY_ALL_PACKAGES, background location, export
compliance.

**Only ShipCheck catches:**

| | Why it matters |
|---|---|
| Missing `NSCameraUsageDescription` while the app calls `launchCameraAsync` | iOS kills the app at the prompt. Guaranteed 2.1. greenlight misses it entirely. |
| Missing `NSUserTrackingUsageDescription` with Meta SDK present | greenlight *detects* the tracking SDKs and prints them, then does not connect that to the missing key |
| Expo's own default purpose strings (`Allow $(PRODUCT_NAME) to…`) | the single most common 5.1.1 nit in Expo apps |
| An SDK that ships no privacy manifest of its own | ITMS-91061 |
| Account deletion (5.1.1(v)) and Restore Purchases (3.1.1) | greenlight documents both rules; neither fired on a fixture that violates both. Its pattern matching does not reach RN code. |
| Icon with an alpha channel / not 1024×1024 | blocks the upload |
| Dead privacy-policy and support URLs | it never makes a request |
| Placeholder text, app name >30 chars, demo account, keyword format | **structural — see below** |
| `developmentClient: true` in the production EAS profile | Expo-specific |
| Prominent-disclosure for runtime permissions | |

## The structural gap, and the actual moat

greenlight cannot check the store listing. Not "does not yet" — *cannot*, in its
current shape. It reads `app.json`, so the best it can say is "expo.description
is empty." It never sees the description, keywords, What's New, screenshots,
review notes, demo account, age rating, or paywall copy you are about to paste
into App Store Connect, because nothing ever collects them.

Roughly half of App Store rejections live in exactly that material (2.3.x).

`shipcheck.metadata.md` is the whole difference. It is unglamorous — a markdown
file the developer fills in — and it is the moat, because:

1. It is the input no code scanner has.
2. Judging it needs an LLM reading current guideline text. Offline bundled rules
   cannot do it.
3. In a plugin, that LLM is the user's own Claude, so it costs us nothing. In a
   web app it is metered inference, which is why AcceptMyApp charges $29.

**Code scanning is commoditised. Store-listing judgment is not.**

## Where greenlight is better, honestly

- **Binary analysis.** It inspects IPA/APK/AAB. ShipCheck does not.
- **Android policy specifics.** Its target-API finding named API 35/36 and the
  31 August 2026 deadline while ours said "check the corpus." Fixed — ours now
  parses the floor and deadline out of the cached policy page, so it stays
  current on its own rather than being hardcoded. Same specificity, self-updating.
- **Maturity and reach.** Homebrew, Go, 2.4k stars, a company behind it.

## False positives, both directions

On the real app, greenlight returned "GREENLIT — no critical issues" with 4
findings, of which two are false positives: a `comingSoon` badge component read
as placeholder content, and a `console.log` in `scripts/reset-project.js`, a
build script that never ships.

ShipCheck had five false-positive classes of its own on that same app until
dogfooding removed them (see `scripts/selftest.py`, which now guards all five).
Nobody gets to be smug here; the difference is that ours are regression-tested.

## What this means for pricing

Charging for what six free tools already do is not a business. Charging for
the half none of them can reach might be.

- Deterministic code/config scanning → this is table stakes now. Free.
- Store-listing judgment, the live corpus, and the Resolution Center reply
  drafter → the paid tier.

That split is not a marketing construct; it maps exactly onto where the cost
and the defensibility actually are.
