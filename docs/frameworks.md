# Framework output

By default Flawless builds one self-contained HTML file. The principles (one purpose, one accent, plain copy, a small spacing scale, accessible and responsive) do not depend on that format. When the user asks for a framework, or `allowed_frameworks` in `flawless.config.json` names one, keep the rules and change only how they are written.

| Target | How the rules map |
| --- | --- |
| Plain CSS or CSS modules | Keep the token block from `core/tokens/base.css` as `:root` variables in a shared file; modules use `var(--accent)` etc. |
| Tailwind | Put the tokens in `tailwind.config` (`colors.accent`, `spacing` limited to the scale, `borderRadius`) and do not add arbitrary values off the scale. Do not use the default blue and violet palettes |
| React, Vue, Svelte | One component per section, tokens as CSS variables on `:root`, props for copy so no text is hard-coded in styles. Keep a `prefers-reduced-motion` rule in the global CSS |
| Astro | Static sections as components; tokens in a global stylesheet; no client JavaScript unless a section needs it |

## What stays the same

- Token names, so `/palette`, `/match`, and `/edit` can still find and change them
- The banned list: hues, gradients, symbols, filler words
- The audit: run `audit.py` on the built output (the HTML file, or a built page), since it reads HTML and inline CSS. Component source files are not audited directly
- The agent states which content is sample content

## Limits

The audit and browser check run on rendered HTML. For a framework project, build first and audit the output. No framework adapter scripts ship with Flawless; this page is guidance for the agent.
