# Workpackets Source Lane

This directory is a root source lane for operator work packets, candidate
instructions, OpenAPI drafts, prompt packets, and planning artifacts that are
useful evidence for ION work but are not automatically active runtime state.

## Current Custody

- lane_class: `root_source_lane_artifacts`
- authority: evidence / candidate input
- active_runtime_authority: false
- production_authority: false
- live_execution_authority: false

Files here should be staged separately from kernel code. A workpacket becomes
active only when a bounded ION packet, receipt, or explicit operator decision
routes it into active context.

## Settlement Rule

Before committing this lane:

1. Confirm each file is intentional evidence or a reusable packet.
2. Keep loose workpackets separate from runtime receipts and generated package
   snapshots.
3. If a file is superseded, classify it in a receipt before moving or deleting
   it.
4. Update `WORKPACKET_INDEX_20260508T190626Z.json` when adding or removing
   source-lane files.
