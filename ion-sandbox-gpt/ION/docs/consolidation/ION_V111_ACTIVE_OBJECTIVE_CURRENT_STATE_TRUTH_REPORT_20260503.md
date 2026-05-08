# ION V111 Active Objective Current-State Truth Report

## Purpose

After V110, package mountability and preservation were correct, but active carrier state still named the older V107 objective. That was operationally misleading for future carriers.

V111 refreshes the active objective through `kernel.ion_carrier_continue` and repairs zero-spawn return-intake wording.

## Implemented

- Refreshed active carrier objective to the current V111 state.
- Used `plan-only` and `max_spawn_rows=0` to avoid creating a new worker obligation.
- Updated `kernel.ion_carrier_continue` so zero active spawn rows produce `NO_TASK_RETURNS_REQUIRED` instead of `WAITING_FOR_TASK_RETURNS`.
- Updated cockpit spawn counts to use the active carrier turn spawn queue when present, so a zero-spawn plan-only turn does not display pending worker work.
- Updated status/cockpit package proof projection to discover the latest `SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json` sidecar instead of hardcoding a branch number.
- Added a focused test proving plan-only zero-spawn turns do not wait for task returns.

## Runtime Proof Target

```yaml
status: ION_STATUS_READY
objective: V111 current-state truth repair
spawn_queue_count: 0
task_return_total: 0
steward_queue_pending_count: 0
next_lawful_action: continue_or_queue_new_work
production_authority: false
live_execution_authority: false
```

## Authority

V111 grants no production authority, live execution authority, file deletion authority, live MCP execution authority, or worker spawn authority.
