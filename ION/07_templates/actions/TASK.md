---
type: template
template_name: TASK
created: 2026-04-03T15:51:02-04:00
status: ACTIVE
---

# TEMPLATE — TASK

Use this when dispatching a bounded work item to a role or lane.

## Required frontmatter

```yaml
---
type: task
agent: <target role>
template: <TASK|CODE|RESEARCH|AUDIT|PATCH_PACKAGE|other bound template>
priority: <P0|P1|P2|P3>
created: <ISO timestamp>
from: <sender>
target: <primary destination path or artifact>
depends_on: <optional dependency or task id>
---
```

## Lifecycle fields

When a live task is advanced or retired, the active system may add:

```yaml
status: <ACTIVE|COMPLETE|BLOCKED|SUPERSEDED>
updated: <ISO timestamp>
completed_by: <role>
```

Completed tasks may then be moved into `ION/05_context/inbox/completed/`.

## Required body sections

```markdown
# Mission: <short task title>

## Goal

## Source / Context

## Requirements

## Deliverables

## Constraints

## Completion Signal
```

## Invariants

1. One task should describe one bounded work unit.
2. Write scope must be explicit.
3. If review is required, the review path must be named.
4. If a missing template is being substituted inline, say so in `Requirements` or `Constraints`.
5. When a task is completed, the system should preserve a visible completion record instead of silently deleting or replacing the task.
6. Live authority fields should use current true names; if a historical token matters for provenance, preserve it explicitly instead of silently treating it as active authority.

## Do not

- assign broad ambiguous ownership
- leave write scope implicit
- hide dependencies in chat only
