# RUNTIME REPORT NAVIGATION PROTOCOL

## Purpose

Define a bounded human-facing navigation/query layer over E3 runtime-report visibility outputs.
This layer consumes downstream packet indexes and dashboards so operators can locate packets
without promoting those visibility artifacts into kernel truth.

## Upstream dependency chain

Navigation is lawful only when it remains explicitly downstream from:

1. runtime-report artifacts
2. governance reflections
3. governance aggregation
4. visibility projection

The navigation layer must never bypass that chain.

## Governing inputs

Primary input:
- `ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json`

Optional companion input:
- `ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md`

## Allowed capabilities

The navigation layer may:
- load the governed packet index
- filter entries by artifact kind, trigger event, source family, source ref, reason, or runtime ref
- render a bounded navigation packet for human use
- write that navigation packet under a governed runtime-report path

The navigation layer may not:
- mutate kernel store/index/graph truth
- alter runtime posture
- reinterpret visibility packets as doctrine or authority
- create hidden autonomous polling or UI daemons

## Output class

Navigation packets are `GENERATED_STATE` witness surfaces.
They remain subordinate to the upstream packet index/dashboard and to all earlier runtime-report stages.

## Default output root

- `ION/05_context/runtime_reports/governance/navigation/`

## Boundary

Navigation output is for bounded human lookup and packet traversal only.
It does not become:
- doctrine
- runtime authority
- route authority
- kernel truth
