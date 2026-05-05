---
type: research
authority: A3_OPERATIONAL
from: Codex
created: 2026-04-12T11:55:22-04:00
status: COMPLETE
ratification: NOT_RATIFIED
topic: Post-Phase-1 next workload plan for bridge packet family status and validator coverage
connections:
  - ION/06_intelligence/orchestration/2026-04-12_phase1_template_governance_rollout_plan.md
  - ION/06_intelligence/research/2026-04-12_phase1_template_governance_gate_surface_map.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/04_packages/kernel/packet_validation.py
  - ION/tests/test_kernel_packet_validation.py
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md
---

# Bridge Packet Family Status And Validation Next Workload Plan

## Why this exists

Phase 1 template-governance restoration is now proved in the live branch. The next
remaining operational gap exposed by that proof loop is not another missing bridge.

It is this:

- the branch now uses `ROLE_CHASSIS_MOUNT`, `DISAGREEMENT_ESCALATION`, and
  `EXTERNAL_RETURN` as real governed packet surfaces,
- but the canonical packet validator and packet-standardization protocol still recognize
  only the older packet family floor.

That makes bridge packet family status and validator coverage the cleanest bounded next
workload after Phase 1 closeout.

## Sources or surfaces considered

- `ION/06_intelligence/orchestration/2026-04-12_phase1_template_governance_rollout_plan.md`
- `ION/06_intelligence/research/2026-04-12_phase1_template_governance_gate_surface_map.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/04_packages/kernel/packet_validation.py`
- `ION/tests/test_kernel_packet_validation.py`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- `ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/03_mason_role_chassis_mount.md`
- `ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_disagreement_drill_browser_mount_boundary/03_disagreement_escalation.md`
- `ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_browser_external_return_drill/04_external_return.md`

## Findings

### 1. The canonical packet floor is still intentionally narrow

`PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md` and `kernel/packet_validation.py`
still define the canonical packet family as:

- `task`
- `role_session`
- `handoff`
- `cursor_handoff`
- `manual_automation_fallback`

That narrowness is coherent with the earlier K-series packet normalization work.

### 2. The Phase 1 proof loop now depends on governed bridge packets outside that floor

The live branch now has real packet use of:

- `ROLE_CHASSIS_MOUNT`
- `DISAGREEMENT_ESCALATION`
- `EXTERNAL_RETURN`

Those packets are lawful current-phase bridge surfaces, but they are not yet inside the
canonical validator taxonomy.

### 3. The proof loop had to validate around the bridge packets rather than through them

During the Phase 1 proof passes, canonical validation was available for the surrounding
`TASK`, `ROLE_SESSION`, and `HANDOFF` packets, but not for the bridge packets
themselves.

That is a truthful workable posture for one first-pass proof loop, but it is the next
clean tooling and law question if the branch wants to keep using these bridge packets.

### 4. Historical estate search should precede packet-family widening

Packet family expansion is not a casual code-only decision.

Before widening the canonical packet taxonomy or packet validator, the branch should
first check whether older estate surfaces already solved:

- bridge-packet classification,
- validator expectations,
- or a two-tier distinction between canonical packets and governed bridge packets.

## Implications

1. The next workload should not be another whole-agent rollout pass.
   It should be a bounded packet-law and validator-coverage decision.

2. The next workload should begin with archaeology and evidence, not implementation.

3. Mason should only implement after the branch decides one of two truthful paths:
   - widen canonical packet law and validator support to include the bridge packets, or
   - explicitly keep the bridge packets outside the canonical validator floor while
     adding the minimum truthful support surface for them.

## Recommended next moves

1. Run one bounded Vestige/Thoth-style archaeology and evidence pass over older packet,
   template, and validator surfaces before changing the live packet floor.

2. File one Codex proposal answering this exact question:
   should `ROLE_CHASSIS_MOUNT`, `DISAGREEMENT_ESCALATION`, and `EXTERNAL_RETURN`
   become canonical packet families, or remain governed bridge packets outside the
   narrow validator floor?

3. If the branch converges on widening, use Mason for the bounded code/test pass in:
   - `ION/04_packages/kernel/packet_validation.py`
   - `ION/tests/test_kernel_packet_validation.py`
   - and the minimum protocol/template documentation tied to that widening

4. If the branch converges on non-widening, explicitly record the distinction and add
   the minimum truthful guidance or support tooling required so future sessions stop
   assuming the validator should already accept the bridge packets.

## Working rule

The next workload is not "make the validator bigger" by reflex.

The next workload is:

- determine the lawful status of the bridge packet set,
- then change tooling only in the direction that the law supports.
