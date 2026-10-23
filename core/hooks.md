# Hooks

Hooks are steps every command runs automatically. The manifest (`manifest.json`) lists which hooks each command uses under `pre_hooks` and `post_hooks`.

## pre: snapshot

Runs before a command changes a file.

`python core/scripts/snapshot.py save <file>`

Gives `/history` and `/revert` something to work with. Skipped for commands that only read.

## post: audit

Runs after a command changes a file.

`python core/scripts/audit.py <file> --a11y --mobile`

Errors must be fixed before delivering. Warnings are reported in one line. If the user has already chosen to override a rule in this conversation, report it but do not re-ask.

## post: state

Runs after audit.

`python core/scripts/state.py page <file> audit=clean` (or `audit=errors`)

If the command changed the scheme, also `python core/scripts/state.py set <key> <value>` for each changed key.

## post: report

One or two sentences saying what changed. In session mode (`active` is true), end with one line: "Audit: clean." or what was left and why.

## Order

pre: snapshot, then the command's own steps, then post: audit, state, report.

## Preview runs

A command run with `--preview` skips every hook and changes nothing. See `core/preview.md`.
