---
name: pipeline
description: Run the full processing pipeline on an inbox item in one session (standard depth). Combines extract → connect → update → verify. Use for moderate-importance sources. For critical sources, use /ralph (fresh context per phase). Triggers on "/pipeline", "/pipeline [file]", "process this fully", "run full pipeline".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## EXECUTE NOW

**Target: $ARGUMENTS**

1. Run /extract on the target
2. For each note created: run /connect, then /update, then /verify
3. Report completion

**START NOW.**

---

# Pipeline

Full pipeline in one session. Standard quality trade-off — each phase gets focused attention but runs sequentially in the same context window.

## When to Use

| Source | Recommended skill |
|--------|------------------|
| Key book chapter, major design session | /ralph (fresh context per phase) |
| Regular source, moderate importance | /pipeline |
| Quick note, obvious content | /extract directly |
| Batch catch-up | /pipeline on each item |

## Phase Execution

```
1. /extract [inbox-file]
   → creates notes in project folder
   → for each note: add to queue

2. For each created note:
   /connect [note]
   /update [note]
   /verify [note]

3. Archive inbox item (move to archive/ or delete)
4. Report batch completion
```

## Quality Trade-Off

Running all phases in one session means later phases run with more context accumulated. For important sources, this degrades quality — use /ralph instead. For standard sources, it's the right balance of quality and efficiency.

## Output

```markdown
## Pipeline Complete: [source]

### Notes Created: N
- [[note 1]] — connected, updated, verified
- [[note 2]] — connected, updated, verified

### Enrichments: M
### Skipped: K

### Cross-Project Connections Found: N

Next: /next (to see what's recommended now)
```
