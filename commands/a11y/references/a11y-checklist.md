# Accessibility checklist

- `<html lang="...">` set to the page language.
- Text on base 4.5:1; muted text 4.5:1; button text on accent 4.5:1; accent used alone as a marker 3:1.
- One `<h1>`; headings in order, no skipped levels.
- Every `<img>` has `alt` (empty `alt=""` if decorative); informative SVGs have `role="img"` and `aria-label`; decorative SVGs `aria-hidden="true"`.
- Links and buttons make sense out of context ("See our walls", not "Click here").
- Visible focus on every interactive element (`:focus-visible`).
- Motion: any animation or transition has a `prefers-reduced-motion` override.
- Meaning is never carried by color alone.
- Form fields have visible labels; error text says what to do.
- Tap targets at least 44px tall.
