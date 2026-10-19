---
name: audit
description: Check a page against every rule and report errors and warnings; asks before fixing.
---

# /audit

Reads a page and reports what breaks the rules. It changes nothing until the user answers the fix question.

## Triggers

- `/audit` or `/audit <page>`.
- Run automatically as the post-hook after every command that changes a file (see `core/hooks.md`).

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | no (read-only) |
| Pre-hooks | none |
| Post-hooks | none |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `core/hooks.md`, `commands/audit/references/slop-audit.md`, `commands/audit/references/report-format.md`, `commands/audit/tokens/severity.json` |
| Scripts | `core/scripts/audit.py` |
| Calls | none |
| Called by | none |
| Hands off to | `/palette`, `/copy`, `/edit`, `/mobile`, `/a11y` |
| Handed off from | none |
| Requires | none |
| State read | `scheme`, `pages` |
| State written | `pages` |
<!-- wiring:end -->

## Steps

1. **Target.** Resolve the page as in `/edit`. If more than one could match, ask which.
2. **Automated pass.** `python core/scripts/audit.py <file> --a11y --mobile`. It reports the current scheme, errors (hard rules), and warnings (judgment calls). Thresholds come from `core/tokens/rules.json`.
3. **Judgment pass.** Walk `commands/audit/references/slop-audit.md` for what a script cannot judge: does the headline say what the thing is, does any element lose nothing if removed, is any section layout repeated, is copy plain.
4. **Report** in three groups using `commands/audit/references/report-format.md`: errors, warnings, passes (one line). Each item is one line with the fix and which command fixes it (`commands/audit/tokens/severity.json`).
5. **Ask one question** (`ask_user_input_v0`): fix all errors, fix selected items, or leave as is. Change nothing before the answer.
6. **On a fix request,** hand off to the owning commands: color and font items to `/palette`, copy items to `/copy`, spacing and structure items to `/edit` (layout), responsive items to `/mobile`, accessibility items to `/a11y`. Each of those runs its own snapshot and post-hooks.

## Outputs

A report. No file changes unless the user asks for fixes.

## Failure cases

- **Page not built with this skill:** report its real scheme; do not treat missing tokens as errors, only rule violations.
- **No `<style>` found (external stylesheet):** say the CSS could not be read and audit the markup only.
- **User already overrode a rule this conversation:** list it as "overridden by you" and do not count it as an error.
