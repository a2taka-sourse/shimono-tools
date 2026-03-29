---
description: The vault's self-knowledge — derivation rationale, configuration state, and evolution history
type: moc
---

# methodology

This folder records what the system knows about its own operation — why it was configured this way, what the current state is, and how it has evolved. Meta-skills (/arscontexta:review, /arscontexta:architect) read from and write to this folder. /arscontexta:remember captures operational corrections here.

## Derivation Rationale

- [[derivation-rationale]] — Why each configuration dimension was set the way it was

## Configuration State

(Populated by /arscontexta:review, /arscontexta:architect)

## Evolution History

(Populated by /arscontexta:review, /arscontexta:architect, /arscontexta:reseed)

## How to Use This Folder

Browse notes:
```bash
ls ops/methodology/
```

Query by category:
```bash
rg '^category:' ops/methodology/
```

Find active directives:
```bash
rg '^status: active' ops/methodology/
```

Ask the research graph: `/arscontexta:ask [question about your system]`

Meta-skills (/arscontexta:review, /arscontexta:architect) read from and write to this folder.
/arscontexta:remember captures operational corrections here.
