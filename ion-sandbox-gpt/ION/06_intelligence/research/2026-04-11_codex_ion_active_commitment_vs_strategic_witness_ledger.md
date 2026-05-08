---
type: research
authority: A3_OPERATIONAL
from: Codex
created: 2026-04-11T20:03:39-04:00
status: COMPLETE
ratification: NOT_RATIFIED
topic: Active-commitment versus strategic-witness ledger for the current M16 recovery lane
connections:
  - ION/06_intelligence/research/2026-04-11_codex_ion_identity_origin_destination_recovery_index.md
  - ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md
  - ION/06_intelligence/research/2026-04-10_m17_handoff_capsule_executor_start_packet_materialization_next_workload_plan.md
  - ION/06_intelligence/orchestration/2026-04-09_ion_current_state_vs_end_state_roadmap.md
  - ION/06_intelligence/orchestration/2026-04-08_ion_acceptance_matrix_and_definition_of_done.md
  - ION/06_intelligence/audits/2026-04-04_T32_operator_session_ratification_ion_production.md
  - ProjectOpus/21_STRATEGIC_DIRECTION/README.md
  - ProjectOpus/21_ARCHAEOLOGY_REMAP/24_ION_EVOLUTION_ORCHESTRATION.md
---

# ION active-commitment vs strategic-witness ledger

## Why this exists

The recovery lane now has bounded answers for:

- what ION is
- where ION came from
- where ION is going

The next remaining confusion vector is not the absence of direction.
It is the mixing of three different classes:

- current branch commitments
- limited production activation
- preserved strategic witness

This file separates those classes so future M16 sessions stop treating every
horizon claim as equally active.

## Sources or surfaces considered

- current branch authority:
  - `ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md`
  - `ION/06_intelligence/research/2026-04-10_m17_handoff_capsule_executor_start_packet_materialization_next_workload_plan.md`
  - `ION/06_intelligence/orchestration/2026-04-09_ion_current_state_vs_end_state_roadmap.md`
  - `ION/06_intelligence/orchestration/2026-04-08_ion_acceptance_matrix_and_definition_of_done.md`
- limited production-root activation:
  - `ION/06_intelligence/audits/2026-04-04_T32_operator_session_ratification_ion_production.md`
- preserved strategic witness:
  - `ProjectOpus/21_STRATEGIC_DIRECTION/README.md`
  - `ProjectOpus/21_ARCHAEOLOGY_REMAP/24_ION_EVOLUTION_ORCHESTRATION.md`
- recovery chain index:
  - `ION/06_intelligence/research/2026-04-11_codex_ion_identity_origin_destination_recovery_index.md`

## Findings

### Classification key

- `Active Branch Commitment`
  - current M16 branch authority explicitly commits the branch to this finish line
    or next bounded workload
- `Explicit Branch Non-Claim`
  - the branch explicitly says this is not yet landed or not yet certified here
- `Limited Production Activation`
  - activated in the top-level production root, but only for the narrower scope
    named there
- `Preserved Strategic Witness`
  - important direction or north-star material preserved in the estate, but not
    immediate implementation authority for the current M16 branch

### Ledger

| Claim / direction | Class | Active scope | Why it belongs there |
| --- | --- | --- | --- |
| M16 branch should satisfy the current-generation definition of done: lawful entry, bounded step execution, handoff without hidden context, honest future structure | `Active Branch Commitment` | current M16 root | The roadmap and acceptance matrix define this as the actual finish line for this generation. |
| M17 handoff-capsule executor-start packet materialization is the next bounded workload | `Active Branch Commitment` | current M16 root | The post-M16 handoff and M17 workload plan explicitly mark this as the next trust gap and next implementation center. |
| M17 must materialize one executor-start packet from successful rehearsal with one receipt and no hidden continuation expansion | `Active Branch Commitment` | current M16 root | The M17 workload plan defines the goal, required outcomes, and tight non-goals. |
| The branch should proceed one bounded architecture center at a time instead of widening into swarm behavior or letting product vision outrun proof | `Active Branch Commitment` | current M16 root | The roadmap explicitly warns against early widening and states the correct next order. |
| M16 has not yet landed executor-start packet materialization | `Explicit Branch Non-Claim` | current M16 root | The post-M16 handoff says this directly. |
| M16 has not yet landed hidden continuation expansion | `Explicit Branch Non-Claim` | current M16 root | The post-M16 handoff says this directly. |
| M16 has not yet landed automatic entry dispatch | `Explicit Branch Non-Claim` | current M16 root | The post-M16 handoff says this directly. |
| Doctrine, kernel doctrine, and registry posture are active for O1 closure in the top-level `ION - Production/ION` tree | `Limited Production Activation` | top-level production root only | T32 activates these surfaces for that narrower root and scope. |
| Daemon autonomy, full production, and universal PASS are not yet certified by T32 | `Explicit Branch Non-Claim` | top-level production root only | T32 explicitly says these are non-claims. |
| Build best ION v3 as the foundation for everything else | `Preserved Strategic Witness` | wider estate | Strategic Direction states this as the larger roadmap foundation, but it is not the immediate M16 implementation authority. |
| Use ION context powers to boost agents/builders | `Preserved Strategic Witness` | wider estate | Strategic Direction preserves this as the next larger platform usage horizon. |
| Build a VS Code fork and later a ground-up IDE | `Preserved Strategic Witness` | wider estate | Strategic Direction preserves this as later roadmap, not current branch commitment. |
| Build a Linux distro and then a full OS | `Preserved Strategic Witness` | wider estate | Strategic Direction preserves this as the far-horizon end state, not immediate branch execution authority. |
| Reach a raw-runtime ION/Aether system that can serve IDEs as clients until it surpasses them | `Preserved Strategic Witness` | wider estate | ION Evolution Orchestration provides this north-star framing, but it is still a strategic target rather than current M16 completion law. |

### Working rule

For the current M16 branch:

- implement from `Active Branch Commitment`
- respect `Explicit Branch Non-Claim`
- consult `Limited Production Activation` only when discussing the top-level
  production root's narrower activation status
- use `Preserved Strategic Witness` for orientation and long-horizon planning,
  not as authority for the next code change in this branch

## Implications

1. The current M16 branch is not directionless.
   It has a specific finish line and a specific next bounded workload.

2. The far-horizon vision is not fake.
   It is preserved strategic witness, but it is not immediate branch authority.

3. Future confusion will usually come from category collapse rather than missing
   documentation:
   branch commitment, limited production activation, and strategic witness are
   different classes.

4. This ledger is the missing bridge between the recovery answers and actual
   implementation prioritization.

## Recommended next moves

1. If the lane continues, derive one implementation-priority card from the
   `Active Branch Commitment` rows only, so future execution sessions can work
   without re-reading all wider-estate strategy.

2. If a shared entry surface is updated later, promote only the stable branch
   commitment subset, not the whole strategic-witness horizon.

3. Keep using the recovery index plus this ledger together:
   the index answers identity/origin/destination, and this ledger answers what
   is actually active right now.
