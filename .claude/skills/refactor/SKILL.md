---
name: refactor
description: Structural cleanup and note quality improvement. Rename notes for better prose-as-title, merge near-duplicates, split over-broad notes, fix schema drift. Triggers on "/refactor", "clean up notes", "fix note quality", "rename this note".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse:
- Note name: refactor that specific note
- "splits": find notes that should be split
- "merges": find near-duplicate notes
- "renames": find notes with weak titles
- Empty: suggest a refactoring target from the lowest-quality notes

**START NOW.**

---

# Refactor

Structural cleanup. Improves note quality without changing the knowledge content.

## Rename Protocol (prose-as-title improvement)

When renaming a note:
1. Propose the new title
2. Wait for approval
3. Rename the file
4. Update ALL wiki links to the old name:

```bash
old_name="old-title"
new_name="new-title"
find ctf/ shimono/ ai-lain/ self/ -name "*.md" -exec sed -i "s/\[\[$old_name\]\]/[[$new_name]]/g" {} \;
mv "project/${old_name}.md" "project/${new_name}.md"
```

**Never rename without updating all references.**

## Split Protocol

When a note makes multiple claims:
1. Identify the distinct claims
2. Propose the split titles (each must pass prose-as-title test)
3. Wait for approval
4. Create new notes for each claim
5. Update the original (becomes synthesis linking to splits, or is archived)
6. Add new notes to queue for connect phase

## Merge Protocol

When two notes substantially overlap:
1. Flag both notes for human review
2. Propose which to keep and what to merge in
3. **Never auto-merge** — requires human judgment
4. After approval: update the surviving note, archive the duplicate

## Quality Signals Worth Refactoring

- Title is a label ("assembly notes") not a claim
- Title contains "and" — likely two claims bundled
- Description restates the title
- Note connects to 5+ topics across different domains (split candidate)
- Note has 0 incoming links and is older than 2 weeks (rename or archive candidate)

## Output

Always propose before acting. Never rename, split, or merge without approval.

```markdown
## Refactor Proposal: [[note name]]

**Issue:** [what's wrong]
**Proposed fix:** [what to change]
**Impact:** [N wiki links would be updated]

Approve? (yes/no/modify)
```
