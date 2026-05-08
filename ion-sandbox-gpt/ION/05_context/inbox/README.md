---
type: inbox_map
authority: A3_OPERATIONAL
created: 2026-04-13T20:10:00-04:00
status: ACTIVE
purpose: Explain current inbox truth for the ratified branch so fresh operators do not assume stale live task files.
connections:
  - ION/06_intelligence/orchestration/2026-04-13_startup_template_feed_and_task_routing_defaults.md
  - ION/06_intelligence/orchestration/2026-04-12_composer2_support_field_setup_and_operator_runbook.md
  - ION/07_templates/actions/TASK.md
---

# Inbox Map

## Current truth

The ratified branch does **not** currently stage the live support-field workload through open task files under `ION/05_context/inbox/`.

The current selected workload is staged primarily through:
- `ION/05_context/comms/kernel_router_runs/2026-04-12_staffing_semantic_identity_agent_onboarding/`
- role-native continuity and handoff surfaces for `Vestige` and `Thoth`
- active orchestration maps under `ION/06_intelligence/orchestration/`

## What exists here now

- `completed/` preserves historical completed task packets
- no open default startup task is currently expected at the inbox root for the staffing / semantic identity lane

## Startup rule

If a fresh operator is continuing the current workload now:
- use the startup routing/defaults map
- use the Composer 2 support-field runbook
- start `Vestige` and `Thoth` through their lane-native continuity / handoff entry surfaces
- do not wait for a new root inbox file unless a new bounded packet is explicitly issued

## Future rule

If a new bounded task is issued for current-phase work, it may appear here as a live task packet and should follow `TASK.md` law.
