# Harmony rules

## Who adapts

Whichever the user fixed stays; the other adapts. When someone says "my palette is green", the palette is fixed and the photo is graded or swapped. When the photo is brand photography and no palette exists, the palette follows the photo. Never decide this silently.

## Why palettes clash with photos

A palette chosen from a library or copied from another reference knows nothing about the photo. Two failures show up most:

1. **Accent hue fights the photo.** A warm brown photo (hue about 20 to 40 degrees) with a green or blue accent reads as two unrelated designs. The accent should come from the photo's own family: orange, amber, rust, brass, or cream on a warm photo; teal or ice on a cool photo; the photo's complement only for a single small marker, and only if the user asks.
2. **Base is a different black.** A pure `#000` or `#0a0a0a` base next to a photo whose shadows are warm brown-black makes the photo's edge visible. The base should equal the photo's shadow tone.

## Measurements (core/scripts/image_harmony.py)

- **Dominant hue:** area-weighted circular mean over pixels with moderate saturation (0.10 to 0.55). The saturation cap keeps small saturated UI (a button, an eyebrow line) from skewing the result.
- **Shadow color:** mean of the darkest 40 percent of pixels.
- **Accent check:** hue distance at most 45 degrees (or neutral photo).
- **Base check:** CIE color difference at most 6 from the shadow color.

## Palette-led grading (grade_photo.py)

1. Find the photo's dominant hue and rotate colors in that family toward the accent hue, keeping 35 percent of their original spread so the picture stays natural rather than a flat tint.
2. Scale saturation down (default keeps 60 percent) so no color shouts.
3. Pull shadows toward the palette base so the photo edge melts into the page.

It writes a new file. Result on a warm brown garage photo with a green palette (`#009966` accent, `#06100c` base): photo hue 32 moved to 148 (accent 160, 12 degrees apart), shadow difference from base 1.4. Strengths: subtle 0.6, standard 0.85, full 1.0.

Limits: grading cannot fix a photo whose subject has a meaningful color (a red car on a green palette turns the car green). In that case swap the photo.

## Worked example (photo-led)

A hero used a warm brown garage photo (dominant hue about 33 degrees, shadows near black) with a green accent (hue 159). Accent distance 126 degrees: clash. The base `#0a0a0a` was fine (difference under 1). Fix: take the accent from the warm family (for example amber `#e9b949` at 9 degrees, or ember `#e8622f` at 17), keep the near-black base, and tint the flat overlay with the photo's shadow color.

## What not to do

- Do not color-grade with CSS filters, blend modes, or overlays to force a match; bake the grade into a new file.
- Do not add a gradient to blend the photo into the base.
- Do not change the photo's position or crop to hide a clash.
