---
description: How this knowledge system was derived — enables /architect and /reseed commands
created: 2026-03-29
engine_version: "1.0.0"
---

# System Derivation

## Configuration Dimensions

| Dimension | Position | Conversation Signal | Confidence |
|-----------|----------|--------------------|--------------------|
| Granularity | Moderate | "design in phases with convergence loops"; "trial-and-error processes become content" | Medium |
| Organization | Light hierarchy | 3 project domains + ops; flat within each project | High |
| Linking | Explicit | "cross-project connections tracked explicitly — techniques inform each other, I want those links visible" | High |
| Processing | Heavy | "trial-and-error processes become content (video/podcast)"; Japanese technical books as source material | High |
| Navigation | 3-tier | 4 domains + cross-cutting concerns + root index; growing multi-project volume | High |
| Maintenance | Condition-based (active) | "surface it directly — proactively flag what's competing for attention and what's stalled" | High |
| Schema | Moderate-dense | 3 distinct project types with different queryable fields; cross-domain linking requires consistent schema | Medium |
| Automation | Full | Claude Code platform detected; full hook + skill support available | High (platform) |

## Personality Dimensions

| Dimension | Position | Signal |
|-----------|----------|--------|
| Warmth | warm | Anime aesthetic (Serial Experiments Lain, Love Plus+); creative + technical blend |
| Opinionatedness | opinionated | Explicit: "I want the agent to proactively flag... not wait for me to ask" |
| Formality | casual | Japanese internet culture context; content creation (YouTube/podcast); "目指せAI Lain" |
| Emotional Awareness | task-focused | Work is technical/creative, not emotionally vulnerable; content output is the primary goal |

## Vocabulary Mapping

| Universal Term | Domain Term | Category |
|---------------|-------------|----------|
| notes | project notes (ctf/, shimono/, ai-lain/) | folder |
| inbox | inbox | folder |
| archive | archive | folder |
| ops | ops | folder |
| note (type) | note (typed per project) | note type |
| reduce | extract | process phase |
| reflect | connect | process phase |
| reweave | update | process phase |
| verify | verify | process phase |
| rethink | review | meta process |
| MOC / topic map | project hub / index | navigation |
| description | description | schema field |
| topics | topics | schema field |
| relevant_notes | relevant_notes | schema field |
| cmd_reduce | /arscontexta:extract | command |
| cmd_reflect | /arscontexta:connect | command |
| cmd_reweave | /arscontexta:update | command |
| cmd_verify | /arscontexta:verify | command |
| cmd_rethink | /arscontexta:review | command |

## Platform

- Tier: Claude Code
- Automation: Full (hooks + skills + pipeline)
- notes_collection: vault-notes

## Active Feature Blocks

- [x] wiki-links — always included (kernel)
- [x] maintenance — always included
- [x] self-evolution — always included
- [x] session-rhythm — always included
- [x] templates — always included
- [x] ethical-guardrails — always included
- [x] helper-functions — always included
- [x] graph-analysis — always included
- [x] processing-pipeline — always included
- [x] schema — always included
- [x] methodology-knowledge — always included
- [x] atomic-notes — included (moderate granularity)
- [x] mocs — included (3-tier navigation)
- [x] multi-domain — included (3 distinct project domains)
- [x] personality — included (strong signals: warm, opinionated, casual)
- [x] self-space — included (ongoing multi-project work; agent tracks project state)
- [ ] semantic-search — excluded (qmd not opted in; explicit cross-project links handle discovery)

## Coherence Validation Results

- Hard constraints checked: 3. Violations: none
- Soft constraints checked: 7. Auto-adjusted: 0. User-confirmed: 0
- Compensating mechanisms active: explicit cross-project wiki links compensate for no semantic search; condition-based maintenance handles moderate-granularity reweaving needs

## Failure Mode Risks (HIGH)

1. **Collector's Fallacy** — 3 parallel projects generate heavy inbox volume; process before adding more
2. **Productivity Porn** — building RAG pipelines, simulation infrastructure, AI characters is inherently interesting work; vault must serve projects, not become the project
3. **Orphan Drift** — high creation volume across 3 domains; mandatory topics footer + reflect phase
4. **Temporal Staleness** — CTF meta shifts, Shimono design decisions get superseded; status fields + staleness conditions

## Generation Parameters

- Folder names: ctf/, shimono/, ai-lain/, inbox/, archive/, self/, templates/, ops/
- Project hub files: ctf/index.md, shimono/index.md, ai-lain/index.md, index.md
- Skills to generate: all 16 (vocabulary-transformed to extract/connect/update/verify/review)
- Hooks: session-orient.sh, session-capture.sh, validate-note.sh, auto-commit.sh
- Templates: ctf-technique.md, ctf-challenge.md, shimono-design.md, ai-lain-component.md, project-hub.md, observation-note.md
- Topology: single-agent with full pipeline orchestration
