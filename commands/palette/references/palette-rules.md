# Palette rules

- **One flat base, one accent.** Base may be any hue outside the banned range in `core/tokens/rules.json` (default 230 to 300 degrees, saturation above 0.15). Neutrals are fine.
- **Accent covers about 5 percent of the screen:** primary button, one small marker, hover states.
- **Contrast:** text on base 4.5:1 or better; accent on base (as a marker) 3:1; button text on accent 4.5:1. Fix a failing accent by darkening it on light bases, lightening it on dark bases, or by changing the button text color between the base color and white.
- **Brand color in the banned range:** say so, offer the closest compliant hue (shift toward teal at 180 to 200 or toward magenta-red above 330), and let the user decide.
- **Dark and light variants:** define the default on `:root` and the other under `@media (prefers-color-scheme: dark)`; keep the same accent hue.
- **Gradients:** none, including text fills and borders. Use flat panels or a flat semi-transparent overlay.
