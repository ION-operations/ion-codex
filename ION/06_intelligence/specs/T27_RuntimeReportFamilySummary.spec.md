# T27 — Runtime Report Family Summary

## Objective

Add a bounded read-only family-summary surface that can collapse successive generations of one runtime-report receipt family into a structural synopsis over the existing downstream witness chain.

## Inputs

- workspace root
- runtime-report temporal selector
- optional packet-index / dashboard / navigation / browser / crosslink path overrides
- optional output stem and creation time

## Required Behavior

1. Resolve the requested family through the existing temporal provenance layer.
2. Reject family-summary requests that resolve to fewer than two matching generations.
3. Preserve first and last generation span for the matched family.
4. Preserve shared family identity fields when stable across the family.
5. Preserve runtime-ref union across all matched generations.
6. Summarize each downstream layer by:
   - presence count
   - always-present / ever-present state
   - max target count
   - stable target kinds
   - transient target kinds
   - emergent target kinds
   - vanished target kinds
   - first / last present generation labels
7. Keep the summary read-only and downstream-only.
8. Support governed markdown/json packet write-out.

## Output Classification

- `summary_kind: RUNTIME_REPORT_FAMILY_SUMMARY`
- `authority_class: GENERATED_STATE`
- `interface_mode: READ_ONLY`

## Governed Output Root

`ION/05_context/runtime_reports/governance/provenance/families/`

## Non-Goals

- no adjudication layer
- no doctrine promotion
- no runtime authority promotion
- no mutation of kernel store/index/graph truth
- no daemon or hidden polling loop
- no claim that a family summary supersedes individual temporal or provenance packets as authority
