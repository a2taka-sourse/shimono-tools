---
name: remember
description: Capture friction, corrections, and methodology learnings as observations in ops/observations/ or methodology notes in ops/methodology/. Rule Zero — ops/methodology/ is the spec. Use when something needs to be remembered across sessions. Triggers on "/remember", "remember this", "note this friction", "capture this correction".
user-invocable: true
allowed-tools: Read, Write, Bash
context: fork
---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse:
- Natural language description of what to remember
- If "always do X": update CLAUDE.md immediately (methodology directive)
- If friction/correction: create observation note in ops/observations/
- If methodology learning: create note in ops/methodology/

**Execute:**
1. Determine what kind of memory this is (observation, methodology, directive)
2. Write the note to the appropriate location
3. For CLAUDE.md directives: propose the change for approval before implementing

**START NOW.**

---

# Remember

Capture things that need to persist across sessions. Two destinations:

## ops/observations/ — Friction and Surprises

For friction, surprises, and process gaps. Use the observation template:

```yaml
---
description: "one sentence about what was noticed"
type: observation
category: friction  # friction | surprise | process-gap | methodology
observed: "2026-03-29"
status: pending
---

# {observation as prose sentence}

{What happened, what triggered this, why it matters}
```

Name the file descriptively: `inbox-backing-up-when-shimono-active.md`

## ops/methodology/ — Methodology Corrections

For corrections to how the system operates. Creates a methodology note:

```yaml
---
description: "the correction as a one-sentence rule"
category: configuration-state  # or pipeline-config, vocabulary-map, etc.
created: "YYYY-MM-DD"
status: active
---

# {the correction}

{What changed and why}
```

## CLAUDE.md Directives

If the user says "always do X" or "never do Y" — this is a CLAUDE.md directive. Propose the exact change and wait for approval before implementing.

```markdown
## Proposed CLAUDE.md Update

Section: [which section]
Change: [exact text to add/modify]
Reason: [what prompted this]

Approve? (yes/no/modify)
```

## Session Capture (automatic)

Session transcripts are auto-saved to ops/sessions/ by the Stop hook. /remember is for explicit, in-session capture of something that shouldn't wait for transcript mining.
