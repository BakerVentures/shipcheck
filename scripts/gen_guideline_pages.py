#!/usr/bin/env python3
"""Generate docs/guidelines/*.html -- SEO explainer pages for individual
guideline clauses, built from the corpus this repo already fetches and
verifies, not hand-typed.

Every quote here is read off disk from corpus/, the same source report.py
reads for citations in an actual scan -- so a claim on these pages is
provably the same text ShipCheck cites in a real report, not separately
maintained marketing copy that can drift from what the tool actually checks.

Run this after /shipcheck:refresh (or scripts/fetch_corpus.py) so the pages
reflect whatever the corpus currently says, not a snapshot from whenever
this script was first run.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "corpus")
OUT = os.path.join(ROOT, "docs", "guidelines")

with open(os.path.join(CORPUS, "manifest.json"), encoding="utf-8") as f:
    MANIFEST = json.load(f)
FETCHED = MANIFEST["generated_at"][:10]


def read(rel):
    with open(os.path.join(CORPUS, rel), encoding="utf-8") as f:
        raw = f.read()
    body = re.sub(r"<!--.*?-->", "", raw, count=1, flags=re.S).strip()
    return body


_MD_TOKEN_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*")


def _inline_md(text):
    """Render the corpus's own markdown links/bold as real HTML, escaping
    everything else -- corpus quotes came out of htmlmd.py's markdown
    renderer (e.g. "you must also [offer account deletion within the
    app](/support/...)"), and a plain html.escape() on the whole string was
    printing that markup literally instead of a working link."""
    out, last = [], 0
    for m in _MD_TOKEN_RE.finditer(text):
        out.append(html.escape(text[last:m.start()]))
        if m.group(1) is not None:
            label, href = m.group(1), m.group(2)
            # every relative link seen in the quoted clauses is Apple's own
            # site (/support/, /design/, /app-store/, /documentation/); if a
            # future page quotes a Google source with a relative link this
            # will need a per-source base instead of a single hardcoded one.
            href = href if re.match(r"^https?://", href) else \
                "https://developer.apple.com" + href if href.startswith("/") else href
            out.append('<a href="%s">%s</a>' % (html.escape(href, quote=True),
                                                  html.escape(label)))
        else:
            out.append("<strong>%s</strong>" % html.escape(m.group(3)))
        last = m.end()
    out.append(html.escape(text[last:]))
    return "".join(out)


def para_html(text):
    """corpus markdown -> simple HTML paragraphs/lists, escaping real content."""
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    out = []
    for b in blocks:
        lines = b.splitlines()
        if all(re.match(r"^[-*]\s+", l) or not l.strip() for l in lines) and \
           any(re.match(r"^[-*]\s+", l) for l in lines):
            items = [re.sub(r"^[-*]\s+", "", l) for l in lines if l.strip()]
            out.append("<ul>" + "".join(
                "<li>%s</li>" % _inline_md(i) for i in items) + "</ul>")
        else:
            out.append("<p>%s</p>" % _inline_md(b).replace("\n", " "))
    return "\n".join(out)


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://bakerventures.github.io/shipcheck/guidelines/{slug}.html">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://bakerventures.github.io/shipcheck/assets/og-card.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#EDF0F3;--ink:#1B2430;--muted:#5A6573;--line:#CBD3DB;--red:#B8122A;--amber:#9A6200;--green:#1F6B45;--panel:#FFFFFF;--code:#141A21;--codeink:#DCE3EA}}
*{{box-sizing:border-box}}
html{{background:var(--bg);color:var(--ink);font:16px/1.6 "IBM Plex Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
body{{margin:0}}
a{{color:var(--red)}}
.wrap{{max-width:720px;margin:0 auto;padding:0 20px 64px}}
header{{padding:28px 0 8px;display:flex;justify-content:space-between;align-items:baseline}}
header .brand{{font-weight:600;letter-spacing:-.01em;text-decoration:none;color:var(--ink)}}
header nav a{{margin-left:20px;color:var(--muted);text-decoration:none;font-size:14px}}
.eyebrow{{font:600 13px "IBM Plex Mono",monospace;color:var(--red);letter-spacing:.04em;margin:40px 0 8px}}
h1{{font-size:clamp(26px,4.5vw,38px);line-height:1.15;letter-spacing:-.02em;font-weight:600;margin:0 0 18px}}
.lede{{font-size:18px;color:var(--muted);margin:0 0 28px}}
.quote{{background:var(--code);color:var(--codeink);border-radius:8px;padding:22px 24px;font:14px/1.7 "IBM Plex Mono",ui-monospace,monospace;margin:0 0 28px}}
.quote .clause{{color:#8FA3B5;display:block;margin-bottom:10px;font-weight:500}}
.quote a{{color:#F2C14E}}
.quote ul{{margin:8px 0 0;padding-left:20px}}
h2{{font-size:20px;letter-spacing:-.01em;font-weight:600;margin:36px 0 12px}}
p{{margin:0 0 14px;max-width:640px}}
ul{{margin:0 0 14px;padding-left:22px}}
li{{margin:0 0 8px}}
code{{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:1px 6px;font:13px "IBM Plex Mono",monospace}}
.fixbox{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px 20px;margin:0 0 20px}}
.fixbox .label{{font:600 12px "IBM Plex Mono",monospace;color:var(--green);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;display:block}}
.cta{{background:var(--ink);color:#fff;border-radius:10px;padding:26px 28px;margin:44px 0 20px}}
.cta h2{{color:#fff;margin-top:0}}
.cta p{{color:#B9C2CC}}
.cta code{{background:#0F151B;border-color:#2B3642;color:#DCE3EA}}
.source{{color:var(--muted);font-size:13px;margin-top:8px}}
footer{{color:var(--muted);font-size:13px;padding:24px 0 0;border-top:1px solid var(--line);margin-top:40px}}
footer a{{color:var(--muted)}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="brand" href="../">shipcheck</a>
  <nav><a href="../#checks">What it checks</a><a href="../#pricing">Pricing</a><a href="https://github.com/BakerVentures/shipcheck">GitHub</a></nav>
</header>
"""

FOOT = """
<footer>
  Guideline text quoted from {source_label}, fetched {fetched} and cached with a SHA-256 in
  <a href="https://github.com/BakerVentures/shipcheck/blob/master/corpus/manifest.json">corpus/manifest.json</a> --
  the same corpus <a href="https://github.com/BakerVentures/shipcheck">ShipCheck</a> cites in a real scan, not separately maintained copy.
  Not affiliated with Apple Inc. or Google LLC. This page is not a guarantee of approval.
</footer>
</div>
</body>
</html>
"""


def render(page):
    quote_html = para_html(page["quote"])
    body_html = "\n".join(
        "<h2>%s</h2>\n%s" % (html.escape(h), para_html(t))
        for h, t in page["sections"]
    )
    fix_html = "".join(
        '<div class="fixbox"><span class="label">%s</span>%s</div>'
        % (html.escape(label), para_html(text))
        for label, text in page["fixes"]
    )
    cta = page.get("cta_findings", "shipcheck scan")
    return HEAD.format(
        title=html.escape(page["title"]),
        description=html.escape(page["description"]),
        slug=page["slug"],
    ) + """
<div class="eyebrow">{eyebrow}</div>
<h1>{h1}</h1>
<p class="lede">{lede}</p>

<div class="quote">
  <span class="clause">{clause_label}</span>
  {quote_html}
</div>

{body_html}

<h2>The fix</h2>
{fix_html}

<div class="cta">
  <h2>ShipCheck catches this before you submit</h2>
  <p>A Claude Code plugin for React Native and Expo. Reads your project and store listing, checks them against the live App Store Review Guidelines and Google Play policies -- the same corpus quoted on this page -- and tells you the clause, the reviewer's likely wording, and the fix.</p>
  <code>/plugin marketplace add BakerVentures/shipcheck</code>
  <p class="source">Free scan on every app. <a href="../#pricing" style="color:#F2C14E">See pricing &rarr;</a></p>
</div>
""".format(
        eyebrow=html.escape(page["eyebrow"]),
        h1=html.escape(page["h1"]),
        lede=html.escape(page["lede"]),
        clause_label=html.escape(page["clause_label"]),
        quote_html=quote_html,
        body_html=body_html,
        fix_html=fix_html,
    ) + FOOT.format(source_label=html.escape(page["source_label"]), fetched=FETCHED)


PAGES = []

PAGES.append(dict(
    slug="5-1-1-v-account-deletion",
    eyebrow="APP STORE GUIDELINE 5.1.1(v)",
    title="Guideline 5.1.1(v): Account Deletion — What Apple Actually Requires (2026)",
    description="Apple's exact wording for guideline 5.1.1(v) account deletion, what counts as compliant, and the fix for React Native and Expo apps.",
    h1="Guideline 5.1.1(v): account deletion",
    lede="If your app supports creating an account, App Review checks that users can delete it "
         "from inside the app -- not just sign out, not just deactivate.",
    clause_label="5.1.1(v) Account Sign-In — App Store Review Guidelines",
    quote=read("apple/asrg.sections/5.1.1v.md"),
    source_label="App Store Review Guidelines, 5.1.1(v)",
    sections=[
        ("What counts as compliant, per Apple's own account-deletion guidance",
         read("apple/account-deletion.md").split("## Frequently")[0].split("## Account deletion guidance")[1]),
        ("Why React Native and Expo apps miss this specifically",
         "Auth is usually wired through Supabase, Firebase Auth, or Clerk, and the SDK "
         "ships a `signOut()` method that's easy to mistake for account deletion in a quick "
         "implementation. `signOut()` clears the local session; the account record and its "
         "data are untouched on the server. A reviewer testing this will sign back in with "
         "the same credentials and find the account still exists -- that's the rejection, "
         "every time.\n\n"
         "If your app also offers a subscription, the deletion flow needs to say what happens "
         "to billing: Apple's own account-deletion guidance calls this out directly, and "
         "`5.1.1(v)`'s neighboring `3.1.2` covers the subscription-disclosure side of the same "
         "screen."),
    ],
    fixes=[
        ("iOS + Android (Supabase example)",
         "Add a server-side delete path that removes the auth user and owned rows -- most auth "
         "providers' client SDKs deliberately can't delete a user themselves (that needs a "
         "service-role key), so this has to be a server function, not a client call. Then wire "
         "a \"Delete Account\" control in Settings that calls it, shows a confirmation naming "
         "what gets deleted, and if the app has a subscription, tells the user how billing is "
         "affected before they confirm."),
        ("Google Play needs one more thing Apple doesn't",
         "Play requires the in-app path *and* a web-accessible account-deletion URL, submitted "
         "separately in Play Console. An iOS-first team that ships the in-app flow and stops "
         "there passes Apple and fails the Play Data safety review."),
    ],
))

PAGES.append(dict(
    slug="3-1-2-subscription-disclosure",
    eyebrow="APP STORE GUIDELINE 3.1.2",
    title="Guideline 3.1.2: Subscription Disclosure on Your Paywall (2026)",
    description="What Apple's guideline 3.1.2(c) requires on a paywall screen before purchase, quoted directly, plus the exact fix for React Native paywalls.",
    h1="Guideline 3.1.2(c): what your paywall has to show before the buy button",
    lede="\"Add subscription terms\" is the reviewer's note. Here's exactly what that means, "
         "quoted from the guideline itself.",
    clause_label="3.1.2(c) Subscription Information — App Store Review Guidelines",
    quote=read("apple/asrg.sections/3.1.2c.md"),
    source_label="App Store Review Guidelines, 3.1.2(c)",
    sections=[
        ("What has to be on screen, not behind a link",
         "Price, billing period, and what auto-renewal means -- visible before the purchase "
         "button is tapped, not on a separate terms page the user has to navigate to. In "
         "practice, App Review wants to see something close to: the plan name, the price and "
         "period (\"$4.99/month\" or \"$39.99/year\"), a plain sentence that it renews "
         "automatically until cancelled, and working links to your Terms of Use and Privacy "
         "Policy on the same screen."),
        ("The most common way RN/Expo apps get this wrong",
         "A paywall built from a design mock rather than from the guideline text: a price, a "
         "\"Start Free Trial\" button, and nothing else. RevenueCat's own prebuilt paywall "
         "templates include the disclosure by default; a hand-rolled paywall component usually "
         "doesn't, because nothing in the UI design process flags it as required. It's a "
         "compliance requirement, not a design preference, and reviewers check for it "
         "specifically."),
    ],
    fixes=[
        ("Put this directly on the paywall screen, above or right below the CTA",
         "Pro Monthly — $4.99/month. Renews automatically until cancelled. "
         "Cancel anytime in Settings. Then Terms of Use and Privacy Policy as tappable links "
         "on the same screen, and a visible Restore Purchases control (guideline 3.1.1, checked "
         "separately, but almost always missing alongside 3.1.2)."),
    ],
))

PAGES.append(dict(
    slug="4-8-sign-in-with-apple",
    eyebrow="APP STORE GUIDELINE 4.8",
    title="Guideline 4.8: When You Need Sign in with Apple (2026)",
    description="Apple's exact requirement for guideline 4.8 login services, the real exemptions, and the fix for Google/Facebook login in React Native apps.",
    h1="Guideline 4.8: do you actually need Sign in with Apple?",
    lede="If your app offers Google or Facebook login for the primary account, Apple requires "
         "an equivalent privacy-preserving option -- with real, specific exemptions most "
         "developers don't know exist.",
    clause_label="4.8 Login Services — App Store Review Guidelines",
    quote=read("apple/asrg.sections/4.8.md"),
    source_label="App Store Review Guidelines, 4.8",
    sections=[
        ("The exemptions, verbatim from the guideline",
         "Another login service is not required if: your app exclusively uses your own "
         "company's account system; it's an education, enterprise, or business app requiring "
         "an existing institutional account; it uses a government or industry-backed citizen "
         "ID; or it's a client for a specific third-party service where users sign in to that "
         "service's own account directly. Most consumer apps with Google/Facebook login as a "
         "convenience option don't qualify for any of these."),
        ("Why this specifically hits Expo apps",
         "`@react-native-google-signin/google-signin` and `react-native-fbsdk-next` are common, "
         "well-documented, easy to add. `expo-apple-authentication` is one more package, one "
         "more entitlement, and easy to defer to \"later.\" The guideline doesn't care that it "
         "was added second -- if Google or Facebook sets up the primary account and there's no "
         "Apple option, it's a 4.8 rejection on the first review, every time."),
    ],
    fixes=[
        ("Add expo-apple-authentication",
         "`npx expo install expo-apple-authentication`, render an `AppleAuthenticationButton` "
         "alongside the other login options, and set `expo.ios.usesAppleSignIn: true` in "
         "app.json to enable the capability. That's the whole fix for most apps -- the "
         "guideline requires parity, not that Apple be the only or the default option."),
    ],
))

PAGES.append(dict(
    slug="itms-91053-privacy-manifest",
    eyebrow="ITMS-91053 · REQUIRED-REASON API",
    title="ITMS-91053: Privacy Manifest Missing Required-Reason API Declaration (2026)",
    description="What ITMS-91053 means, why it's the most common Expo App Store upload rejection, and the exact reason code to add to fix it.",
    h1="ITMS-91053: privacy manifest doesn't declare required-reason API",
    lede="This one blocks the upload itself, before a human reviewer ever sees the app -- and "
         "it's the single most common upload-time rejection in Expo projects.",
    clause_label="Apple Developer Documentation — Describing use of required reason API",
    quote=read("apple/required-reason-api.md").split("## See Also")[0].split("## Overview")[1] if "## Overview" in read("apple/required-reason-api.md") else read("apple/required-reason-api.md")[:900],
    source_label="Apple Developer Documentation, required-reason API",
    sections=[
        ("Why Expo apps trip this without writing any native code",
         "`expo-file-system`, `expo-device`, `expo-constants`, and "
         "`@react-native-async-storage/async-storage` are near-universal in Expo apps, and each "
         "touches an API in Apple's required-reason list -- reading file timestamps, disk "
         "space, system boot time, or UserDefaults. Since 1 May 2024, App Store Connect rejects "
         "the upload outright if your app's own `PrivacyInfo.xcprivacy` doesn't declare the "
         "categories your code (or a linked SDK's code) actually uses."),
        ("The rule that trips people up: SDKs declare their own use",
         "A package that ships its own `PrivacyInfo.xcprivacy` -- most current versions of "
         "`expo-device`, `expo-file-system`, and `@react-native-async-storage/async-storage` do "
         "-- has already declared its own API use. Your app's manifest doesn't need to repeat "
         "it. What's actually missing is usually required-reason API touched by your app's own "
         "code, or by a dependency that hasn't shipped a manifest yet."),
    ],
    fixes=[
        ("Add the entry to your app's PrivacyInfo.xcprivacy",
         "In app.json: `expo.ios.privacyManifests` (Expo SDK 50+), or directly in "
         "`ios/<App>/PrivacyInfo.xcprivacy` for a bare project. Each entry needs "
         "`NSPrivacyAccessedAPIType` set to the category (e.g. "
         "`NSPrivacyAccessedAPICategoryFileTimestamp`) and an approved reason code in "
         "`NSPrivacyAccessedAPITypeReasons` -- for file timestamps, that's usually `C617.1`. "
         "The full, current code list is in Apple's own required-reason API documentation, "
         "since Apple revises it."),
    ],
))

PAGES.append(dict(
    slug="2-3-1-placeholder-metadata",
    eyebrow="APP STORE GUIDELINE 2.3.1",
    title="Guideline 2.3.1: Placeholder Text and Misleading Metadata (2026)",
    description="Apple's exact wording on guideline 2.3.1 accurate metadata, what counts as placeholder content, and how to check your listing before submitting.",
    h1="Guideline 2.3.1: placeholder text and misleading metadata",
    lede="Leftover \"Lorem ipsum,\" a TODO in What's New, or a screenshot showing a feature "
         "that's flagged off in this build -- all the same guideline, and one of the easiest "
         "rejections to avoid entirely.",
    clause_label="2.3.1 Accurate Metadata — App Store Review Guidelines",
    quote=read("apple/asrg.sections/2.3.1.md"),
    source_label="App Store Review Guidelines, 2.3.1",
    sections=[
        ("What reviewers actually check",
         "Every text field in App Store Connect -- description, What's New, keywords, review "
         "notes -- against what the build actually does, and every screenshot against what's "
         "reachable in the submitted binary. \"Generic descriptions will be rejected\" is in "
         "the guideline text itself for the Notes for Review field specifically: a reviewer who "
         "hits a login wall with review notes that just say \"nothing special\" can't verify "
         "the app at all."),
        ("The RN/Expo-specific version of this",
         "Marketing screenshots generated before a feature was cut, or before it was put behind "
         "a flag for a phased rollout. The screenshot shows the feature; the shipped build "
         "doesn't have it reachable. It reads to a reviewer exactly like a fabricated listing, "
         "even when the omission was entirely accidental."),
    ],
    fixes=[
        ("Before submitting, check three things against the actual build",
         "Every screenshot description matches something a reviewer can actually reach in this "
         "specific build. The What's New and description have no leftover template text -- "
         "search for \"lorem,\" \"TODO,\" \"placeholder,\" and \"coming soon\" specifically, "
         "since those are the most common leftovers. And the review notes describe, "
         "specifically, any feature gated behind a flag, a subscription, or a login -- generic "
         "notes are named in the guideline as a rejection reason, not just a best practice."),
    ],
))

PAGES.append(dict(
    slug="google-play-target-api-level",
    eyebrow="GOOGLE PLAY · TARGET API LEVEL",
    title="Google Play Target API Level Requirement (2026): Current Floor and Deadline",
    description="Google Play's current target API level requirement for new apps and updates, quoted directly, with the deadline and the fix for React Native / Expo.",
    h1="Google Play's target API level requirement, as of {fetched}".format(fetched=FETCHED),
    lede="This floor moves roughly once a year and Google enforces it at the Play Console "
         "upload step -- get it wrong and the release is blocked before any review happens.",
    clause_label="Target API level requirements — Play Console Help",
    quote=read("google/target-api-level.sections/app-update-requirements.md"),
    source_label="Play Console Help, target API level requirements",
    sections=[
        ("Why this number is dangerous to memorize",
         "It moves. The table above is quoted live from Google's own page, fetched "
         "{fetched} and re-fetched weekly by ShipCheck's corpus refresh -- not typed in by "
         "hand once and left to go stale. A blog post or Stack Overflow answer citing \"the "
         "current requirement\" is very often citing last year's number.".format(fetched=FETCHED)),
        ("The Expo-specific fix",
         "`targetSdkVersion` lives in `android/build.gradle` for a bare or prebuilt project. In "
         "a managed Expo project without a checked-in `android/` directory, set it via the "
         "`expo-build-properties` config plugin instead -- editing `android/build.gradle` "
         "directly gets silently overwritten on the next `expo prebuild`."),
    ],
    fixes=[
        ("In android/build.gradle",
         "Set `targetSdkVersion` to the current floor for new apps shown in the table above. "
         "If you're on a managed Expo workflow, do this through `expo-build-properties` in "
         "app.json instead, and rebuild."),
    ],
))

os.makedirs(OUT, exist_ok=True)
index_links = []
for page in PAGES:
    out_path = os.path.join(OUT, page["slug"] + ".html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(page))
    index_links.append((page["slug"], page["h1"], page["description"]))
    print("wrote", out_path)

print("\n%d pages written" % len(PAGES))
with open(os.path.join(OUT, "_index_data.json"), "w", encoding="utf-8") as f:
    json.dump(index_links, f, indent=2)

INDEX_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>App Store & Play Guideline Explainers — ShipCheck</title>
<meta name="description" content="Plain-English explainers for the App Store and Google Play guidelines ShipCheck checks, each quoting the policy text verbatim from the same corpus ShipCheck cites in a real scan.">
<link rel="canonical" href="https://bakerventures.github.io/shipcheck/guidelines/">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#EDF0F3;--ink:#1B2430;--muted:#5A6573;--line:#CBD3DB;--red:#B8122A;--panel:#FFFFFF}
*{box-sizing:border-box}
html{background:var(--bg);color:var(--ink);font:16px/1.6 "IBM Plex Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
body{margin:0}
a{color:var(--red)}
.wrap{max-width:720px;margin:0 auto;padding:0 20px 64px}
header{padding:28px 0 8px;display:flex;justify-content:space-between;align-items:baseline}
header .brand{font-weight:600;letter-spacing:-.01em;text-decoration:none;color:var(--ink)}
header nav a{margin-left:20px;color:var(--muted);text-decoration:none;font-size:14px}
h1{font-size:clamp(26px,4.5vw,38px);line-height:1.15;letter-spacing:-.02em;font-weight:600;margin:40px 0 12px}
.lede{font-size:18px;color:var(--muted);margin:0 0 36px;max-width:620px}
.list{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.list li{border-bottom:1px solid var(--line);padding:20px 0}
.list a{display:block;text-decoration:none;color:var(--ink);font-weight:600;font-size:17px;margin-bottom:6px}
.list a:hover{color:var(--red)}
.list p{margin:0;color:var(--muted);font-size:15px;max-width:600px}
footer{color:var(--muted);font-size:13px;padding:24px 0 0;border-top:1px solid var(--line);margin-top:20px}
footer a{color:var(--muted)}
</style>
</head>
<body>
<div class="wrap">
<header>
  <a class="brand" href="../">shipcheck</a>
  <nav><a href="../#checks">What it checks</a><a href="../#pricing">Pricing</a><a href="https://github.com/BakerVentures/shipcheck">GitHub</a></nav>
</header>

<h1>Guideline explainers</h1>
<p class="lede">Plain-English breakdowns of the App Store and Google Play rules ShipCheck checks -- each one quotes the policy text verbatim from the corpus ShipCheck actually fetches, not separately maintained copy.</p>

<ul class="list">
__ITEMS__
</ul>

<footer>
  Quoted text is fetched and cached with a SHA-256 in <a href="https://github.com/BakerVentures/shipcheck/blob/master/corpus/manifest.json">corpus/manifest.json</a>.
  Not affiliated with Apple Inc. or Google LLC.
</footer>
</div>
</body>
</html>
"""


def render_index(links):
    items = "\n".join(
        '  <li><a href="%s.html">%s</a><p>%s</p></li>'
        % (slug, html.escape(h1), html.escape(desc))
        for slug, h1, desc in links
    )
    return INDEX_HEAD.replace("__ITEMS__", items)


with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(render_index(index_links))
print("wrote", os.path.join(OUT, "index.html"))

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://bakerventures.github.io/shipcheck/guidelines/</loc></url>
{entries}
</urlset>
"""


def render_sitemap(links):
    entries = "\n".join(
        "  <url><loc>https://bakerventures.github.io/shipcheck/guidelines/%s.html</loc></url>"
        % slug
        for slug, _, _ in links
    )
    return SITEMAP.format(entries=entries)


with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(render_sitemap(index_links))
print("wrote", os.path.join(OUT, "sitemap.xml"))
