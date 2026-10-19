---
name: copy
description: Offer three plain rewrites of the headline, supporting text, button labels, or a section.
---

# /copy

Writes or rewrites visible text. Plain, specific, short. It changes only the text the user named.

## Triggers

- `/copy`: ask which part.
- `/copy headline`, `/copy buttons`, `/copy <section name>`.
- Called by `/new` (all hero text), `/edit` (copy category), `/section` (section text), and `/ref` (new copy for a reference-based build).

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `commands/copy/references/copy.md`, `commands/copy/references/rewrites.md`, `commands/copy/tokens/formulas.json` |
| Scripts | `core/scripts/audit.py` |
| Calls | none |
| Called by | `/edit`, `/new`, `/ref`, `/section` |
| Hands off to | none |
| Handed off from | `/audit` |
| Requires | none |
| State read | `scheme` |
| State written | `pages` |
<!-- wiring:end -->

## Steps

1. **Part.** If not stated, ask which part: headline, supporting sentence, buttons, or a named section (`ask_user_input_v0`).
2. **Facts first.** Gather what is true about the subject from the page and conversation. Do not invent statistics, awards, prices, hours, addresses, reviews, or testimonials. If the text needs one, ask for the real one.
3. **Draft three options.** Use the formulas in `commands/copy/tokens/formulas.json` and the examples in `commands/copy/references/copy.md`. Each option is plain, concrete, and within the limits: headline 8 words or fewer, two lines at most; supporting sentence under 20 words; buttons verb plus object.
4. **Check each option** against `core/tokens/rules.json`: banned words, banned symbols (`/`, `·`, `•`, em dash), filler text, emoji. Discard and redraft any that fail.
5. **Present** the three, mark the recommended one, and let the user pick (`ask_user_input_v0`) or type their own.
6. **Apply** the pick to the named part only. Pre-hook snapshot, then post-hooks: audit, state, report.

## Voice

Say what it is and who it is for, in words a customer uses. Short sentences. No metaphors standing in for the product. No second pitch in the supporting sentence. Brand name appears once, small, above the headline.

## Outputs

Three options and, after the pick, an edited file.

## Failure cases

- **User's own text contains a banned phrase:** say which phrase, give a plain alternative, and let them decide. Their final word applies, and the override is remembered for the conversation.
- **Not enough facts to write anything specific:** ask one question about what the business actually does, rather than writing generic copy.
- **Non-English copy:** the banned-word list is English; keep the other rules (no symbols separators, no filler, short and concrete).
