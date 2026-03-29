---
name: connect
description: Find connections between notes and update project hubs. Requires semantic judgment — genuine relationships only. Use after /extract creates notes, when exploring cross-project connections, or when a topic needs synthesis. Triggers on "/connect", "/connect [note]", "find connections", "update project hub", "connect these notes".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0 — before any processing)

Read `ops/derivation-manifest.md` for vocabulary mapping and `ops/config.yaml` for processing depth.

**Processing depth:**
- `deep` — Full dual discovery (project hub + keyword search). Evaluate every candidate. Multiple passes. Synthesis detection. Bidirectional link evaluation.
- `standard` — Top 5-10 candidates. Standard evaluation. Bidirectional check for strong connections only.
- `quick` — Single pass, obvious connections only.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If note name provided: find connections for that note
- If `--handoff`: output RALPH HANDOFF block at end
- If empty: find recently created notes or ask which note to connect
- If "recent": connect all notes created today

**Execute these steps:**

1. Read the target note fully
2. Search ALL project folders (ctf/, shimono/, ai-lain/) for related notes — cross-project connections are explicitly the goal
3. Evaluate each candidate: genuine connection only if you can complete "[[A]] connects to [[B]] because [specific reason]"
4. Add inline wiki-links where connections pass the articulation test
5. Update relevant project hub (index.md) with the note
6. Report what was connected and why

**START NOW.**

---

# Connect

Find connections, weave the knowledge graph, update project hubs. Cross-project connections are the most valuable ones — a CTF memory technique connecting to AI Lain's RAG design is worth more than ten same-domain connections.

## Philosophy

**The network IS the knowledge.**

Individual notes are less valuable than their relationships. A note with fifteen incoming links is an intersection of fifteen lines of thought. Cross-project connections — CTF ↔ AI Lain, Shimono ↔ AI Lain — reveal structural parallels that neither domain would surface alone.

This is not keyword matching. You are building a traversable knowledge graph.

**Quality over speed. Explicit over vague.**

Every connection must pass the articulation test: "[[A]] connects to [[B]] because [specific reason]." "Related" is not a relationship.

## Discovery Process

### Step 1: Search ALL Project Folders

```bash
# Find notes related to a concept across all projects
grep -r "concept" ctf/ shimono/ ai-lain/ --include="*.md" -l
```

Do not limit search to the note's home project. The best connections cross projects.

**Valuable cross-project patterns to watch for:**
- CTF memory architecture ↔ AI Lain RAG indexing
- Shimono simulation pipeline ↔ AI Lain character pipeline
- CTF assembly knowledge ↔ AI Lain implementation notes
- Shimono RAG design ↔ AI Lain RAG design

### Step 2: Browse Project Hubs

Read the relevant project hub(s) for curated context. What's already connected in this area?

### Step 3: Evaluate Candidates

**The Articulation Test:**
Complete this sentence: `[[note A]] connects to [[note B]] because [specific reason]`

If you cannot fill in [specific reason] with something substantive, the connection fails.

**Valid relationship types:**
- `extends` — adds a dimension to the other note
- `grounds` — provides the foundation or mechanism
- `contradicts` — creates a genuine tension
- `exemplifies` — concrete instance of the other note
- `synthesizes` — emerges from combining both
- `enables` — makes the other note actionable

**Reject if:**
- Connection is "related" without specifics
- Keyword match only, no semantic depth
- Would confuse more than clarify

### Step 4: Add Inline Connections

The wiki link IS the argument. The title works as prose when linked.

Good: `Since [[episodic chunking preserves emotional continuity]], the memory layer needs separate buckets for emotional and factual recall.`

Bad: `This relates to [[episodic chunking preserves emotional continuity]].`

If you catch yourself writing "relates to" or "see also" — STOP. Restructure so the claim does the work.

**Relevant Notes format:**
```yaml
relevant_notes:
  - "[[other note]] — extends this by adding the temporal dimension"
  - "[[another note]] — provides the mechanism this note depends on"
```

### Step 5: Update Project Hub

Every note belongs in at least one project hub (ctf/index.md, shimono/index.md, ai-lain/index.md). Add it to Core Ideas with a context phrase explaining WHY it belongs.

If the note spans multiple projects, add it to all relevant hubs.

**Hub size check:** After updating, count entries in Core Ideas. If approaching 40, note it: "project hub approaching split threshold."

## Synthesis Opportunity Detection

While evaluating connections, watch for:
- Two notes making complementary arguments that together imply a higher-order claim
- A pattern appearing across 3+ notes that hasn't been named
- A cross-project structural parallel worth documenting

When you detect this: note it in output, do NOT create the synthesis note during connect — flag it for future work.

## Quality Gates

1. **Articulation test** — every connection passes "[[A]] connects to [[B]] because [specific reason]"
2. **Prose test** — every inline link reads as natural prose
3. **Bidirectional check** — explicitly decide if A→B implies B→A
4. **Hub coherence** — after updating a hub, does the synthesis still hold?
5. **Link verification** — every wiki link target exists (`ls ctf/"note name.md"`)

## Output Format

```markdown
## Connections Complete: [[note name]]

### Discovery Trace

Project folders searched: ctf/, shimono/, ai-lain/
- grep "concept" — found: [[note A]], [[note B]]
- Project hub ctf/index.md — relevant context: X
- Cross-project check — found: [[ai-lain note]] with RAG pattern overlap

### Connections Added

- -> [[target]] — [relationship]: [why]
- <- [[incoming]] — [relationship]: [why]
- inline: added link to [[note]] in paragraph about X

### Project Hub Updates

**[[ctf/index]]**
- Added [[note]] to Core Ideas — [contribution]
- Agent note: [navigation insight]

### Cross-Project Connections Found

- [[ctf/technique]] ↔ [[ai-lain/component]] — [structural parallel]

### Synthesis Opportunities

[Notes that could combine into a higher-order claim]

### Next Step

[/update [note-title] — suggested]
```

---

## Handoff Mode (--handoff flag)

```
=== RALPH HANDOFF: connect ===
Target: [[note name]]

Work Done:
- Connections added: N (articulation test: PASS)
- Project hub updates: [[hub-name]]
- Cross-project connections: M
- Synthesis opportunities: [count or NONE]

Files Modified:
- [project]/[note name].md
- [project]/index.md

Queue Updates:
- Advance phase: connect -> update
=== END HANDOFF ===
```
