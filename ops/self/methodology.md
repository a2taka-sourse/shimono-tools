---
description: How I process, connect, and maintain knowledge across three parallel projects
type: moc
---

# methodology

## Principles

- **Prose-as-title:** Every note is a proposition. "Assembly notes" is not a title. "x86 stack frame layout determines where local variables live relative to RBP" is a title.
- **Wiki links as connections:** The link IS the argument. `since [[episodic chunking preserves emotional continuity]]` means something. "See also" means nothing.
- **Pipeline discipline:** inbox/ first, then extract, connect, update, verify. Never write directly to project folders.
- **Cross-project connections are the point:** When a CTF technique and a Shimono simulation decision share a structural pattern, that connection is more valuable than either note alone.
- **Content pipeline awareness:** Notes in shimono/ and ai-lain/ are also raw material for video/podcast content. Design decisions that get debated on air need especially clear rationale in their notes.

## Processing Cycle

### For technical source material (books, papers, challenge descriptions)
1. Capture to inbox/ with a note about what project it serves and why it matters
2. `/arscontexta:extract` — pull out technique notes or study notes with specific, arguable titles
3. `/arscontexta:connect` — search ALL project folders for connections, not just the home project
4. `/arscontexta:update` — check what older notes should reference this
5. `/arscontexta:verify` — cold-read test, schema check, link check

### For design decisions (Shimono, AI Lain)
1. Capture the decision being made and the alternatives considered to inbox/
2. `/arscontexta:extract` — one design-decision note per decision, not per topic
3. `/arscontexta:connect` — connect to related design decisions, simulation notes, architecture decisions
4. Check for cross-project patterns (a Shimono RAG decision may echo an AI Lain architecture choice)
5. `/arscontexta:verify`

### For CTF challenges
1. Document the challenge in inbox/ during solving
2. Post-solve: `/arscontexta:extract` — extract the technique used, not just the solution
3. Link the technique note to the challenge note; both get connections to any related technique notes
4. Update the CTF project hub with the new technique

## Session Rhythm

Orient → Work → Persist. Every session.

**Orient:** Read self/ (identity, methodology, goals), check reminders, run `/arscontexta:next` for priority surfacing. Be concrete: which project needs attention, what's in the inbox, what's stalled.

**Work:** Focus on one task. Discoveries become future tasks, not immediate tangents. When something good surfaces, write it down before moving on.

**Persist:** Update goals.md, commit new notes, ensure project hubs reference new notes.

## Cross-Project Connections

When connecting notes, always run `/arscontexta:connect` with scope = all project folders. Cross-project connections are explicitly tracked. Valuable patterns:
- CTF memory architecture ↔ AI Lain RAG design
- Shimono simulation pipeline ↔ AI Lain RAG pipeline
- Assembly study ↔ CTF challenge techniques

When a note spans multiple projects, list all relevant project hubs in its Topics footer.

---

Topics:
- [[identity]]
- [[goals]]
