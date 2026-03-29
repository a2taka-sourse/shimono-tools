---
_schema:
  entity_type: shimono-design-decision
  applies_to: "shimono/*.md (type: design-decision)"
  required:
    - description
    - domain
    - status
    - topics
  optional:
    - relevant_notes
    - simulation_ref
    - alternatives_considered
    - content_potential
    - collaborator_notes
  enums:
    domain:
      - climate
      - terrain
      - society
      - geography
      - lore
      - simulation
      - content
    status:
      - proposed
      - accepted
      - implemented
      - revisited
      - rejected
  constraints:
    description:
      max_length: 200
      format: "One sentence rationale — WHY this decision was made, not just what it is"
    topics:
      format: "Array of wiki links; must include [[shimono/index]]"

# Template fields
description: ""
type: design-decision
domain: climate       # climate | terrain | society | geography | lore | simulation | content
status: proposed      # proposed | accepted | implemented | revisited | rejected
simulation_ref: ""    # link to JAX/NeuralGCM notebook, spreadsheet, or SeesaaWiki page
alternatives_considered: []  # brief strings describing alternatives
content_potential: false     # true if this could become a video/podcast debate topic
collaborator_notes: ""       # notes from しかバトン/Shikabaton collaboration
topics:
  - "[[shimono/index]]"
relevant_notes: []
---

# {decision as a claim — what was decided and why it matters}

## Context

{What question or problem this decision addresses}

## Decision

{The choice made and the key reasoning}

## Alternatives Considered

{What was weighed and why this won}

## Simulation Implications

{If applicable: how this affects NeuralGCM/JAX modeling}

## Content Angle

{If applicable: how this could be framed as a debate topic for video/podcast}

---

Relevant Notes:
- [[related decision]] — this constrains that decision because...

Topics:
- [[shimono/index]]
