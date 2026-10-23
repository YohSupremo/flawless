# /audit --explain

```text
> /audit --explain examples/a11y-before.html
CURRENT SCHEME
  base: #f1eadd
  surface: #e7dfce
  text: #1f1a15
  accent: #b23a14
  fonts: ['"Anton", Impact, "Arial Narrow", sans-serif', '"DM Sans", system-ui, sans-serif']
  radius: 4px
  contrast: {'text on base': 14.43, 'muted text on base': 1.85, 'accent on base (marker)': 5.0, 'text on surface': 13.02, 'button text on accent': 5.99}
  mode: strict
ERRORS
  - low contrast: muted text on base is 1.85:1 (needs 4.5:1)
      why: WCAG contrast keeps text readable.
      fix: Darken or lighten the text or background (/palette or /a11y).
  - a11y: <html> has no lang attribute
      why: Screen readers pick pronunciation from the lang attribute.
      fix: Add lang="en" (or the right language) to <html>.
  - a11y: <img> without alt
      why: Images need a text alternative.
      fix: Add alt text, or alt="" for decorative images.
  - a11y: outline removed with no :focus-visible replacement
      why: Keyboard users need a visible focus indicator.
      fix: Add a :focus-visible style.
```
