# T28 — Runtime Report Operator Digest

## Objective

Add a bounded read-only operator-digest surface that can combine multiple runtime-report family summaries into one higher-order digest over the downstream witness chain.

## Inputs

- workspace root
- one or more runtime-report temporal selectors
- optional packet-index / dashboard / navigation / browser / crosslink path overrides
- optional output stem and creation time

## Required Behavior

1. Resolve each selector through the existing family-summary layer.
2. Reject operator-digest requests with no selectors.
3. Reject operator-digest requests when any selected family fails to resolve lawfully.
4. Preserve family count and total generation count.
5. Preserve trigger-event / artifact-kind / source-family unions across selected families.
6. Preserve runtime-ref union across selected families.
7. Preserve per-family:
   - generation count
   - first / last generation markers
   - first / last source refs
   - ever-present layers
   - always-present layers
   - transient layers
   - emergent layers
   - vanished layers
8. Preserve per-layer rollups across families:
   - family presence count
   - always-present family count
   - stable target-kind union
   - transient target-kind union
   - emergent target-kind union
   - vanished target-kind union
9. Keep the digest read-only and downstream-only.
10. Support governed markdown/json packet write-out.

## Output Classification

- `digest_kind: RUNTIME_REPORT_OPERATOR_DIGEST`
- `authority_class: GENERATED_STATE`
- `interface_mode: READ_ONLY`

## Governed Output Root

`ION/05_context/runtime_reports/governance/digests/`

## Non-Goals

- no adjudication layer
- no doctrine promotion
- no runtime authority promotion
- no mutation of kernel store/index/graph truth
- no daemon or hidden polling loop
- no claim that an operator digest supersedes family summaries, temporal traces, provenance traces, or individual witness packets as authority
