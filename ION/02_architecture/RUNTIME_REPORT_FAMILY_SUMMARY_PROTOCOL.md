# RUNTIME REPORT FAMILY SUMMARY PROTOCOL

## Purpose

Define a bounded, read-only structural synopsis over downstream runtime-report witness material so a long temporal receipt family can be collapsed into one operator-facing family packet without becoming an authority layer.

## Scope

This protocol applies only to downstream runtime-report witness surfaces already established by prior layers:
- artifact emission
- governance reflection
- governance aggregation
- visibility projection
- navigation packets
- browser bundles
- crosslink packets
- single-receipt provenance traces
- comparative provenance traces
- temporal provenance traces

It does not alter kernel truth, doctrine, route authority, runtime authority, store state, index state, or graph state.

## Law

1. Family summary is **read-only**.
2. Family summary is **temporal-family-bounded**, not open-ended historical analysis.
3. Family summary may collapse one receipt family by preserving:
   - generation count
   - first/last generation span
   - shared family identity fields
   - runtime-ref union
   - per-layer presence coverage
   - per-layer stable target kinds
   - per-layer transient target kinds
   - per-layer emergent target kinds
   - per-layer vanished target kinds
4. Family summary may not claim that one generation is more correct, more authoritative, or more valid than another.
5. Family summary packets remain **GENERATED_STATE** and downstream witness material.

## Required Inputs

A lawful family-summary request must identify a receipt family through one or more bounded family fields such as:
- exact source ref
- source-ref containment
- trigger event
- artifact kind
- source family

A lawful family summary must resolve to at least two matching generations.

## Structural Output Model

A family-summary packet must preserve:
- generation count
- first/last generation span
- shared trigger event / artifact kind / source family when stable
- runtime-ref union
- per-layer presence counts
- per-layer always-present / ever-present state
- per-layer stable / transient / emergent / vanished target kinds
- first and last present generation labels for each layer

A family-summary packet may include:
- packet-index path
- output path
- selector family identity

## Output Paths

Governed family-summary outputs belong under:

`ION/05_context/runtime_reports/governance/provenance/families/`

## Boundary

Family summary does not become:
- kernel truth
- doctrine
- route authority
- runtime authority
- summary authority

It is a bounded visibility aid that compresses one temporal witness family into an operator-readable structural synopsis.
