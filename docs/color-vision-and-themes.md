# Color vision, themes, and system preferences

The audit measures contrast between named tokens in the default theme. It does not simulate color vision, and it does not read other themes. This page is the checklist for those, until they are automated.

## Color vision (about 1 in 12 men and 1 in 200 women)

- Never use color alone to carry meaning (error red versus success green). Add text, an icon, or a pattern
- The single-accent rule helps: there is no second hue to confuse. If a page uses two status colors anyway, check them in a deuteranopia and protanopia simulator (browser devtools has a "Emulate vision deficiencies" option under Rendering)
- Check that the accent still separates from the base in grayscale: contrast against the base (3:1 for a marker) is what keeps it visible

## Themes

- Light and dark: the audit reads the first declaration of each token. Declare the default theme first and the other under `@media (prefers-color-scheme: dark)` or `[data-theme="dark"]`. Then audit the dark theme by temporarily swapping its values in, or with `palette.py BASE TEXT ACCENT ACCENT_INK` using the dark values
- Every theme needs its own contrast pass: text 4.5:1, button text 4.5:1, accent marker 3:1
- Photos and overlays: re-check text over images in each theme (`/match`)

## High contrast and forced colors

- Under `@media (forced-colors: active)` the browser replaces colors. Do not rely on background color alone to show a button or a focus ring: keep a real `border` or `outline` (use `outline: 2px solid` rather than `box-shadow` for focus)
- Do not set `forced-color-adjust: none` unless there is a specific reason
- Prefer system colors (`CanvasText`, `Canvas`, `LinkText`) inside a `forced-colors` block

## System preferences

- `prefers-reduced-motion` is already required by the audit
- `prefers-contrast: more`: raise borders and muted text to full text color
- `color-scheme: light dark` on `:root` lets form controls follow the theme

## Planned

Automated checks for these (a theme pass in `audit.py`, a vision-simulation pass in the browser check) are not implemented.
