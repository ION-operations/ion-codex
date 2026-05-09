# ION Root Source Lane Policy

status: `RECONSTRUCTED_METADATA`

This policy repairs the missing source-lane metadata referenced by capsule row
`C-049`. It is a custody policy for loose root source lanes. It is not a claim
that every file in those lanes is accepted runtime state.

## Lanes

| Lane | Class | Default Custody | Commit Guidance |
| --- | --- | --- | --- |
| `workpackets/` | root source lane | candidate packets / planning evidence | review separately from code |
| `diffs/` | root source lane | patch evidence | link to receipts before acceptance |
| `ION_sandbox/` | sandbox snapshot bulk | package snapshot evidence | compare/archive or isolate to release branch |
| `what_is_ion/` | source reference lane | explainer/reference input | commit only if intentionally part of public/reference package |
| `assessment/` | assessment lane | workflow assessment evidence | commit with evidence/research context |
| `ion-sandbox-gpt/` | release residue | release-root residue | compare to release branch before staging |

## Authority

These lanes are evidence and source inputs. They do not override:

1. `ION/REPO_AUTHORITY.md`
2. `ION/02_architecture/ION_MOUNT_CONTRACT.md`
3. current active packets and receipts
4. tests and proof gates
5. explicit operator instructions

## Settlement Rules

1. Do not mix bulk source-lane snapshots with focused kernel/runtime commits.
2. Do not delete, move, or hide a meaningful source-lane artifact without a
   lifecycle receipt.
3. Index files may be reconstructed when missing, but they must say so.
4. Binary package artifacts should be reviewed before commit and may need
   archive, release-branch, or ignore custody instead of active-root tracking.
5. Runtime logs, upload tickets, queue run scratch, and generated local service
   state require explicit acceptance before commit.

## Current Repair

The following missing metadata surfaces were reconstructed on 2026-05-09 from
the current working tree and the dirty-tree settlement manifest:

- `workpackets/README.md`
- `workpackets/WORKPACKET_INDEX_20260508T190626Z.json`
- `diffs/README.md`
- `diffs/DIFF_INDEX_20260508T190626Z.json`
- `ION_sandbox/README.md`
- `ION_sandbox/ION_SANDBOX_INDEX_20260508T190626Z.json`
- `ION/05_context/current/source_lanes/ION_ROOT_SOURCE_LANE_POLICY_20260508T190626Z.md`
- `ION/05_context/current/source_lanes/receipts/ION_ROOT_SOURCE_LANE_FORMALIZATION_RECEIPT_20260508T190626Z.json`

The full dirty-tree classification manifest was generated outside the repo at:

`/tmp/ion_dirty_tree_settlement_manifest_20260509T160155Z.json`
