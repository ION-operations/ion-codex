---
type: research
authority: A3_OPERATIONAL
template: SYSTEM_EVOLUTION
from: Codex
created: 2026-04-03T12:02:45-04:00
status: IN_PROGRESS
ratification: NOT_RATIFIED
responding_to:
  - ION/06_intelligence/research/2026-04-03_TOTAL_ION_DIRECTION_vizier.md
  - ION/06_intelligence/audits/2026-04-03_continuity_roundtable_kickoff.md
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
---

# Codex Phase 0B Build/Run Priorities

## Purpose

This note is narrower than the deep dive.
It answers one question:

What should the team build next if the goal is to get ION actually running in
its current IDE-native phase rather than merely describing a future system?

My answer is: prove the loop, then harden the loop, then automate the loop.

---

## 1. Definition of success for Phase 0B

Phase 0B is successful when a real bounded task can move through a lawful path
without hidden-chat dependence.

Minimum success criteria:

1. the task enters through a visible intake surface,
2. the target role reads its own private continuity first,
3. the role performs template-governed work,
4. the role updates its own `MINI.md` and `CAPSULE.md`,
5. the role emits a signal or public artifact that others can inspect,
6. another role can review or audit from disk,
7. a fresh session can resume from the resulting private `MINI.md`.

If those seven conditions are not met, the system is not running yet in the
sense that matters.

---

## 2. Build order I would follow now

### Priority 1: Correct runtime truth before adding new machinery

Boot documents, continuity law, and active role behavior must agree.

Current examples of misalignment:

- `RELAY.boot.md` still starts from root shared surfaces even though relay law
  rejects shared-root continuity ownership.
- `PLAN.md`, `MINI.md`, `CAPSULE.md`, and `STATUS.md` still read like stronger
  authorities than the corrected continuity law allows.
- `MULTI_CHAT_COORDINATION.md` still carries the older shared-surface model.

Until the runtime truth surfaces agree, every new agent/chat risks inheriting a
mixed model.

### Priority 2: Make the inbox real with one actual task packet

`ION/05_context/inbox/` exists but has no demonstrated traffic.

That should change before further architectural expansion.

The team should prove at least one real packet flow such as:

1. Sovereign intent becomes relay packet or direct visible directive.
2. Vizier receives a concrete inbox task.
3. Vizier completes one bounded output.
4. Vice or Nemesis reviews that output from disk.
5. Signals announce completion or dissent.

Without traffic, the bus is a declaration, not an operating surface.

### Priority 3: Explicitly define the temporary projection regime

The corrected law already says root surfaces are temporary curated projections.
The team should now choose one temporary regime and state it plainly:

- either Vizier manually curates root projections after each major transition,
- or root projections are suspended and everyone reads agent-private state plus
  signals until manual compilation procedure exists.

The dangerous state is ambiguity, where different roles silently assume
different projection rules.

### Priority 4: Land missing identity surfaces for active leadership

There is still no visible `VIZIER.boot.md`.
Codex also has no formal role surface if Codex is to remain an active
contributor rather than a transient external observer.

This does not mean create endless new agents.
It means that any role doing meaningful work should have a lawful identity,
lane, and boot contract.

### Priority 5: Exercise one real review stack

ION's differentiator is not just "task gets done."
It is that governed work remains answerable.

That means at least one cycle should include:

- primary work,
- conjugate review or explicit non-engagement rationale,
- external audit or auditability check,
- visible outcome.

That is how the system proves it is more than a solo-agent file ritual.

### Priority 6: Only after repeated proof, automate

After two or three successful manual loops, the next automation targets become
obvious:

- projection compilation,
- packet generation,
- signal normalization,
- validation of allowed writes,
- model/chassis provenance capture.

Automation should compress known good behavior, not guess it.

---

## 3. First runnable slice I would recommend

I would recommend a deliberately small live slice.

### Candidate slice

Subject:
`"Codify the IDE-native reference implementation phase and update the team on the current operational contract."`

### Suggested path

1. Sovereign or Relay emits one bounded visible packet.
2. Vizier receives a task file in `ION/05_context/inbox/`.
3. Vizier reads private `agents/vizier/MINI.md` and `CAPSULE.md`.
4. Vizier produces one research or directive artifact.
5. Vizier updates private continuity.
6. Vice either haunts the artifact or explicitly records non-engagement.
7. Nemesis checks whether the output is auditable and whether the continuity
   transition was lawful.
8. A fresh session proves resume from the updated `MINI.md`.

This is small enough to run now and rich enough to expose real failures.

---

## 4. What I would not build first

### Not first: full compiler stack

Compilers are useful, but if the manual source model is still mixed, the
compiler will just industrialize ambiguity.

### Not first: API-native runtime extraction

The team already has the right instinct here.
Do not rush the API layer while the IDE-native semantic kernel is still being
named and tested.

### Not first: clone proliferation

The roundtable already held this correctly.
More agents on a mixed continuity model means more drift, not more progress.

### Not first: decorative dashboards

A dashboard over non-lawful state creates false confidence.
Operator surfaces should come after trustworthy state transitions.

---

## 5. Exact considerations for "getting it running"

### 5.1 Private continuity must always win over convenience

If a role can only resume because the operator remembers the last chat, the
system has not actually resumed.

### 5.2 Every important transition needs an external artifact

If a human cannot inspect the transition from disk, the transition is not yet
lawful enough for ION.

### 5.3 Signals should announce, not duplicate

The signal should point.
The artifact should hold substance.

### 5.4 Write authority should become machine-checkable

Even before a full gatekeeper exists, the team should write as though a
gatekeeper will later validate:

- who may write where,
- which artifact classes may trigger which downstream actions,
- what counts as projection vs source state.

### 5.5 Model allocation should be tracked from the start

Since ION is explicitly thinking about same-family and cross-company switching,
the team should capture:

- which chassis produced which artifact,
- when a role switched chassis,
- whether the switch altered trust posture.

This does not need a full router first.
It needs disciplined recording.

---

## 6. My recommended immediate work queue

1. Reconcile boot docs against `CONTINUITY_ARCHITECTURE.md`.
2. Decide temporary policy for root projections during manual-recovery phase.
3. Create and run one real inbox task cycle.
4. Record that cycle as the first Phase 0B proof artifact.
5. Re-run the same pattern from a fresh session to test resume.
6. Only then decide what should be automated next.

---

## 7. Final recommendation

The next milestone should not be "more architecture landed."
It should be:

> "One lawful, inspectable, resumable ION loop has been demonstrated in the
> current IDE-native runtime."

Once that exists, the build has a heart.
Before that, it still mostly has a theory.

## Upstream Reads

- `ION/02_architecture/CONTINUITY_ARCHITECTURE.md`
- `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
- `ION/03_registry/boots/RELAY.boot.md`
- `ION/03_registry/boots/VICE.boot.md`
- `ION/05_context/comms/sovereign/directive_recalibration.md`
- `ION/06_intelligence/audits/2026-04-03_continuity_roundtable_kickoff.md`
- `ION/06_intelligence/research/2026-04-03_TOTAL_ION_DIRECTION_vizier.md`

## Downstream Expects

- Possible conversion of these priorities into a ratified Phase 0B task list
- Boot correction pass
- First real inbox-driven loop

## Open Questions

1. Which role should own the first proof-loop packet: Relay or Vizier?
2. Should Phase 0B require Vice engagement on the very first loop, or only
   Nemesis auditability check?
3. Does the team want root projections actively curated during proof loops, or
   intentionally de-emphasized until manual compile procedure exists?
