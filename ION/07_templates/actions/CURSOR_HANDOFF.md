---
type: template
template_name: CURSOR_HANDOFF
created: 2026-04-03T16:27:55-04:00
revised: 2026-04-09T00:03:00-04:00
status: ACTIVE
---

# TEMPLATE — CURSOR_HANDOFF

Use this for a handoff specifically intended for another IDE chat or bounded IDE-native
execution surface.

## Required frontmatter

```yaml
---
type: cursor_handoff
template: CURSOR_HANDOFF
created: <ISO timestamp>
status: <ACTIVE|COMPLETE>
target_surface: <receiving chat or executor surface>
objective: <bounded task>
---
```

## Required sections

```markdown
# Cursor Handoff: <title>

## Role / chassis target

## Load order

## Exact files to read first

## Task to perform

## Boundaries

## Expected output artifact
```

## Invariants

1. Keep the initial read set small and explicit.
2. Name source continuity and projection surfaces correctly.
3. If the receiving surface is optional or non-default, say so.
4. New canonical cursor handoffs should satisfy the normalized packet protocol.
