---
description: First session guide — creating your first note and building cross-project connections
type: manual
generated_from: "arscontexta-1.0.0"
---

# Getting Started

## First Session

1. **Orient:** Read `self/goals.md` to see the three active threads. Check `ops/reminders.md` for anything time-bound.

2. **Pick a project to start with.** All three are initialized but empty. A good first session: process a CTF chapter you've been reading, or capture a Shimono design decision that's been rolling around in your head.

3. **Capture to inbox/** — don't write directly to ctf/, shimono/, or ai-lain/. Everything goes through inbox/ first.

4. **Run `/extract`** on your inbox item. The skill will create your first notes in the right project folder.

5. **Run `/connect`** on a new note. Even at day one, check ALL project folders for connections — cross-project links are the point.

## Your First Note

A note looks like this:

```yaml
---
description: "why this matters beyond just the title"
type: technique
category: forensics
status: learning
topics:
  - "[[ctf/index]]"
---

# x86 stack frame layout determines where local variables live relative to RBP

When RBP is saved and a new frame established, local variables are at negative offsets from RBP.
This means patching [RBP - offset] lets you modify local state without touching the stack pointer.
```

The title is a claim. The description adds context the title doesn't. The topics footer connects it to the CTF project hub.

## First Cross-Project Connection

After a few notes, you'll see a pattern: a CTF memory layout technique looks a lot like something in AI Lain's RAG memory system. When that happens, add the wiki link:

In the CTF technique note:
```markdown
Since [[episodic chunking preserves emotional continuity — a memory architecture for AI Lain]],
the same isolation principle applies here...
```

That's the system working.

## Session Rhythm

Every session: **Orient → Work → Persist**

- Orient: read self/, check /next
- Work: extract, connect, build
- Persist: update goals.md, commit

## Next

- [[skills]] — all available commands
- [[workflows]] — the full processing pipeline
