---
type: template
template_name: PATCH_PACKAGE
created: 2026-04-03T15:51:02-04:00
status: ACTIVE
---

# TEMPLATE — PATCH PACKAGE

Use this when routing a proposed textual or structural correction without directly taking
over another role's governance surface.

## Required frontmatter

```yaml
---
type: patch_package
from: <role>
created: <ISO timestamp>
status: <PROPOSED|ROUTED|SUPERSEDED>
target_owner: <role or lane owner>
targets:
  - <file path>
---
```

## Required body sections

```markdown
# Patch Package: <title>

## Why this patch exists

## Exact surfaces in scope

## Observed drift or defect

## Proposed replacement or correction

## Why this should be applied by the target owner

## Risks if deferred
```

## Invariants

1. Keep scope narrow.
2. Quote or restate only the minimum needed to patch correctly.
3. Preserve the difference between "recommended correction" and "already applied."

## Do not

- silently patch another role's owned governance surface under this template
- bundle unrelated fixes together
