---
type: research
authority: A3_OPERATIONAL
from: Codex
created: 2026-04-11T09:50:33-04:00
status: COMPLETE
ratification: NOT_RATIFIED
topic: Fresh-agent entry chain and stale-surface fences for the current M16 root
connections:
  - ION/README.md
  - ION/MASTER_ORCHESTRATION_INDEX.md
  - ION/STATUS.md
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/SYSTEM_MAP.md
  - ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md
  - ION/06_intelligence/research/2026-04-11_codex_ion_identity_lineage_destination_evidence_map.md
  - ION/06_intelligence/research/2026-04-11_codex_ion_identity_lineage_destination_working_map.md
  - ION/docs/program/01_what_ion_is.md
  - ION/docs/program/13_implementation_state_and_roadmap.md
  - 00_CONSOLIDATED_ATLAS/07_MASTER_REPORT.md
  - ProjectOpus/21_ARCHAEOLOGY_REMAP/05_OPEN_CONTRADICTIONS.md
---

# M16 entry chain and stale-surface fences

## Why this exists

The current production estate already has enough material to orient a fresh agent,
but the material is distributed across current branch docs, production-root stubs,
ProjectOpus archaeology, and atlas contradiction maps.

This file defines the safest startup order for a fresh agent entering
`ION_Working_Branch_M16/ION` and names the surfaces that should be fenced off
until the agent already understands the current branch.

## Sources or surfaces considered

- Current M16 entry and projection surfaces:
  - `ION/README.md`
  - `ION/MASTER_ORCHESTRATION_INDEX.md`
  - `ION/STATUS.md`
- Current M16 doctrine / workflow / system surfaces:
  - `ION/01_doctrine/CANONICAL_WORKFLOW.md`
  - `ION/AGENT_CONTRACT.md`
  - `ION/SYSTEM_MAP.md`
  - `ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md`
  - `ION/02_architecture/CONTINUITY_ARCHITECTURE.md`
- Current M16 orchestration frontier:
  - `ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md`
  - `ION/06_intelligence/orchestration/2026-04-09_ion_full_system_architecture_and_end_state_framework.md`
  - `ION/06_intelligence/orchestration/2026-04-08_ion_acceptance_matrix_and_definition_of_done.md`
  - `ION/06_intelligence/orchestration/2026-04-09_ion_current_state_vs_end_state_roadmap.md`
- Recovery and contradiction surfaces:
  - `ION/06_intelligence/research/2026-04-11_codex_ion_identity_lineage_destination_evidence_map.md`
  - `ION/06_intelligence/research/2026-04-11_codex_ion_identity_lineage_destination_working_map.md`
  - `00_CONSOLIDATED_ATLAS/07_MASTER_REPORT.md`
  - `ProjectOpus/21_ARCHAEOLOGY_REMAP/05_OPEN_CONTRADICTIONS.md`
- Known misleading startup surfaces:
  - `ION/docs/program/01_what_ion_is.md`
  - `ION/docs/program/13_implementation_state_and_roadmap.md`

## Findings

### 1. The safest fresh-agent entry chain is branch-first, not estate-first

The current M16 root already provides a legitimate startup order.
For a fresh agent entering to do work in this branch, the safest order is:

1. `ION/README.md`
2. `ION/01_doctrine/CANONICAL_WORKFLOW.md`
3. `ION/AGENT_CONTRACT.md`
4. `ION/SYSTEM_MAP.md`
5. `ION/06_intelligence/orchestration/2026-04-09_ion_full_system_architecture_and_end_state_framework.md`
6. `ION/MASTER_ORCHESTRATION_INDEX.md`
7. `ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md`
8. `ION/06_intelligence/orchestration/2026-04-09_ion_current_state_vs_end_state_roadmap.md`
9. `ION/06_intelligence/orchestration/2026-04-08_ion_acceptance_matrix_and_definition_of_done.md`
10. `ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md`
11. `ION/tests/test_kernel_workflow_rehearsal.py` and the core frontier tests only after the read surfaces above

This order keeps the agent inside the current branch's live workflow, current frontier,
and current completion criteria before it encounters wider archaeology.

### 2. Root projections are useful for posture, but not source continuity

`ION/STATUS.md` and the root trio are projection surfaces.
They are helpful for posture and read order, but they are not the source continuity model.
`ION/02_architecture/CONTINUITY_ARCHITECTURE.md` remains the correction surface:
private continuity is source truth; shared root projections are projections.

So the startup rule is:

- use `README.md` and `STATUS.md` to orient
- use doctrine, workflow, orchestration, and tests to verify
- do not treat projections as the place where agents author their own continuity

### 3. Identity / lineage / destination understanding should be a second pass

Once a fresh agent understands the live M16 branch, the next safe layer is:

1. `ION/06_intelligence/research/2026-04-11_codex_ion_identity_lineage_destination_evidence_map.md`
2. `ION/06_intelligence/research/2026-04-11_codex_ion_identity_lineage_destination_working_map.md`
3. `ProjectOpus/21_STRATEGIC_DIRECTION/README.md`
4. `ProjectOpus/21_ARCHAEOLOGY_REMAP/25_ION_AETHER_CANONICAL_BOUNDARY_PACKET.md`
5. `00_CONSOLIDATED_ATLAS/02_CONSOLIDATION/ROOT_CONTRIBUTION_MAP.md`
6. `00_CONSOLIDATED_ATLAS/02_CONSOLIDATION/LOSS_REGRESSION_MATRIX.md`
7. `ProjectOpus/21_ARCHAEOLOGY_REMAP/05_OPEN_CONTRADICTIONS.md`

This second pass is where a fresh agent should learn the broader organism,
the lineage roots, and the long-horizon destination.

### 4. The main startup decoys are now identifiable

The most dangerous startup surfaces for a fresh agent in this branch are:

- `ION/docs/program/01_what_ion_is.md`
  - it is a stub, so it invites overcompensation
- `ION/docs/program/13_implementation_state_and_roadmap.md`
  - it is also a stub, so it cannot anchor current branch status
- any broad ProjectOpus or atlas surface read before the live branch workflow
  - these are valuable, but they preserve contradictions and witness layers rather than current branch execution law
- any attempt to flatten the long-horizon OS vision into the M16 finish line
  - the branch has a bounded current-generation finish line that is smaller than the total estate vision

### 5. The right fence is not “ignore archaeology”; it is “sequence archaeology”

The atlas explicitly warns against trusting settled-canon claims without revalidation.
ProjectOpus explicitly preserves unresolved contradictions.
So archaeology should not be ignored.
It should be read after the current branch center is understood.

The startup sequence therefore needs two gates:

- Gate A: current M16 workflow and frontier comprehension
- Gate B: broader identity / lineage / destination comprehension

Skipping Gate A is what lets fresh agents drown in the estate before they understand the branch they are standing in.

## Implications

1. The current M16 root already contains a workable startup spine.
   The failure mode is not missing entry surfaces; it is entering wider archaeology too early.

2. Fresh agents should be told explicitly that top-level production program docs are unfinished,
   so they do not mistake stubs for missing architecture.

3. The broader production estate should be introduced as witness and lineage support for the current branch,
   not as the first thing an execution agent reads when it needs to act inside M16.

## Recommended next moves

1. Keep using this entry-chain map plus the identity/lineage/destination evidence set
   as the bounded orientation package for current M16 recovery work.

2. If a future shared entrypoint is needed, route it through an existing current-branch
   projection surface only after governance-visible review, rather than silently promoting this note.

3. Use this document to fence future Codex/Vizier/Nemesis startup packets:
   branch-first, then identity/lineage, then wider archaeology.
