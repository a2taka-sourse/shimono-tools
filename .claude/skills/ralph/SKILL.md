---
name: ralph
description: Orchestrated fresh-context pipeline. Runs extract → connect → update → verify with fresh context per phase via subagent spawning. Maximum quality for important sources. Triggers on "/ralph", "/ralph [source]", "full pipeline", "orchestrate processing".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## EXECUTE NOW

**Source: $ARGUMENTS**

1. Read ops/queue/queue.json for pending tasks, or use the provided source
2. For each task: spawn subagent for the current_phase, read HANDOFF output, advance queue
3. Continue until batch is done

**START NOW.**

---

# Ralph

Orchestrated processing with fresh context per phase. Each phase runs in isolation — extract gets fresh context for source analysis, connect gets fresh context for graph traversal, update gets fresh context for backward pass, verify gets fresh context for quality assessment.

## Orchestration Pattern

```
read queue → pick next task → determine current_phase
  → invoke /extract --handoff [target]    (if phase = extract)
  → OR /connect --handoff [note]          (if phase = connect)
  → OR /update --handoff [note]           (if phase = update)
  → OR /verify --handoff [note]           (if phase = verify)
  → read RALPH HANDOFF block from output
  → advance queue: current_phase → next, append to completed_phases
  → loop until batch done
```

## Phase Sequence

extract → connect → update → verify → done

## Queue Advancement

After each HANDOFF block:
```bash
jq '(.tasks[] | select(.id=="TASK_ID")).current_phase = "NEXT_PHASE" |
    (.tasks[] | select(.id=="TASK_ID")).completed_phases += ["CURRENT_PHASE"]' \
    ops/queue/queue.json > tmp.json && mv tmp.json ops/queue/queue.json
```

## When to Use Ralph vs Manual

| Situation | Use |
|-----------|-----|
| Important source (key book chapter, major design decision) | /ralph — fresh context per phase |
| Quick note from a meeting or conversation | /extract directly |
| Multiple notes in queue needing connection | /connect manually |
| Batch catch-up processing | /pipeline |

## Output

Reports each phase completion with the HANDOFF summary. Final output shows full batch completion.
