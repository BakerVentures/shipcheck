# ShipCheck Privacy Policy

**Last updated: 23 September 2026.** Applies to ShipCheck v0.2.16.

ShipCheck is operated by **Baker Ventures LLC**. Questions, deletion requests, or
anything else about this page: **rsb.baker+shipcheck@gmail.com**.

This policy covers three separate things, which have very different data flows:

1. the **ShipCheck plugin** — the scanner, the slash commands, and the GitHub Action;
2. the **license validation endpoint** — the only service Baker Ventures runs that a
   ShipCheck user's machine ever talks to;
3. the **documentation site** at `bakerventures.github.io/shipcheck/` and
   `shipcheck.bakerventuresstudio.com`.

Where this page and the code disagree, the code is the truth. The two files that
matter are short enough to read in full: `scripts/license.py` (the function
`_payload()` is the entire outbound request body) and `server/validate.js`.

---

## The short version

- **Your project never leaves your machine.** No source, no file paths, no dependency
  list, no store metadata, no findings, no scores. The scanner has no telemetry, no
  analytics, no crash reporting, and no install identifier of any kind.
- **The only data that reaches Baker Ventures** is a license check: your license key,
  the plugin version, and an opaque per-app hash. That is three fields, and only if
  you have bought a license.
- **There are no analytics or error-tracking services** anywhere in the plugin, the
  server, or the site.
- **We never see your payment details.** Purchases are handled by Lemon Squeezy as
  merchant of record.

---

## 1. The scanner — what it does and does not do

`/shipcheck:scan`, `/shipcheck:android`, `/shipcheck:reply`, the `shipcheck` CLI and
the GitHub Action all run the same scanner (`scripts/scan.py`) inside your own Claude
Code session or your own CI runner.

**What it reads, locally:** `app.json` / `app.config.js`, `package.json` and
`node_modules` package manifests, `Info.plist`, `PrivacyInfo.xcprivacy`,
`AndroidManifest.xml`, `build.gradle`, `eas.json`, app icon PNGs, your source files,
and the `shipcheck.metadata.md` file you write yourself.

**What it writes, locally:** `shipcheck-report.md` in your project (only when you ask
for a report), and nothing else. `/shipcheck:refresh` additionally writes a policy
corpus into the plugin's own data directory.

**What it transmits: nothing about your project.** There is no "ShipCheck server" that
receives a scan. The scanner contains exactly one network function, `head_ok()`, and it
is used for one purpose, described next.

### The one outbound request the scanner makes

If your `shipcheck.metadata.md` lists a **privacy policy URL, support URL, or marketing
URL**, ShipCheck sends an HTTP `HEAD` (falling back to `GET`) to each one, to check it
is reachable — because App Review opens every link in your listing and a dead privacy
policy URL is a routine rejection.

- Those requests go to **your own servers**, not to ours. We never learn the URLs, the
  result, or that a scan happened.
- The request carries the User-Agent `ShipCheck/0.1 (link checker)` and nothing else
  about you or your project.
- Whoever hosts those URLs will see the request in their own logs, the same as any
  other visitor.
- **`--offline` skips this entirely**, and the scan still runs.

---

## 2. Fetching Apple and Google policy text

ShipCheck ships with a cached copy of the Apple and Google policy corpus, so a normal
scan fetches nothing. When you run **`/shipcheck:refresh`**, `scripts/fetch_corpus.py`
downloads the public policy pages listed in `scripts/sources.py` — `developer.apple.com`,
`developer.android.com`, `support.google.com`, `play.google.com`, `docs.expo.dev` and
similar.

- These requests go **directly from your machine to Apple, Google and Expo.** They do
  not pass through any Baker Ventures server, and we receive no record of them.
- Those sites can see what any web server sees: your IP address, the timestamp, the
  page requested, and a User-Agent string. For compatibility, the fetcher sends a
  standard desktop-browser User-Agent rather than identifying itself as ShipCheck, and
  it keeps session cookies only in memory for the duration of a single request.
- Nothing about your project is included in, or inferable from, these requests.
- If you never run `/shipcheck:refresh`, ShipCheck makes no policy-corpus requests at all.

---

## 3. The license check — the only data flow that reaches Baker Ventures

This section is the one that matters. If you use ShipCheck without a license key, skip
it: with no key on the machine, `scripts/license.py` returns "free" without making any
request at all.

### 3.1 What is sent

When a report is generated and a license key is present (in `~/.shipcheck/license` or
the `SHIPCHECK_LICENSE_KEY` environment variable), the plugin makes **one** HTTPS POST
to the validation endpoint. The complete request body is:

| Field | Value |
|---|---|
| `license_key` | The key you bought. |
| `plugin_version` | A version string, e.g. `0.2.11`. |
| `app_token` | Optional. `sha256(license_key + ":" + bundle_id)`, truncated to 32 hex characters, computed **on your machine**. Omitted when the project has no bundle identifier. |

That is the entire body. No project path, no repository name, no dependency list, no
store metadata, no findings, no score, no username, no machine identifier, no
hardware fingerprint.

The `app_token` exists so a $29 **single-app** license can be pinned to one app. It is
a hash: the server cannot recover your bundle identifier from it without already
knowing that bundle identifier. It is stable for a given (license, app) pair, which is
exactly what binding requires and the only thing it can be used for.

As with any HTTPS request, the transport itself carries your **source IP address**, the
**timestamp**, TLS connection metadata, and the User-Agent `ShipCheck/<version>`. We
list these because they are real, even though the application does not record them —
see §3.4.

### 3.2 What the server does with it

`server/validate.js` is a single Express route. On receiving a request it:

1. checks an in-memory cache for a recent verdict on that key;
2. if there is none, forwards **the license key alone** to Lemon Squeezy's license
   validation API (`api.lemonsqueezy.com`) using our API key, to confirm the key is
   real and active;
3. maps the returned product variant to a tier (`single`, `unlimited`, `agency`);
4. for a `single` tier only, records the `app_token` against that key so the license
   stays bound to one app;
5. answers `{valid, tier, bound_app}`.

The plugin version is received but is not used, stored, or logged.

### 3.3 What the server stores

| Store | Contents | Where | Retention |
|---|---|---|---|
| Verdict cache | License key → `{valid, tier, timestamp}` | Memory only | 7 days for a positive verdict, 10 minutes for a refusal; capped at 50,000 entries; **erased on every restart or redeploy** |
| Rate-limit counters | License key → recent request timestamps | Memory only | 60-second rolling window |
| App bindings | License key → list of `app_token` hashes, in `bindings.json` | Disk | **Indefinite.** There is no automatic expiry — see §7 for deletion |

`bindings.json` is the only durable record we keep. It contains license keys and opaque
hashes. It contains no bundle identifiers, no email addresses, no IP addresses, no
project data.

The `/health` route returns two aggregate numbers — how many verdicts are cached and how
many licenses have bindings. It returns no keys, tokens, or per-customer data.

### 3.4 What the server logs

The application writes **no request log**. It has no logging middleware. It prints to
standard error in exactly two situations: when the upstream Lemon Squeezy call fails,
and when writing `bindings.json` fails. Both lines contain only an error message — never
your license key, your `app_token`, or your IP address.

**What we cannot fully determine, and will not guess:** the hosting provider keeps its
own HTTP access logs, outside the application's control. The deployment blueprint in
`render.yaml` targets **Render**, whose platform logging typically records source IP,
request path, status code, timestamp and User-Agent, with retention set by Render's own
policy and plan. We do not control the contents or the retention period of those logs
and we are not going to state a figure we cannot verify. If you need that answered
precisely, email us and we will check the provider's current policy and tell you what we
find.

### 3.5 Fail-open, and why it is a privacy fact and not just an uptime one

The client treats **only** a well-formed, explicit `{"valid": false}` as a reason to
downgrade you to the free tier. A timeout, a DNS failure, a 5xx, a rate-limit response,
an unreachable host, a captive portal, or any malformed reply all cause ShipCheck to
**fail open** and treat you as fully licensed.

The practical consequence: **you can block the validation endpoint at your firewall and
ShipCheck keeps working at full tier.** No license data will reach us, and nothing will
break. A positive verdict is also cached locally for 7 days, so a licensed user's
machine contacts us at most about once a week per license-and-app pair, not on every
scan.

### 3.6 Current deployment status

As of the date at the top of this page, the default endpoint
`https://api.shipcheck.dev/validate` **does not resolve in DNS and the validation server
is not deployed.** Every license check therefore fails open, and **no license data
currently reaches any Baker Ventures server at all.** Sections 3.1–3.5 describe what the
server receives and stores once it is deployed, so that the description is on record
before any data flows rather than after. The date at the top of this page will be
updated when that changes.

---

## 4. Purchases

ShipCheck licenses are sold through **Lemon Squeezy**, acting as merchant of record.
When you buy a license you give Lemon Squeezy your name, email address, payment details
and the tax-location information they are required to collect. **We never see or handle
your card details.**

From Lemon Squeezy's dashboard we can see your order: the license key, your email
address and the product bought. We use that only to deliver the license, to answer
support email, and to honour refunds. Lemon Squeezy's own privacy policy governs their
processing and their retention, including records they must keep for tax purposes.

---

## 5. Third parties — the complete list

| Party | What they get | Why |
|---|---|---|
| **Lemon Squeezy** | Your purchase details directly from you at checkout; your license key from our server at each validation | License issuance, payment processing, license validation |
| **Our hosting provider** (Render, per `render.yaml`) | The validation request in transit, plus their own platform access logs (§3.4) | Running the validation endpoint |
| **GitHub** | Your IP address when you install the plugin from the repository or view the docs site on GitHub Pages | Distribution and documentation hosting |
| **Cloudflare** | Your IP address when you visit `shipcheck.bakerventuresstudio.com` | CDN/DNS for the marketing site |
| **Google Fonts** (`fonts.googleapis.com`) | Your IP address when you view a page on the documentation site | Web fonts on the site only — **the plugin itself loads nothing from Google** |

These providers process this data to provide their service to us, under their own terms.
We do not authorise them to use it for any other purpose.

**There are no other third parties.** No analytics (no PostHog, Google Analytics,
Plausible, or anything else), no error tracking (no Sentry), no advertising or
attribution SDKs, no data brokers, no session recording. We do not sell your data, share
it for advertising, or combine it with data from other sources. There is nothing to sell:
the durable record we hold is a license key and a list of hashes.

---

## 6. CI and the GitHub Action

The ShipCheck GitHub Action runs the same scanner inside **your** runner. The report is
written into your workspace and stays in your CI. If you supply a license key as a repo
secret, the license check described in §3 runs from your runner's IP address instead of
your laptop's; nothing else changes. Whatever your CI provider logs about your own jobs
is governed by their policy, not this one.

---

## 7. Retention, deletion, and how to revoke

| Data | Where it lives | How long | How to get rid of it |
|---|---|---|---|
| Your license key | `~/.shipcheck/license` on your machine (mode `600`) | Until you delete it | `rm ~/.shipcheck/license` |
| Cached verdicts | `~/.shipcheck/cache.json` on your machine (mode `600`) | 7 days positive / 10 minutes negative | `python3 scripts/license.py --clear-cache`, or just delete the file |
| Server verdict cache | Our server's memory | ≤ 7 days, and erased on restart | Expires by itself |
| App bindings | `bindings.json` on our server | Indefinite | **Email us** — see below |
| Hosting access logs | Our hosting provider | Set by the provider; not determined by us (§3.4) | Ask us and we will check |
| Purchase records | Lemon Squeezy | Their policy plus their tax-record obligations | Request via Lemon Squeezy; we will support the request |

**To stop all outbound traffic, in order of bluntness:**

1. Run scans with `--offline` and do not run `/shipcheck:refresh`. Nothing leaves the
   machine at all.
2. `rm -rf ~/.shipcheck` — removes your key and cache. With no key, the plugin makes no
   license request; it reverts to the free tier.
3. Block `api.shipcheck.dev` at your firewall. ShipCheck fails open and keeps working at
   full tier (§3.5).
4. Uninstall the plugin. Nothing of ours remains on the machine except files you can
   delete yourself: `~/.shipcheck/` and any `shipcheck-report.md` you generated.

**To have the record on our side deleted, or to ask what we hold about you:** email
**rsb.baker+shipcheck@gmail.com** from the address on your order, or include your license
key. We will delete the license's entry from `bindings.json` and confirm. Note that
deleting a binding frees a single-app license to bind to a different app; it does not
cancel or refund the license. If you want the purchase record removed as well, say so and
we will pass the request to Lemon Squeezy, who hold it.

---

## 8. Other disclosures

**Children.** ShipCheck is a developer tool, not directed at children, and we do not
knowingly collect data from anyone under 13.

**Sensitive data.** We do not collect, and the product has no use for, health data,
precise location, biometric data, contacts, or any special-category personal data.

**International.** Our validation endpoint and our providers are based in the United
States, so a license check is processed in the US. If you are in the EEA or UK, our
lawful bases are performance of a contract (validating the license you bought) and
legitimate interests (rate limiting, to stop a leaked key being abused). You may ask us
for access to, correction of, or deletion of what we hold, using the email address above.

**Security.** The local verdict cache is written mode `600` by the code itself, and
`/shipcheck:unlock` creates the license file mode `600` as well. The license
check and the upstream Lemon Squeezy call are HTTPS. Our Lemon Squeezy API key lives in
the server's environment and is never sent to a client.

**Changes.** Material changes get a new date at the top of this page. Because this file
lives in the public repository, every revision and its diff are visible in the ShipCheck
commit history — you never have to take our word for what changed.

---

## Contact

**Baker Ventures LLC** — **rsb.baker+shipcheck@gmail.com**

This page describes the behaviour of the code in this repository. If you find a
discrepancy between what it says and what the code does, that is a bug in one of them and
we want to hear about it.
