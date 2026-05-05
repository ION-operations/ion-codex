# V113 Zero-Spawn Execution-Cycle Bloat Guard Lock

## Lock

V113 prevents plan-only zero-spawn carrier turns from creating hot execution-cycle context bundles.

V112 package comparison showed that a zero active spawn queue still generated role sessions, handoffs, compiled context bundles, and context-load receipts under `ION/05_context/current/execution_cycles/`. That is not a file-loss defect, but it is a packaging trust defect because no-op carrier refreshes can grow hot context.

## Current Objective

```text
V113 zero-spawn execution-cycle bloat guard: plan-only carrier turns with max_spawn_rows=0 defer context bundle materialization and keep hot package growth bounded.
```

## Required Runtime State

```yaml
kernel_status: ION_STATUS_READY
spawn_queue_count: 0
zero_spawn_execution_bundle_materialized: false
fresh_package_tests: pass
production_authority: false
live_execution_authority: false
```

## Scope

This lock does not remove existing execution-cycle evidence. Existing files remain preserved. The repair only prevents future zero-spawn carrier refreshes from producing worker context artifacts when no worker can lawfully be spawned.

## Exit Condition

V113 is complete when:

- `build_cycle_plan(..., spawn_row_limit=0)` creates no execution bundle directory
- deferred spawn candidates remain visible in the active role plan
- active carrier turn spawn queue remains empty
- full tests pass
- preservation report shows zero protected and unexpected removals
