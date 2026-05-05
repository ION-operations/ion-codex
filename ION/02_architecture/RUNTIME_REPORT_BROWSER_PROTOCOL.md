# RUNTIME REPORT BROWSER PROTOCOL

## Purpose

Define a bounded read-only browser layer over the runtime-report visibility chain.
This layer sits on top of the E3 packet index and the F1 navigation/query surface so
operators can browse downstream witness material without promoting it into kernel truth.

## Upstream dependency chain

Browser access is lawful only when it remains explicitly downstream from:

1. runtime-report artifacts
2. governance reflections
3. governance aggregation
4. visibility projection
5. navigation/query packets

The browser layer must never bypass that chain.

## Governing inputs

Primary inputs:
- `ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json`
- `ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md`

Optional companion input:
- `ION/05_context/runtime_reports/governance/navigation/*.md`

## Allowed capabilities

The browser layer may:
- execute read-only queries over the downstream packet index
- compute matched facet counts for artifact kind, trigger event, and source family
- render bounded markdown, HTML, and JSON browser views
- optionally write those views under a governed browser output root
- optionally ask the F1 navigator to emit a companion navigation packet

The browser layer may not:
- mutate kernel store/index/graph truth
- alter runtime posture or trigger state changes
- reinterpret browser outputs as doctrine or authority
- create hidden autonomous polling, UI daemons, or mutable control planes

## Output class

Browser packets are `GENERATED_STATE` witness surfaces.
They remain subordinate to the packet index, operator dashboard, and all earlier
runtime-report stages.

## Default output root

- `ION/05_context/runtime_reports/governance/browser/`

## Boundary

Browser output is for bounded human lookup and read-only browsing only.
It does not become:
- doctrine
- runtime authority
- route authority
- kernel truth
