---
type: patch_package
from: browser-class external carrier
created: 2026-04-12T11:49:46-04:00
status: PROPOSED
target_owner: Codex
targets:
  - ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_disagreement_drill_browser_mount_boundary/README.md
---

# Patch Package: Browser-Class README Clarification

## Why this patch exists

The disagreement drill bundle README currently summarizes the drill correctly but does
not explicitly point the reader to the supporting research and audit artifacts that live
in their lawful lanes.

## Exact surfaces in scope

- `ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_disagreement_drill_browser_mount_boundary/README.md`

## Observed drift or defect

The README names a real artifact set spanning research, audit, proposal, handoff, and
signal, but it leaves the lane-owned research and audit artifacts implicit.

## Proposed replacement or correction

After the `It proves:` list, add:

`Support artifacts for this drill live in their lawful lanes:`

- `ION/06_intelligence/research/2026-04-12_phase1_browser_mount_boundary_research.md`
- `ION/06_intelligence/audits/2026-04-12_phase1_browser_mount_boundary_audit.md`

## Why this should be applied by the target owner

Codex owns live-branch landing in the current phase, so the proposed clarification
should be compared and applied by Codex rather than silently imported from the external
carrier.

## Risks if deferred

The drill would remain correct but slightly harder for a fresh session to trace from the
bundle entrypoint alone.
