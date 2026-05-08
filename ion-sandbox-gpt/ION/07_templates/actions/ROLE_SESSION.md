---
type: template
template_name: ROLE_SESSION
created: 2026-04-03T17:34:38-04:00
revised: 2026-04-09T00:03:00-04:00
status: ACTIVE
---

# TEMPLATE — ROLE_SESSION

Use this when the sequential kernel generates or a role records one bounded role-pass
session inside a larger trace or execution bundle.

## Required frontmatter

```yaml
---
type: role_session
template: ROLE_SESSION
created: <ISO timestamp>
status: <PLANNED|ACTIVE|COMPLETE>
role: <role name>
objective: <bounded objective>
workstream: <optional workstream>
source_task: <optional task path>
next_role: <optional next role>
---
```

## Required body sections

```markdown
# Role Session: <role>

## Role

## Purpose

## Source Task / Objective

## Required Reads

## Expected Output

## Next Target

## Notes
```

## Invariants

1. A role session records one pass only.
2. It does not claim independent review already happened unless the role actually performed it.
3. Source continuity should be listed before shared projections when both appear.
4. New canonical role-session packets should satisfy the normalized packet protocol.
5. Historical names may appear as witness, but live role fields should resolve to current true names under lineage law.
