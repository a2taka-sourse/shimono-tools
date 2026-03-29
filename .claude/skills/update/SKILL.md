---
name: update
description: Update old notes with new context. The backward pass. Revisit existing notes that predate newer related content — add connections, sharpen claims, consider splits. Triggers on "/update", "/update [note]", "update old notes", "backward pass", "revisit notes".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary and `ops/config.yaml` for processing depth and reweave scope.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If note name provided: update that specific note
- If `--handoff`: output RALPH HANDOFF block at end
- If empty: find notes that most need updating (oldest, sparsest, most outdated)
- If `--sparse`: find notes with fewest connections

**Execute these steps:**

1. Read the target note fully
2. Ask: "If I wrote this today, with everything I now know, what would be different?"
3. Search ALL project folders for newer notes that should connect to this one
4. Evaluate what needs changing: add connections, sharpen claim, consider split, challenge claim
5. For interactive mode: present proposal before applying
6. Apply changes
7. Report what changed and why

**START NOW.**

---

# Update

Revisit old notes with everything you know today. Notes are living documents — they grow, get rewritten, split apart, sharpen their claims. Old notes don't know about new notes. This backward pass keeps the network alive.

## The Core Question

**"If I wrote this note today, with everything I now know, what would be different?"**

Not "add backward links." A full reconsideration.

## What Updating Can Do

| Action | When |
|--------|------|
| Add connections | Newer notes exist that should link here |
| Rewrite content | Understanding evolved |
| Sharpen the claim | Title too vague to be useful |
| Split the note | Multiple claims bundled together |
| Challenge the claim | New evidence contradicts the original |
| Improve the description | Better framing emerged |

## Discovery

Search ALL project folders for newer notes that relate to the target:

```bash
# Find notes that might relate to this one
grep -r "key concept" ctf/ shimono/ ai-lain/ --include="*.md" -l

# Check backlinks
grep -rl "\[\[target note title\]\]" ctf/ shimono/ ai-lain/ --include="*.md"
```

Cross-project updates are especially valuable — a CTF technique note might need to reference a new AI Lain architecture decision that uses the same memory pattern.

## Sharpening Test

Read the title. Could someone disagree with this specific claim?
- If yes → sharp enough
- If no → too vague, needs sharpening

Example:
- Vague: "assembly matters" (who disagrees?)
- Sharp: "x86 stack frame layout determines where local variables live relative to RBP" (arguable position)

## Quality Gates

1. **Articulation test** — every new connection passes "[[A]] connects to [[B]] because [specific reason]"
2. **Improvement test** — is the note better after changes? More useful? More connected?
3. **Coherence test** — does the note still cohere as a single focused piece?
4. **Network test** — do the changes improve traversal paths?

**When NOT to change:** The note is accurate, well-connected, and recent. "Improvement" is only cosmetic rewording. The note is a historical record.

## Interactive Mode: Show Proposal First

```markdown
## Update Proposal: [[target note]]

**Last modified:** YYYY-MM-DD
**Newer notes evaluated:** N, backlinks: M

### Claim Assessment

[Does the claim hold? Need sharpening? Splitting? Revision?]

### Proposed Changes

**1. [change type]: [description]**
Current: > [existing text]
Proposed: > [new text]
Rationale: [why]

### Connections to Add
- [[newer note]] — [relationship]: [specific reason]

Apply these changes? (yes/no/modify)
```

## Output Format

```markdown
## Update Complete: [[target note]]

### Changes Applied
| Type | Description |
|------|-------------|
| connection | added [[note A]] inline |
| sharpen | description updated |

### Network Effect
- Outgoing links: 3 -> 5
- Now bridges [[ctf]] and [[ai-lain]]

### Cascade Recommendations
- [[related note]] might benefit from update (similar vintage)
```

---

## Handoff Mode (--handoff flag)

```
=== RALPH HANDOFF: update ===
Target: [[note name]]

Work Done:
- Notes updated: N
- Claim status: unchanged | sharpened | challenged | split
- Network effect: M new traversal paths

Queue Updates:
- Advance phase: update -> verify
=== END HANDOFF ===
```
