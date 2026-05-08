# T16 — Runtime Report Trigger Policy

## Objective

Define the machine-facing policy surface for bounded automatic emission of runtime packets during already-invoked kernel events.

## Required fields

- `workspace_root`
- `generated_at` (optional)
- `emit_manifest_packet_on_create`
- `emit_review_packet_on_escalation`
- `emit_scope_status_on_governed_write_sync`
- `emit_scope_status_on_capsule_sync`
- `require_blocking_posture_for_scope_status`

## Events

- `PLANNER_MANIFEST_CREATED`
- `REVIEW_ESCALATED`
- `GOVERNED_WRITE_SYNCED`
- `CAPSULE_SYNCED`

## Output receipt

Each triggered emission returns a receipt containing:

- event
- artifact kind
- source ref
- reason
- artifact result

## Constraints

- artifacts must remain `GENERATED_STATE`
- emission requires an explicit workspace root
- sync-triggered scope reports default to blocking posture only
- trigger handling must not imply autonomous scheduling
