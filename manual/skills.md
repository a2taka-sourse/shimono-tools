---
description: Complete reference for every available command — when to use each and examples
type: manual
generated_from: "arscontexta-1.0.0"
---

# Skills

All commands use the format `/arscontexta:skill-name` from the plugin, or directly as `/skill-name` when the vault is the working directory.

**Note:** Restart Claude Code after setup to activate all skills.

## Processing Pipeline

| Command | When to Use | Example |
|---------|-------------|---------|
| `/extract [file]` | Process source material from inbox/ into notes | `/extract inbox/elf-chapter-3.md` |
| `/connect [note]` | Find connections for a new note across all projects | `/connect "ELF section headers encode symbol visibility"` |
| `/update [note]` | Update old notes with new context (backward pass) | `/update "x86 stack frame layout"` |
| `/verify [note]` | Quality gate: description, schema, links | `/verify "竪野 rainfall gradient"` |

## Orchestration

| Command | When to Use | Example |
|---------|-------------|---------|
| `/seed [source]` | Bootstrap a new source into the pipeline | `/seed "CTF book chapter 4"` |
| `/ralph [source]` | Full pipeline with fresh context per phase (important sources) | `/ralph inbox/elf-deep-dive.md` |
| `/pipeline [file]` | Full pipeline in one session (standard sources) | `/pipeline inbox/lain-architecture-notes.md` |
| `/tasks` | Inspect and manage the processing queue | `/tasks` |

## Navigation & Analysis

| Command | When to Use | Example |
|---------|-------------|---------|
| `/next` | Get the recommended next action with priority context | `/next` |
| `/stats` | Vault metrics: notes per project, connections, queue state | `/stats` |
| `/graph` | Graph analysis: orphans, dangling links, cross-project map | `/graph orphans` |

## Growth

| Command | When to Use | Example |
|---------|-------------|---------|
| `/learn [topic]` | Research a topic and file to inbox with provenance | `/learn "ELF lazy binding mechanics"` |
| `/remember [note]` | Capture friction or correction as observation | `/remember "description validation failing on Shimono notes"` |
| `/validate` | Batch schema validation across all project folders | `/validate ctf` |

## Evolution

| Command | When to Use | Example |
|---------|-------------|---------|
| `/review` | Triage accumulated observations and tensions | `/review` |
| `/refactor [note]` | Rename, split, or merge notes for better structure | `/refactor "assembly notes"` |

## Plugin Commands (always available)

| Command | When to Use |
|---------|-------------|
| `/arscontexta:next` | Priority recommendations |
| `/arscontexta:health` | System health diagnostic |
| `/arscontexta:ask` | Query the methodology knowledge base |
| `/arscontexta:architect` | Get research-backed configuration advice |
| `/arscontexta:help` | See all available commands |
| `/arscontexta:tutorial` | Interactive walkthrough |

## See Also

- [[workflows]] — how skills chain together in the processing pipeline
- [[meta-skills]] — deep guide to /review, /remember, /ask
- [[manual]] — back to hub
