---
description: How to adjust your system via ops/config.yaml and /arscontexta:architect
type: manual
generated_from: "arscontexta-1.0.0"
---

# Configuration

## ops/config.yaml

The live operational config. Edit directly for quick adjustments.

Key settings you might want to change:

```yaml
processing:
  depth: standard       # deep (fresh context per phase) | standard | quick
  chaining: suggested   # manual (you invoke) | suggested (queued) | automatic

features:
  semantic-search: false  # change to true and install qmd for semantic search
```

### Processing Depth

- **deep** — Spawns fresh context per phase. Maximum quality. Use for important sources (key chapters, major design decisions).
- **standard** — Sequential in one session. Good balance for most work.
- **quick** — Compressed pipeline for catch-up processing.

### Pipeline Chaining

- **manual** — Each skill outputs "Next: /skill [target]" — you decide when to run it.
- **suggested** — Next step is suggested and queued — you can skip it.
- **automatic** — Phases chain without manual intervention.

## Adding Semantic Search

If keyword search becomes insufficient as the vault grows:

1. Install qmd: `npm install -g @tobilu/qmd` (or `bun install -g @tobilu/qmd`)
2. Run: `qmd init` in the vault root
3. Run: `qmd collection add . --name vault-notes --mask "**/*.md"`
4. Run: `qmd update && qmd embed`
5. Update ops/config.yaml: `semantic-search: true`
6. Run `/arscontexta:architect` to update the skills for semantic search support

## Adjusting Maintenance Thresholds

In ops/config.yaml:
```yaml
maintenance_conditions:
  inbox_age_days: 3        # days before inbox items are flagged
  observation_threshold: 10
  tension_threshold: 5
  hub_size_threshold: 40   # when to suggest splitting a project hub
```

## Architectural Changes

For significant changes (new project domain, schema restructuring, processing depth changes):

Use `/arscontexta:architect` — it reads ops/derivation.md, understands the rationale behind current choices, and proposes changes with research backing.

Changes from /architect require approval before implementing. Never auto-applied.

## See Also

- [[workflows]] — how config affects pipeline behavior
- [[meta-skills]] — /architect in detail
- [[manual]] — back to hub
