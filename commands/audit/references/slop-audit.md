Automated first pass: `python core/scripts/audit.py page.html` prints the page's current scheme and flags gradients, blue-violet hues, banned symbols and words, emoji, glass blur, and off-scale spacing. The questions below cover what a script cannot judge.

# Slop audit

Run this on the finished output. Any "yes" means fix it before delivering.

## Color
- Any gradient at all (linear, radial, conic, mesh, blurred blob, text fill, border)? Search the CSS for "gradient".
- Any base, accent, tint, shadow, or glow with HSL hue between 230 and 300 degrees (blue-violet to purple)?
- More than one accent hue?
- Is the base a flat color or a photo, with legibility handled by a flat overlay?

## Symbols
- Any `/` or `·` or `•` used between words or labels?
- Any em dash in visible copy?
- Any emoji, sparkle icon, or decorative arrow outside a button?

## Information
- Any pill tag, badge, or "New" label the user did not ask for?
- More than one of: subheading, tagline, intro paragraph under the same heading?
- Any invented stat, testimonial, logo, review count, or date?
- Any element whose removal would lose nothing?
- Any small uppercase label above a heading that just restates the heading?

## Hero
- Headline longer than two lines or about eight words?
- Does the headline say what the thing is without needing the paragraph?
- Any word from the banned list: elevate, unleash, reimagine, seamless, empower, next-gen, journey, "where X meets Y"?
- Buttons vague ("Get started", "Learn more") instead of specific?

## Spacing
- Any gap between hero elements larger than 48px, or section padding above 96px?
- Spacing values outside the scale (4, 8, 16, 24, 32, 48, 64, 96)?
- Narrow centered text column floating in empty space?
- Cards or containers all padded identically large?

## Components
- Mixed corner radii, or pill shapes on everything?
- Heavy drop shadows or glass blur?
- More than one entrance animation, or any looping animation?

## Imagery (added)
- Is there a photo? If yes, do the palette and the photo agree (`python core/scripts/image_harmony.py <photo> --base <hex> --accent <hex>`)? If not, call `/match`, which asks which side is fixed.
- Any gradient, blur, blend mode, or CSS filter used to blend the photo into the page? (A grade must be baked into a new image file.)

## Hero text (added)
- Any eyebrow, kicker, or tag line above the headline that lists services joined with `&`, `/`, or `·`?
- Does the headline end on a single-word line? (`text-wrap: balance` fixes it.)
- If this page came from `/ref`: does any text match the reference? Run the audit with `--avoid`.

## Motion (added)
- Does anything loop, float, parallax, shimmer, or type itself out?
- Is there a `prefers-reduced-motion` rule? Do animations touch only opacity, transform, and clip-path?
