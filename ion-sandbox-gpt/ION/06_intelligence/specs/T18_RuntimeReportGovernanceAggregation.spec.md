# T18 — Runtime Report Governance Aggregation

## Objective

Specify bounded aggregation of E1 runtime-report governance reflections into broader operator/system witness surfaces.

## Inputs

- `RuntimeReportTriggerReceipt`
- optional E1 governance metadata (`governance_event_id`, `governance_ledger_path`, `operator_summary_path`)
- explicit workspace root
- explicit aggregation policy

## Outputs

- optional append to `ION/05_context/history/system_ledger.json`
- optional operator rollup under `ION/05_context/runtime_reports/governance/rollups/`
- receipts annotated with aggregation metadata

## Required properties

- explicit opt-in
- workspace-root bounded output paths
- `GENERATED_STATE` classification for rollups
- aggregation remains subordinate witness over prior runtime artifacts and receipts

## Forbidden claims

- no doctrine promotion
- no kernel truth promotion
- no autonomous daemon or background summarizer claim
