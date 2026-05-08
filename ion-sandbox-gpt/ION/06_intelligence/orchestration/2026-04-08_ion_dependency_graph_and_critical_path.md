---
type: orchestration_dependencies
authority: A3_OPERATIONAL
created: 2026-04-08T22:25:00-04:00
status: ACTIVE
purpose: Dependency graph and critical path for completion
---

# ION Dependency Graph and Critical Path

## Critical path overview

The shortest trustworthy route to completion is now:

1. operator entry surface,
2. packet/handoff normalization,
3. horizon state + tightening,
4. horizon packet enactment + receipts,
5. horizon-to-execution workflow rehearsal,
6. blind continuation / takeover rehearsal,
7. lawful orchestration scheduler definition,
8. executor capability registry and takeover law,
9. manual/automation equivalence proof and context-perfect continuation,
10. bounded parallelism and settlement law definition,
11. bounded multi-agent fan-out/fan-in implementation,
12. evaluation/regression harness,
13. completion ratification.

## Why this is the critical path

Because each later step depends on the previous one being legible and provable:
- you cannot trust scheduler law if a fresh executor still cannot continue from bounded artifacts,
- you cannot trust executor selection without an explicit scheduling center,
- you cannot trust multi-agent execution without strong handoff and settlement law,
- you cannot trust completion without repeated rehearsals and regression evidence.

## Dependency ladder

### D1. Operator entry surface
Blocks:
- scenario onboarding
- productized operation
- operator acceptance

Status:
Landed.

### D2. Packet and handoff normalization
Blocks:
- takeover proofs
- manual/auto equivalence proofs
- external/API parity proofs
- swarm-safe fan-out

Status:
Landed.

### D3. Horizon record and tightening machinery
Blocks:
- real future-window orchestration
- planning credibility beyond the next step
- lawful scheduler emergence

Status:
Landed.

### D4. Horizon enactment and receipt machinery
Blocks:
- packet-ready future work returning into the loop
- traceability between horizon state and enacted packet
- operator rediscovery of enactment posture

Status:
Landed.

### D5. Scenario/rehearsal suite spine
Blocks:
- trust claims
- evaluation baselines
- completion ratification

Status:
Materially landed through L4; broader parallel settlement cases remain.

### D6. Blind continuation / takeover proof
Blocks:
- trustworthy executor neutrality
- lawful capability selection
- any claim that continuity survives executor replacement

Status:
Landed through K7/L4.

### D7. Scheduler doctrine/state/policy
Blocks:
- principled next-executor choice
- carrier-binding law
- branch-aware orchestration
- non-brittle future-window control

Status:
Landed through L0-L4.

### D8. Executor capability registry
Blocks:
- principled next-executor choice
- lawful external/swarm scaling

Status:
Landed.

### D9. Bounded parallelism and settlement law definition
Blocks:
- swarm readiness
- bounded parallel work

Status:
Current architecture center landed as M0 doctrine; embodiment still pending.

### D10. Fan-in / merge embodiment
Blocks:
- lawful swarm readiness
- bounded parallel work in code/runtime

### D11. Evaluation and regression
Blocks:
- trustworthy completion claims
- future change control

## Parallelizable work

These can proceed in parallel once their prerequisites exist:
- operator CLI polish and examples,
- horizon visualization/projections,
- scheduler receipt/readout design,
- packet catalog improvement,
- acceptance bundle assembly,
- packaging notes and quickstarts,
- targeted audits that sharpen takeover or equivalence proof.

## Sequencing rule

Do not widen into bounded swarm execution until:
- K7 blind continuation proof exists,
- L0-L4 executor neutrality and continuation work exists,
- and M0 settlement law definition exists.

That is the correct guardrail against premature scale.
