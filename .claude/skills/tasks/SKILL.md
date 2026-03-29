---
name: tasks
description: Manage and inspect the pipeline task queue. Show queue state, advance tasks, archive completed batches, clear stuck tasks. Triggers on "/tasks", "show queue", "what's in the pipeline", "task status".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## EXECUTE NOW

**Command: $ARGUMENTS**

Parse:
- Empty / "list": show current queue state
- "archive [batch]": archive completed batch
- "clear [task-id]": remove stuck task
- "reset [task-id]": reset task to earlier phase

**START NOW.**

---

# Tasks

Manage the unified processing queue at ops/queue/queue.json.

## Queue Display

```bash
cat ops/queue/queue.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
tasks = data.get('tasks', [])
if not tasks:
    print('Queue is empty.')
else:
    for t in tasks:
        print(f\"{t['id']:30} {t['current_phase']:15} {t['status']:10} {t.get('project','?')}\")
"
```

## Queue Operations

### Archive completed batch
Move task files for completed batch to ops/queue/archive/{date}-{batch}/

### Clear stuck task
Remove a task that's genuinely stuck (not just stalled):
```bash
jq 'del(.tasks[] | select(.id=="TASK_ID"))' ops/queue/queue.json > tmp.json && mv tmp.json ops/queue/queue.json
```

### Reset to earlier phase
```bash
jq '(.tasks[] | select(.id=="TASK_ID")).current_phase = "extract" |
    (.tasks[] | select(.id=="TASK_ID")).completed_phases = []' \
    ops/queue/queue.json > tmp.json && mv tmp.json ops/queue/queue.json
```

## Output

```markdown
## Queue State

| ID | Phase | Status | Project |
|----|-------|--------|---------|
| [id] | connect | pending | ctf |
| [id] | verify | pending | shimono |

Maintenance tasks: N
Pipeline tasks: N
Total: N
```
