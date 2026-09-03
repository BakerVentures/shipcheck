---
name: license
description: Check ShipCheck license status (alias of /shipcheck:unlock).
---

Manage the ShipCheck license. Identical to `/shipcheck:unlock` — both names
exist because purchase receipts tell buyers to run `unlock`, while `license`
is the name people reach for when checking status.

If `$ARGUMENTS` contains a key, write it to `~/.shipcheck/license` (create the
directory, `chmod 600` the file), clear any cached validation in
`~/.shipcheck/cache.json`, then verify:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/license.py"
```

If `$ARGUMENTS` is empty, just run that command and report the current tier.

Pass `--app-id <bundle identifier>` when the project has one. Tiers:

| Tier | What it unlocks |
|---|---|
| `free` | risk score + the top 3 findings |
| `single` | $29 one-time, bound to **one** app, unlimited scans of it forever |
| `unlimited` | $49/year, any number of apps |
| `agency` | $149/year, any number of apps, shareable across a team |

A `single` licence binds to the first bundle id it sees. If the user hits
"already bound to another app", that is expected — they need the $49/year plan,
not a bug report.

Tell the user what leaves their machine, because it is the product's privacy
guarantee and it is verifiable: only the license key, the plugin version, and an
opaque per-app token are sent, to a single validation endpoint. That token is
`sha256(license_key + ":" + bundle_id)` — it lets a one-app licence bind to one
app without the server ever learning which app it is. No project files, no dependency list, no
metadata, and no findings ever leave the machine. They can read
`scripts/license.py` — the function `_payload()` is the entire request body.

If validation fails because the endpoint is unreachable, ShipCheck fails open
and treats the license as valid. Say so; a paying user should never be blocked
by an outage.
