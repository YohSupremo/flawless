# Motion catalog

Allowed patterns, each built from `commands/animate/tokens/animations.css`.

| Area | Pattern | What moves | Notes |
|---|---|---|---|
| Hero entrance | Fade, slide up, or mask reveal on the headline block, then siblings with a stagger of 80ms | opacity, transform, clip-path | Once on load; total under 1 second |
| Scroll reveal | Section content fades and rises once as it enters the viewport | opacity, transform | IntersectionObserver; unobserve after the first reveal |
| Hover and focus | Button color shift (no glow), card lifts 2px, link underline slides | background, transform | 150ms; same treatment on `:focus-visible` |
| Image motion | Mask reveal on load, or a very slow scale from 1.03 to 1 | clip-path, transform | Once; never a looping zoom |

## Banned by default

Looping animation of any kind, parallax, floating or bobbing elements, marquees, glow or pulse effects, typewriter text, confetti, gradient shimmer, auto-playing carousels, bounce and elastic easing, scroll-jacking, animated counters for statistics.

## Choosing the pace

| Pace | Duration | Feels |
|---|---|---|
| Quick | 200ms | tools, dashboards |
| Standard | 400ms | most sites |
| Slow | 600ms | editorial, hero image reveals; never above 700ms |

## Principles

- Motion explains or orients; it never decorates.
- One signature moment per page (usually the hero); everything else is quiet.
- If you notice the animation, it is too much.
- Everything is visible and usable with motion off.
