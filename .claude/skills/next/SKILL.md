---
name: next
description: Surface the most valuable next action across all three projects. Combines task queue, inbox pressure, project staleness, maintenance conditions, and goals. Recommends one specific action with rationale. Direct and opinionated — if Shimono has been untouched for 5 days, say so. Triggers on "/next", "what should I do", "what's next", "prioritize".
version: "1.0"
generated_from: "arscontexta-v1.6"
user-invocable: true
context: fork
model: sonnet
allowed-tools: Read, Grep, Glob, Bash
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary and `ops/config.yaml` for maintenance thresholds.

---

## EXECUTE NOW

**INVARIANT: /next recommends, it does not execute.** Present one recommendation with rationale. This prevents cognitive outsourcing.

**Execute these steps:**

1. Read `ops/queue/queue.json` — reconcile maintenance conditions
2. Read `self/goals.md` — current active threads per project
3. Check inbox/ for age of items
4. Check project staleness: last modified date for ctf/, shimono/, ai-lain/
5. Count pending observations (ops/observations/) and tensions (ops/tensions/)
6. Rank by consequence speed (session > multi-session > slow)
7. Output ONE recommendation with direct rationale

**START NOW.**

---

# Next

Surface the most valuable next action with direct, opinionated prioritization.

## Maintenance Condition Evaluation

For each condition, evaluate and create/close queue entries:

| Condition | Evaluation |
|-----------|------------|
| Inbox age > 3 days | `find inbox/ -name "*.md" -mtime +3` |
| Orphan notes | Notes with no incoming links in ctf/, shimono/, ai-lain/ |
| Dangling links | `grep -r '\[\[' ctf/ shimono/ ai-lain/ --include="*.md" -o` → verify targets exist |
| Observations ≥ 10 | `ls ops/observations/ \| wc -l` |
| Tensions ≥ 5 | `ls ops/tensions/ \| wc -l` |
| Hub size > 40 | Count Core Ideas entries in each index.md |
| Project staleness | `find ctf/ shimono/ ai-lain/ -name "*.md" -newer ops/queue/queue.json` |
| Stalled pipeline | Tasks in queue with current_phase not advancing |

## Project Staleness Check

```bash
# Find most recently modified file per project
find ctf/ -name "*.md" -not -name "index.md" -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1
find shimono/ -name "*.md" -not -name "index.md" -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1
find ai-lain/ -name "*.md" -not -name "index.md" -printf "%T@ %p\n" 2>/dev/null | sort -n | tail -1
```

If a project hasn't had new notes in 2+ sessions while others are active, flag it directly.

## Priority Ranking

| Priority | Triggers |
|----------|---------|
| Session (highest) | Dangling links, orphan notes, inbox overflow, stalled pipeline |
| Multi-session | Project untouched while others active, pipeline batch stalled |
| Slow | Observations threshold, hub oversizing, review needed |

## Output Format

Be direct. Don't hedge.

```markdown
## What's Next

**Recommended:** /extract [inbox/file.md] (CTF chapter on ELF format)

**Why:** Inbox has 2 items from 4 days ago. CTF is the active project and this directly feeds Defcon prep.

**Also worth knowing:**
- Shimono hasn't had new notes in 6 days while CTF and AI Lain are active — is that deliberate?
- 1 orphan note in ai-lain/ needs connection
- Queue has 2 notes pending connect phase

**If you'd rather:** /connect [[last-technique-note]] | /review (3 pending observations)
```

**Cross-project awareness:** If two projects are both active and one is clearly behind, say so. If the queue has items in one project but the other two are stalled, surface that. Proactive flagging is the job.
