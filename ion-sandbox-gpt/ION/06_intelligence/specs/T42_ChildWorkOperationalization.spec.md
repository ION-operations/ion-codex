# T42 — Child Work Operationalization

## Intent

Turn planner-gated child-work issuance into a **supervised service path** with explicit policy, control, approval, and receipts.

## Inputs

The supervised child-work service must accept either:

### A. Manifest selection
- `manifest_id`

### B. Question/delta selection
- `question_id`
- `work_unit_id`
- `delta_id`

## Required request fields

- `workspace_root`
- `repo_root`
- `doctrine`
- `selection_mode`
- optional `agent_bindings`
- policy posture fields:
  - `context_mode`
  - `automation_stage`
  - `route_stage`
  - `calibration_status`
  - `threshold_action`
- approval/control fields:
  - `supervisor_present`
  - `explicit_approval`
  - `dry_run`

## Required derived checks

The implementation must derive or inspect:
- runtime dispatch posture for the parent work unit,
- runtime review pressure for the selected planner delta,
- parent spawn policy approval requirements,
- operator service mode,
- work-unit or manifest holds.

## Required statuses

- `ISSUED`
- `DRY_RUN`
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`
- `APPROVAL_REQUIRED`

## Required side effects

When issuance succeeds:
1. child work units and context packages are persisted through the existing planner/child path,
2. the planner manifest is marked executed,
3. a service receipt JSON is written,
4. a service ledger row is appended.

## Required refusal behavior

The service must refuse lawfully when:
- operator stop or hold is active,
- runtime dispatch posture requires manual fallback,
- automation policy blocks issuance,
- explicit approval is required but absent.

## Required daemon-service integration

The daemon service must expose the supervised child-work service as a direct delegated path.
This integration does not imply a hidden unattended child-issuance loop.

## Non-goals

- unattended multi-agent field
- autonomous approval inference
- MCP / external execution
- authority promotion of child-work service receipts
