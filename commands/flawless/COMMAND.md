---
name: flawless
description: Turn the skill on for the whole conversation, and manage session mode (status, off).
---

# /flawless

Switches clean-ui on for the rest of the conversation. After this, every UI request follows the rules without being asked, all commands share one session scheme, and every file is audited before delivery.

## Triggers

- `/flawless`: turn on.
- `/flawless status`: print the session scheme, the pages built, and each page's last audit result.
- `/flawless off`: turn off.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | no (read-only) |
| Pre-hooks | none |
| Post-hooks | none |
| Reads | `core/rules.md`, `core/state.md`, `core/hooks.md`, `commands/flawless/references/session-mode.md`, `commands/flawless/tokens/session-template.json` |
| Scripts | `core/scripts/state.py`, `core/scripts/palette.py` |
| Calls | `/palette` |
| Called by | none |
| Hands off to | none |
| Handed off from | none |
| Requires | none |
| State read | `active`, `scheme`, `pages` |
| State written | `active`, `scheme` |
<!-- wiring:end -->

## Steps: `/flawless`

1. **Check for an existing scheme.** If a page is attached or was built earlier in the conversation, run `python core/scripts/state.py init --scheme-from <page>` and use that scheme. Do not ask about colors.
2. **If the message already includes a request, a brand, or colors,** take them as given and go straight to the request. Skip the question.
3. **Otherwise ask one question** (use `ask_user_input_v0`): how should the session get its colors? Options: use my own colors, pick a palette, decide when the first page is built.
   - *Own colors:* ask for hex values, then run `core/scripts/palette.py`. If a value is in the banned hue range, say so and ask keep-or-override.
   - *Pick a palette:* call `/palette` in suggest-only mode (three options for the stated subject, or three general ones if no subject yet).
   - *Decide later:* record nothing; the first `/new` or build sets the scheme.
4. **Record the scheme** with `state.py set` for each key, then `state.py flag active on`. Also write the scheme in plain words in your reply so it survives if the state file is lost.
5. **Reply in two lines:** the skill is on, and the scheme (or "scheme set on first build"). Then list nothing else.

## Steps: `/flawless status`

Run `python core/scripts/state.py show`. Print the scheme (base, text, accent, fonts, radius), then the pages with their last audit result. If state is missing, say so and rebuild from the newest page. Print nothing else.

## Steps: `/flawless off`

Run `state.py flag active off`. Say the skill is off. Stop applying session rules (auto-audit line, session scheme reuse for new pages). Typed commands still work.

## What session mode changes

Rules for the active period are in `commands/flawless/references/session-mode.md`. In short: every UI request is handled by the skill; new pages reuse the session scheme; post-hooks run on every file; overrides are asked once and remembered.

## Limits to state if asked

The session lasts as long as this conversation. A new conversation needs `/flawless` again. In a very long conversation, retype `/flawless` to refresh the rules.

## Failure cases

- **State file missing:** rebuild from the newest page, or from the plain-words scheme given earlier in the conversation.
- **User gives a blue-violet brand color:** do not silently swap it. Offer the closest compliant hue and let the user decide.
- **User types `/flawless` when already on:** say it is already on and show `status`.
