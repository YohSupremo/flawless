# Flawless or clean-ui?

**Public name: Flawless.** This is the name in the README, the repository, and the slash commands (`/flawless`, `/flawless-c`).

**Internal identifier: `clean-ui`.** It remains in three places because it is an identifier, not a brand:

| Where | Why it stays |
| --- | --- |
| `name: clean-ui` in `SKILL.md` and `"name"` in `manifest.json` | Agents and uploaded skills may already refer to the skill by this name; changing it can break triggering and existing installs |
| `CLEAN_UI_STATE` and `~/.clean-ui-state.json` | Existing users have state there. Still honored |
| Comments and docstrings that say "clean-ui" | Historical |

New names added in this version: `FLAWLESS_STATE`, `FLAWLESS_PROJECT_ROOT`, `.flawless-state.json`, `flawless.config.json`. They take priority over the old ones.

## Renaming everything (the owner's decision)

If you want one name only, change these together and bump the manifest version:

1. `name:` in `SKILL.md` and `manifest.json`, and the `# Clean UI` heading in `SKILL.md`
2. The layout block in `SKILL.md` (`clean-ui/`)
3. The default state path in `core/scripts/state.py` (keep reading the old path as a fallback so nobody loses state)
4. Docstrings in `audit.py` and `palette.py`
5. Run `python core/scripts/build.py`, `python core/scripts/validate.py`, and the tests
