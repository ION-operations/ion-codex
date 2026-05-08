# ION V114 Deferred Spawn Visibility Report

## Purpose

V113 stopped zero-spawn carrier turns from writing hot execution-cycle bundles, but cockpit/status still needed to explain the new state. A top-bar view showing `0/5` without deferred/materialization context can make it look like hidden worker work exists.

## Implemented

- Added `plan_spawn_count`, `deferred_spawn_count`, and `execution_bundle_materialized` to `kernel.ion_status`.
- Added the same deferred/materialization fields to the cockpit top bar projection.
- Updated the JOC runtime status panel to display deferred spawn count and bundle state.
- Added regression coverage for deferred spawn visibility in status and cockpit tests.

## Runtime Proof Target

```yaml
status: ION_STATUS_READY
spawn_queue_count: 0
plan_spawn_count: 0
deferred_spawn_count: greater_than_zero
execution_bundle_materialized: false
cockpit_status: ION_COCKPIT_VIEW_MODEL_READY
production_authority: false
live_execution_authority: false
```

## Authority

V114 grants no production authority, live execution authority, deletion authority, worker spawn authority, or live MCP execution authority.
