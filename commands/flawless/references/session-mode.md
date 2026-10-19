# Session mode rules

While `active` is true:

1. **Scope:** any request that produces or changes UI is handled by this skill. That includes "make a login page", "add a navbar", "fix this button", pasted HTML, and screenshots. Non-UI questions are answered normally with no mention of the skill.
2. **One scheme:** the session scheme (base, surface, text, accent, fonts, radius) is used for every page and component. It changes only through `/palette`, `/edit`, or an explicit color or font request.
3. **Hooks always run:** snapshot before changes, audit, state update, and report after.
4. **Audit line:** every reply that delivers a file ends with "Audit: clean." or the leftover items and why.
5. **Overrides:** rules are defaults. When a request breaks one, ask keep-or-override once. If the user overrides, record it in the conversation and do not re-ask for the same override.
6. **Commands:** all commands work without setup. Commands that offer choices use one round of `ask_user_input_v0`.
7. **Drift check:** if the conversation is long and earlier pages used a different scheme, say so before building and ask which to use.

## Ending

`/flawless off` ends the mode. The scheme stays in state but is no longer applied automatically.
