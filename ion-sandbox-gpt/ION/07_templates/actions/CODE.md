---
type: template
template_name: CODE
created: 2026-04-03T18:58:00-04:00
status: ACTIVE
---

# TEMPLATE — CODE

Use this for bounded implementation work that changes source files, tests, or tightly
scoped runtime surfaces.

## Recommended frontmatter

```yaml
---
type: implementation
from: <role>
created: <ISO timestamp>
status: <ACTIVE|COMPLETE|BLOCKED>
target: <primary file or package path>
connections:
  - <supporting paths>
---
```

## Required body sections

```markdown
# Implementation: <title>

## Goal

## Scope

## Files changed

## Tests or verification

## Risks or follow-ups
```

## Invariants

1. Scope must stay bounded to the governing task.
2. Verification must say what was actually run, or explicitly say no automated test
   applied.
3. If judgment authority is still needed after the code change, call that out rather
   than implying the implementation completed the whole governance loop.
