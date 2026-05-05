---
type: registry_index
authority: A3_OPERATIONAL
created: 2026-04-07T22:23:00-04:00
updated: 2026-04-22T20:05:00-04:00
status: ACTIVE_FIRST_PASS
topic: Current-phase intelligent domain registry for the live ION root
---

# ION Domain Registry

This directory contains the first explicit domain-governance layer for the live `ION/` root.

## Current structure

- `domain.*.domain.yaml` — active or proposed domain records
- `activation_witness/*.yaml` — witness of how or why a domain entered current live state

## Current first-pass active domains

- `domain.construction_routing_integration.domain.yaml`
- `domain.continuity_context_resumability.domain.yaml`
- `domain.current_phase_orchestration_management.domain.yaml`
- `domain.communications_packet_relay.domain.yaml`
- `domain.archaeology_drift_watch.domain.yaml`

## Important rule

A domain record is current operational truth.
An activation witness is supporting witness.
They must not be collapsed into one file.

## Current-phase clarification

Current-phase orchestration-management is explicitly represented as its own domain with
**Steward** as primary role truth and **Codex** as common supporting carrier.

When naming orchestration truth, prefer Steward-facing law; preserve Codex where
carrier/chassis or historical continuity matters.
