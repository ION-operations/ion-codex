# ION Deep Operational Cartography and Core System Telemetry Protocol — V105

```yaml
schema_id: ion.deep_operational_cartography.protocol.v105
line: V105_DEEP_OPERATIONAL_CARTOGRAPHY_AND_CORE_SYSTEM_TELEMETRY
production_authority: false
```

## Purpose

ION must stop treating system audits as isolated status reports. Every core system needs the same discipline the UI now demands for lane timelines, receipt hydration, and debug overlays: requested state versus effective state, event lineage, hydration/projection proof, timing, and current gate.

This protocol establishes deep operational cartography as a maintained ION surface. It maps each core system as one of:

```text
READY_SURFACE_PRESENT
PARTIAL_OR_DISCONNECTED
MISSING_SURFACE
```

A system is not considered operational merely because doctrine exists. Operational status requires doctrine, registry/policy where applicable, kernel or runtime surface where applicable, test or audit proof where applicable, active-state visibility when applicable, and an explicit next gate.

## Core telemetry triad

The operator request that triggered V105 is canonized as a reusable instrumentation standard:

```text
1. lane timeline: requested lane, effective lane, lane-change reason, organ events per message
2. receipt/repair hydration: latest receipts map to the correct assistant bubble even across mixed utterance_id/atom_id cases
3. debug overlay: SSE throughput, render timings, DB hydration time, kernel projection time, and watcher refresh time
```

This triad is not limited to the chat UI. ION should apply the same standard to front door, carriers, workers, context lifecycle, temporal enforcement, template graph evolution, and release packaging.

## Rule

A core system may be described as designed, present, tested, wired, or operational only if the current cartography audit records the supporting surfaces. Otherwise it must be called partial, disconnected, missing, or blocked.

## Required current outputs

```text
ION/04_packages/kernel/ion_deep_operational_cartography.py
ION/05_context/current/ION_DEEP_OPERATIONAL_CARTOGRAPHY_AUDIT_V105.json
ION/05_context/current/ION_LONG_HORIZON_ORCHESTRATION_PLAN_V105.json
ION/05_context/current/ION_CORE_SYSTEM_TELEMETRY_REQUIREMENTS_V105.json
ION/05_context/current/CARRIER_AGENT_SYSTEM_BUILD_PLAN_V105.json
```

## Non-authority boundary

V105 does not grant production authority, unrestricted carrier authority, unrestricted visual/computer-use authority, or external-worker authority. It prepares the operational map required to decide what to build next without losing existing systems.
