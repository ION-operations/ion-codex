# ION V105 Deep Operational Cartography and Preparedness Report

```yaml
schema_id: ion.v105.deep_operational_cartography.report
line: V105_DEEP_OPERATIONAL_CARTOGRAPHY_AND_CORE_SYSTEM_TELEMETRY
created_at: 2026-05-02T20:58:20+00:00
production_authority: false
verdict: DEEP_CARTOGRAPHY_PREPARED_WITH_DISCONNECTED_SYSTEMS
ready_count: 3
partial_count: 11
missing_count: 0
blocked_count: 0
```

## Executive finding

V105 confirms the uncomfortable but useful truth: ION has many of the advanced systems Braden expected to exist, including temporal context machinery, context lifecycle/metabolism audit, agent context systems, carrier profiles, template graph evolution surfaces, model-routing economics, visual/browser harness surfaces, and a local deterministic autonomous-loop survival path. The failure mode is not total absence. The failure mode is that too many surfaces remain partial, audit-adjacent, or disconnected from packaging, front-door runtime, carrier execution, UI hydration, and production verification.

## The governing distinction

```text
doctrine present ≠ wired runtime
module present ≠ enforced gate
audit pass ≠ production readiness
carrier profile ≠ mounted carrier
UI view model ≠ complete operator observability
```

## System cartography summary

| System | Verdict | Severity | Summary |
|---|---:|---:|---|
| `root_authority_and_mount_invariant` | `READY_SURFACE_PRESENT` | `info` | Shell root and agent entry authority are physically present. |
| `temporal_context_stack` | `READY_SURFACE_PRESENT` | `info` | Temporal/context doctrine, kernel adapters, enforcement audit, and focused test are present. |
| `context_lifecycle_and_metabolism` | `PARTIAL_OR_DISCONNECTED` | `warning` | Context lifecycle/metabolism is incomplete. |
| `local_autonomous_loop_survival_path` | `PARTIAL_OR_DISCONNECTED` | `warning` | Local autonomous-loop survival path is incomplete. |
| `active_agent_context_systems` | `READY_SURFACE_PRESENT` | `info` | Agent context-system and rolling context-window surfaces are present. |
| `front_door_persona_relay_steward_runtime` | `PARTIAL_OR_DISCONNECTED` | `warning` | Front-door runtime path is not yet proven end-to-end. |
| `receipt_repair_and_hydration_mapping` | `PARTIAL_OR_DISCONNECTED` | `warning` | Receipt/repair surfaces exist but UI hydration mapping is not proven. |
| `joc_cockpit_ui_and_core_telemetry` | `PARTIAL_OR_DISCONNECTED` | `warning` | JOC/cockpit exists but lacks the requested lane timeline, hydration, and debug telemetry overlays. |
| `cursor_carrier_and_codex_extension_surface` | `PARTIAL_OR_DISCONNECTED` | `warning` | Cursor/Codex carrier surfaces are incomplete. |
| `chatgpt_browser_carrier_surface` | `PARTIAL_OR_DISCONNECTED` | `warning` | ChatGPT carrier profile is incomplete. |
| `template_graph_evolution_and_writeback_metabolism` | `PARTIAL_OR_DISCONNECTED` | `warning` | Template graph evolution surfaces are incomplete. |
| `release_packaging_and_productized_runtime_boundary` | `PARTIAL_OR_DISCONNECTED` | `warning` | Release/productized runtime boundary is incomplete. |
| `model_router_budget_and_provider_economics` | `PARTIAL_OR_DISCONNECTED` | `warning` | Model routing/economics stack is incomplete. |
| `visual_browser_and_computer_use_lane` | `PARTIAL_OR_DISCONNECTED` | `warning` | Visual/browser lane is incomplete. |


## Highest priority disconnections

1. **Lifecycle-aware packaging is still open.** ION can classify hot/warm/cold context, but the release/carrier packager is not yet hard-bound to those classifications.
2. **Front-door runtime is not proven end-to-end.** Persona/Relay/Steward doctrine and planning surfaces exist, but one operator message must still be proven through Relay packet, Steward verdict, Persona render, and receipt.
3. **Receipt hydration and repair mapping are not proven.** Receipt primitives exist, but mixed `utterance_id` / `atom_id` assistant-bubble hydration is not yet an audited system.
4. **JOC/core telemetry lacks the requested triad.** The basic cockpit exists, but the lane timeline widget, receipt hydration view, and runtime debug overlay are not implemented.
5. **Carrier systems exist but need mount proof per host.** ChatGPT browser, Cursor, Codex, and MCP profiles exist, but each host must be proven by survey, command path, return intake, and stop conditions.
6. **Template graph evolution needs metabolism.** Proposal/review/commit surfaces exist, but writebacks must become diffs/residues rather than repeated hot graph snapshots.

## UI/front-door telemetry triad to implement

```text
lane timeline widget:
  requested lane -> effective lane -> reason -> organ events -> authority verdict -> repair obligations

receipt/repair hydration mapper:
  latest receipt source/DB rows -> utterance_id/atom_id resolver -> correct assistant bubble -> supersession chain

debug overlay:
  SSE event throughput -> render timings -> DB hydration time -> kernel projection time -> file watcher refresh time
```

## Long-horizon orchestration stance

The next work must be sequentially ruthless: make the operational map stable, bind packaging to lifecycle, then build the front-door/UI telemetry and carrier mounts. External worker adapters stay blocked until lifecycle, return intake, and carrier proof are stable.

## Artifacts emitted

```text
ION/04_packages/kernel/ion_deep_operational_cartography.py
ION/tests/test_kernel_ion_deep_operational_cartography.py
ION/02_architecture/ION_DEEP_OPERATIONAL_CARTOGRAPHY_AND_CORE_SYSTEM_TELEMETRY_PROTOCOL.md
ION/05_context/current/ION_DEEP_OPERATIONAL_CARTOGRAPHY_AUDIT_V105.json
ION/05_context/current/ION_LONG_HORIZON_ORCHESTRATION_PLAN_V105.json
ION/05_context/current/ION_CORE_SYSTEM_TELEMETRY_REQUIREMENTS_V105.json
ION/05_context/current/CARRIER_AGENT_SYSTEM_BUILD_PLAN_V105.json
ION/05_context/signals/v105_deep_operational_cartography_receipt_20260502.txt
```

## Validation

```text
13 passed
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_deep_operational_cartography.py ION/tests/test_kernel_ion_operational_truth_audit.py ION/tests/test_kernel_ion_context_lifecycle.py ION/tests/test_kernel_ion_temporal_context_enforcement_audit.py ION/tests/test_kernel_ion_autonomous_loop.py ION/tests/test_kernel_ion_cockpit_view_model.py -q
```

Full-suite verification remains not claimed. Pytest plugin autoload was disabled to avoid host plugin latency/noise.

## Boundary

V105 is a preparedness and cartography pass. It does not claim production readiness, unrestricted agent authority, unrestricted visual/computer-use authority, real subagent spawning in ChatGPT browser, or complete front-door runtime. It gives the next branch a truthful map to build from.
