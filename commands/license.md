---
name: license
description: Store or check your ShipCheck license key.
---

Manage the ShipCheck license.

If `$ARGUMENTS` contains a key, write it to `~/.shipcheck/license` (create the
directory, `chmod 600` the file), clear any cached validation in
`~/.shipcheck/cache.json`, then verify:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/license.py"
```

If `$ARGUMENTS` is empty, just run that command and report the current tier.

Tell the user what leaves their machine, because it is the product's privacy
guarantee and it is verifiable: only the license key and the plugin version are
sent, to a single validation endpoint. No project files, no dependency list, no
metadata, and no findings ever leave the machine. They can read
`scripts/license.py` — the function `_payload()` is the entire request body.

If validation fails because the endpoint is unreachable, ShipCheck fails open
and treats the license as valid. Say so; a paying user should never be blocked
by an outage.
