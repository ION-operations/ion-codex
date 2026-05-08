# T20 — Runtime Report Navigation Query

## Objective

Specify a bounded query/navigation surface over the E3 runtime-report packet index.

## Inputs

- packet index JSON under `ION/05_context/runtime_reports/governance/indexes/`
- optional operator dashboard markdown under `ION/05_context/runtime_reports/governance/dashboards/`

## Query fields

- `artifact_kind`
- `trigger_event`
- `source_family`
- `source_ref_contains`
- `runtime_ref_contains`
- `reason_contains`
- `limit`

## Required behavior

1. Load the packet index as a governed downstream input.
2. Filter entries without mutating them.
3. Render a navigation packet that states:
   - packet index path
   - optional operator dashboard path
   - total indexed entries
   - matched entries
   - matched packet summaries
4. Keep all outputs classified as `GENERATED_STATE`.
5. Permit bounded write-out under `ION/05_context/runtime_reports/governance/navigation/`.

## Forbidden behavior

- no mutation of kernel truth
- no implied doctrine promotion
- no runtime control effects
- no background polling or hidden UI daemon

## Acceptance notes

A conforming implementation should:
- return empty results lawfully when no packet index exists yet
- support filtered navigation over E3-generated entries
- write a governed navigation packet for operator use
