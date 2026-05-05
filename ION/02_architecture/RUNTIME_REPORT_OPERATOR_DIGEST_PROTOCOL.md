# RUNTIME REPORT OPERATOR DIGEST PROTOCOL

## Purpose

Define a bounded, read-only higher-order digest over selected runtime-report family summaries so operators can view several receipt families together without turning the digest into an authority surface.

## Scope

This protocol applies only to downstream runtime-report witness surfaces already established by prior layers:
- artifact emission
- governance reflection
- governance aggregation
- visibility projection
- navigation packets
- browser bundles
- crosslink packets
- provenance traces
- comparative provenance traces
- temporal provenance traces
- family summaries

It does not alter kernel truth, doctrine, route authority, runtime authority, store state, index state, or graph state.

## Law

1. Operator digest is **read-only**.
2. Operator digest is **family-summary-bounded**, not open-ended historical analysis.
3. Operator digest may combine multiple family summaries by preserving:
   - family count
   - total generation count
   - shared trigger-event / artifact-kind / source-family unions
   - runtime-ref union
   - per-family identity and generation span markers
   - per-family ever-present / always-present / transient / emergent / vanished layers
   - per-layer family-presence counts
   - per-layer stable / transient / emergent / vanished target-kind unions
4. Operator digest may not claim that one family is more correct, more authoritative, or more valid than another.
5. Operator digests remain **GENERATED_STATE** and downstream witness material.

## Required Inputs

A lawful operator-digest request must include one or more lawful temporal-family selectors that can each resolve to a valid family summary.

Each selected family must resolve to at least two matching generations through the family-summary layer.

## Structural Output Model

An operator-digest packet must preserve:
- family count
- total generation count
- shared trigger-event union
- shared artifact-kind union
- shared source-family union
- runtime-ref union
- per-family generation count and first/last span markers
- per-family layer presence/transience markers
- per-layer family-presence counts
- per-layer stable / transient / emergent / vanished target-kind unions

A digest packet may include:
- packet-index path
- output path
- selector labels for each included family

## Output Paths

Governed operator-digest outputs belong under:

`ION/05_context/runtime_reports/governance/digests/`

## Boundary

Operator digest does not become:
- kernel truth
- doctrine
- route authority
- runtime authority
- digest authority

It is a bounded visibility aid over selected family summaries.
