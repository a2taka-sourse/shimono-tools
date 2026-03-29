---
_schema:
  entity_type: ctf-technique
  applies_to: "ctf/*.md (type: technique)"
  required:
    - description
    - category
    - status
    - topics
  optional:
    - relevant_notes
    - challenges
    - tools
    - source_ref
  enums:
    category:
      - assembly
      - forensics
      - network
      - crypto
      - pwn
      - rev
      - misc
    status:
      - learning
      - practiced
      - solid
  constraints:
    description:
      max_length: 200
      format: "One sentence — when/why to apply this technique, beyond just restating the title"
    topics:
      format: "Array of wiki links; must include [[ctf/index]]"

# Template fields
description: ""
type: technique
category: assembly  # assembly | forensics | network | crypto | pwn | rev | misc
status: learning    # learning | practiced | solid
challenges: []      # wiki links to challenge notes where this was used
tools: []           # tools used with this technique (strings)
source_ref: ""      # link to study note or external reference
topics:
  - "[[ctf/index]]"
relevant_notes: []  # "[[note]] — relationship context" strings
---

# {prose-as-title: a specific claim about this technique}

{Body: explain the mechanism. Why does this work? When does it apply? What breaks if you miss it?}

---

Relevant Notes:
- [[related technique]] — extends this by...

Topics:
- [[ctf/index]]
