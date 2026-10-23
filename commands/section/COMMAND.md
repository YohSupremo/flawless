---
name: section
description: Add a section from the pattern library, with a layout different from its neighbors.
---

# /section

Adds one section below the hero. One job, one heading, content only, layout varied.

## Triggers

- `/section`: ask which type.
- `/section <type>`: "/section how it works", "/section faq".
- Called by `/new` (all sections after the hero) and `/edit` (layout category, adding a section).

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/base.css`, `core/tokens/rules.json`, `commands/section/references/sections.md`, `commands/section/tokens/layouts.css`, `core/preview.md` |
| Scripts | `core/scripts/audit.py` |
| Calls | `/copy`, `/mobile` |
| Called by | `/edit`, `/new` |
| Hands off to | none |
| Handed off from | none |
| Requires | none |
| State read | `scheme` |
| State written | `pages` |
<!-- wiring:end -->

## Steps

1. **Type.** If not stated, ask which one (`ask_user_input_v0`, four options). Offer the four that suit the page and are not already on it, from `commands/section/references/sections.md`.
2. **Facts.** If the type needs real facts (pricing, hours, address, quotes, images), ask for them. If the user wants a preview, write short realistic sample content and tell them which parts are samples. Never write "Sample copy" or "Coming soon" in the page.
3. **Layout choice.** Read the layout of the section above and the section below. Choose a pattern from `commands/section/tokens/layouts.css` that differs from both. Three equal cards in a row is allowed once per page, only for a true set of three.
4. **Text.** Call `/copy` rules for the heading and item text. One h2. No intro paragraph under it.
5. **Build.** Copy the pattern's CSS from `layouts.css` into the page's `<style>` using the existing tokens. Alternate flat `--base` and `--surface` backgrounds. Section padding 96px desktop, 48px mobile.
6. **Placement.** Where the user says; otherwise after the last content section and before the footer.
7. **Responsive.** Run the `/mobile` checks for the new section (columns collapse to one, images stack, tap targets 44px).
8. **Hooks.** Pre-hook snapshot; post-hooks audit, state, report.

## Never add

Stat strips, "trusted by" rows, six-tile icon grids, unrequested newsletter bars, scroll indicators, floating cards, "why choose us" blocks, a closing banner that repeats the hero.

## Preview mode

`/section --preview ...` shows the proposed change and its audit result without writing anything, then asks whether to apply it. Full rules: `core/preview.md`.

## Outputs

The page with one new section and a note of which content is sample.

## Failure cases

- **Page has only a hero and the user asks for three sections:** build them in sequence, each with a different layout, then audit once.
- **Requested type needs images and the user has none:** use a flat single-color illustration or a labeled placeholder, not a gradient.
- **Pricing requested without real prices:** ask for them or use obviously editable sample tiers and say so in the reply.
