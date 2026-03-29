---
description: Common issues and resolution patterns
type: manual
generated_from: "arscontexta-1.0.0"
---

# Troubleshooting

## Orphan Notes

Notes with no incoming links are invisible to graph traversal.

**Detect:** `/graph orphans`

**Fix:** Run `/connect [orphan-note]` — search across all three project folders for connections. If truly disconnected, add it to the relevant project hub manually.

## Dangling Links

Wiki links pointing to notes that no longer exist (renamed or deleted).

**Detect:** `/graph dangling`

**Fix:** Either create the missing note, or update the link to point to the renamed note. Use `/refactor` for coordinated renames that update all references.

## Inbox Overflow

Too many items accumulating without processing.

**Detect:** `/next` will flag this proactively when inbox items are 3+ days old.

**Fix:** Run `/extract` on the oldest items first. If overwhelmed, use `/pipeline --quick` for catch-up processing.

## Project Staleness

A project that hasn't had new notes in multiple sessions while others are active.

**Detect:** `/next` will surface this directly: "Shimono hasn't had new notes in 6 days while CTF is active — is that deliberate?"

**Response options:** Either pick it up, or explicitly note in self/goals.md that it's deliberately deferred.

## Schema Drift

Notes missing required fields (description, type, status, topics).

**Detect:** `/validate [project]`

**Fix:** Run `/verify [note]` for each violation. The validate-note.sh hook prevents this at creation time; /validate catches drift that accumulates post-creation.

## Skills Not Available

Skills created during setup aren't discoverable in the current session.

**Fix:** Restart Claude Code. Skills require a restart to appear in the skill index.

## Cross-Project Connections Not Found

The connect skill only searched the home project folder.

**Fix:** This shouldn't happen — the connect skill is instructed to search ALL project folders. If it's not doing this, run `/remember "connect skill not searching cross-project"` to log the friction, then manually check the other project folders.

## Vault Hook Errors

Hooks failing silently or not running.

**Check:** Verify `.arscontexta` exists in the vault root. Hooks only run when this file is present.

**Check:** Ensure hook scripts are executable: `chmod +x .claude/hooks/*.sh`

**Check:** The vault's `.claude/settings.json` must be the settings file in scope when Claude Code starts in the vault directory.

## See Also

- [[skills]] — command reference
- [[meta-skills]] — /remember for capturing friction
- [[manual]] — back to hub
