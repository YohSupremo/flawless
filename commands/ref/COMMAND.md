---
name: ref
description: Read the idea behind a reference image (hierarchy, composition, tone) and build something new from it, never a repaint.
---

# /ref

Takes the idea from a reference, not its surface. The reference's palette, fonts, copy, brand, photo, and exact layout are replaced; its principles are kept.

## Triggers

- `/ref` with an image attached or linked.
- Under `/flawless`, a shared screenshot with "something like this" routes here.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | no (read-only) |
| Pre-hooks | none |
| Post-hooks | none |
| Reads | `core/rules.md`, `core/state.md`, `commands/ref/references/ref-analysis.md`, `commands/ref/tokens/brief-template.md` |
| Scripts | `core/scripts/analyze_layout.py`, `core/scripts/extract_palette.py`, `core/scripts/audit.py`, `core/scripts/image_harmony.py` |
| Calls | `/palette`, `/copy`, `/match` |
| Called by | none |
| Hands off to | `/new`, `/edit` |
| Handed off from | none |
| Requires | none |
| State read | `active`, `scheme`, `pages` |
| State written | none |
<!-- wiring:end -->

## Steps

1. **Look at the image.** Then run `python core/scripts/analyze_layout.py <image>` (weight, accent share, calm space, contrast) and `python core/scripts/extract_palette.py <image>` (colors). Numbers support what you see; confirm the accent and the text and subject zones by eye.
2. **Write the idea brief** using `commands/ref/tokens/brief-template.md` (focal point, composition, hierarchy, content budget, contrast strategy, type character, copy tone, rhythm, mood, rule breakers). One or two plain lines each. Method and a worked example: `commands/ref/references/ref-analysis.md`.
3. **Show the brief and ask one question:** carry over all principles, or only chosen ones? Offer "close match" only if the user asked for a copy.
4. **Settle the surface.** Palette priority, highest first: (a) the existing page's current colors, fonts, radius; (b) the brand's own colors; (c) a palette the user picks through `/palette`. If the page uses a photo, `/match` runs before delivery: when the palette is from (a) or (b), or the user stated it, the palette is fixed and the photo is graded or swapped to fit it; only a photo the user must keep, with no palette decided, leads the palette. The reference's palette and fonts are never used unless the user asks for them by name. A palette and a photo that were chosen separately is the most common failure (a green palette on a warm brown photo).
5. **Hand off:**
   - No existing page: to `/new`, passing the carried principles, the subject, and the scheme from step 4. Copy comes from `/copy` rules, never from the reference.
   - Existing page: to `/edit` with the principles as the requested change. The scheme stays exactly as it is; only composition, hierarchy, spacing, and copy tone change, using existing tokens.
6. **Do not echo the reference.** Transcribe the reference's visible text into a do-not-reuse list (headline, supporting lines, button labels, eyebrow, micro text). Write new copy for the new subject. After building, run `python core/scripts/audit.py <file> --avoid "<phrase 1>|<phrase 2>"` with that list; any reused phrase is an error. Then change at least one structural choice (flip the subject side, change the type style, change the button treatment, restructure lower sections) and say which one. The same headline, the same eyebrow, and the same layout with new colors is a repaint, not a build.
7. **Leave out the reference's rule breakers** (badges, stat lines, symbols, gradients, corner microcopy) and list them in one line.

## Outputs

The idea brief, then a built or edited page through `/new` or `/edit`.

## Failure cases

- **Several images:** build one brief per image, then ask which principles to combine. Do not average them.
- **Image is a full-page screenshot with many sections:** brief the hero first; ask whether to brief other sections too.
- **User says "copy it exactly":** that is a close-match request; still use the user's own copy, brand, and imagery, and leave out the rule breakers.
- **Output matches the reference too closely** (same headline, same eyebrow line, same arrangement): treat it as a failure, rewrite the copy, apply the structural change, and re-run the avoid-list audit.
- **Pillow not installed:** `pip install pillow --break-system-packages`, or describe by eye and say the numbers were skipped.
