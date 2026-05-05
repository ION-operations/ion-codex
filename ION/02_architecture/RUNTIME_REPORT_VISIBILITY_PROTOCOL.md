# RUNTIME REPORT VISIBILITY PROTOCOL

## Purpose

Project selected runtime-report witness outputs into downstream operator visibility surfaces without promoting them into kernel truth.

## Surfaces

E3 may emit only bounded downstream visibility artifacts:
- packet index JSON under governed runtime-report paths
- operator dashboard markdown under governed runtime-report paths

These surfaces are downstream from:
1. runtime report artifacts
2. governance reflections
3. governance aggregation witnesses
4. kernel truth surfaces (which remain upstream and authoritative)

## Lawful constraints

1. E3 is optional and off by default.
2. E3 only projects receipts that already carry E2 aggregation witness markers.
3. E3 never mutates kernel store, kernel index, kernel graph, doctrine, or route authority.
4. E3 outputs remain `GENERATED_STATE` witness/projection material.
5. Caller must still provide an explicit governed workspace root through the trigger request.
6. Packet indexes and dashboards must preserve links back to upstream artifacts, governance paths, and aggregation witnesses.
7. E3 must not imply a background dashboard daemon, autonomous operator plane, or hidden scheduler.

## Default governed output paths

- `ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json`
- `ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md`

## Boundary

E3 improves operator visibility across already-aggregated runtime-report events. It does not create a new authority tier.
