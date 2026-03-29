---
_schema:
  entity_type: ctf-challenge
  applies_to: "ctf/*.md (type: challenge)"
  required:
    - description
    - difficulty
    - status
    - topics
  optional:
    - relevant_notes
    - techniques_used
    - platform
    - flag
  enums:
    difficulty:
      - beginner
      - intermediate
      - hard
      - expert
    status:
      - attempted
      - solved
      - writeup-pending
      - writeup-done
  constraints:
    description:
      max_length: 200
      format: "Key insight or technique used — what this challenge taught"
    topics:
      format: "Array of wiki links; must include [[ctf/index]]"

# Template fields
description: ""
type: challenge
platform: ""          # picoCTF | Defcon | HTB | etc.
difficulty: beginner  # beginner | intermediate | hard | expert
status: attempted     # attempted | solved | writeup-pending | writeup-done
techniques_used: []   # wiki links to technique notes
flag: ""              # flag value (optional)
topics:
  - "[[ctf/index]]"
relevant_notes: []
---

# {challenge name — what it reveals or teaches}

## Problem

{Description of the challenge}

## Approach

{How you attacked it — dead ends count}

## Solution

{The technique that worked and why}

## Key Insight

{The one thing worth remembering about this challenge}

---

Relevant Notes:
- [[technique used]] — used to solve this

Topics:
- [[ctf/index]]
