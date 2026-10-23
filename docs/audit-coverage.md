# What the audit can and cannot check

`core/scripts/audit.py` reads the HTML as text. It does not render the page. That makes it fast and dependency-free, and it limits what it can know. Rules fall into three groups.

## Checked automatically

A pass or fail from the text of the file. Reliable for what it covers.

| Rule | Level |
| --- | --- |
| Gradients in CSS or HTML | error |
| Hex and `hsl()` colors in the banned hue range | error |
| Banned symbols in visible copy (slash, middle dot, bullet, em dash) | error |
| Banned stock words and phrases | error |
| Emoji in visible copy | error |
| Filler text (lorem ipsum, placeholder, TBD) | error |
| Spacing values off the scale in `padding`, `margin`, `gap` | error |
| Backdrop blur | error |
| Infinite animations | error |
| Motion with no `prefers-reduced-motion` rule | error |
| Hero button count | error |
| Eyebrow label count | error |
| Badge, pill, chip, tag classes | error |
| Contrast of text, muted text, button text (from design tokens) | error |
| `lang` on `<html>`, `alt` on `<img>`, focus outline removed (`--a11y`) | error |
| Viewport meta tag, a `max-width` media query (`--mobile`) | error |

## Checked heuristically

Pattern guesses that can be wrong in both directions. Reported as warnings.

| Rule | Known limits |
| --- | --- |
| Headline over the word limit, more than one `<br>` | Counts words in the first `<h1>` only |
| Possible statistics and trust claims | Regex on numbers and phrases; misses wording it does not know; may flag real, supplied numbers |
| Possible second accent | Looks at saturated hex colors only; named colors, `hsl()`, and `var()` chains are not counted |
| Large shadows, `transition: all`, long durations, layout properties in keyframes, overshoot easing | CSS text patterns; duration check looks for the first value only |
| Same grid column count everywhere | Counts `repeat(n` in `grid-template-columns` |
| Small fonts, small button padding on phones (`--mobile`) | Looks at `px` font sizes and the first `.btn` rule; cannot compute actual tap target size |
| `<svg>` without a label, missing `text-wrap: balance` | Text presence only |
| Contrast between tokens | Only the tokens `--base`, `--surface`, `--text`, `--text-muted`, `--accent`, `--accent-ink`. Text over photos and any other color pair is not measured |

## Needs a human or the agent

The script cannot see these. `/audit` has the agent do a judgment pass (`commands/audit/references/slop-audit.md`) for them.

- Does the headline say what the thing is? Does each section have one job?
- Heading hierarchy beyond "there is an h1"
- Meaningful link and button text (the banned phrase list catches only the stock ones)
- Whether alt text describes the image, as opposed to being present
- Layout quality, visual hierarchy, whitespace
- Whether copy is invented, accurate, or in the right tone
- Keyboard order and focus behavior in practice, touch target sizes as rendered, horizontal overflow, reduced-motion behavior as it runs. The optional [browser check](./browser-checks.md) covers some of these
- Color-vision and theme issues. See [`color-vision-and-themes.md`](./color-vision-and-themes.md)

## Reading CSS

The audit uses regular expressions, not a CSS parser. Its supported subset is in [`css-support.md`](./css-support.md). A clean audit means no known violation was found in that subset, not that the page is flawless.

## Tests

`tests/fixtures/good` must stay free of findings; every file in `tests/fixtures/bad` must keep producing the findings listed in `tests/fixtures/expected.json`. Run `python -m unittest discover -s tests`.
