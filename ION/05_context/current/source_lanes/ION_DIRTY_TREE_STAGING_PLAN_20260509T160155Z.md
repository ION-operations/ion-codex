# ION Dirty Tree Staging Plan

status: `PROPOSED_NOT_STAGED`

This plan is based on:

- `/tmp/ion_dirty_tree_settlement_manifest_20260509T160155Z.json`
- branch `feature/codex-capsule-chat-active-root`
- head `b24ecb5`

No files have been staged by this plan.

## Proposed Commit Groups

### 1. Source-Lane Metadata Repair

Default action: commit after review.

Paths:

- `workpackets/README.md`
- `workpackets/WORKPACKET_INDEX_20260508T190626Z.json`
- `diffs/README.md`
- `diffs/DIFF_INDEX_20260508T190626Z.json`
- `ION_sandbox/README.md`
- `ION_sandbox/ION_SANDBOX_INDEX_20260508T190626Z.json`
- `ION/05_context/current/source_lanes/ION_ROOT_SOURCE_LANE_POLICY_20260508T190626Z.md`
- `ION/05_context/current/source_lanes/receipts/ION_ROOT_SOURCE_LANE_FORMALIZATION_RECEIPT_20260508T190626Z.json`
- `ION/05_context/current/source_lanes/ION_DIRTY_TREE_STAGING_PLAN_20260509T160155Z.md`

Validation:

- `python3 -m json.tool` on all new JSON files.
- `git diff --check`.

### 2. Core Kernel And Tests

Default action: split into feature commits after focused tests.

Buckets:

- `core_kernel_code`
- `test_coverage`
- `protocol_registry_template_docs`
- `custom_gpt_action_integration_docs`
- `local_service_systemd_templates`

Likely commit slices:

- Custom GPT action gateway and OpenAPI surfaces.
- Public cockpit auth and local cockpit app.
- Single-carrier sequence runner and receipt template.
- Assistant Work candidate lifecycle and route compiler.
- Stale-surface audit and sandbox preflight.

### 3. Browser Extension Bridge

Default action: validate source and dist provenance before staging.

Buckets:

- `browser_extension_bridge`

Required check:

- Confirm `src/content.ts` and `src/approval_ui.ts` produce the checked-in
  `dist/content.js`, or regenerate `dist/content.js` in a separate approved
  build step.

### 4. Active Context And Receipts

Default action: review field diffs and commit only authoritative state.

Buckets:

- `active_context_state_projection`
- `ai_assistant_work_candidate_state`
- `self_knowledge_candidate_state`
- `single_carrier_sequence_receipts`
- `codex_queue_run_evidence`
- `codex_queue_task_returns`
- `chatops_bridge_receipts`
- `action_gateway_receipts_state`

Hold by default:

- runtime upload tickets
- transient logs
- queue scratch not referenced by accepted receipts
- regenerated timestamps without state value

### 5. Bulk Custom GPT Packaging

Default action: do not commit into this feature commit set by default.

Bucket:

- `custom_gpt_packaging_orchestration_bulk`

Reason:

- 3,902 files.
- Large generated/packaging evidence lane.
- Needs separate custody decision: archive, dedicated release branch, or
  selected manifest-only commit.

### 6. ION Sandbox Snapshot

Default action: do not commit into this feature commit set by default.

Bucket:

- `sandbox_snapshot_bulk`

Reason:

- 3,736 untracked Git files observed in the snapshot bucket.
- Full nested package snapshot should be compared against the published release
  root before commit, archive, or ignore custody is chosen.

### 7. Loose Root Source Artifacts

Default action: review separately from code.

Buckets:

- `root_source_lane_artifacts`
- `research_evidence_lane`
- `ion_sandbox_gpt_release_residue`

Rule:

- Commit only if the artifact is intentionally part of the active root evidence
  package. Otherwise archive, ignore, or move under a future approved custody
  receipt.

## Next Approval Gate

Recommended next command set before staging:

```bash
python3 -m json.tool workpackets/WORKPACKET_INDEX_20260508T190626Z.json
python3 -m json.tool diffs/DIFF_INDEX_20260508T190626Z.json
python3 -m json.tool ION_sandbox/ION_SANDBOX_INDEX_20260508T190626Z.json
python3 -m json.tool ION/05_context/current/source_lanes/receipts/ION_ROOT_SOURCE_LANE_FORMALIZATION_RECEIPT_20260508T190626Z.json
git diff --check
```

After that, the operator should approve one of:

- stage metadata repair only
- stage metadata plus one focused feature slice
- continue read-only review of bucket contents
- archive or ignore specific bulk buckets with a separate lifecycle receipt
