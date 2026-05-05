# T13 — Runtime State Query Consumption Schema

## Scope

Defines the C3 consumption contract for machine-readable runtime posture.

## Required View Shapes

### RuntimeStateScopeView
- `scope_type`
- `scope_ref`
- `manifest` (optional)
- `automation` (optional)
- `work_unit` (optional)
- `state_refs[]`
- `latest_timestamp` (optional)

### RuntimeReviewPressure
- `requires_review`
- `reason`
- `source_created_at`
- `detail_refs[]`

### RuntimeDispatchPosture
- `dispatch_permitted`
- `reason`
- `blockers[]`
- `source_created_at`

## Consumption Rules

- review escalation may include runtime-state references in context
- signal follow-up may include runtime-state references in context
- daemon dispatch must skip work units with explicit runtime-state blocking posture

## Graph Rules

Nodes:
- `manifest_route_state:{manifest_id}`
- `automation_state:{automation_state_id}`

Edges:
- `MANIFEST_FOR_WORK`
- `AUTOMATION_FOR_WORK`
- `MANIFEST_BINDS_AUTOMATION`
