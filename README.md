# Flawless

Flawless is an agent skill for building web interfaces that feel deliberate, readable, and human-made. It helps an AI assistant create or refine landing pages, product pages, dashboards, components, and other UI while keeping the visual system focused:

- One clear purpose per page
- One accent color and a restrained palette
- Direct, plain-language copy
- Tight spacing and a small radius scale
- Responsive, accessible layouts
- No gradients, filler badges, invented claims, or generic AI-style copy

Flawless is a collection of skill instructions, command references, design tokens, and Python validation scripts. It is not a web framework and does not ship a runtime application.

![A Flawless landing page on phone and desktop](./examples/screenshots/landing.phone.png)

See the [`examples/`](./examples) folder for a complete landing page, pages before and after `/audit`, phone and accessibility fixes, command transcripts, and screenshots.

## Who this is for

Use Flawless when you want an AI coding assistant to:

- Build a new page from a short brief
- Improve an existing page without losing its visual scheme
- Turn a reference image into a new, original direction
- Review copy, accessibility, mobile behavior, motion, or visual consistency
- Keep a page’s design decisions consistent across a conversation

The skill works best with an agent environment that supports skill files, slash commands, and file editing.

## Getting started

1. Make this directory available to your agent as a skill. Where it goes, which agents work, dependencies, and state storage are in [`INSTALL.md`](./INSTALL.md).
2. Use [`SKILL.md`](./SKILL.md) as the skill entry point.
3. Start with a command at the beginning of a message:

```text
/new landing page for a neighborhood bike workshop
```

To keep the rules active for the rest of a conversation, turn on session mode:

```text
/flawless
```

Then ask for ordinary UI work. Flawless will route new work to `/new` and changes to `/edit` while reusing the session’s design scheme.

## Commands

| Command | Purpose | Example |
| --- | --- | --- |
| `/flawless` | Turn the skill on, inspect session status, or turn it off | `/flawless status` |
| `/flawless-c` | List every command | `/help` |
| `/new` | Build a page from scratch | `/new product page for a ceramic studio` |
| `/edit` | Change an existing page while keeping its scheme | `/edit make the headline shorter` |
| `/audit` | Check a page against the design, accessibility, and mobile rules | `/audit the coffee page` |
| `/palette` | Choose or apply a compliant color palette | `/palette warmer accent` |
| `/copy` | Generate plain rewrites for page copy | `/copy headline` |
| `/section` | Add a section from the pattern library | `/section how it works` |
| `/match` | Make a photo and palette work together | `/match` |
| `/animate` | Add restrained entrance, scroll, hover, or image motion | `/animate hero entrance` |
| `/mobile` | Check and fix the phone layout | `/mobile` |
| `/ref` | Analyze an attached reference image and create a new direction | `/ref` |
| `/a11y` | Check contrast, alt text, focus styles, language, and reduced motion | `/a11y` |
| `/history` | List saved page versions | `/history` |
| `/revert` | Restore a previous page version | `/revert 2` |

Commands are case-insensitive. `/help` is an alias for `/flawless-c` and also shows, for each command, whether it changes files, needs a page, asks to confirm, supports preview, what it typically outputs, and how it commonly fails.

Two options worth knowing:

- `--preview` on `/edit`, `/palette`, `/copy`, `/section`, `/match`, `/animate`, `/mobile`, and `/a11y` shows the proposed change and its audit result without writing anything ([`core/preview.md`](./core/preview.md)).
- `/audit --explain` adds the design principle and a suggested fix under each finding.

## Typical workflow

### Create a page

```text
/new landing page for an independent bookstore
```

Flawless identifies the page’s single purpose, settles a palette and type pairing, writes concise copy, builds the page, and runs its post-build checks.

### Refine a page

```text
/edit make the primary button more specific
/mobile
/a11y
```

Edits preserve the existing scheme unless the request is specifically about colors, fonts, or another scheme category. File-changing commands save a snapshot first so the result can be reviewed or reverted.

### Review before delivery

```text
/audit the bookstore page
```

An audit reports errors and warnings rather than silently changing the page. Errors should be fixed before delivery.

## What the rules enforce

The shared rules in [`core/rules.md`](./core/rules.md) and thresholds in [`core/tokens/rules.json`](./core/tokens/rules.json) cover:

- Color contrast and accent usage
- Typography and headline length
- Spacing and section padding
- Button and tap-target sizing
- Mobile layout behavior
- Accessibility basics
- Reduced motion
- Copy that avoids filler, unsupported claims, and stock phrases
- Visual patterns that commonly make generated UI feel generic

What the audit checks automatically, what it only guesses, and what needs a human is listed in [`docs/audit-coverage.md`](./docs/audit-coverage.md).

The design rules are defaults, not a substitute for the user’s brand. A project can set a strictness mode (`strict`, `balanced`, `brand-first`), brand colors, and an accessibility target in `flawless.config.json` ([`docs/configuration.md`](./docs/configuration.md)). If a request intentionally breaks a rule, the agent should make that override explicit rather than changing it silently.

## Output expectations

Unless a user requests a framework or another format, page builds produce one self-contained HTML file. The file includes:

- CSS in a `<style>` tag
- Design tokens at the top of the stylesheet
- A real fallback font stack
- Responsive behavior
- Accessible focus and interaction states

When content is illustrative, the agent should identify which content is sample content in its response. Flawless does not invent statistics, reviews, prices, addresses, awards, or other factual claims.

## Repository layout

```text
SKILL.md                 Skill router and shared behavior (internal name: clean-ui, see docs/naming.md)
manifest.json            Source of truth for commands and wiring
INSTALL.md               Installation, dependencies, state storage
docs/                    Audit coverage, configuration, CSS support, browser checks, framework,
                         content, i18n, and color-vision guidance
examples/                Sample pages, before and after, transcripts, screenshots
tests/                   Unit tests and good and bad HTML fixtures
commands/<name>/         Command instructions, references, and tokens
core/rules.md            Shared design rules
core/workflow.md         Page-building workflow
core/hooks.md            Snapshot, audit, state, and reporting hooks
core/state.md            Session scheme and page state
core/tokens/             Shared CSS and threshold tokens
core/scripts/            Audit, palette, state, snapshot, build, validate, and browser-check tools
```

The command table and command wiring blocks are generated from `manifest.json`. Edit the manifest when adding or changing a command, rather than editing generated sections by hand.

## Development and validation

The scripts require Python 3.9 or newer and only the standard library (Pillow for the image tools, Playwright for the optional browser check). From the repository root:

```text
python core/scripts/build.py                  regenerate derived files
python core/scripts/validate.py               check structure, links, hooks, generated files
python -m unittest discover -s tests          run the tests
```

GitHub Actions ([`.github/workflows/ci.yml`](./.github/workflows/ci.yml)) runs all three on every push and pull request, fails if generated files are out of date, and audits the example pages.

`validate.py` checks the command structure, referenced files, command relationships, generated files, router coverage, token files, palettes, and Markdown path references.

For a page that has been changed, run the page audit with accessibility and mobile checks:

```text
python core/scripts/audit.py path/to/page.html --a11y --mobile
python core/scripts/audit.py path/to/page.html --a11y --mobile --explain
```

Optional, with Playwright installed: `python core/scripts/browser_check.py path/to/page.html` checks overflow, tap targets, keyboard focus, and reduced motion in a real browser ([`docs/browser-checks.md`](./docs/browser-checks.md)).

### Generated files

Files generated from `manifest.json` begin with a "GENERATED FILE" notice (or a generated-from line inside the wiring block of each `COMMAND.md`). Do not edit them by hand. When changing command metadata or wiring, edit [`manifest.json`](./manifest.json), run the build script, then the validator. The generated files are [`core/graph.md`](./core/graph.md), [`commands/flawless-c/tokens/command-table.md`](./commands/flawless-c/tokens/command-table.md), [`commands/palette/references/palettes.md`](./commands/palette/references/palettes.md), and the wiring block in each `COMMAND.md`.

### Adding tests

Add a page to `tests/fixtures/bad/` that breaks one rule, list the findings it must produce in `tests/fixtures/expected.json`, and run the suite. Good pages go in `tests/fixtures/good/` and must stay free of findings.

## License

[MIT](./LICENSE).
