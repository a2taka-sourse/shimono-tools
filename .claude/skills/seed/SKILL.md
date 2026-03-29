---
name: seed
description: Bootstrap processing for a new source. Creates inbox entry with provenance, queues for extraction, and sets up the task file. Use when starting to process a new book chapter, challenge set, or design session. Triggers on "/seed", "/seed [source]", "start processing this", "add this to the pipeline".
user-invocable: true
allowed-tools: Read, Write, Bash
context: fork
---

## EXECUTE NOW

**Source: $ARGUMENTS**

1. Create inbox entry with provenance metadata
2. Create task file in ops/queue/
3. Add entry to ops/queue/queue.json
4. Report: what was created, what project it serves, next step

**START NOW.**

---

# Seed

Bootstrap a new source into the processing pipeline. The starting point before /extract.

## What Seed Creates

1. **Inbox entry** — `inbox/YYYYMMDD-{source-slug}.md` with provenance YAML
2. **Task file** — `ops/queue/{source-slug}-001.md` as the shared state for all pipeline phases
3. **Queue entry** — in ops/queue/queue.json with status: pending, current_phase: extract

## Queue Entry Format

```json
{
  "id": "source-slug-001",
  "type": "extract",
  "status": "pending",
  "target": "inbox/YYYYMMDD-source-slug.md",
  "batch": "source-slug",
  "created": "2026-03-29T00:00:00Z",
  "current_phase": "extract",
  "completed_phases": [],
  "project": "ctf"
}
```

## Task File Format

```markdown
# Batch: {source-slug}

Source: {original source description}
Project: {ctf | shimono | ai-lain}
Created: {date}

## Extract Notes
(populated by /extract)

## Connect
(populated by /connect)

## Update
(populated by /update)

## Verify
(populated by /verify)
```

## Output

```markdown
## Seeded: [source]

Project: [ctf | shimono | ai-lain]
Inbox: inbox/[filename].md
Task file: ops/queue/[batch]-001.md
Queue: 1 entry added (current_phase: extract)

Next: /extract inbox/[filename].md
```
