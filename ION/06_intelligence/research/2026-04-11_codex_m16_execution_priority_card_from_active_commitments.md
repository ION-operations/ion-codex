---
type: research
authority: A3_OPERATIONAL
from: Codex
created: 2026-04-11T20:05:29-04:00
status: COMPLETE
ratification: NOT_RATIFIED
topic: M16 execution priority card derived from active branch commitments only
connections:
  - ION/06_intelligence/research/2026-04-11_codex_ion_active_commitment_vs_strategic_witness_ledger.md
  - ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md
  - ION/06_intelligence/research/2026-04-10_m17_handoff_capsule_executor_start_packet_materialization_next_workload_plan.md
  - ION/02_architecture/HANDOFF_CAPSULE_EXECUTOR_ENTRY_REHEARSAL_PROTOCOL.md
  - ION/tests/test_kernel_schedule_handoff_entry_rehearsal.py
  - ION/tests/test_kernel_schedule_handoff_entry_rehearsal_cli.py
  - ION/tests/test_kernel_schedule_activation_handoff_capsule.py
  - ION/tests/test_kernel_schedule_takeover_entry_activation.py
---

# M16 execution priority card from active commitments

## Why this exists

The active-commitment ledger says the current M16 branch is not directionless:

- it has a defined finish line
- it has a defined next bounded workload

This file turns those active commitment rows into one execution card so a future
implementation session can act without re-reading the full wider-estate recovery
stack.

## Sources or surfaces considered

- `ION/06_intelligence/research/2026-04-11_codex_ion_active_commitment_vs_strategic_witness_ledger.md`
- `ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md`
- `ION/06_intelligence/research/2026-04-10_m17_handoff_capsule_executor_start_packet_materialization_next_workload_plan.md`
- `ION/02_architecture/HANDOFF_CAPSULE_EXECUTOR_ENTRY_REHEARSAL_PROTOCOL.md`
- `ION/tests/test_kernel_schedule_handoff_entry_rehearsal.py`
- `ION/tests/test_kernel_schedule_handoff_entry_rehearsal_cli.py`
- `ION/tests/test_kernel_schedule_activation_handoff_capsule.py`
- `ION/tests/test_kernel_schedule_takeover_entry_activation.py`

## Findings

### 1. Current top priority

The top priority for the current M16 branch is:

- M17 handoff-capsule executor-start packet materialization

This is the live next architecture center because:

- M15 materialized the compact handoff capsule
- M16 proved direct executor-entry rehearsal from that capsule
- M17 is the next explicit trust gap

### 2. Objective

Land one bounded M17 surface that:

- materializes one executor-start packet from a successful M16 rehearsal
- preserves linkage back to the capsule / activation / continuation chain
- persists one executor-start materialization receipt

### 3. Non-goals

Do not widen into:

- new planner behavior
- autonomous dispatch widening
- hidden continuation expansion
- shadow continuation systems

Those are explicitly outside the current bounded move.

### 4. Read set before implementation

Read in this order:

1. `ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md`
2. `ION/06_intelligence/research/2026-04-10_m17_handoff_capsule_executor_start_packet_materialization_next_workload_plan.md`
3. `ION/02_architecture/HANDOFF_CAPSULE_EXECUTOR_ENTRY_REHEARSAL_PROTOCOL.md`
4. `ION/tests/test_kernel_schedule_handoff_entry_rehearsal.py`
5. `ION/tests/test_kernel_schedule_handoff_entry_rehearsal_cli.py`
6. `ION/tests/test_kernel_schedule_activation_handoff_capsule.py`
7. `ION/tests/test_kernel_schedule_takeover_entry_activation.py`

### 5. Probable implementation center

The existing proof and orchestration chain suggests the next implementation
center should stay near the schedule / handoff capsule path that already owns:

- takeover entry activation
- activation handoff capsule materialization
- handoff entry rehearsal

So the next implementation session should look first at the kernel schedule /
handoff-capsule family rather than reopening unrelated orchestration domains.

### 6. Proof expectation

The next implementation session should leave behind:

- one new bounded M17 code surface
- one focused proof surface or proof widening
- one receipt family or receipt widening for executor-start materialization
- one orchestration/update note that truthfully moves the frontier from M16 to
  post-M17 only if the proof actually lands

### 7. Working rule

For the next implementation session:

- build only from the `Active Branch Commitment` rows
- ignore far-horizon IDE / OS strategy for code-scope decisions
- keep the branch subordinate to the current proof center
- if M17 cannot be landed cleanly, emit a narrow blocker note rather than
  widening scope

## Implications

1. The current branch now has an operator-grade execution target, not just a
   narrative direction.

2. Future sessions do not need to rediscover what is active.
   They can use this card plus the active-commitment ledger directly.

3. This card narrows the next execution pass back to the schedule/handoff-capsule
   proof center, which is where the branch authority already points.

## Recommended next moves

1. Use this card as the first planning surface for the next real M17
   implementation pass.

2. If the next session is read-only, audit the schedule/handoff-capsule module
   family for the exact insertion point of executor-start packet materialization.

3. If the next session is write-capable, implement M17 directly from this card
   rather than reopening broader strategy or identity work.
