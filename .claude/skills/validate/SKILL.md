---
name: validate
description: Batch schema validation across all project folders. Checks required fields, enum values, topics footer, description quality. Use for periodic health maintenance. Triggers on "/validate", "validate schema", "check all notes", "batch validate".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse:
- Empty: validate all project folders (ctf/, shimono/, ai-lain/)
- `ctf | shimono | ai-lain`: validate that project only
- `--fix`: attempt to fix simple violations automatically

**Steps:**

1. For each target folder, scan all .md files
2. Check: description present, type valid, status valid, topics non-empty
3. Report violations grouped by severity

**START NOW.**

---

# Validate

Batch schema validation. The PostToolUse hook catches single-note violations at creation time. This catches drift that accumulates over time.

## Checks

```bash
# Missing descriptions
rg -L '^description:' ctf/ shimono/ ai-lain/ --include="*.md" --glob='!index.md'

# Empty topics
rg '^topics: \[\]' ctf/ shimono/ ai-lain/ --include="*.md"

# Missing type
rg -L '^type:' ctf/ shimono/ ai-lain/ --include="*.md" --glob='!index.md'

# Check description is not identical to filename
# (manual review for this one)
```

## Output Format

```markdown
## Validation Report

### CTF (N notes)
[PASS | N violations]
- [note path]: missing description
- [note path]: empty topics

### Shimono (N notes)
[PASS | N violations]

### AI Lain (N notes)
[PASS | N violations]

### Summary
Total violations: N
Recommended action: /verify [note] for each violation
```
