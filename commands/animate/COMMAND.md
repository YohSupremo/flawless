---
name: animate
description: Add restrained motion after asking what kind: entrance, scroll reveal, hover, or image motion.
---

# /animate

Adds motion deliberately. It asks what the user wants, applies a small set of rule-checked patterns, and always includes reduced-motion support.

## Triggers

- `/animate`: ask what kind.
- `/animate <what>`: "/animate hero entrance", "/animate hover on buttons".
- Called by `/edit` when the components and images category includes motion.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `core/tokens/motion.css`, `commands/animate/references/motion-catalog.md`, `commands/animate/tokens/animations.css`, `commands/animate/tokens/scroll-reveal.js` |
| Scripts | `core/scripts/audit.py` |
| Calls | none |
| Called by | `/edit` |
| Hands off to | none |
| Handed off from | none |
| Requires | none |
| State read | `scheme` |
| State written | `pages` |
<!-- wiring:end -->

## Questions (one round, `ask_user_input_v0`)

Skip any question the message already answers.

1. **Where?** (multi-select, up to 4): Hero entrance on load; Scroll reveal for sections; Hover and focus on buttons and cards; Image motion (reveal or slow zoom).
2. **Style?** (single-select): Fade; Slide up; Mask reveal (clip-path wipe); None extra, just fade and keep it quiet.
3. **Pace?** (single-select): Quick (200ms); Standard (400ms); Slow (600ms).

Image motion is only offered when the page has a photo or illustration. Do not ask about anything the rules ban (looping, parallax, floating, shimmer); if the user asks for one, say it is not allowed by default and offer the closest allowed pattern. If they insist, ask keep-or-override once.

## Steps

1. **Target and scheme.** Resolve the page. Read its tokens with `python core/scripts/audit.py <file>`. Motion never changes colors, fonts, or layout.
2. **Ask** the questions above.
3. **Pre-hook:** snapshot.
4. **Add motion tokens** from `core/tokens/motion.css` to `:root` if absent, setting `--dur` to the chosen pace and `--ease`, `--stagger`, `--rise` as given. Add the `prefers-reduced-motion` block from the same file.
5. **Add the chosen patterns** from `commands/animate/tokens/animations.css`; for scroll reveal also add `commands/animate/tokens/scroll-reveal.js`. Use only the patterns for the chosen areas. Catalog and rules: `commands/animate/references/motion-catalog.md`.
6. **Check limits:** one entrance per element, stagger at most 120ms, durations 120 to 700ms, only opacity, transform, clip-path.
7. **Post-hooks:** audit with `--a11y --mobile`, state, report in one or two sentences naming what animates and the pace.

## Outputs

The page with motion tokens, the chosen patterns, and reduced-motion support.

## Failure cases

- **Page already has animation:** list it, then replace it with the chosen pattern rather than stacking a second one on the same element.
- **Content must be visible without JavaScript:** scroll reveal starts hidden only when the script has run (a `js` class on `<html>`); with no script everything shows.
- **Long pages:** reveal each section once; never re-trigger on scroll up.
- **Audit warns about keyframes animating layout properties:** rewrite using transform.
