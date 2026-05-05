# T21 — Runtime Report Browser Read-Only View

## Objective

Specify a bounded read-only browser surface over the E3 packet index and F1 navigation layer.

## Inputs

- packet index JSON under `ION/05_context/runtime_reports/governance/indexes/`
- optional operator dashboard markdown under `ION/05_context/runtime_reports/governance/dashboards/`
- optional F1 navigation packet(s) under `ION/05_context/runtime_reports/governance/navigation/`

## Required behavior

1. Load downstream packet-index data through the existing navigation/query layer.
2. Compute matched facet counts for:
   - artifact kind
   - trigger event
   - source family
3. Render a read-only browser view in markdown, HTML, and JSON.
4. Keep all outputs classified as `GENERATED_STATE`.
5. Permit bounded write-out under `ION/05_context/runtime_reports/governance/browser/`.
6. Preserve explicit boundary language that the browser remains downstream witness material.

## Forbidden behavior

- no mutation of kernel truth
- no doctrine promotion
- no runtime control effects
- no hidden background polling or UI daemon
- no reinterpretation of browser views as operational authority

## Acceptance notes

A conforming implementation should:
- return empty read-only results lawfully when no packet index exists yet
- support filtered browsing over E3-projected entries
- write governed markdown, HTML, and JSON browser outputs for operator use
