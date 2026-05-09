# Diffs Source Lane

This directory stores patch artifacts and candidate change files that can be
reviewed, applied, or archived by a later ION work cycle.

## Current Custody

- lane_class: `root_source_lane_artifacts`
- authority: patch evidence / candidate input
- active_runtime_authority: false
- production_authority: false
- live_execution_authority: false

Diff files here are not accepted state by themselves. They should be linked to
receipts or workpackets before being treated as landed changes.

## Settlement Rule

Before committing this lane:

1. Confirm the diff is still useful evidence.
2. Confirm whether it has already been applied, superseded, or rejected.
3. Keep patch evidence separate from active kernel commits.
4. Update `DIFF_INDEX_20260508T190626Z.json` when diff custody changes.
