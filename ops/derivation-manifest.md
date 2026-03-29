---
engine_version: "0.2.0"
research_snapshot: "2026-02-10"
generated_at: "2026-03-29T00:00:00Z"
platform: claude-code
kernel_version: "1.0"

dimensions:
  granularity: moderate
  organization: light-hierarchy
  linking: explicit
  processing: heavy
  navigation: 3-tier
  maintenance: condition-based
  schema: moderate-dense
  automation: full

active_blocks:
  - wiki-links
  - maintenance
  - self-evolution
  - session-rhythm
  - templates
  - ethical-guardrails
  - helper-functions
  - graph-analysis
  - processing-pipeline
  - schema
  - methodology-knowledge
  - atomic-notes
  - mocs
  - multi-domain
  - personality
  - self-space

coherence_result: passed

vocabulary:
  # Level 1: Folder names
  notes: "ctf | shimono | ai-lain"
  notes_collection: "vault-notes"
  inbox: "inbox"
  archive: "archive"
  ops: "ops"

  # Level 2: Note types
  note: "note"
  note_plural: "notes"

  # Level 3: Schema field names (structural — never transform)
  description: "description"
  topics: "topics"
  relevant_notes: "relevant_notes"

  # Level 4: Navigation terms
  topic_map: "project hub"
  topic_map_plural: "project hubs"
  hub: "vault index"

  # Level 5: Process verbs
  reduce: "extract"
  reflect: "connect"
  reweave: "update"
  verify: "verify"
  validate: "validate"
  rethink: "review"

  # Level 6: Command names
  cmd_reduce: "/arscontexta:extract"
  cmd_reflect: "/arscontexta:connect"
  cmd_reweave: "/arscontexta:update"
  cmd_verify: "/arscontexta:verify"
  cmd_rethink: "/arscontexta:review"
  cmd_next: "/arscontexta:next"
  cmd_remember: "/arscontexta:remember"
  cmd_learn: "/arscontexta:learn"

  # Level 7: Extraction categories by project
  extraction_categories:
    ctf:
      - name: "techniques"
        what_to_find: "Reusable patterns, methods, approaches (assembly, forensics, network)"
        output_type: "technique"
      - name: "challenge-writeups"
        what_to_find: "Per-challenge solution notes with technique used"
        output_type: "challenge"
      - name: "study-notes"
        what_to_find: "Concepts from Japanese technical books (assembly, x86)"
        output_type: "study-note"
      - name: "open-problems"
        what_to_find: "Unresolved technique questions or gaps"
        output_type: "open-problem"
    shimono:
      - name: "design-decisions"
        what_to_find: "Design choices made for 下腦/竪野 with rationale and alternatives considered"
        output_type: "design-decision"
      - name: "simulation-notes"
        what_to_find: "NeuralGCM/JAX pipeline choices, RAG system architecture decisions"
        output_type: "simulation-note"
      - name: "content-segments"
        what_to_find: "Video/podcast debate topics ready for recording"
        output_type: "content-segment"
      - name: "world-facts"
        what_to_find: "Established canon facts about 下腦/竪野"
        output_type: "world-fact"
    ai-lain:
      - name: "architecture-decisions"
        what_to_find: "RAG structure, memory system, context management choices"
        output_type: "architecture-decision"
      - name: "implementation-notes"
        what_to_find: "Claude API specifics, pixel avatar UI choices"
        output_type: "implementation-note"
      - name: "aesthetic-notes"
        what_to_find: "Serial Experiments Lain styling, Love Plus+ game feel decisions"
        output_type: "aesthetic-note"

platform_hints:
  context: fork
  allowed_tools:
    - Read
    - Write
    - Edit
    - Grep
    - Glob
    - Bash
    - WebSearch
    - WebFetch
  semantic_search_tool: null

personality:
  warmth: warm
  opinionatedness: opinionated
  formality: casual
  emotional_awareness: task-focused
---
