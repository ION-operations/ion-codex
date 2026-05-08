# ION V113 Zero-Spawn Execution-Cycle Bloat Guard Report

## Purpose

V112 fixed package-runnable status tests, then its preservation diff exposed another issue: a plan-only carrier turn with `max_spawn_rows=0` still created role-session packets, handoffs, compiled context bundles, and context-load receipts.

Those files are important when workers are actually spawned. They are bloat when the active carrier turn emits no spawn rows.

## Implemented

- Added `spawn_row_limit` to `kernel.ion_cycle_runner.build_cycle_plan`.
- Passed `max_spawn_rows` from `kernel.ion_carrier_continue` into the cycle planner.
- When `spawn_row_limit=0`, the planner now defers spawn candidates, writes no execution bundle, and marks context package fields as deferred instead of materializing worker prompts.
- Added a regression test proving zero-spawn planning creates no execution-cycle directory.

## Runtime Proof Target

```yaml
status: ION_STATUS_READY
active_spawn_count: 0
deferred_spawn_count: greater_than_zero
execution_bundle_materialized: false
trace_path: null
session_paths: []
handoff_paths: []
production_authority: false
live_execution_authority: false
```

## Authority

V113 grants no production authority, live execution authority, deletion authority, worker spawn authority, or live MCP execution authority.
