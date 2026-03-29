---
_schema:
  entity_type: observation
  applies_to: "ops/observations/*.md"
  required:
    - description
    - category
    - observed
    - status
  enums:
    category:
      - friction
      - surprise
      - process-gap
      - methodology
    status:
      - pending
      - promoted
      - implemented
      - archived
  constraints:
    description:
      max_length: 200
      format: "One sentence about what was noticed"

# Template fields
description: ""
type: observation
category: friction     # friction | surprise | process-gap | methodology
observed: ""           # YYYY-MM-DD
status: pending        # pending | promoted | implemented | archived
---

# {observation as a prose sentence}

{Body: what happened, what triggered this, why it matters for methodology}

---

Topics:
- [[ops/methodology/methodology]]
