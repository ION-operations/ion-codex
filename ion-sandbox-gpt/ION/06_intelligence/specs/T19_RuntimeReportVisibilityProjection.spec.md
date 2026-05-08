# T19_RuntimeReportVisibilityProjection

## Intent

Define the bounded downstream visibility layer for aggregated runtime-report witnesses.

## Inputs

- `RuntimeReportTriggerReceipt[]` carrying E2 aggregation witness fields
- explicit workspace root
- optional packet-index and dashboard path overrides

## Outputs

### Packet index

Machine-readable JSON object:
- `index_kind`
- `authority_class`
- `updated_at`
- `entry_count`
- `entries[]`

Each entry records:
- visibility event id
- trigger event
- artifact kind
- source ref + source family
- artifact path + generated time
- runtime refs
- governance / aggregation witness paths

### Operator dashboard

Markdown dashboard with:
- coverage summary
- trigger-event counts
- artifact-kind counts
- source-family counts
- recent projected packets
- explicit downstream boundary text

## Rules

- [ ] Projection runs only when explicitly requested.
- [ ] Projection only consumes receipts that already carry E2 aggregation witness markers.
- [ ] Projection never mutates kernel store, kernel index, or graph truth.
- [ ] Packet index entries keep pointers to upstream artifacts, summaries, rollups, and ledgers.
- [ ] Dashboard remains a downstream view, not doctrine or runtime authority.
- [ ] Default paths stay under governed `ION/05_context/runtime_reports/governance/` roots.
