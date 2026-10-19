---
name: flawless-c
description: List every command with its description and an example.
---

# /flawless-c

Prints the command list. It is read-only and runs no scripts.

## Triggers

- `/flawless-c`
- `/help` (alias, same output)

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | no (read-only) |
| Pre-hooks | none |
| Post-hooks | none |
| Reads | `commands/flawless-c/references/usage.md`, `commands/flawless-c/tokens/command-table.md` |
| Scripts | none |
| Calls | none |
| Called by | none |
| Hands off to | none |
| Handed off from | none |
| Requires | none |
| State read | none |
| State written | none |
<!-- wiring:end -->

## Steps

1. Output the table in `commands/flawless-c/tokens/command-table.md` exactly as written.
2. Add one line below it: "Type a command at the start of a message. `/flawless` keeps the skill on for the whole conversation."
3. Stop. Do not run scripts, ask questions, or comment on the skill.

## Keeping the table correct

The table is generated from `manifest.json` by `python core/scripts/build.py`, so it always matches the real command set. When a command is added, renamed, or removed, edit the manifest and rebuild. `python core/scripts/validate.py` fails if the table is out of date.

## Phrasing the command

See `commands/flawless-c/references/usage.md` for how commands are recognized and how to type them.

## Failure cases

- **Table file is empty or missing:** run `python core/scripts/build.py` to regenerate it, then print it.
- **User asks about one command in detail** ("what does /edit do exactly?"): answer from that command's `COMMAND.md` in a few lines, then offer the full list. Do not print the table unasked.
- **User types a command that is not in the table:** say it is not a command and print the table.
