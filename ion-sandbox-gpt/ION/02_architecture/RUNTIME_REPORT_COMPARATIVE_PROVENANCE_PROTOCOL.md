# RUNTIME REPORT COMPARATIVE PROVENANCE PROTOCOL

## Purpose

Define a bounded, read-only comparison surface over downstream runtime-report witness material so two or more receipts can be placed side by side across the same lineage chain without becoming an authority layer.

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

It does not alter kernel truth, doctrine, route authority, runtime authority, store state, index state, or graph state.

## Law

1. Comparative provenance is **read-only**.
2. Comparative provenance is **structural**, not adjudicative.
3. Comparative provenance may compare presence, target kinds, and downstream target refs.
4. Comparative provenance may not claim that one receipt is correct, superior, or authoritative.
5. Comparative packets remain **GENERATED_STATE** and downstream witness material.

## Required Inputs

A lawful comparative request must provide at least two receipt selectors.

Each selector resolves through the existing provenance-trace selection rules and may target receipts by bounded receipt-identification fields such as:
- entry index
- packet-index pointer
- source ref
- trigger event
- artifact kind

## Comparative Output Model

A comparative packet must preserve:
- compared receipt count
- per-receipt identity
- per-layer receipt views
- shared presence across compared receipts
- shared target kinds
- divergent target kinds

A comparative packet may include:
- packet-index path
- runtime refs
- target refs for each compared receipt

## Output Paths

Governed comparative outputs belong under:

`ION/05_context/runtime_reports/governance/provenance/comparisons/`

## Boundary

Comparative provenance does not become:
- kernel truth
- doctrine
- route authority
- runtime authority
- comparative analysis authority

It is a bounded visibility aid over already-generated downstream witness chains.
