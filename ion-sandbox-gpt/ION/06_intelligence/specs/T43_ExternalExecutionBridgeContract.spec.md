# T43 — External Execution Bridge Contract

## Scope

Machine-readable contract for exporting lawful external execution packets and accepting bounded returned execution payloads.

## Required surface

- `kernel/external_execution_bridge.py`

## Inputs

### ExternalExecutionBridgeRequest

Required:
- `workspace_root`
- `action_mode`
- `work_unit_id`

Optional:
- `submission`
- `context_mode`
- `automation_stage`
- `route_stage`
- `calibration_status`
- `threshold_action`
- `review_required`
- `manual_fallback_required`
- `supervisor_present`
- `explicit_approval`
- `dry_run`
- `actor`
- `action_timestamp`

## Action modes

- `EXPORT_DISPATCH_PACKET`
- `ACCEPT_EXECUTION_RETURN`

## Outputs

### ExternalExecutionBridgeReceipt

Must include:
- bridge status
- requested time
- action mode
- work unit id
- control state
- policy evaluation
- optional dispatch result
- optional execution result
- optional export packet path
- optional MCP automation surface
- bridge receipt path
- bridge ledger path

## Statuses

- `EXPORTED`
- `RETURN_ACCEPTED`
- `DRY_RUN`
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`
- `APPROVAL_REQUIRED`

## Lawful behavior

1. Export must use the normal dispatch path.
2. Return acceptance must use the normal execution path.
3. Returned external execution must enter only as proposed commit delta material.
4. Governed write remains downstream from this bridge.
