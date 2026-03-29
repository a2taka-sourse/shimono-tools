---
description: Why each configuration dimension was chosen — the reasoning behind initial system setup
category: derivation-rationale
created: 2026-03-29
status: active
---

# derivation rationale for multi-project vault

## Domain

The user runs three parallel long-term projects: CTF/Security (working toward Defcon CTF, Forensics focus), 下腦 world-building (fictional planet, NeuralGCM/JAX simulation, YouTube/podcast output), and AI character system (Love Plus+ resurrection as locally-running AI, Serial Experiments Lain aesthetic). There is deliberate cross-domain connection: CTF memory techniques inform RAG architecture, simulation pipelines inform AI character pipelines.

## Dimension Choices

**Granularity: Moderate.** The user's projects operate in phases with convergence loops. Design decisions need context; they're not atomic claims. Techniques are closer to atomic, but they need enough surrounding context (when to apply, what they solve) that pure atomic granularity would fragment them. Moderate granularity: one decision or technique per note, with enough body to be self-contained.

**Organization: Light hierarchy.** Three project domains are genuinely distinct (different note types, different vocabularies, different output targets). Flat within each project, light hierarchy across via project folder structure. The shared wiki-link namespace enables cross-project connections without path prefixes.

**Linking: Explicit.** The user confirmed: "yes, track cross-project connections explicitly." Wiki links across project folders (ctf/ ↔ ai-lain/ ↔ shimono/) are the mechanism. No qmd/semantic search configured; explicit links are sufficient for a focused multi-project workspace.

**Processing: Heavy.** Trial-and-error processes become content (YouTube/podcast). Japanese technical books are source material. CTF challenges produce technique extraction. Every project generates note-worthy material that requires transformation, not just storage. The generation effect is especially important here — content that reaches video/podcast audiences needs to have been genuinely processed, not just captured.

**Navigation: 3-tier.** Three distinct project domains + cross-cutting patterns + vault root index. Growing multi-project volume (each project active, each generating notes) requires at least 3 tiers to remain navigable. Project hubs emerge naturally; topic sub-MOCs emerge when a hub exceeds ~35 notes.

**Maintenance: Active condition-based.** The user explicitly requested proactive priority surfacing: "I want the agent to proactively flag what's competing for attention and what's stalled, not wait for me to ask." Active condition-based maintenance with direct priority reporting is the configuration that meets this requirement.

**Schema: Moderate-dense.** Three project types with genuinely different queryable fields. CTF needs category (forensics/assembly/network), status (learning/practiced/solid), challenge links. Shimono needs domain (climate/terrain/society), simulation_ref, status (proposed/accepted/implemented). AI Lain needs component (rag/ui/api/memory/aesthetic), status (planned/in-progress/done/blocked). These fields enable real queries; they're not ceremonial.

**Automation: Full.** Claude Code platform. All hooks, skills, and session capture available from day one.

## Personality

Warm, opinionated, casual. Anime/Japanese internet culture context. Explicit request for direct priority surfacing (opinionated). Technical + creative blend. Casual register throughout. Task-focused emotional awareness (the work is technical/creative, not emotionally vulnerable).

## Coherence Notes

Explicit linking without semantic search is a soft constraint — the compensating mechanism is explicit cross-project wiki links, which the user confirmed they want to maintain. The system will be explicitly link-rich rather than semantically discovered. If keyword search becomes insufficient as the vault grows, `/arscontexta:architect` can propose adding qmd.

Moderate granularity with heavy processing is coherent: each note is human-scale (not atomic-tiny), but each requires genuine transformation during extraction (title as claim, description that adds information, visible reasoning).

---

Topics:
- [[methodology]]
