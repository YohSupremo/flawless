# Mobile checklist

- Viewport meta with `viewport-fit=cover`.
- Hero: single column, image first or behind with a stronger flat overlay, text bottom-aligned or centered vertically, buttons full width.
- Headline: `clamp(40px, 9vw, 112px)` or similar; never below 40px.
- Body: 16px minimum; nothing under 14px.
- Buttons: height at least 44px (padding 16px works), 16px gap between stacked buttons.
- Sections: 48px vertical padding; `.wrap` side padding 24px.
- Grids: `grid-template-columns: 1fr`. Alternating row images lose their `order` swap.
- Tables and code: inside `overflow-x: auto` containers.
- Fixed or sticky bars: add `env(safe-area-inset-top)` or `env(safe-area-inset-bottom)` to padding.
- No hover-only information. Hover styles are enhancements.
