# Known limitation: this case cannot complete in the current eval sandbox

Four runs against this case (2026-09-03), summarized:

1. `max_turns: 25`, fixture scanned in place inside the plugin's own source
   tree -> hit the turn cap; the agent spent turns fighting the corpus-reading
   checklist in `SKILL.md` Step 2, which was genuinely too exhaustive. **Fixed**
   in `skills/shipcheck/SKILL.md` (triage from `facts` first, batch reads) --
   that fix stands regardless of the eval's outcome.
2. Same prompt, `max_turns: 45` -> hit the cap again; grading failed outright
   because the account's session usage limit was hit mid-grade (unrelated to
   the plugin).
3. Same prompt, limit cleared -> hit the cap again at 46 turns / $2.23. Trace
   showed the real cause: the plugin's own source tree (which the fixture
   lives inside, under `examples/`) is read-only in this sandbox, and the
   agent burned ~15 turns discovering that and improvising around it
   (`/dev/stdout`, `$TMPDIR`, permission probes) before Step 2 even started.
   Once past that, the corpus reads it made were well-scoped (3.1.2 variants,
   2.3.x, 4.8, 4.2, the matching category/testing files) -- confirms the Step
   2 fix works as intended.
4. Prompt updated to tell the agent to copy the fixture into its own writable
   cwd first -> `cp -R`, `mkdir`, and `touch` all failed silently or with a
   nonzero exit. The agent concluded "Bash is read-only in this sandbox" and
   switched to manually recreating every file with the `Write` tool one at a
   time (12+ synthetic node_modules stub files alone), burning the turn budget
   on file reconstruction instead of scanning.

None of the last three failures are shipcheck defects. A real user never hits
any of this: their project already exists, writable, on their own filesystem
-- there is no "copy a fixture into a sandbox" step in real usage. This is a
constraint of `claude plugin eval`'s early-access sandbox (Bash write access
appears to be denied entirely in this configuration) colliding with a plugin
that reads/writes an arbitrary project directory rather than only files inside
`${CLAUDE_PLUGIN_DATA}`.

**Before spending more budget re-running this case**, either:
- point it at a fixture outside the plugin's own repo (so "the plugin source
  is read-only" stops applying), or
- confirm whether `--allow-tools Bash` in a different eval build actually
  grants write access, since this session's behavior ("read-only Bash") wasn't
  documented anywhere I could find, or
- test manually instead: install the plugin for real (`/plugin marketplace add
  BakerVentures/shipcheck`) and run `/shipcheck:scan` against a real project in
  an ordinary Claude Code session, which has none of these sandbox
  restrictions. This is actually the higher-fidelity test for this product,
  since ShipCheck's whole job is reading/writing an arbitrary project
  directory that a sandboxed eval necessarily can't represent well.

Total spend chasing this case: ~$6.56 across 4 runs. The graders and prompt
are left in place for whoever wants to retry under different conditions.

## Real-world validation (outside the eval sandbox)

Ran the actual installed plugin in a genuine headless Claude Code session
(`claude -p "/shipcheck:scan"` with a scoped `--allowedTools`, not
`claude plugin eval`) against a plain writable copy of this fixture outside
the plugin's source tree -- no sandbox restrictions, because a real user's
project is never inside the plugin's own directory.

Result: 27 turns, $1.95, ~5 minutes. Completed cleanly, no permission
fighting, no wasted reads. Produced 52 findings (34 deterministic + 18
judgment), including two genuinely sharp catches neither I nor any prior pass
this session had noticed: `app/index.tsx` imports `expo-tracking-transparency`
which isn't in `package.json` (verified true -- Metro would fail to resolve
it), and the paywall button passes an undefined `pkg` variable to
`Purchases.purchasePackage()`. It correctly caught the 2.3.10
metadata-references-another-platform violation this eval case was designed to
test, with the right clause. Every citation checked was a real, verbatim
corpus quote. The "Likely to pass" section showed sophisticated conditional
reasoning (e.g. correctly exempting the Kids-category ad-SDK ban because the
declared category is Health & Fitness, while separately flagging that the
same SDK would be disqualifying if it were Kids) rather than generic
boilerplate.

This is the real signal the sandboxed eval case above couldn't produce. The
report it generated replaced the earlier, partly hand-simulated one at
`examples/bad-expo-app/shipcheck-report.md`.
