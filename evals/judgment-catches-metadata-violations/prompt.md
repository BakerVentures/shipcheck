---
max_turns: 30
allowed_tools: [Read, Glob, Grep, Bash, Write, Skill]
---

Copy `${CLAUDE_PLUGIN_ROOT}/examples/bad-expo-app` to `./bad-app` in your own
current directory (the plugin's own source tree is read-only, so work from
the copy, not the original). `cd` into `./bad-app`, then run a ShipCheck
rejection-risk scan on it, following the shipcheck skill. Produce
`shipcheck-report.md` there.
