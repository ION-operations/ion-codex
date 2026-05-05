---
type: doctrine
authority: A1_CANONICAL
template: MANUAL
affinity: WORKFLOW
affirms:
  - ION/01_doctrine/SOVEREIGN_CONSTITUTION.md
  - ION/01_doctrine/SOVEREIGN_KERNEL.md
created: 2026-04-08T18:50:00-04:00
status: ACTIVE
---

# Canonical Workflow Doctrine

## Supreme statement

ION has **one** workflow.

Manual execution, IDE-native execution, daemon-assisted execution, external/API execution, and later swarm execution are all lawful carriers of the **same** workflow. They are not different processes.

## Canonical loop

1. **Read lawful state**
   - kernel truth
   - route state
   - automation state
   - review pressure
   - operator control
2. **Compile bounded context**
   - template
   - packet / capsule / manifest / context package
   - exact allowed writes and next actions
3. **Determine the next lawful step**
   - scheduler / planner / threshold / review / policy
4. **Choose the next executor**
   - same agent
   - another local agent
   - external/API worker
5. **Execute one bounded step**
   - never jump multiple hidden steps
6. **Return the result as proposal, not truth**
   - commit delta
   - signal
   - child result
   - external execution return
7. **Land, hold, or escalate**
   - validation
   - governed write
   - review escalation
8. **Update kernel truth and emit the next handoff**
   - store / index / graph
   - runtime / route / automation state
   - next packet or handoff
9. **Resume lawfully after interruption**
   - recovery / replay must re-enter the same loop

## Invariants

1. There is no separate “manual workflow” and “automation workflow.”
2. Automation is the canonical workflow becoming more explicit and more kernel-carried.
3. External execution does not become kernel truth directly.
4. Generated witness artifacts do not outrank kernel truth.
5. Every step must be bounded enough that a fresh capable executor can continue from the lawful outputs.
6. If a runtime surface cannot be mapped to one step in this loop, it is not yet trusted as core workflow.


## Execution symmetry

The workflow must feel natural under both manual and automated carriage. If a step only works when hidden automation exists, the workflow is not finished yet.

A lawful system therefore supports:
- automation-carried execution when the runtime is available, and
- manual fallback of that same step when the runtime is held, disabled, or absent.

## Orchestration horizon

ION must not only decide the next bounded step. It must also shape the upcoming window of work:

- **Immediate horizon**: precise next executable packets
- **Near horizon**: ordered likely-next work that still needs refinement
- **Far horizon**: looser future chains that become more precise as they approach

This is the same law under manual and automated execution.

## Carrier mapping

### Manual / chat / IDE-carried
The working agent carries more of the transitions itself, but must still use the same templates, packets, and gates.

### Supervised automation-carried
The kernel carries more of the transitions explicitly through runtime modules such as daemon service, child-work service, recovery/replay, and external execution bridge.

### Parallel / swarm-carried
Future swarms are valid only if each child worker still receives a bounded packet, performs one bounded step, and returns a proposal into the same landing and handoff law.

## What is forbidden

- Hidden multi-step jumps that do not emit lawful state or handoff.
- Treating witness/report surfaces as kernel truth.
- Treating external/API work as direct authority.
- Treating support layers as replacements for the canonical loop.
