# T23 — Runtime Report Anchor Normalization Schema

## Intent

Specify the normalized anchor and pointer fields used by downstream runtime-report visibility, navigation, browser, and crosslink layers.

## Scope

Applies only to generated witness surfaces under the runtime-report chain.

## Required normalized fields

### Crosslink target
- `target_kind: string`
- `label: string`
- `relative_path: string`
- `exists: boolean`
- `anchor_kind: string | null`
- `anchor_fragment: string | null`
- `target_ref: string`  
  Computed as `relative_path + anchor_fragment` when a fragment exists.

### Packet-index entry extensions
- `artifact_anchor: string | null`
- `packet_index_pointer: string | null`
- `operator_dashboard_anchor: string | null`
- `governance_ledger_entry_index: integer | null`
- `operator_summary_anchor: string | null`
- `system_ledger_entry_index: integer | null`
- `operator_rollup_anchor: string | null`

## Pointer conventions

### Packet index JSON object
- pointer form: `#/entries/<zero-based-index>`

### Root-array ledgers
- pointer form: `#/<zero-based-index>`

## Markdown anchor conventions

### Artifact anchor
- stable id derived from `artifact_kind` + `source_ref`

### Dashboard anchor
- stable id derived from `trigger_event` + `source_ref` + normalized entry index

### Governance summary anchor
- stable id derived from `artifact_kind` + `source_ref` + batch position

### Governance rollup anchor
- stable id derived from `trigger_event` + `source_ref` + batch position

## Non-goals

- no mutable control plane
- no authority promotion
- no runtime-state mutation through anchor traversal
- no background indexing service

## Verification minimum

1. Crosslink JSON exports include `anchor_kind`, `anchor_fragment`, and `target_ref`.
2. Browser HTML/markdown links include normalized fragments when available.
3. Generated dashboard/summary/rollup/artifact files emit matching stable anchors.
4. Full kernel suite remains green.
