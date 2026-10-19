---
name: new
description: Build a page from scratch, asking only for what is missing.
---

# /new

Creates a page or component from nothing, following `core/workflow.md`.

## Triggers

- `/new <what to build>`: "/new landing page for a bike workshop".
- Under `/flawless`, any plain request such as "make a pricing page" routes here.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/workflow.md`, `core/delivery.md`, `core/tokens/base.css`, `core/tokens/rules.json`, `core/hooks.md`, `core/state.md`, `commands/new/references/type-pairings.md`, `commands/new/references/torque-hero-notes.md`, `commands/new/tokens/hero.html`, `commands/new/tokens/intake.json`, `core/tokens/motion.css` |
| Scripts | `core/scripts/audit.py`, `core/scripts/palette.py`, `core/scripts/state.py`, `core/scripts/snapshot.py`, `core/scripts/image_harmony.py` |
| Calls | `/palette`, `/copy`, `/section`, `/match` |
| Called by | none |
| Hands off to | none |
| Handed off from | `/ref` |
| Requires | none |
| State read | `active`, `scheme` |
| State written | `scheme`, `pages` |
<!-- wiring:end -->

## Inputs

Collected from the message first; ask only for the missing ones (`commands/new/tokens/intake.json` lists them):

1. **Subject:** what the business or product is, and its name.
2. **The one action:** what the visitor should do (book, buy, call, visit).
3. **Colors:** the user's own, the session scheme, or a pick through `/palette`.
4. **Real facts:** only the ones the page needs (address, hours, prices). Never invented.

## Steps

1. **Intake.** Read the message, fill the inputs above. If 3 or more are missing, ask one `ask_user_input_v0` round (at most three questions). If only colors are missing, go to step 2.
2. **Scheme.** Order: session scheme, then the user's own or brand colors, then `/palette` in suggest mode with three options. Verify with `core/scripts/palette.py`.
3. **Fonts.** Reuse session fonts. Otherwise choose one display and one body for the brand; the type-character table in `commands/new/references/type-pairings.md` helps.
4. **Copy.** Call `/copy` rules for the headline, supporting sentence, and buttons. Plain words, no banned phrases.
5. **Build.** Start from `core/tokens/base.css` and `commands/new/tokens/hero.html`. Fill the hero. Each extra section comes from `/section` patterns, one job each, layouts varied.
6. **Images.** Use a real image path if the user has one. Otherwise a flat single-color illustration or a labeled placeholder. Never a gradient stand-in. **When a photo is used, run `/match` before delivering.** If the palette is the user's, the photo is graded or swapped to fit it; only a photo the user must keep leads the palette.
7. **Post-hooks.** Audit with `--a11y --mobile`, fix errors, record state, report in two or three sentences naming the accent, fonts, and which content is sample.

## Outputs

One self-contained HTML file in `/mnt/user-data/outputs/`. For published artifacts, publish the file; otherwise present it.

## Interconnections

- Uses `/palette` for colors, `/copy` for text, `/section` for everything after the hero, and `/match` when a photo is on the page.
- Writes the session scheme to state if it was empty.
- Later `/edit`, `/mobile`, `/audit`, `/a11y`, `/history`, and `/revert` operate on what `/new` produced.

## Failure cases

- **User wants a blue-violet palette or a gradient:** ask keep-or-override once, then follow the answer.
- **No subject given at all ("make me a website"):** ask one question: what is it for?
- **Invented-content risk:** if the page needs prices, hours, or reviews and the user gave none, build the layout with realistic sample items and say which are samples. Do not write "Sample copy" in the page.
