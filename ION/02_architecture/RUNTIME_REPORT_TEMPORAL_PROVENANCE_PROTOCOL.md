# RUNTIME REPORT TEMPORAL PROVENANCE PROTOCOL

## Purpose

Define a bounded, read-only temporal comparison surface over downstream runtime-report witness material so successive generations of one receipt family can be traced across the same lineage chain without becoming an authority layer.

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

It does not alter kernel truth, doctrine, route authority, runtime authority, store state, index state, or graph state.

## Law

1. Temporal provenance is **read-only**.
2. Temporal provenance is **family-bounded**, not open-ended history scraping.
3. Temporal provenance may compare successive generations by:
   - chronological ordering
   - layer presence
   - target kinds
   - target refs
   - added or removed target kinds between generations
4. Temporal provenance may not claim that a later generation is more correct, more authoritative, or more valid than an earlier one.
5. Temporal provenance packets remain **GENERATED_STATE** and downstream witness material.

## Required Inputs

A lawful temporal request must identify a receipt family through one or more bounded family fields such as:
- exact source ref
- source-ref containment
- trigger event
- artifact kind
- source family

A lawful temporal trace must resolve to at least two matching generations.

## Temporal Output Model

A temporal packet must preserve:
- generation count
- per-generation identity
- chronological ordering
- per-layer generation views
- per-layer stable target kinds
- per-layer emergent target kinds
- per-layer vanished target kinds
- transition summaries between successive generations

A temporal packet may include:
- packet-index path
- packet-index pointers
- runtime refs
- downstream target refs for each generation

## Output Paths

Governed temporal outputs belong under:

`ION/05_context/runtime_reports/governance/provenance/temporal/`

## Boundary

Temporal provenance does not become:
- kernel truth
- doctrine
- route authority
- runtime authority
- temporal analysis authority

It is a bounded visibility aid over already-generated downstream witness chains across successive generations of one receipt family.
