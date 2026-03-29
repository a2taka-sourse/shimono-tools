---
name: graph
description: Generate and run graph analysis queries across the vault. Find orphans, measure connection density, trace cross-project paths, detect synthesis opportunities. Triggers on "/graph", "analyze connections", "find orphans", "graph analysis", "map connections".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write
context: fork
---

## EXECUTE NOW

**Query: $ARGUMENTS**

Parse:
- Empty: run all standard analyses
- "orphans": find notes with no incoming links
- "density": measure connection counts per note
- "cross": find cross-project connections
- "dangling": find broken wiki links
- "paths [note]": find all paths from a note through the graph

**START NOW.**

---

# Graph

The vault is a graph database on the filesystem. Markdown files are nodes, wiki links are edges, YAML frontmatter is the property store, ripgrep is the query engine.

## Standard Analyses

### Orphan Detection
```bash
# Notes with no incoming links
find ctf/ shimono/ ai-lain/ -name "*.md" -not -name "index.md" | while read f; do
  title=$(basename "$f" .md)
  rg -q "\[\[$title\]\]" ctf/ shimono/ ai-lain/ self/ index.md 2>/dev/null || echo "Orphan: $f"
done
```

### Dangling Links
```bash
# Wiki links to non-existent files
rg -o '\[\[([^\]]+)\]\]' ctf/ shimono/ ai-lain/ -r '$1' --no-filename | sort -u | while read title; do
  find . -name "${title}.md" -not -path "./.git/*" 2>/dev/null | grep -q . || echo "Dangling: [[$title]]"
done
```

### Cross-Project Connection Map
```bash
# Links from CTF to other projects
echo "=== CTF → Shimono/AI Lain ==="
grep -r '\[\[' ctf/ --include="*.md" -h | grep -oP '\[\[\K[^\]]+' | while read link; do
  find shimono/ ai-lain/ -name "${link}.md" 2>/dev/null | grep -q . && echo "  ctf → $link"
done
```

### Connection Density
```bash
# Notes by outgoing link count
for f in ctf/*.md shimono/*.md ai-lain/*.md; do
  [ -f "$f" ] && echo "$(grep -o '\[\[' "$f" | wc -l) $f"
done | sort -n | head -20
```

## Output Format

```markdown
## Graph Analysis

### Orphans (N found)
- [path] — suggested connection: [[possible link]]

### Dangling Links (N found)
- [note] references [[non-existent]] — fix or remove

### Cross-Project Connections
| Source | Target | Count |
|--------|--------|-------|
| ctf/ | ai-lain/ | N |
| shimono/ | ai-lain/ | N |

### Lowest Density Notes (candidates for /connect)
- [note] — 0 outgoing links

### Synthesis Opportunities
[Notes with structural parallels worth combining]
```
