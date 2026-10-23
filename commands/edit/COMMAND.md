---
name: edit
description: Change an existing page while keeping its scheme; prompts for a category when no change is described.
---

# /edit

Changes part of an existing page. The scheme (base, surface, text, accent, fonts, radius, spacing scale) stays exactly as it is unless the change is about the scheme.

## Triggers

- `/edit`: no change described. Ask which category.
- `/edit <change>`: "/edit make the headline shorter". Infer the category, skip the category question.
- Under `/flawless`, plain change requests about an existing page route here.

<!-- wiring:start -->
## Wiring

_Generated from `manifest.json` by `core/scripts/build.py`. Edit the manifest, not this block._

| | |
|---|---|
| Modifies files | yes |
| Pre-hooks | `snapshot` |
| Post-hooks | `audit`, `state`, `report` |
| Reads | `core/rules.md`, `core/tokens/rules.json`, `core/hooks.md`, `core/state.md`, `commands/edit/references/categories.md`, `commands/edit/references/edit-examples.md`, `commands/edit/tokens/categories.json`, `core/preview.md` |
| Scripts | `core/scripts/audit.py`, `core/scripts/snapshot.py`, `core/scripts/state.py` |
| Calls | `/palette`, `/copy`, `/section`, `/mobile`, `/animate`, `/match` |
| Called by | none |
| Hands off to | `/revert` |
| Handed off from | `/audit`, `/ref` |
| Requires | none |
| State read | `active`, `scheme`, `pages` |
| State written | `scheme`, `pages` |
<!-- wiring:end -->

## Target

The page the user names, links, attaches, or has been working on. If more than one page could match, ask which one in a single question. For a published artifact, read it into the container first. For pasted HTML, save it to a file first.

## Steps

1. **Pre-hook.** Snapshot the file. Run `python core/scripts/audit.py <file>`; this prints the current scheme and any existing violations.
2. **No change described?** Show the scheme in a few lines and the audit result, then ask which categories to change (`ask_user_input_v0`, multi-select, the four options in `commands/edit/tokens/categories.json`). After the answer, ask one follow-up per chosen category (see `commands/edit/references/categories.md`). One follow-up round only. If the user types a change in their own words instead of picking, use it and skip questions.
3. **Change described?** Infer the category from `categories.json` keywords and go to step 4.
4. **Route by category** (what to call):
   - *Colors and fonts:* run `/palette` in apply mode for color changes; for fonts, change only `--font-display` and `--font-body` and the Google Fonts link. Change `:root` tokens only, plus dark-mode tokens if the page has them.
   - *Copy:* run `/copy` for the named part. Change no other text.
   - *Layout and spacing:* adding a section calls `/section`. Responsive fixes call `/mobile`. Anything else (order, alignment, spacing) is edited directly on the scale in `core/tokens/rules.json`.
   - *Components and images:* buttons, cards, and `--radius` (one value everywhere, 0 to 6px) are edited directly. Motion calls `/animate`. Adding or swapping a photo calls `/match` afterward so the palette still fits it.
5. **Rule check on the requested change.** If it would break a rule in `core/rules.md` (blue-violet hue, any gradient, a second accent, banned symbol, invented content, flowery copy), do not apply it silently. Ask once with two options: keep the scheme with a compliant version (describe it concretely), or make the change as requested. Follow the answer. Remember an override for the rest of the conversation.
6. **Apply only the requested change,** using existing tokens. Do not restyle anything the user did not mention.
7. **Post-hooks.** Audit, state update, report in one or two sentences.
8. **Pre-existing violations.** If the audit before the edit already had errors, apply the change first, then list them in one line and ask whether to fix them (hand off to `/audit` fix flow). Do not fix them unprompted.

## Scheme changes

If the user asks for a scheme change ("/edit new accent color"), treat it as the request. Pick values under the color rules (via `/palette`), change `:root` tokens only, update the session scheme in state, and confirm what moved.

## Preview mode

`/edit --preview ...` shows the proposed change and its audit result without writing anything, then asks whether to apply it. Full rules: `core/preview.md`.

## Outputs

The same file, edited, with a snapshot of the previous version. Published artifacts: send the change as edits on the publish call.

## Failure cases

- **Edit would change two categories at once:** do them in the order colors and fonts, copy, layout, components, and audit once at the end.
- **The page was not made by this skill:** run the audit, report the scheme it actually has, and edit within it. Do not convert it to this skill's tokens unless asked.
- **User wants to undo:** hand off to `/revert`.
