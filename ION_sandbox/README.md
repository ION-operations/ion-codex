# ION Sandbox Source Lane

This directory stores sandbox package snapshots and candidate release roots.
It is not the active ION runtime root.

## Current Custody

- lane_class: `sandbox_snapshot_bulk`
- authority: package snapshot / evidence
- active_runtime_authority: false
- production_authority: false
- live_execution_authority: false

The current observed snapshot is large enough that it should not be mixed into
a normal runtime feature commit. It should be compared against the intended
release branch or archived with an explicit receipt before staging.

## Settlement Rule

Before committing this lane:

1. Compare the snapshot against any published release branch or package bundle.
2. Decide whether the active root needs a full nested package snapshot or only
   a manifest and provenance receipt.
3. Do not delete or move this lane without an explicit lifecycle receipt.
4. Keep sandbox package custody separate from active kernel/runtime changes.
