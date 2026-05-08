---
type: template
template_name: DISAGREEMENT_ESCALATION
created: 2026-04-12T11:26:36-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
---

# TEMPLATE — DISAGREEMENT ESCALATION

Use this when a material disagreement must be turned into a lawful artifact flow rather
than being resolved informally.

## Required frontmatter

```yaml
---
type: disagreement_escalation
template: DISAGREEMENT_ESCALATION
created: <ISO timestamp>
status: <ACTIVE|RECONCILING|RECONCILED|ESCALATED|HELD>
initiated_by: <role>
disagreement_class: <ROLE_MOUNT|EVIDENCE|IMPLEMENTATION|PROTOCOL|LANDING>
subject: <short subject>
primary_artifact: <path or packet under dispute>
---
```

## Required body sections

```markdown
# Disagreement Escalation: <title>

## Trigger

## Surfaces In Disagreement

## Why Work Is Held

## Required Artifact Set

## Reconciliation Rule

## Next Decision Surface
```

## Invariants

1. The disagreement class must be explicit.
2. The packet must name the blocked or disputed surface.
3. The required artifact set must be explicit.
4. The packet must not pretend reconciliation already happened.
5. If the disagreement is unresolved, the next decision surface must say where it goes.
