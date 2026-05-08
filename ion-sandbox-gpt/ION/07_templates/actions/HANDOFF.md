---
type: template
template_name: HANDOFF
created: 2026-04-03T16:27:55-04:00
revised: 2026-04-09T00:03:00-04:00
status: ACTIVE
---

# TEMPLATE — HANDOFF

Use this when one role is passing a bounded result or next-action packet to another.

## Required frontmatter

```yaml
---
type: handoff
template: HANDOFF
created: <ISO timestamp>
status: <ACTIVE|COMPLETE>
from: <sender>
to: <receiver>
objective: <bounded next step>
---
```

## Required sections

```markdown
# Handoff: <title>

## From

## To

## What was completed

## What remains

## Exact artifacts to read

## Risks / warnings

## Requested next action
```

## Invariants

1. Handoffs should point to exact artifact paths.
2. They should preserve unresolved questions, not flatten them away.
3. A handoff is not a silent transfer of authority.
4. New canonical handoffs should satisfy the normalized packet protocol.
