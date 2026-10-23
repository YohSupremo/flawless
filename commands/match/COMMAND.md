---
name: match
description: Make the palette and the photo agree. Adapts the photo to your palette, or the palette to your photo, depending on which one is fixed.
---

# /match

Fixes a palette and a photo that do not agree (for example a green palette on a warm brown motorcycle photo, or a pure black base beside a brown-black photo). One of the two is fixed and the other adapts.

## Triggers

- `/match`, or `/match <page>`.
- Called by `/new`, `/ref`, and `/edit` whenever a photo is added or changed.
- Under `/flawless`, a complaint like "the colors don't match the image" routes here.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `core/state.md`, `commands/match/references/harmony-rules.md`, `commands/match/tokens/harmony.json`, `core/preview.md` |
| Scripts | `core/scripts/image_harmony.py`, `core/scripts/palette.py`, `core/scripts/state.py`, `core/scripts/grade_photo.py` |
| Calls | `/palette` |
| Called by | `/edit`, `/new`, `/ref` |
| Hands off to | none |
| Handed off from | `/palette` |
| Requires | none |
| State read | `scheme` |
| State written | `scheme` |
<!-- wiring:end -->

## Which one is fixed?

This decides everything, so settle it first and never assume.

| Fixed | Adapts | When | What `/match` does |
|---|---|---|---|
| **Palette** | the photo | The user chose or gave the palette: an existing page, brand colors, a palette picked through `/palette`, or a stated color ("my palette is green") | Grade the photo to the palette, or swap the photo (palette-led, the default when a palette is stated) |
| **Photo** | the palette | The photo is brand photography or a specific shot the user must keep, and no palette has been decided | Take the base and accent from the photo (photo-led) |

If the message does not say, ask one question: "Which stays as it is, the palette or the photo?" A stated palette always wins over a guessed one. Thresholds are in `core/tokens/rules.json` (`imagery`). Method, examples: `commands/match/references/harmony-rules.md`.

## Steps

1. **Settle which is fixed** (table above).
2. **Find the photo.** Use the file the page references (`hero.jpg`, the `url(...)` in CSS). If there is only a screenshot, crop the photo area out of it (exclude text and buttons) and say the result is approximate. Ask for the photo file when the page uses one you cannot see.
3. **Measure.** `python core/scripts/image_harmony.py <photo> --base <base> --accent <accent>`. It reports the photo's dominant hue and shadow color, the accent's hue distance, and the base's color difference from the photo's shadows. If both pass, say the palette and photo fit and stop.
4. **Palette-led (palette fixed).** Offer three options with `ask_user_input_v0`:
   - **Grade the photo to the palette.** Run `python core/scripts/grade_photo.py <photo> <graded.jpg> --base <base> --accent <accent> --preview <preview.png>`. The original is never overwritten. Show the before and after preview and let the user choose strength (subtle 0.6, standard 0.85, full 1.0) if they want to adjust.
   - **Swap the photo.** Describe what to look for: subject, lighting, and a dominant hue within 45 degrees of the accent. Give image search terms. Verify any new photo with `image_harmony.py` before using it.
   - **Keep the mismatch.** One plain sentence about how it will read; no changes.
5. **Photo-led (photo fixed).** Run `--suggest`, present three palettes whose accent is in the photo's hue family, each with the base set to the photo's shadow color and contrast numbers from `core/scripts/palette.py`. Apply the choice through `/palette` apply mode.
6. **Apply.** Palette-led: point the page at the graded file, tint the flat overlay with the base color at 50 to 60 percent, keep the original file beside it. Photo-led: apply through `/palette`. Pre-hook snapshot first.
7. **Re-check.** Run `image_harmony.py` on the file now used. Report the before and after hue distance in one or two sentences.

## Rules

- Never fix a mismatch with a CSS filter, blend mode, gradient, or blur over the photo. A grade is baked into a new image file by `grade_photo.py`, and the original is kept.
- A flat overlay is allowed; tint it with the base color (palette-led) or the photo's shadow color (photo-led).
- A neutral (gray) photo accepts any accent outside the banned hues; only the base is matched.
- Do not change fonts, copy, or layout. Palette-led never recolors the page; photo-led never recolors the photo.

## Preview mode

`/match --preview ...` shows the proposed change and its audit result without writing anything, then asks whether to apply it. Full rules: `core/preview.md`.

## Outputs

A palette decision and, after approval, edited color tokens with the session scheme updated through `/palette`.

## Failure cases

- **No Pillow or numpy:** `pip install pillow numpy --break-system-packages`, or judge by eye and say so.
- **Graded photo looks muddy:** lower the strength to 0.6, or raise `--keep-saturation`; do not stack a second grade on the first.
- **Photo is mostly neutral (gray):** it accepts any accent; only the base needs matching, which `--strength` handles through the shadows.
- **Photo has two strong colors (for example blue sky and orange rock):** the dominant hue is a compromise. Show both candidate hues and ask which one the accent should follow.
- **Light-base page with a dark photo:** the base cannot match; say so and recommend a dark base for the photo section, or a flat panel that separates the photo from the base.
- **User's brand color conflicts with the photo:** ask keep-or-override once; the usual better answer is a different photo.
