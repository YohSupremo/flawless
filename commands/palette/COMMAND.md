---
name: palette
description: Show compliant palettes with contrast values, and apply the chosen one to the color tokens.
---

# /palette

Chooses or changes colors. It is the only command, besides the colors category of `/edit`, that writes the session scheme.

## Triggers

- `/palette`: suggest three palettes.
- `/palette <direction>`: "/palette warmer accent", "/palette dark".
- Called by `/new`, `/edit`, `/ref`, and `/flawless` in suggest mode or apply mode.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `core/state.md`, `commands/palette/references/palettes.md`, `commands/palette/references/palette-rules.md`, `commands/palette/tokens/palettes.json` |
| Scripts | `core/scripts/palette.py`, `core/scripts/state.py`, `core/scripts/image_harmony.py` |
| Calls | none |
| Called by | `/edit`, `/flawless`, `/match`, `/new`, `/ref` |
| Hands off to | `/match` |
| Handed off from | `/a11y`, `/audit` |
| Requires | none |
| State read | `scheme` |
| State written | `scheme` |
<!-- wiring:end -->

## Modes

- **Suggest:** present options, change nothing.
- **Apply:** write the chosen colors to `:root` tokens (and the dark-mode block if the page has one), update state, run post-hooks.

## Steps

1. **Context.** If a page exists, its current palette is option 1 ("keep"). Otherwise pick the subject from the request.
2. **Pick candidates.** From `commands/palette/tokens/palettes.json`, take the three whose `suits` fits the subject. If the user gave a direction ("warmer", "darker"), adjust within the same entries or move to the nearest entries, never inventing a gradient or a blue-violet hue.
3. **Verify.** For every candidate and every user-supplied color: `python core/scripts/palette.py <base> <text> <accent> <accent-ink>`. It checks the hue range and contrast thresholds in `core/tokens/rules.json`.
4. **Present** three options with hex values and contrast (text on base, accent on base, button text on accent). Mark the recommended one. Use `ask_user_input_v0` to let the user choose, or accept their own hex values.
5. **Failing choice.** If a color fails, say which check failed and offer the nearest passing adjustment (see `commands/palette/references/palette-rules.md`). If the user's brand color is blue-violet, ask keep-or-override.
6. **Apply** (apply mode only). Pre-hook snapshot. Change only the color tokens. Update the session scheme with `state.py set`. Post-hooks: audit, state, report.

## Outputs

A palette decision, and in apply mode an edited file with updated tokens and state.

## Photos

If the page has a photo, a palette that ignores it can clash (green accent on a warm brown photo). Before applying, run `python core/scripts/image_harmony.py <photo> --base <base> --accent <accent>`. If it reports a clash, say so and hand off to `/match`, which asks which side is fixed. If the user chose this palette, the photo adapts, not the palette.

## Failure cases

- **Page hard-codes colors instead of tokens:** replace the hard-coded values with the new ones throughout, then recommend moving to tokens. Do not leave mixed old and new colors.
- **Light and dark variants:** keep the accent hue; change base, surface, text, and accent lightness only.
- **User asks for a gradient:** decline in one line and offer a flat color or flat two-tone panel instead. Override only if the user insists after the question.
