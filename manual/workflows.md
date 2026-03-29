---
description: Processing pipeline, maintenance cycle, and session rhythm
type: manual
generated_from: "arscontexta-1.0.0"
---

# Workflows

## Processing Pipeline

Every piece of content flows through the same path:

```
inbox/ → /extract → /connect → /update → /verify → project folder
```

**capture** (inbox/) → **extract** (notes created) → **connect** (graph woven) → **update** (old notes updated) → **verify** (quality gate)

### When to Use Ralph vs Pipeline vs Manual

| Source Importance | Recommended Approach |
|------------------|---------------------|
| Key book chapter, major design session | `/ralph` — fresh context per phase |
| Regular source, moderate importance | `/pipeline` — one session, full pipeline |
| Quick idea, obvious content | `/extract` directly |
| Batch catch-up | `/pipeline` on each inbox item |

### Cross-Project Connections

Run `/connect` with scope = all folders. Don't limit to the home project:
- CTF memory analysis → AI Lain RAG architecture
- Shimono simulation pipeline → AI Lain character pipeline
- Assembly study → CTF challenge techniques

## Session Rhythm

**Orient → Work → Persist**

### Orient (start of every session)
1. The session-orient.sh hook injects vault structure and inbox state automatically
2. Read self/goals.md for current active threads
3. Run `/next` for priority recommendation — it will flag what's stalled or competing

### Work
- Focus on one task. Write down discoveries as notes before moving on.
- If you're in CTF work and you notice a connection to AI Lain — add the wiki link immediately. It won't exist next session.

### Persist (end of every session)
- Update self/goals.md with current active threads
- The Stop hook captures the session transcript to ops/sessions/ automatically
- Commit is handled by auto-commit.sh after writes

## Maintenance Cycle

Maintenance is condition-based, not time-based. `/next` evaluates these conditions and surfaces them proactively:

| What Gets Flagged | Condition |
|-------------------|-----------|
| Orphan notes | Any note with no incoming links |
| Inbox overflow | Items older than 3 days |
| Observation backlog | 10+ pending observations |
| Tension backlog | 5+ pending tensions |
| Project staleness | Project not touched in 2+ sessions while others are active |
| Hub oversizing | Project hub Core Ideas exceeds 40 entries |

You don't manage these manually. When `/next` says "Shimono hasn't had new notes in 6 days," that's the system doing its job.

## Content Pipeline (Shimono + AI Lain)

Notes tagged `content_potential: true` in shimono/ are candidates for video/podcast debate segments. When enough content-ready notes accumulate on a topic, run `/connect` to find the debate angle, then use the content-segment template to structure the segment.

## See Also

- [[skills]] — command reference
- [[configuration]] — adjusting pipeline settings
- [[manual]] — back to hub
