# RUNTIME_REPORT_ANCHOR_NORMALIZATION_PROTOCOL

## Purpose

Define a bounded, read-only normalization layer for downstream runtime-report witness surfaces so crosslinks can target stable packet rows, receipt sections, and JSON entry pointers rather than only whole files.

This protocol is downstream from:
- runtime-report artifacts
- governance reflections
- governance aggregation
- visibility projection
- navigation, browser, and crosslink surfaces

It does **not** introduce new kernel truth, route authority, runtime authority, or doctrine.

## Governing constraints

1. Anchors and pointers are **navigation aids**, not state authority.
2. Normalization must remain deterministic from already-produced downstream witness data.
3. File paths remain primary; fragments refine traversal inside those files.
4. JSON ledgers and indexes use JSON-pointer style fragments.
5. Markdown witness packets use stable anchor ids emitted into the file body.
6. No daemon, poller, or mutable UI control surface is implied.

## Normalized target families

### 1. Artifact anchors

Generated runtime-report artifacts emit a stable top-level anchor derived from:
- artifact kind
- source ref

This permits crosslink traversal into a specific artifact packet rather than only to its containing file.

### 2. Packet-index pointers

`runtime_report_packet_index.json` targets use a JSON pointer of the form:
- `#/entries/<zero-based-index>`

This preserves row-precise traversal without reclassifying the JSON index as operational authority.

### 3. Dashboard section anchors

`runtime_report_operator_dashboard.md` emits stable per-entry anchors derived from:
- trigger event
- source ref
- normalized entry index

### 4. Governance summary anchors

Governance summaries emit stable per-receipt anchors derived from:
- artifact kind
- source ref
- batch position

### 5. System/governance ledger pointers

JSON ledgers use root-array pointers of the form:
- `#/<zero-based-index>`

### 6. Governance rollup anchors

Rollups emit stable per-receipt anchors derived from:
- trigger event
- source ref
- batch position

## Required downstream metadata

Packet-index entries may carry normalized traversal fields such as:
- `artifact_anchor`
- `packet_index_pointer`
- `operator_dashboard_anchor`
- `governance_ledger_entry_index`
- `operator_summary_anchor`
- `system_ledger_entry_index`
- `operator_rollup_anchor`

These remain descriptive traversal metadata only.

## Boundary

Anchor normalization is a downstream traversal discipline over witness outputs.
It does not convert any browser, navigation, dashboard, ledger, summary, rollup, or artifact surface into kernel truth.
