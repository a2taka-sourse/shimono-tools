---
name: extract
description: Extract structured notes from source material (books, challenge descriptions, session dumps, articles). Comprehensive extraction is the default — every insight that serves CTF, Shimono, or AI Lain gets extracted. Zero extraction from a relevant source is a BUG. Triggers on "/extract", "/extract [file]", "extract insights", "process this source", "mine this".
version: "1.0"
generated_from: "arscontexta-v1.6"
user-invocable: true
allowed-tools: Read, Write, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0 — before any processing)

Read these files to configure domain-specific behavior:

1. **`ops/derivation-manifest.md`** — vocabulary mapping, extraction categories, platform hints
2. **`ops/config.yaml`** — processing depth, pipeline chaining, selectivity

If these files don't exist, use defaults: depth=standard, chaining=suggested, selectivity=moderate.

**Processing depth:**
- `deep` — fresh context, maximum quality gates, every candidate evaluated
- `standard` — full pipeline, balanced attention (default)
- `quick` — compressed pass, high-volume catch-up

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If target is a file path: extract from that file
- If target contains `--handoff`: output RALPH HANDOFF block at end
- If target is empty: check inbox/ for unprocessed items; list and ask which to process

**Execute these steps:**

1. Read `ops/derivation-manifest.md` for extraction categories by project (ctf, shimono, ai-lain)
2. Read the target file fully — understand what project it serves
3. Run comprehensive extraction: for EACH section/concept, ask "Would a future session benefit from this being a retrievable note?"
4. For each yes: determine note type, write title as a prose claim, draft description + body
5. Check for duplicates against existing notes in the relevant project folder
6. Create notes in the appropriate project folder (ctf/, shimono/, or ai-lain/)
7. Create queue entries in ops/queue/queue.json for connect phase
8. Report extraction results

**START NOW.** Reference below is methodology — use to guide, not as output.

---

# Extract

Extract structured notes from source material. Raw content enters. Structured notes with prose-as-title claims exit.

## The Comprehensive Extraction Principle

**For relevant sources, COMPREHENSIVE EXTRACTION is the default.** Extract ALL:
- Techniques, patterns, methods — CTF techniques, simulation approaches, architecture patterns
- Design decisions — choices made with rationale visible
- Tensions — contradictions or trade-offs (these are valuable, not problems)
- Enrichments — content that improves existing notes (create enrichment tasks)

**"We already know this" means we NEED the articulation.**

## Extraction by Project

### CTF/Security

| Category | What to Find | Note Type |
|----------|--------------|-----------|
| Techniques | Reusable patterns, assembly methods, forensics approaches | technique |
| Challenge writeups | Per-challenge solution + technique used | challenge |
| Study notes | Concepts from Japanese technical books (assembly, x86) | study-note |
| Open problems | Unresolved technique questions | open-problem |

### Shimono World-Building

| Category | What to Find | Note Type |
|----------|--------------|-----------|
| Design decisions | Choices made for 下腦/竪野 with rationale | design-decision |
| Simulation notes | NeuralGCM/JAX pipeline choices | simulation-note |
| Content segments | Video/podcast debate topics | content-segment |
| World facts | Canon facts about 下腦/竪野 | world-fact |

### AI Lain

| Category | What to Find | Note Type |
|----------|--------------|-----------|
| Architecture decisions | RAG, memory, context structure choices | architecture-decision |
| Implementation notes | Claude API, pixel UI specifics | implementation-note |
| Aesthetic notes | Lain/Love Plus+ design choices | aesthetic-note |

## Quality Bar for Extracted Notes

**Title as claim:** Does the title work as prose when linked? `since [[ELF section headers encode symbol visibility]]` reads naturally?

**Description adds information:** Does the description add context beyond the title? One sentence, max 200 chars.

**Claim is specific:** Is it specific enough to disagree with? "Assembly notes" fails. "x86 stack frame layout determines where local variables live relative to RBP" passes.

**Reasoning visible:** Does the body show the path to the conclusion?

## INVALID Skip Reasons (bugs, not judgment)

- "We already have something similar" → near-duplicates add value; extract and flag for merge review
- "This is obvious" → obvious reasoning, when articulated, builds the strongest paths
- "This is too detailed" → detail creates precision; extract and let the graph show what matters
- "I don't know where to put it" → put it in inbox/ with a note; routing is not extraction's job

## Note Creation Format

```yaml
---
description: "one sentence adding context beyond the title"
type: technique  # or challenge, design-decision, architecture-decision, etc.
category: forensics  # project-specific enum
status: learning  # project-specific enum
topics:
  - "[[ctf/index]]"  # or shimono/index, ai-lain/index
relevant_notes: []
---

# title as a prose claim

Body: mechanism, context, when this applies, what breaks if missed.
```

## Output Format

```markdown
## Extraction Complete: [source file]

Project: [ctf | shimono | ai-lain]

### Notes Created

| # | Title | Type | Notes |
|---|-------|------|-------|
| 1 | [title] | technique | [any flags] |
| 2 | [title] | challenge | — |

### Enrichment Tasks

- [[existing note]] needs updating with [what was found]

### Skipped (with reason)

- [content] — reason: [specific reason, not a bug reason]

### Next Step

[/connect [note-title] — suggested] or [manual]
```

## Quality Gates

1. **Skip rate check** — for domain-relevant sources, skip rate must be < 10%. More than 10% skipped is a signal to re-evaluate.
2. **Title prose test** — every title must complete `since [[title]]` naturally.
3. **Description quality** — description must add information the title doesn't contain.
4. **Duplicate check** — search the relevant project folder before creating.

## Pipeline Chaining

After extraction:
- **manual:** Output "Next: /connect [note-title]"
- **suggested:** Output next step AND add queue entries for connect phase
- **automatic:** Queue entries added, connect phase proceeds

---

## Handoff Mode (--handoff flag)

When invoked with `--handoff`, append this block after completing normal workflow:

```
=== RALPH HANDOFF: extract ===
Target: [source file]
Project: [ctf | shimono | ai-lain]

Work Done:
- Notes created: N
- Enrichment tasks: M
- Skipped: K (rate: X%)

Files Created:
- [project]/[note-name].md
- ops/queue/queue.json (updated)

Queue Updates:
- Added N entries at current_phase: "connect"
=== END HANDOFF ===
```
