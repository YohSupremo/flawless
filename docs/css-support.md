# CSS the audit understands

The audit reads CSS from inline `<style>` blocks with regular expressions. This is deliberate: no dependencies, fast, easy to read. It is also approximate. This page lists what works, what is approximate, and what is not seen.

## Supported

- Design tokens as custom properties named `--base`, `--surface`, `--text`, `--text-muted`, `--accent`, `--accent-ink`, `--radius`, `--font-display`, `--font-body`
- Colors written as `#rgb`, `#rrggbb`, `rgb()`, `rgba()`, `hsl()`, `hsla()` (hue rule only for hsl)
- `padding`, `margin`, `gap` and their `-top/-left/...` forms, with `px` values
- `font-size` in `px`, `animation`, `transition`, `@keyframes`, `@media (max-width: ...)`

## Approximate

| Situation | Behavior |
| --- | --- |
| A token declared in several scopes (for example a dark theme under `@media` or `[data-theme]`) | The first declaration wins. That is the default theme, which is what the contrast numbers describe |
| Shorthand such as `padding: 0 clamp(...)`, `margin: auto` | `var()` and `clamp()` values are skipped; plain `px` values are checked |
| `rem`, `em`, `%`, `vw` spacing | Not checked against the scale |
| `.btn` padding | Only the first `.btn` rule is read |

## Not seen

- External stylesheets (`<link rel="stylesheet">`). The audit says so and checks the markup only
- Colors from `oklch()`, `lab()`, `color-mix()`, named colors, and `var()` chains
- Computed values, inheritance, specificity, the cascade
- Nested CSS rules and `@layer`
- Styles set by JavaScript

If a page needs these checked, use the [browser check](./browser-checks.md), which reads computed styles from a real render. Replacing the regex reader with a CSS parser is a larger change and would add a dependency; the tests in `tests/fixtures` are there to make that change safe if it is ever made.
