---
name: refresh
description: Re-fetch the Apple and Google policy corpus and print a changelog of what policy text changed.
---

Re-fetch every policy page and report what moved.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_corpus.py" \
  --out "${CLAUDE_PLUGIN_DATA}/corpus" --diff
```

If `${CLAUDE_PLUGIN_DATA}` is not set, fall back to
`${CLAUDE_PLUGIN_ROOT}/corpus`.

Then summarise for the user, in this order:

1. Any source that **failed** to fetch — these are dead or moved URLs and are the
   most important thing on the screen, because a silently stale corpus is the
   one way this tool gives dangerous advice.
2. Sources whose text **changed**, with the added/removed/edited section anchors
   and a plain-language description of what actually changed. Be specific:
   "3.1.2(c) now also requires X" is useful, "3.1.2 changed" is not.
3. A one-line all-clear for everything unchanged.

If a clause the user has an open finding against has changed, say so explicitly
and recommend re-running `/shipcheck:scan`.
