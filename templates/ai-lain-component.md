---
_schema:
  entity_type: ai-lain-component
  applies_to: "ai-lain/*.md (type: architecture-decision | implementation-note | aesthetic-note)"
  required:
    - description
    - component
    - status
    - topics
  optional:
    - relevant_notes
    - blockers
    - alternatives_considered
    - lain_aesthetic_fit
  enums:
    type:
      - architecture-decision
      - implementation-note
      - aesthetic-note
      - open-problem
    component:
      - rag
      - ui
      - api
      - memory
      - aesthetic
      - pipeline
    status:
      - planned
      - in-progress
      - done
      - blocked
      - revisited
  constraints:
    description:
      max_length: 200
      format: "One sentence — what this component does or what this decision enables"
    topics:
      format: "Array of wiki links; must include [[ai-lain/index]]"

# Template fields
description: ""
type: architecture-decision   # architecture-decision | implementation-note | aesthetic-note | open-problem
component: rag                # rag | ui | api | memory | aesthetic | pipeline
status: planned               # planned | in-progress | done | blocked | revisited
blockers: []                  # strings describing what's blocking, if status is blocked
alternatives_considered: []   # brief strings
lain_aesthetic_fit: ""        # how this fits the Serial Experiments Lain aesthetic goal
topics:
  - "[[ai-lain/index]]"
relevant_notes: []
---

# {component decision or note as a claim}

## Context

{What problem this addresses or what aspect of the character system this covers}

## Decision / Implementation

{The choice made or the implementation approach}

## Lain Aesthetic

{How this fits "目指せAI Lain" — the Serial Experiments Lain aesthetic and Love Plus+ feel}

## Technical Notes

{Implementation details, API specifics, integration points}

---

Relevant Notes:
- [[related component]] — this depends on that because...

Topics:
- [[ai-lain/index]]
