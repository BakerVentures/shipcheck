---
type: llm
weight: 1.5
---

`shipcheck.metadata.md` in the fixture project contains this in the
Description field: "Also available on Android and on our website." This is a
judgment finding no script can catch mechanically — it requires reading the
metadata and recognizing it violates guideline 2.3.10 (App Store Review
Guidelines: metadata should not reference other platforms).

Score 1 if the report flags this specific problem (referencing another
platform in the metadata), ideally citing guideline 2.3.10 or a nearby 2.3.x
clause. Score 0.5 if it's flagged but with no guideline citation or the wrong
clause family (e.g. citing a privacy clause instead of a metadata clause).
Score 0 if this specific issue is not mentioned at all.
