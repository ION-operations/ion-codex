---
type: orchestration_map
authority: A3_OPERATIONAL
created: 2026-04-13T20:15:00-04:00
status: ACTIVE
purpose: >-
  State the current-phase startup defaults for template feed, bounded context formation,
  packet sender truth, inbox truth, and packet-routing targets.
connections:
  - ION/06_intelligence/orchestration/2026-04-12_current_branch_active_center_map.md
  - ION/06_intelligence/orchestration/2026-04-12_governed_template_context_feed_map.md
  - ION/06_intelligence/orchestration/2026-04-12_composer2_support_field_setup_and_operator_runbook.md
  - ION/05_context/inbox/README.md
  - ION/07_templates/actions/TASK.md
  - ION/07_templates/actions/ROLE_SESSION.md
  - ION/07_templates/actions/TEMPLATE_SURFACE_CHANGE.md
  - ION/07_templates/bindings/STEWARD__TASK.md
  - ION/07_templates/bindings/CODEX__TASK.md
---

# Startup Template Feed And Task Routing Defaults

## Why this file exists

A fresh operator should not have to reconstruct startup routing from scattered protocol notes.
This file states the current default startup chain plainly.

## Current startup truth

### Sender / router truth
- `Steward` is the current-phase orchestration truename.
- `Codex` is the common Cursor-native carrier / chassis alias for Steward-held routing.

### Template-feed floor
The startup-critical governed template floor is:
- `TASK`
- `ROLE_SESSION`
- `HANDOFF`
- `CURSOR_HANDOFF`
- `SIGNAL`
- `ROLE_CHASSIS_MOUNT`
- `TEMPLATE_SURFACE_CHANGE` when law/template correction is the work itself

### Current routing binding default
- primary truth-facing routing binding: `STEWARD__TASK`
- supporting carrier-compatibility binding: `CODEX__TASK`

## Current startup context-feed chain

1. active law spine
2. governed template context-feed map
3. startup routing/defaults map
4. current workload plan / consolidation proposal
5. lane-native handoff / continuity for the selected target role

## Current inbox truth

The live staffing / semantic identity workload is **not** currently staged as an open task file at the root of `ION/05_context/inbox/`.

Use instead:
- `ION/05_context/comms/kernel_router_runs/2026-04-12_staffing_semantic_identity_agent_onboarding/06_operator_onboarding_sequence.md`
- `ION/05_context/inbox/README.md`
- lane-native entry surfaces for `Vestige` and `Thoth`

Historical completed tasks remain under:
- `ION/05_context/inbox/completed/`

## Default packet targets for the current live workload

### Vestige
Default target when archaeology/continuity evidence is needed now:
- `ION/06_intelligence/archaeology/vestige/continuity.md`
- `ION/06_intelligence/archaeology/vestige/watchlist.md`
- `ION/06_intelligence/archaeology/vestige/open_threads/2026-04-12_current_phase_staffing_and_semantic_identity.md`

### Thoth
Default target when active-branch evidence is needed now:
- `ION/agents/thoth/MINI.md`
- `ION/agents/thoth/CAPSULE.md`
- `ION/05_context/comms/kernel_router_runs/2026-04-12_staffing_semantic_identity_agent_onboarding/05_thoth_cursor_handoff.md`

### Mason
Do not target by default.
Activate only when a real bounded implementation packet exists.

## Default operator entry surfaces

### For branch orientation
- `ION/README.md`
- `ION/STATUS.md`
- `ION/SYSTEM_MAP.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`

### For current-phase startup
- `ION/06_intelligence/orchestration/2026-04-12_current_branch_active_center_map.md`
- `ION/06_intelligence/orchestration/2026-04-12_governed_template_context_feed_map.md`
- `ION/06_intelligence/orchestration/2026-04-12_post_ratification_execution_preparation_and_startup_map.md`
- `ION/06_intelligence/orchestration/2026-04-12_composer2_support_field_setup_and_operator_runbook.md`
- this file

## Activation rule for broader roles

Broader lawful roles may activate only when:
- a bounded packet exists,
- the target role is explicitly named,
- and the activation path is lawful under the current registry / precedence / template posture.

## Law/template correction rule

If the work is to repair routing law, binding law, truename law, or template law itself, route it through:
- `TEMPLATE_SURFACE_CHANGE`
under Steward-held orchestration truth.
