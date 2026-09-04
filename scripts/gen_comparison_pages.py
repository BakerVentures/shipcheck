#!/usr/bin/env python3
"""Generate docs/guidelines/vs-*.html -- comparison pages built from
marketing/competitive-analysis.md, which documents an actual measured
head-to-head (both tools run against the same seeded-violation fixture),
not a marketing claim. Every specific finding quoted on this page traces
back to that file -- re-run the comparison in competitive-analysis.md and
update this generator's PAGES list if the numbers ever change, rather than
letting this page drift into an unverified claim.
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "guidelines")

# Import first, deliberately: this executes gen_guideline_pages.py's own
# top-level PAGES build immediately, regenerating the 8 guideline pages and
# a fresh (8-entry) _index_data.json/index.html/sitemap.xml before anything
# below runs. This script's own writes below then merge into that fresh
# state rather than racing it -- doing the import later would let its
# top-level side effect clobber the merged _index_data.json this script
# just wrote.
sys.path.insert(0, HERE)
import gen_guideline_pages as ggp  # noqa: E402

with open(os.path.join(ROOT, "corpus", "manifest.json"), encoding="utf-8") as f:
    MANIFEST = json.load(f)
FETCHED = MANIFEST["generated_at"][:10]

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
.wrap{{max-width:760px;margin:0 auto;padding:0 20px 64px}}
header{{padding:28px 0 8px;display:flex;justify-content:space-between;align-items:baseline}}
header .brand{{font-weight:600;letter-spacing:-.01em;text-decoration:none;color:var(--ink)}}
header nav a{{margin-left:20px;color:var(--muted);text-decoration:none;font-size:14px}}
.eyebrow{{font:600 13px "IBM Plex Mono",monospace;color:var(--red);letter-spacing:.04em;margin:40px 0 8px}}
h1{{font-size:clamp(26px,4.5vw,38px);line-height:1.15;letter-spacing:-.02em;font-weight:600;margin:0 0 18px}}
.lede{{font-size:18px;color:var(--muted);margin:0 0 28px;max-width:640px}}
h2{{font-size:20px;letter-spacing:-.01em;font-weight:600;margin:36px 0 12px}}
h3{{font-size:16px;font-weight:600;margin:24px 0 8px}}
p{{margin:0 0 14px;max-width:660px}}
ul{{margin:0 0 14px;padding-left:22px}}
li{{margin:0 0 8px}}
code{{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:1px 6px;font:13px "IBM Plex Mono",monospace}}
table{{width:100%;border-collapse:collapse;margin:0 0 20px;font-size:14px}}
th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font:600 12px "IBM Plex Mono",monospace;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}}
td.only{{font-weight:500}}
.tablewrap{{overflow-x:auto;margin:0 0 20px;-webkit-overflow-scrolling:touch}}
.honest{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--amber);border-radius:6px;padding:16px 20px;margin:0 0 20px}}
.honest .label{{font:600 12px "IBM Plex Mono",monospace;color:var(--amber);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px;display:block}}
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
  Every specific finding on this page traces back to
  <a href="https://github.com/BakerVentures/shipcheck/blob/master/marketing/competitive-analysis.md">marketing/competitive-analysis.md</a>
  in the shipcheck repo -- both tools run against the same seeded-violation fixture, findings recorded either way. Not affiliated with the tools named here.
</footer>
</div>
</body>
</html>
"""


def render(page):
    return HEAD.format(
        title=html.escape(page["title"]),
        description=html.escape(page["description"]),
        slug=page["slug"],
    ) + page["body"] + FOOT


PAGES = []

PAGES.append(dict(
    slug="vs-free-claude-code-checkers",
    title="ShipCheck vs. Free Claude Code App Store Checkers (2026)",
    description="A measured, honest comparison of ShipCheck against greenlight and other free Claude Code plugins that check App Store rejection risk -- both run against the same seeded-violation fixture.",
    body="""
<div class="eyebrow">MEASURED COMPARISON</div>
<h1>ShipCheck vs. the free Claude Code checkers</h1>
<p class="lede">There are at least six free tools in the same install surface as ShipCheck, and the strongest of them -- greenlight, from RevylAI -- has 2.4k stars and does more than ShipCheck in one specific area. This page is the actual data, not a marketing claim: both tools were run against the same real Expo app and the same seeded-violation fixture, and every finding below is what each one actually reported.</p>

<div class="honest">
  <span class="label">Read this first</span>
  An earlier version of our own go-to-market research assumed the free competition was thin -- "two free Claude-Code-native competitors." It wasn't. There are at least six, including one with 2.4k stars and a company behind it. We're leaving that mistake visible rather than quietly fixing the story, because the honest comparison below is a stronger pitch than the wrong one was.
</div>

<h2>What both tools catch</h2>
<p>Target API level, foreground service types, missing app privacy manifest, Sign in with Apple, <code>QUERY_ALL_PACKAGES</code>, background location, export compliance. If your app only has these problems, either tool will tell you -- and greenlight is free.</p>

<h2>What only ShipCheck catches</h2>
<div class="tablewrap">
<table>
<tr><th>Finding</th><th>Why it matters</th></tr>
<tr><td class="only">Missing <code>NSCameraUsageDescription</code> while the app calls <code>launchCameraAsync</code></td><td>iOS kills the app at the permission prompt. Guaranteed 2.1 rejection. greenlight misses it entirely.</td></tr>
<tr><td class="only">Missing <code>NSUserTrackingUsageDescription</code> with a Meta SDK present</td><td>greenlight detects the tracking SDK and prints it, but doesn't connect that to the missing key.</td></tr>
<tr><td class="only">Expo's own default purpose strings (<code>Allow $(PRODUCT_NAME) to&hellip;</code>)</td><td>the single most common 5.1.1 nit in Expo apps specifically.</td></tr>
<tr><td class="only">An SDK that ships no privacy manifest of its own</td><td>ITMS-91061 -- the upload is rejected before a human ever reviews it.</td></tr>
<tr><td class="only">Account deletion (5.1.1(v)) and Restore Purchases (3.1.1)</td><td>greenlight's own docs describe both rules; neither fired on a fixture that violates both. Its pattern matching doesn't reach into React Native source.</td></tr>
<tr><td class="only">Icon with an alpha channel, or not 1024&times;1024</td><td>blocks the upload outright.</td></tr>
<tr><td class="only">Dead privacy-policy and support URLs</td><td>greenlight never makes the request to check.</td></tr>
<tr><td class="only">Placeholder text, app name over 30 chars, missing demo account, keyword formatting</td><td>structural -- see below, this is the real gap.</td></tr>
<tr><td class="only"><code>developmentClient: true</code> left in the production EAS profile</td><td>Expo-specific; ships the dev menu into a release build.</td></tr>
<tr><td class="only">Prominent-disclosure requirement for runtime permissions</td><td>Play-specific, easy to miss.</td></tr>
</table>
</div>

<h2>The structural gap: greenlight can't read your store listing</h2>
<p>Not "doesn't yet" -- <em>can't</em>, in its current shape. It reads <code>app.json</code>, so the most it can say is "expo.description is empty." It never sees the actual description, keywords, What's New text, screenshot descriptions, review notes, demo account, age rating, or paywall copy you're about to paste into App Store Connect, because nothing in its design ever collects them.</p>
<p>Roughly half of App Store rejections live in exactly that material (guideline 2.3.x). <code>shipcheck.metadata.md</code> -- an unglamorous markdown file you fill in once -- is the actual moat, for three reasons: it's an input no code scanner has; judging it needs a model reading current guideline text, which offline bundled rules can't do; and in a Claude Code plugin, that model is the one you already have open, so it costs us nothing to run and costs you nothing extra to use.</p>

<h2>Where greenlight is honestly better</h2>
<ul>
  <li><strong>Binary analysis.</strong> It inspects the actual IPA/APK/AAB. ShipCheck doesn't.</li>
  <li><strong>Maturity and reach.</strong> Homebrew, Go, 2.4k stars, a company behind it.</li>
</ul>
<p>Both tools also had real false positives on the same real app until dogfooding caught them -- greenlight flagged a <code>comingSoon</code> UI badge and a stray <code>console.log</code> in a build script that never ships. ShipCheck had five false-positive classes of its own until <code>scripts/selftest.py</code> was written specifically to guard against them. Nobody gets to be smug about this; the difference is ours are now regression-tested against a real fixture on every push.</p>

<h2>What this actually means for pricing</h2>
<p>Charging for what six free tools already do isn't a business. Deterministic code and config scanning is table stakes now, and it's free everywhere, including in ShipCheck's own free scan. What's still worth paying for is the half none of the free tools can reach at all: store-listing judgment against the live guideline text, the fetched-and-hashed corpus that stays current on its own, and the Resolution Center reply drafter for when a rejection has already landed.</p>

<div class="cta">
  <h2>See what ShipCheck catches that the free tools don't</h2>
  <p>Free scan on every app -- the deterministic checks are the same ones every tool in this comparison runs, on the house. The judgment layer -- your store listing, the paywall, the guideline text current as of today -- is what's actually being sold.</p>
  <code>/plugin marketplace add BakerVentures/shipcheck</code>
  <p class="source"><a href="../#pricing" style="color:#F2C14E">See pricing &rarr;</a></p>
</div>
""",
))

os.makedirs(OUT, exist_ok=True)
for page in PAGES:
    out_path = os.path.join(OUT, page["slug"] + ".html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(page))
    print("wrote", out_path)
print("\n%d comparison page(s) written" % len(PAGES))

# Merge into the same index/sitemap gen_guideline_pages.py maintains, rather
# than keeping a second copy of that render logic -- run
# gen_guideline_pages.py again after this script if either page set changes,
# so the merged _index_data.json below reflects both.
index_path = os.path.join(OUT, "_index_data.json")
try:
    with open(index_path, encoding="utf-8") as f:
        index_links = json.load(f)
except (OSError, json.JSONDecodeError):
    index_links = []

known = {slug for slug, _, _ in index_links}
for page in PAGES:
    if page["slug"] not in known:
        index_links.append((page["slug"], page["title"], page["description"]))

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index_links, f, indent=2)
print("updated", index_path)

# Re-render index.html and sitemap.xml against the merged list, reusing
# gen_guideline_pages.py's own render functions (imported at the top of
# this file) rather than a second copy of that template.
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(ggp.render_index(index_links))
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(ggp.render_sitemap(index_links))
print("wrote", os.path.join(OUT, "index.html"), "and sitemap.xml (merged)")
