# Directory and awesome-list submissions

## Anthropic community plugin catalog
Form: linked from https://code.claude.com/docs/en/plugins (search the page for "community" and "submit"). Fields you'll need:

Name: shipcheck
One-line: Scan React Native/Expo apps against the live App Store and Google Play guidelines and get clause-cited fixes before you submit.
Category: Developer tools / Mobile
Repo: https://github.com/BakerVentures/shipcheck
Safety notes: read-only against the project; network calls limited to public Apple/Google policy pages and an optional license check sending key + version only. No project contents transmitted.

## Awesome-list PRs (one line each, follow each list's format)

travisvn/awesome-claude-skills:
- [shipcheck](https://github.com/BakerVentures/shipcheck) — App Store / Google Play rejection-risk scanner for React Native and Expo apps, checked against live guidelines.

hesreallyhim/awesome-claude-code -- DO NOT PR. Their CONTRIBUTING.md is explicit:
"Do not open a PR. Just fill out the form... It is not possible to submit a
resource recommendation using the `gh` CLI." Submit instead via their issue
form: https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml
Two more blockers to clear first, both stated in their own rules:
  - the resource must be 14+ days old with ongoing commits, OR have 100+ stars
    (this repo has neither yet -- wait, or come back once it does)
  - "if your project requires any form of signup or payment, this is a
    blocker for reviewing it" -- shipcheck's paid tier makes this a real
    obstacle, not just a formality. Worth reading their full CONTRIBUTING.md
    before deciding whether to submit at all.

Also submit at: claudemarketplaces.com, claudeskills.info, awesomeclaude.ai, agentskill.club, mcpmarket.com.
Checked these directly rather than trusting "paste-the-URL form" -- that
assumption didn't hold:
  - claudemarketplaces.com: no visible submission form without logging in
    (Login is the only path found).
  - claudeskills.info: /submit redirects straight to a Google OAuth consent
    screen asking to grant the site access to your real Google account.
    Not something to click through casually -- decide deliberately whether
    you want claudeskills.info to have that grant before doing this one.
  - agentskill.club: says it "automatically discovers and synchronizes GitHub
    repositories daily" -- may index shipcheck without any manual submission
    at all, given it's a public, well-structured repo already. No submission
    link found in a quick pass; worth checking back in a week before trying
    to force a manual submit.
  - mcpmarket.com: not checked. shipcheck is a Claude Code plugin (skills +
    commands + scripts), not an MCP server -- this directory's category may
    not even apply.
  - awesomeclaude.ai: not checked.

## GitHub repo settings
Topics: claude-code, claude-code-plugin, app-store, app-review, expo, react-native, ios, google-play, aso
About: Catch App Store and Google Play rejections before you submit. Claude Code plugin for React Native and Expo.
Website: your GitHub Pages URL
(Already set on the live repo -- verified 2026-09-04.)

## claude-plugins-community (Anthropic's official community catalog)
Researched 2026-09-04. This is the real, lowest-friction submission path found so
far -- no OAuth grant to a third party, no new account: it's a form at
platform.claude.com/plugins/submit gated behind your own existing Anthropic
Console login (the individual-author path; the claude.ai form is for Team/
Enterprise orgs instead). Approved plugins get pinned into
`anthropics/claude-plugins-community`'s `marketplace.json`, which syncs
nightly -- distinct from `claude-plugins-official`, which is Anthropic's
hand-picked list with no public application process at all.

I ran `claude plugin validate --strict .` and `claude plugin validate --strict
.claude-plugin/plugin.json` against this repo -- both pass, so the plugin
itself won't be the blocker if you submit.

**This step needs you**, not me: it's your Console login. Suggested content
for the form (matches what's already live in plugin.json/README.md, so it
won't drift):

- Name: shipcheck
- Display name: ShipCheck
- One-line: App Store / Google Play rejection-risk checker for React Native
  and Expo apps. Scans your project and store metadata, cites the exact
  guideline clause, and gives you the fix.
- Category: Developer tools / Mobile
- Repo: https://github.com/BakerVentures/shipcheck
- Homepage: https://bakerventures.github.io/shipcheck/
- Marketplace source: BakerVentures/shipcheck (this repo's own
  `.claude-plugin/marketplace.json` is already the install source used in the
  README's `/plugin marketplace add` instructions)
- Safety notes: read-only against the project; network calls limited to
  public Apple/Google policy pages and an optional license check sending key
  + version + an opaque per-app token only. No project contents transmitted.

Context on the wider ecosystem (why this matters less than it might seem):
the community + official marketplaces together hold 9,000+ plugins/skills as
of mid-2026 (4,000+ skills, 770+ MCP servers, 2,500+ third-party
marketplaces per one July 2026 estimate) -- a single new listing is easy to
get lost in. The guideline-explainer SEO pages under `docs/guidelines/`
(built and shipped 2026-09-04) are the more durable channel for the same
reason: organic search doesn't require getting noticed inside a crowded
directory. Treat this submission as free and worth doing, not as the primary
growth lever.

No dedicated Claude-Code-plugin-developer Discord or plugin-specific
newsletter/roundup was found in a research pass -- inconclusive rather than
ruled out, worth a second look later rather than assumed absent.
