---
name: learn
description: Research a topic and grow your knowledge graph. Files results to inbox/ with full provenance, chains to /extract. Useful for CTF technique research, Shimono world-building references, AI architecture patterns. Triggers on "/learn", "/learn [topic]", "research this", "find out about".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch
context: fork
---

## EXECUTE NOW

**Topic: $ARGUMENTS**

Parse immediately:
- If topic provided: research that topic
- If empty: read `self/goals.md` for highest-priority unexplored direction
- If includes `--deep`/`--light`/`--moderate`: force that depth

**Steps:**

1. Read `ops/config.yaml` for research depth and `ops/derivation-manifest.md` for vocabulary
2. Determine which project this serves (ctf, shimono, ai-lain) from the topic
3. Research using WebSearch/WebFetch
4. File result to `inbox/` with full provenance metadata
5. Suggest next step based on pipeline chaining mode

**START NOW.**

---

# Learn

Research a topic and file the result to inbox/ for processing through the pipeline.

## Provenance Metadata (required for all filings)

```yaml
---
source_type: web-search  # web-search | manual | import
research_prompt: "the query that generated this"
research_server: web-search
generated: "YYYY-MM-DDTHH:MM:SSZ"
project: ctf  # ctf | shimono | ai-lain
---
```

The `research_prompt` field is the most critical. Knowing "I searched for X because I was exploring Y" is part of the knowledge graph.

## Filing Format

File as `inbox/YYYYMMDD-{topic-slug}.md` with provenance YAML + research content.

## Output

```markdown
## Research Filed

Topic: [topic]
Project: [ctf | shimono | ai-lain]
Filed: inbox/[filename].md
Provenance: [research_prompt preserved]

Next: /extract inbox/[filename].md
```
