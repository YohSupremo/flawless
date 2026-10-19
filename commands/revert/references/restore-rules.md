# Restore rules

- `/revert` restores the highest numbered version. `/revert N` restores vN.
- A restore writes the file's current content as a new version first, then copies vN over the page.
- After a restore, `state.py init --scheme-from` re-syncs the session scheme with the page.
- Restoring does not delete newer versions. History only grows.
- For published artifacts, the restored file must be published to the same URL to take effect.
