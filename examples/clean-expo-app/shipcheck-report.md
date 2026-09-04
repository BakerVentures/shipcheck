# ShipCheck report

**Clean App** · v1.0.0 · generated 2026-09-04 13:39

## Rejection risk: 0 / 100

**Nothing blocking found**

`[░░░░░░░░░░░░░░░░░░░░]` 0 critical · 0 high · 0 medium · 0 low

> Checked against policy text fetched 2026-09-04 from 37 official Apple and Google sources. Run `/shipcheck:refresh` to re-fetch and see what changed.

---

## Findings

Nothing found. See *Likely to pass* below for what was checked.

---

## Likely to pass

Checked and found clean, so you can trust the list above is the whole problem:

- ✅ **1024px icon has no alpha channel** *(ASC:screenshot-specifications)* — assets/icon.png (icon) is 1024x1024 with no transparency.
- ✅ **Export compliance key is set** *(ASC:export-compliance)* — ITSAppUsesNonExemptEncryption = False
- ✅ **Target API level meets Play's floor** *(play:target-api-level)* — android/build.gradle sets targetSdkVersion = 36, at or above the current floor of API 36.
- ✅ **No placeholder text in metadata** *(2.3.1)* — Checked 19 filled-in field(s) against common placeholder patterns (lorem ipsum, TODO, TBD, example.com, ...) -- none matched.

---

## Not checked

ShipCheck could not verify these. They are not passes:

- ⚠️ **Uninstalled dependencies** — These are in package.json but not under node_modules, so their privacy manifests could not be checked: react-native. Run a full install and re-scan.

---

<sub>ShipCheck v0.2.10 · free tier · findings are advisory: App Review outcomes are decided by Apple and Google, not by this tool.</sub>
