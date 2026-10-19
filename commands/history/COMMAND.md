---
name: history
description: List the saved versions of a page.
---

# /history

Read-only. Shows what `/revert` can restore.

## Triggers

- `/history` or `/history <page>`.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | no (read-only) |
| Pre-hooks | none |
| Post-hooks | none |
| Reads | `core/hooks.md`, `commands/history/references/versioning.md`, `commands/history/tokens/history-format.md` |
| Scripts | `core/scripts/snapshot.py` |
| Calls | none |
| Called by | none |
| Hands off to | none |
| Handed off from | none |
| Requires | none |
| State read | `pages` |
| State written | none |
<!-- wiring:end -->

## Steps

1. **Target.** Resolve the page; ask if more than one could match.
2. **List.** `python core/scripts/snapshot.py list <file>`. Versions are stored beside the file in `<name>.history/vN.html`.
3. **Report** as a short numbered list: version number, and the command that created it if it is known from this conversation (for example "v3 before /edit radius"). Do not invent descriptions you do not know.
4. **Offer** one line: "`/revert` restores the latest, or `/revert 2` restores a specific one."

## How versions are made

Every command that changes a file runs the snapshot pre-hook (`core/hooks.md`) before it edits. A `/revert` also saves the current state first, so a revert can itself be undone.

## Failure cases

- **No versions:** say none are saved yet; versions begin with the first change made through this skill.
- **Container reset:** history files live in the working container and may be gone in a new session. Say so if the list is empty but the user expects versions. A published artifact keeps only its current published state.
