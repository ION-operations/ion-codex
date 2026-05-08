---
type: orchestration_acceptance
authority: A3_OPERATIONAL
created: 2026-04-08T22:35:00-04:00
status: ACTIVE
purpose: Acceptance matrix and definition of done for ION completion
---

# ION Acceptance Matrix and Definition of Done

## Definition of done

ION is done at this generation when the following are all true:

1. **Canonical legibility**
   The workflow, its packets, and its carriers are easier to understand than to misunderstand.

2. **Executor neutrality**
   At least two different carriers can continue the same scope lawfully using the same packet law.

3. **Manual/automatic equivalence**
   Runtime-off/manual fallback exists for every important automated step.

4. **Bounded externality**
   External/API execution can carry the same step without acquiring direct authority.

5. **Multi-agent continuity**
   Another executor can take over mid-stream from lawful outputs only.

6. **Parallel boundedness**
   The system can safely fan out bounded work and merge it back through explicit law.

7. **Horizon intelligence**
   The system maintains immediate/near/far orchestration and progressively tightens future work.

8. **Scheduler explicitness**
   The organism can explain why a next step is selected, deferred, or rebound under explicit scheduler law.

9. **Operational trust**
   Operators can start, stop, replay, inspect, and understand the runtime truthfully.

10. **Rehearsed proof**
   Completion claims are backed by scenario suites, not only unit tests and doctrine.

11. **Extension readiness**
   Future integrated systems can be added through clear lawful templates rather than ad hoc drift.

## Acceptance matrix

| Capability | Manual carrier | IDE carrier | Supervised runtime | External/API carrier | Swarm carrier | Acceptance requirement |
|---|---|---:|---:|---:|---:|---|
| read lawful state | required | required | required | required | required | same authoritative state families |
| compile bounded context | required | required | required | packet import/export form | required | packet family normalized |
| determine next step | guided/manual | guided/manual | runtime-assisted | delegated but bounded | branch-local | same policy/review law |
| execute one bounded step | required | required | required | required | required | never hidden multi-step jump |
| return proposal | required | required | required | required | required | no direct truth assertion |
| governed landing | required | required | required | required | required | same validation/write/review gates |
| emit next handoff | required | required | required | required | required | takeover packet sufficiently complete |
| recovery/replay | desirable | desirable | required | desirable | required | same re-entry law |
| horizon update | required | required | required | supportive | required | immediate/near/far updated honestly |
| schedule tightening / deferral | guided/manual | guided/manual | runtime-assisted | supportive | branch-aware | explicit scheduler law and receipt surfaces |
| carrier rebinding | guided/manual | required | required | delegated return | required | same step, same packet law, different carrier |

## Scenario categories that must pass

### S1 — Single-carrier manual sequence
One executor performs multiple lawful steps using only bounded packets and handoffs.

### S2 — Mid-stream takeover
A second executor continues from lawful artifacts only.

### S3 — Runtime-assisted sequence
Daemon/service carries several transitions without violating the same law.

### S4 — Manual fallback of an automated step
Runtime-off/manual fallback yields the same essential outputs and gates.

### S5 — External/API carrier parity
A bounded packet is exported, returned, and landed lawfully.

### S6 — Interruption and replay
A bounded interrupted run resumes truthfully.

### S7 — Multi-child fan-out/fan-in
Two or more bounded child returns merge or escalate under explicit law.

### S8 — Horizon refinement
Far and near horizon items get tighter as work approaches.

### S9 — Scheduler selection / defer / rebind
The organism can explain why a candidate was selected, deferred, or rebound to another carrier under explicit law.

## Release / ratification evidence bundle

Before calling the project complete, assemble:
- doctrine and system-map snapshot
- packet family catalog
- acceptance checklist
- passing scenario outputs
- carrier-equivalence evidence
- takeover evidence
- scheduler-law evidence
- swarm-safe merge evidence
- unresolved frontier statement

## Failure criteria

The project is not done if any of these remain true:
- the next executor still needs hidden context to continue,
- carrier change implies process change,
- horizon language remains ceremonial rather than live,
- scheduler choice remains mostly hidden intuition,
- parallel work exists without merge law,
- or completion claims rest mainly on module tests.
