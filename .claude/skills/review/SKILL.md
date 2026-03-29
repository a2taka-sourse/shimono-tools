---
name: review
description: Challenge system assumptions against accumulated evidence. Triages observations and tensions, detects patterns, generates proposals. The scientific method applied to this vault. Triggers on "/review", "review observations", "challenge assumptions", "what have I learned".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md`, `ops/config.yaml`, and all files in `ops/methodology/`.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

- Empty: full review (drift check + triage all pending observations + tensions)
- "triage": triage only, no pattern detection
- "drift": drift check only
- specific filename: triage that one item interactively

**START NOW.**

---

# Review

The system is not sacred. Evidence beats intuition. Observations in ops/observations/ and tensions in ops/tensions/ are evidence from actual use. This command triages them and proposes system changes when patterns emerge.

## Phase 0: Drift Check

Rule Zero: `ops/methodology/` is the canonical spec. Before triaging observations, check whether the system has drifted from what the methodology says.

Read all files in ops/methodology/. Compare against:
- Does CLAUDE.md still match the methodology?
- Are skills following the documented pipeline?
- Do templates match the documented schemas?

Flag any drift. Drift that isn't caught becomes technical debt.

## Phase 1: Triage Observations

Read all pending observations in ops/observations/ (status: pending).

For each observation, triage:
- **PROMOTE** → create a note in the relevant project folder (the observation is a genuine insight)
- **IMPLEMENT** → update CLAUDE.md or a skill immediately (the observation is a methodology correction)
- **ARCHIVE** → mark as archived (the observation was resolved or is no longer relevant)
- **KEEP PENDING** → needs more evidence before acting

## Phase 2: Triage Tensions

Read all pending tensions in ops/tensions/ (status: pending).

For each tension, triage:
- **RESOLVED** → one side was wrong; update the note that was wrong
- **DISSOLVED** → the tension was artificial; remove both tension markers
- **KEEP PENDING** → genuine unresolved conflict; needs more evidence

## Phase 3: Pattern Detection

After triage, look at what was promoted and implemented. Are there patterns?
- Multiple observations about the same friction → systemic issue, propose structural fix
- Observations spanning multiple projects → cross-project methodology improvement
- Tension clusters → schema or vocabulary clarification needed

## Phase 4: Proposals

For each pattern detected, generate a concrete proposal:
- What should change (CLAUDE.md section, skill instruction, template field)
- What evidence supports it
- What the change would look like

**NEVER auto-implement.** Always propose for approval.

## Output Format

```markdown
## Review Complete

### Drift Check
[No drift detected | Drift found: description]

### Observations Triaged: N

| Observation | Action | Notes |
|-------------|--------|-------|
| [title] | PROMOTE / IMPLEMENT / ARCHIVE | [details] |

### Tensions Triaged: M

| Tension | Action | Notes |
|---------|--------|-------|
| [title] | RESOLVED / DISSOLVED / KEEP | [details] |

### Patterns Detected

[Pattern description → proposed change]

### Proposals (requiring approval)

**Proposal 1: [title]**
Evidence: [observations/tensions supporting this]
Proposed change: [what specifically would change]
Approve? (yes/no/modify)
```
