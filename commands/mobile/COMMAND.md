---
name: mobile
description: Check and fix the phone layout.
---

# /mobile

Makes the page work at about 390px wide without changing the desktop design.

## Triggers

- `/mobile` or `/mobile <page>`.
- Called by `/section` (after adding a section) and `/edit` (responsive fixes).

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `commands/mobile/references/mobile-checklist.md`, `commands/mobile/tokens/breakpoints.css`, `core/preview.md` |
| Scripts | `core/scripts/audit.py` |
| Calls | none |
| Called by | `/edit`, `/section` |
| Hands off to | none |
| Handed off from | `/audit` |
| Requires | none |
| State read | `scheme` |
| State written | `pages` |
<!-- wiring:end -->

## Steps

1. **Static check.** `python core/scripts/audit.py <file> --mobile`. Thresholds (font sizes, tap target, headline size) come from `core/tokens/rules.json`.
2. **Read the media queries** and check against `commands/mobile/references/mobile-checklist.md`: hero stacks, image order, buttons full width, headline at least 40px via `clamp()`, body text at least 16px, columns collapse to one, no horizontal scroll, tap targets at least 44px tall.
3. **Fix** failures by editing responsive rules only, using the snippets in `commands/mobile/tokens/breakpoints.css`. Do not change desktop rules, colors, fonts, or copy. Pre-hook snapshot first.
4. **Post-hooks:** audit with `--mobile`, state, report what changed in one or two sentences.

## Rules

- One breakpoint at 820px for layout; add 480px only if something still breaks.
- Same content on every screen size. Do not hide or add content per breakpoint.
- Wide content (tables, code) scrolls inside its own container; the page body never scrolls sideways.
- Honor safe-area insets on fixed or sticky bars.

## Preview mode

`/mobile --preview ...` shows the proposed change and its audit result without writing anything, then asks whether to apply it. Full rules: `core/preview.md`.

## Outputs

The page with responsive rules fixed, or a report that nothing needed changing.

## Failure cases

- **Fixed pixel widths that overflow:** replace with `max-width: 100%` and relative units; flag any that were intentional.
- **Image-heavy hero crops badly on phones:** move the image above the text (`order: -1`) with a capped height, or darken a flat overlay, rather than shrinking the headline below 40px.
