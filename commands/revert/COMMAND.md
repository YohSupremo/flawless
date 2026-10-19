---
name: revert
description: Restore the previous version of a page, or a numbered one.
---

# /revert

Undoes the last change (or goes back to a chosen version). Needs `/history` information to know what exists.

## Triggers

- `/revert`: restore the latest snapshot.
- `/revert <N>`: restore version N.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/hooks.md`, `core/state.md`, `commands/revert/references/restore-rules.md`, `commands/revert/tokens/revert-message.md` |
| Scripts | `core/scripts/snapshot.py`, `core/scripts/state.py` |
| Calls | none |
| Called by | none |
| Hands off to | none |
| Handed off from | `/edit` |
| Requires | `/history` |
| State read | `pages`, `scheme` |
| State written | `scheme`, `pages` |
<!-- wiring:end -->

## Steps

1. **Target.** Resolve the page; ask if more than one could match.
2. **Check versions** as `/history` does. If none exist, say so and stop.
3. **Restore.** `python core/scripts/snapshot.py restore <file> [N]`. The script saves the current file first, so the revert can be undone with another `/revert`.
4. **Published artifact:** publish the restored file to the same link so the page matches.
5. **State.** Re-read the scheme from the restored file with `python core/scripts/state.py init --scheme-from <file>` so the session scheme matches what is now on the page. Tell the user if the scheme changed.
6. **Post-hooks:** audit (report, do not fix), state, report in one sentence: "Restored v2. The change before it is saved as v5."

## Rules

- Never revert without a target version that exists.
- Never revert more than the user asked for. `/revert` is one step back, not a reset to v1.
- If the user asks to undo a revert, restore the version saved just before it.

## Failure cases

- **Scheme mismatch after revert:** the session scheme and the restored page disagree. Say which, and ask which to keep (`/palette` apply to re-sync, or leave).
- **Version file missing:** report which version is missing and list what remains.
