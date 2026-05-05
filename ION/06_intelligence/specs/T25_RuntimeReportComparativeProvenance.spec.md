# T25 — Runtime Report Comparative Provenance

## Objective

Add a bounded read-only comparison surface that can place two or more runtime-report receipts side by side across the existing downstream witness chain.

## Inputs

- workspace root
- two or more runtime-report provenance selectors
- optional packet-index / dashboard / navigation / browser / crosslink path overrides
- optional output stem and creation time

## Required Behavior

1. Reject comparison requests with fewer than two selectors.
2. Resolve each selector through the existing single-receipt provenance layer.
3. Preserve receipt identity for each compared item.
4. Compare each downstream layer by:
   - shared presence
   - shared target kinds
   - divergent target kinds
   - per-receipt target refs
5. Keep the comparison read-only and downstream-only.
6. Support governed markdown/json packet write-out.

## Output Classification

- `comparison_kind: RUNTIME_REPORT_COMPARATIVE_PROVENANCE_TRACE`
- `authority_class: GENERATED_STATE`
- `interface_mode: READ_ONLY`

## Governed Output Root

`ION/05_context/runtime_reports/governance/provenance/comparisons/`

## Non-Goals

- no adjudication layer
- no doctrine promotion
- no runtime authority promotion
- no mutation of kernel store/index/graph truth
- no daemon or hidden polling loop
