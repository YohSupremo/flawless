# Configuration and strictness modes

Flawless is opinionated by default. A project can loosen or tune the rules without editing the skill.

## flawless.config.json

`audit.py` looks for `flawless.config.json` next to the page, then in up to five parent folders. `--config path` overrides the search. A config file that is not valid JSON stops the audit with an error rather than being ignored.

| Key | Effect |
| --- | --- |
| `mode` | `strict` (default), `balanced`, or `brand-first`. See below |
| `brand_colors` | Hex colors exempt from the banned-hue rule and from second-accent warnings |
| `accessibility_target` | `AA` (default, 4.5:1 text) or `AAA` (7:1 text) |
| `max_headline_words` | Overrides the headline limit |
| `typography`, `allowed_frameworks`, `content_tone`, `page_type` | Read by the agent when building (see [`frameworks.md`](./frameworks.md), [`content-models.md`](./content-models.md)); the audit script does not check them |

Example: [`../flawless.config.example.json`](../flawless.config.example.json).

## Modes

`--mode` on the command line beats the config file.

| Rule | strict | balanced | brand-first |
| --- | --- | --- | --- |
| Banned blue-violet hues | error | error, but only above 0.35 saturation | warning |
| Brand colors | still checked | still checked | exempt (always exempt when listed in `brand_colors`) |
| Gradients | error | error | warning |
| Backdrop blur | error | error | warning |
| Spacing off the scale | error | warning | warning |
| Badges, pills, tags | error | warning | warning |
| Eyebrow labels | 1 allowed, a second is an error | 2 allowed, beyond that a warning | 3 allowed, beyond that a warning |
| Headline length warning | over 8 words | over 10 | over 12 |
| Contrast, alt text, `lang`, focus, viewport, reduced motion | error | error | error |

Accessibility and contrast rules are never relaxed by a mode. A mode changes taste rules, not whether people can use the page.

When a rule is relaxed, the finding still appears as a warning, so it is visible and explainable (`--explain`).
