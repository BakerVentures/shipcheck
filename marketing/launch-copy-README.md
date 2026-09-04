# Before you post any of this

`show-hn.md`, `x-thread.md`, and `product-hunt.md` came from the original
marketing kit drop, not from me, and I only just re-read them closely tonight.
Wording is now consistent with what actually shipped (pricing, "free scan on
every app" not "first scan," and the X thread points at the real
`docs/demo/*.gif` files instead of placeholders).

**One thing I have not verified and can't: all three posts open with a
first-person story — "I got rejected three times, once for a missing privacy
manifest, once for a paywall missing the renewal period, once for a
screenshot of a flagged feature."** I have no evidence this literally happened
to you. It reads as a plausible, well-constructed example the kit generated to
match shipcheck's own feature set, not a verified account of a real rejection.

Before you post any of these, do one of:
- **If it's true** (or close enough that you'd stand behind it if someone
  asked "which app, what did the rejection email actually say"), post it as
  written.
- **If it's not**, rewrite the opening with something you actually
  experienced, or drop the personal-anecdote framing and lead with the
  product directly. HN and Reddit in particular will ask follow-up questions
  a fabricated story can't survive, and it's the kind of thing that damages
  trust in everything else you say once it's caught.

I'm flagging this rather than silently leaving it, and rather than silently
rewriting it myself -- I don't know what actually happened to your apps, and
inventing a *different* fake story wouldn't fix the problem, it would just
move it.

**What I actually found, checking RizzMaxx's own docs (I have read access and
looked rather than guess):**

- Not the specific three-part story as drafted. The one build-processing
  rejection I found (1.0.2 build 35, ITMS-90186/90062) was a version-number
  mistake, not a content-guideline issue -- not usable here.
- But there IS a real one, in `docs/build-29-conversion-growth-plan.md:60`:
  *"Fake-discount copy got us rejected once; the price on the button must be
  real."* -- a genuine paywall-copy rejection, still fairly close to
  shipcheck's actual 3.1.2 checks (paywall discloses accurate terms).
- And extensive real evidence that 3.1.2 paywall disclosure is something your
  team has hardened against from hard experience: `flirtgym-1.0.3-cowork-prompt.md`
  has a full pre-submission checklist for exactly the things shipcheck checks
  (renewal terms in a sticky footer, Restore Purchases, dead legal links,
  account deletion reachable without an active subscription) with the comment
  "this is the App Store 3.1.2 rejection surface."

If you want a true opening line instead of the drafted one, the discount-copy
rejection is a real story you could tell in one or two sentences. I didn't
rewrite the drafts myself with it because I only have that one line of
context, not the full story the way you'd tell it.
