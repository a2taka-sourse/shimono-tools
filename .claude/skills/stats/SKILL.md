---
name: stats
description: Show vault statistics and knowledge graph metrics per project. Notes count, connection density, inbox pressure, pipeline state, cross-project connection count. Triggers on "/stats", "vault stats", "show metrics", "how big is my vault".
version: "1.0"
generated_from: "arscontexta-v1.6"
user-invocable: true
context: fork
model: sonnet
allowed-tools: Read, Grep, Glob, Bash
---

## EXECUTE NOW

Collect and display vault metrics immediately.

---

# Stats

```bash
# Notes per project
echo "CTF: $(find ctf/ -name "*.md" -not -name "index.md" 2>/dev/null | wc -l) notes"
echo "Shimono: $(find shimono/ -name "*.md" -not -name "index.md" 2>/dev/null | wc -l) notes"
echo "AI Lain: $(find ai-lain/ -name "*.md" -not -name "index.md" 2>/dev/null | wc -l) notes"

# Inbox pressure
echo "Inbox: $(find inbox/ -name "*.md" 2>/dev/null | wc -l) items"

# Cross-project connections (links from ctf/ to shimono/ or ai-lain/, etc.)
echo "Cross-project links:"
grep -r '\[\[' ctf/ --include="*.md" -o | grep -c 'shimono\|ai-lain' 2>/dev/null || echo "0 ctf→other"
grep -r '\[\[' shimono/ --include="*.md" -o | grep -c 'ctf\|ai-lain' 2>/dev/null || echo "0 shimono→other"
grep -r '\[\[' ai-lain/ --include="*.md" -o | grep -c 'ctf\|shimono' 2>/dev/null || echo "0 ai-lain→other"

# Pending queue
cat ops/queue/queue.json 2>/dev/null | grep -c '"status": "pending"' || echo "0 pending tasks"

# Observations and tensions
echo "Observations: $(find ops/observations/ -name "*.md" 2>/dev/null | wc -l)"
echo "Tensions: $(find ops/tensions/ -name "*.md" 2>/dev/null | wc -l)"
```

## Output Format

```markdown
## Vault Stats

### Notes
| Project | Count | Last Activity |
|---------|-------|--------------|
| CTF | N | [date] |
| Shimono | N | [date] |
| AI Lain | N | [date] |
| Inbox | N | [oldest item age] |

### Graph Health
- Cross-project connections: N
- Orphan notes: N
- Dangling links: N

### Pipeline
- Queue depth: N tasks
- Pending observations: N
- Pending tensions: N

### Activity
[Which project has been most active recently]
[Which project is stalling]
```
