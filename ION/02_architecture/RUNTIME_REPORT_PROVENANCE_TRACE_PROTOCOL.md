# RUNTIME_REPORT_PROVENANCE_TRACE_PROTOCOL

## Purpose

Define a bounded, read-only provenance-trace layer over downstream runtime-report witness surfaces so one receipt can be followed across:
- artifact emission
- governance reflection
- governance aggregation
- visibility projection
- navigation packets
- browser bundles
- crosslink packets

This protocol is downstream from all prior runtime-report surfaces and does **not** create kernel truth, doctrine, route authority, or runtime authority.

## Governing constraints

1. Provenance traces are **lineage views**, not state authority.
2. Traces must be derived from already-produced packet-index entries and downstream witness files.
3. Resolution starts from one receipt selector only; no broad uncontrolled graph crawl is implied.
4. Missing downstream files stay visible as absence rather than being synthesized.
5. All traced outputs remain read-only and workspace-root bounded.
6. No daemon, watcher, or mutable UI control surface is implied.

## Receipt selector forms

A trace may be resolved by one of:
- `entry_index`
- `packet_index_pointer`
- `source_ref`
- `trigger_event`
- `artifact_kind`

Selectors may be combined for disambiguation.

## Provenance layers

### 1. Artifact
Links the generated runtime-report artifact and its stable artifact anchor when present.

### 2. Governance reflection
Links the governance ledger row and governance summary receipt section when present.

### 3. Governance aggregation
Links the system-ledger row and operator-rollup receipt section when present.

### 4. Visibility projection
Links the packet-index row and operator-dashboard entry section.

### 5. Navigation packets
Locates matching F1 navigation packets that mention the same receipt.

### 6. Browser bundles
Locates matching F2 read-only browser markdown/html/json bundles.

### 7. Crosslink packets
Locates matching F3 crosslink markdown/json packets.

## Boundary

A provenance trace is a downstream read-only lineage packet over witness material.
It may follow the chain across multiple generated files, but it does not promote any of them into operational or constitutional authority.
