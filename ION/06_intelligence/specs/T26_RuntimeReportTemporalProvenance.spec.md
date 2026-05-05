# T26 — Runtime Report Temporal Provenance

## Objective

Add a bounded read-only temporal comparison surface that can compare successive generations of one runtime-report receipt family across the existing downstream witness chain.

## Inputs

- workspace root
- runtime-report temporal provenance selector
- optional packet-index / dashboard / navigation / browser / crosslink path overrides
- optional output stem and creation time

## Required Behavior

1. Reject temporal requests that do not identify a bounded receipt family.
2. Reject temporal requests that resolve to fewer than two matching generations.
3. Resolve each matched generation through the existing single-receipt provenance layer.
4. Preserve chronological order across compared generations.
5. Compare each downstream layer by:
   - per-generation target counts
   - per-generation target kinds
   - per-generation target refs
   - stable target kinds across all generations
   - emergent target kinds across successive transitions
   - vanished target kinds across successive transitions
6. Keep the comparison read-only and downstream-only.
7. Support governed markdown/json packet write-out.

## Output Classification

- `comparison_kind: RUNTIME_REPORT_TEMPORAL_PROVENANCE_TRACE`
- `authority_class: GENERATED_STATE`
- `interface_mode: READ_ONLY`

## Governed Output Root

`ION/05_context/runtime_reports/governance/provenance/temporal/`

## Non-Goals

- no adjudication layer
- no doctrine promotion
- no runtime authority promotion
- no mutation of kernel store/index/graph truth
- no daemon or hidden polling loop
- no claim that later generations supersede earlier generations as authority
