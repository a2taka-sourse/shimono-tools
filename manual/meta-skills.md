---
description: Deep guide to /review, /remember, /arscontexta:ask, and /arscontexta:architect
type: manual
generated_from: "arscontexta-1.0.0"
---

# Meta-Skills

Meta-skills are for the system itself, not for the domain content.

## /review (formerly /rethink)

**What:** Triages accumulated observations and tensions. Detects patterns. Proposes system changes.

**When to use:** When `/next` flags 10+ observations or 5+ tensions. Or when something feels off and you want to check if the system has drifted.

**Modes:**
- `/review` — full review (drift check + triage all pending)
- `/review drift` — just check if CLAUDE.md has drifted from ops/methodology/
- `/review triage` — just triage pending items, skip pattern detection

**What it does NOT do:** Auto-implement changes. All proposals require your approval.

## /remember

**What:** Captures friction, corrections, and methodology learnings immediately.

**When to use:** When something goes wrong that shouldn't, or when you want the system to always/never do something.

**Use cases:**
- "The description validation is flagging false positives on Shimono notes" → friction observation
- "Always check cross-project connections before declaring a note done" → CLAUDE.md directive
- "The connect skill isn't finding CTF-to-AI Lain links" → process gap

For CLAUDE.md directives, /remember proposes the change and waits for approval.

## /arscontexta:ask

**What:** Queries the 249-note research knowledge base backing this vault's design.

**When to use:** When you want to understand WHY a design choice was made, or want research backing for a methodology question.

**Examples:**
- `/arscontexta:ask why is moderate granularity better than atomic for design decisions?`
- `/arscontexta:ask what's the research on condition-based vs time-based maintenance?`
- `/arscontexta:ask how do cross-domain connections affect knowledge graph value?`

Also queries ops/methodology/ for your vault's own self-knowledge.

## /arscontexta:architect

**What:** Research-backed configuration advice. Reads your derivation.md and proposes specific changes.

**When to use:** When you want to evolve the system — add semantic search, restructure a project, adjust processing depth.

**Never auto-implements.** All proposals require approval.

**Good times to run it:**
- After 50+ notes — get feedback on how the vault is developing
- When a project scales significantly (Shimono content pipeline gets busy)
- When adding a new project domain

## ops/methodology/ (System Self-Knowledge)

Browse directly or query with /arscontexta:ask:

```bash
ls ops/methodology/
cat ops/methodology/derivation-rationale.md
```

This folder records why the vault was configured the way it was. When you wonder "why does the pipeline work this way?", the answer is here.

## See Also

- [[workflows]] — how meta-skills fit into the maintenance cycle
- [[configuration]] — adjusting settings
- [[manual]] — back to hub
