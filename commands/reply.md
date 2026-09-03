---
name: reply
description: Draft a Resolution Center reply to an App Store or Play rejection, addressing the cited guideline.
---

**This command requires a paid licence.** Check first:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/license.py" --require-pro \
  --app-id "<bundle id from app.json, if you have it>"
```

If that exits non-zero, tell the user the reply drafter is a paid feature, show
them the one-line unlock (`/shipcheck:license <key>`, $29 one-time for this app
or $49/year for unlimited apps), and stop. Do not draft the reply anyway. Say it
once, plainly, without a sales pitch.

The user will paste the rejection message from App Store Connect Resolution
Center (or the Play Console policy notice). It may be in `$ARGUMENTS`; if not,
ask for it and wait.

Then:

1. **Identify the cited clause.** Pull the exact guideline number out of the
   rejection text. Read that clause from `corpus/` — do not rely on the
   reviewer's paraphrase and do not rely on memory.

2. **Work out what they actually want.** Reviewers cite a clause but reject for a
   specific observed behaviour. Separate the two. If the rejection is ambiguous,
   say which reading you are answering and note the other.

3. **Check whether it is fixed.** Look at the project. If `shipcheck-report.md`
   exists, cross-reference. Never draft a reply claiming a fix you cannot see in
   the code. If it is not fixed, say so and fix it first — sending a reply that
   claims an unmade change costs another full review cycle and damages the
   account's standing.

4. **Draft the reply.** The register that works with App Review is: brief,
   factual, specific, no arguing, no apologising at length, no marketing. State
   what was changed, where, and how the reviewer can verify it. Give exact
   navigation steps and demo credentials if a login is involved.

   Shape:
   - One sentence acknowledging the guideline.
   - What was changed, concretely, in the build being resubmitted.
   - Exactly how to see it: screen-by-screen navigation, credentials, test IAP.
   - If you disagree with the rejection: one short paragraph of factual
     clarification with a reference to the guideline text, and a request for
     clarification rather than a rebuttal.
   - A closing line requesting re-review.

   Keep it under 250 words. Reviewers read a lot of these.

5. Write it to `shipcheck-reply.md` and show it in chat so the user can edit
   before pasting.

Tell the user plainly whether they need a new build (most fixes) or whether the
reply alone can resolve it (metadata-only and misunderstanding cases).
