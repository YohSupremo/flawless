# Flawless

Flawless is an agent skill for building web interfaces that feel deliberate, readable, and human-made. It helps an AI assistant create or refine landing pages, product pages, dashboards, components, and other UI while keeping the visual system focused:

- One clear purpose per page
- One accent color and a restrained palette
- Direct, plain-language copy
- Tight spacing and a small radius scale
- Responsive, accessible layouts
- No gradients, filler badges, invented claims, or generic AI-style copy

Flawless is a collection of skill instructions, command references, design tokens, and Python validation scripts. It is not a web framework and does not ship a runtime application.

## Who this is for

Use Flawless when you want an AI coding assistant to:

- Build a new page from a short brief
- Improve an existing page without losing its visual scheme
- Turn a reference image into a new, original direction
- Review copy, accessibility, mobile behavior, motion, or visual consistency
- Keep a page’s design decisions consistent across a conversation

The skill works best with an agent environment that supports skill files, slash commands, and file editing.

## Getting started

1. Make this directory available to your agent as a skill.
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

Commands are case-insensitive. `/help` is an alias for `/flawless-c`.

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

The design rules are defaults, not a substitute for the user’s brand. If a request intentionally breaks a rule, the agent should make that override explicit rather than changing it silently.

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
SKILL.md                 Skill router and shared behavior
manifest.json            Source of truth for commands and wiring
commands/<name>/         Command instructions, references, and tokens
core/rules.md            Shared design rules
core/workflow.md         Page-building workflow
core/hooks.md            Snapshot, audit, state, and reporting hooks
core/state.md            Session scheme and page state
core/tokens/             Shared CSS and threshold tokens
core/scripts/             Audit, palette, state, snapshot, and build tools
```

The command table and command wiring blocks are generated from `manifest.json`. Edit the manifest when adding or changing a command, rather than editing generated sections by hand.

## Development and validation

The scripts require Python 3. From the repository root, regenerate derived documentation and validate the skill:

```text
python core/scripts/build.py
python core/scripts/validate.py
```

`validate.py` checks the command structure, referenced files, command relationships, generated files, router coverage, token files, palettes, and Markdown path references.

For a page that has been changed, run the page audit with accessibility and mobile checks:

```text
python core/scripts/audit.py path/to/page.html --a11y --mobile
```

When changing command metadata or wiring, update [`manifest.json`](./manifest.json), run the build script, then run the validator. Keep generated files such as [`core/graph.md`](./core/graph.md) and [`commands/flawless-c/tokens/command-table.md`](./commands/flawless-c/tokens/command-table.md) in sync.

## License

No license file is currently included in this repository. Add one before distributing Flawless outside your own projects.
