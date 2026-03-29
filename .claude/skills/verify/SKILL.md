---
name: verify
description: Combined quality gate — description quality (cold-read test) + schema compliance + link health. Use after creating notes or as periodic maintenance. Triggers on "/verify", "/verify [note]", "verify note quality", "check note health".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary and `ops/config.yaml` for verification settings.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If note name: verify that specific note
- If `--batch`: verify all notes in the specified project folder
- If empty: verify recently created notes

**Execute these steps:**

1. Run Test 1: Description Quality (cold-read test)
2. Run Test 2: Schema Compliance
3. Run Test 3: Link Health
4. Fix immediately: description failures and schema failures
5. Log: link failures for next connect session
6. Report results

**START NOW.**

---

# Verify

Three checks in one phase. The final quality gate before a note is considered processed.

## Test 1: Description Quality (Cold-Read Test)

Read ONLY the title and description. Without reading the body, predict what the note contains. Then read the body. If your prediction missed major content, the description needs improvement.

**Description quality standards:**
- Adds information the title doesn't contain
- One sentence, max 200 chars
- Specific enough to make a retrieval decision
- Answers "would I read this note?" from the description alone

**Fix:** Rewrite immediately. Ask: "What does this note argue that a future agent needs to know to decide whether to read it?"

## Test 2: Schema Compliance

Check against the relevant template in templates/. Required fields:
- `description` — present and non-empty, differs from title
- `type` — valid enum for this note type
- `status` — valid enum
- `topics` — array with at least one project hub link

```bash
# Check for missing description
rg -L '^description:' ctf/ shimono/ ai-lain/ --include="*.md"

# Check for empty topics
rg 'topics: \[\]' ctf/ shimono/ ai-lain/ --include="*.md"
```

**Fix:** Add missing fields immediately. Update template enums if needed.

## Test 3: Link Health

All wiki links in the note must resolve to existing files.

```bash
# Extract all wiki links from note and check they exist
grep -o '\[\[[^\]]*\]\]' "path/to/note.md" | sed 's/\[\[//;s/\]\]//' | while read link; do
  find . -name "${link}.md" | grep -q . || echo "Dangling: [[$link]]"
done
```

**Fix:** Fix or remove dangling links. Log for connect phase if the target note should exist but doesn't.

## Output Format

```markdown
## Verify Complete: [[note name]]

### Test 1: Description Quality
[PASS | FAIL — rewritten to: "new description"]

### Test 2: Schema Compliance
[PASS | FAIL — fields fixed: type, status]

### Test 3: Link Health
[PASS | FAIL — dangling: [[link]], flagged for connect]

### Overall: [PASS | PASS WITH FIXES | FAIL]
```

## Pipeline Chaining

After verify:
- **manual:** Output "Processing complete for [[note]]"
- **suggested:** Output completion + advance queue to "done"
- **automatic:** Queue entry marked done
