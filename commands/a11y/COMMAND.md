---
name: a11y
description: Check contrast, language, alt text, focus styles, and reduced motion; asks before fixing.
---

# /a11y

Accessibility check and fix. The check is read-only; fixes need the user's yes.

## Triggers

- `/a11y` or `/a11y <page>`.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `commands/a11y/references/a11y-checklist.md`, `commands/a11y/tokens/a11y.css`, `core/tokens/motion.css` |
| Scripts | `core/scripts/audit.py` |
| Calls | none |
| Called by | none |
| Hands off to | `/palette` |
| Handed off from | `/audit` |
| Requires | none |
| State read | `scheme` |
| State written | `pages` |
<!-- wiring:end -->

## Steps

1. **Run** `python core/scripts/audit.py <file> --a11y`. It reports contrast ratios for text on base, muted text, accent as a marker, text on surface, and button text on accent; the `lang` attribute; `<img>` without alt; `<svg>` without a role or label; removed focus outlines; animation with no reduced-motion rule.
2. **Read the page** for what the script cannot check using `commands/a11y/references/a11y-checklist.md`: heading order, link and button text that makes sense out of context, form labels, tap targets, color-only meaning.
3. **Report** with `commands/audit/references/report-format.md`: errors, warnings, passes. Show contrast ratios as numbers.
4. **Ask one question:** fix all, fix selected, or leave as is.
5. **Fix** with the snippets in `commands/a11y/tokens/a11y.css`. Pre-hook snapshot first. Contrast fixes change color tokens, so route them through `/palette` apply mode so the session scheme stays in sync. Post-hooks: audit, state, report.

## Rules

- Never remove a focus outline without adding `:focus-visible`.
- Never fix contrast by adding a gradient or a glow; change the color value.
- Decorative SVGs get `aria-hidden="true"`; meaningful ones get `role="img"` and `aria-label`.

## Outputs

A report; after approval, an edited file.

## Failure cases

- **Accent fails as a marker (under 3:1) but passes as button background:** warn, and leave it unless the accent is the only thing carrying meaning.
- **Muted text under 4.5:1:** raise its opacity (for example .72 to .8) rather than changing its hue.
- **Page in a language other than English:** set `lang` to the correct code, not `en`.
