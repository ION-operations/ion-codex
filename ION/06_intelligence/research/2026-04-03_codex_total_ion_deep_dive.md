---
type: research
authority: A3_OPERATIONAL
template: RESEARCH
from: Codex
created: 2026-04-03T12:02:45-04:00
status: IN_PROGRESS
ratification: NOT_RATIFIED
responding_to:
  - ION/05_context/comms/sovereign/directive_recalibration.md
  - ION/06_intelligence/audits/2026-04-03_continuity_roundtable_kickoff.md
  - ION/06_intelligence/research/2026-04-03_TOTAL_ION_DIRECTION_vizier.md
  - ION/06_intelligence/research/2026-04-03_codex_protocol_field_working_thesis.md
---

# Codex Deep Dive: ION Kernel, Protocol Field, and the IDE-Native Reference Implementation

## What This Document Is

This is my current best attempt to name what ION is, what layer of it is
already real in the active `ION/` root, what remains contradictory, and what
must be proven in practice before the team should trust scale, automation, or
API extraction.

This is not a ratification artifact.
It is a working synthesis from the live repository state.

---

## 1. The deepest statement I can make right now

ION is not primarily a codebase.
ION is not primarily a chat system.
ION is not primarily a memory system.
ION is not primarily an orchestration daemon.

ION is a governed cognitive operating environment in which work, memory,
routing, signaling, and trust are meant to be produced by the same protocolized
action rather than by separate subsystems.

That is the deepest simplification I currently trust.

If an agent works lawfully inside ION:

1. the task is received through governed context,
2. the work is performed under a template,
3. the output is emitted in a governed form,
4. the output updates the agent's continuity,
5. the output updates system visibility,
6. the output changes what future agents will see and trust.

In a mature ION, these are not six systems.
They are six faces of one transition.

---

## 2. ION's kernel is smaller than its ecosystem

The current tree contains a lot of material: schemas, phase plans, research,
daemon ideas, routing ideas, model-allocation ideas, archaeology, relay, audit,
and authority resolutions.

But the kernel appears smaller than the full ecosystem around it.

### 2.1 Kernel candidates I currently believe are real

1. A filesystem substrate that can hold durable, inspectable state.
2. Templates that govern not just output shape, but continuity behavior.
3. A private `MINI.md` per agent that acts as the routing primitive.
4. A private `CAPSULE.md` per agent that acts as the memory primitive.
5. Signals and public artifacts for inter-agent visibility.
6. A governance hierarchy that decides who may create, classify, review, block,
   or release which outputs.

Everything else looks like one of three things:

- an adapter,
- an automation layer,
- or an optimization layer.

### 2.2 Why that matters

If the kernel is not stable, automating anything above it will multiply drift.
If the kernel is stable, much of the rest of ION becomes a substrate problem.

This is why the continuity correction was so important.
It did not just fix a file-layout issue.
It corrected the kernel.

---

## 3. The right separation is kernel vs adapter vs automation

One reason ION has been hard to name is that several layers were being discussed
at once.

I think the system becomes much clearer when separated into these layers:

### 3.1 Semantic kernel

This is the substrate-independent part:

- template law
- continuity law
- routing law
- authority law
- write boundaries
- trust classification
- release and dissent rules

This layer should survive substrate changes.

### 3.2 Execution adapter

This is how the kernel is presently enacted.
Right now the active adapter is the IDE substrate:

- Cursor/Codex sessions
- IDE-native tools
- rich local repository awareness
- human-visible filesystem coordination

This is not a fake system.
It is the current runtime adapter.

### 3.3 Automation and service layer

This is what later makes the kernel easier to run:

- compilers
- daemons
- gatekeepers
- MCP exposure
- API-native orchestration
- model routers
- validation services

The clean way to say the current phase is:

> `ION/` is an IDE-native reference implementation of ION whose semantic kernel
> is being made strict enough that later API-native execution can be mostly a
> substrate swap rather than a conceptual rewrite.

That is much stronger than calling the current build a temporary emulation.

---

## 4. Why "protocol field" is a better name than "protocol"

The user has been reaching toward something deeper than "agents follow rules,"
and I think that instinct is correct.

A weak protocol is a checklist.
A strong protocol is a field.

What makes ION feel like a field is that almost every meaningful rule leans on
other rules:

- template choice changes output shape
- output shape changes what can be routed
- routing changes what the next agent sees
- visibility changes what the next agent may infer
- authority class changes whether that output may be trusted
- trust changes whether the output may enter future context
- governance determines who can ratify or block that flow

This is not linear.
It is coupled.

That coupling is what makes continuity possible at scale.
The continuity is not an after-action note stapled onto work.
It is the residue of work performed inside a sufficiently complete field.

That is why I do not think the central claim should be:

> "An agent that follows protocol produces continuity."

I think the stronger claim is:

> Under a sufficiently whole protocol field, lawful work emits continuity,
> recoverability, and answerability as a side effect of doing the work.

That is a different standard.
It is not asking whether the agent obeyed.
It is asking whether the field was whole enough to shape the cognition.

---

## 5. What the live repository already proves

The repository is early, but it already proves some important things.

### 5.1 The active build is intentionally IDE-native

`ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md` is not an accidental stopgap.
It is explicit about mapping ION roles and transitions onto the IDE task/subagent
environment.

This means the current build should not be judged as a failed API orchestration
system.
It should be judged as an IDE-native enactment of ION.

### 5.2 The continuity law has corrected toward private source state

`ION/02_architecture/CONTINUITY_ARCHITECTURE.md` is the most important recent
correction in the tree.
It states plainly that:

- continuity is per-agent private,
- no agent writes another agent's continuity,
- shared views are compiled or curated projections,
- the root-level surfaces are temporary projections rather than raw source truth.

That is a kernel correction, not a cosmetic refinement.

### 5.3 The governance structure is already richer than a flat agent swarm

The current role stack is not just "many agents."
It is structured:

- Sovereign as human final authority
- Vizier as architect/coordinator
- Vice as conjugate internal opposition
- Nemesis as external audit and release gate
- Relay as faithful user-facing courier
- execution-tier and archaeology-tier roles below that

This matters because ION is not trying to maximize agent autonomy.
It is trying to maximize lawful intelligence under role differentiation.

### 5.4 Model plurality is already part of the design, not a later add-on

The Daimon protocol and the multi-model orchestration inventory both point to
the same conclusion: model diversity in ION is not just cost routing.
It is cognitive-basis routing.

If that holds, then chassis choice is not merely an implementation detail.
It is part of how the field preserves alternate dimensions of answerability.

---

## 6. What is still contradictory or incomplete

The tree also shows very clear incompletions.

### 6.1 The old shared-surface model still haunts the active build

`ION/PLAN.md`, `ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md`, and
`ION/02_architecture/MULTI_CHAT_COORDINATION.md` still carry assumptions from
the earlier shared-surface model.

Some of their content remains useful.
But they cannot be treated as clean current law without re-reading them through
the corrected continuity architecture.

### 6.2 Boot documents are unevenly corrected

`VICE.boot.md` is largely aligned with private continuity law.
`RELAY.boot.md` still instructs session start by reading root `MINI.md`,
`STATUS.md`, and `CAPSULE.md` before private relay state, even though the relay
protocol says Relay must not treat shared root files as its continuity.

That kind of mismatch matters because boots are runtime truth surfaces.
If the boot is mixed, the role will be mixed.

### 6.3 The inbox exists physically but not operationally

`ION/05_context/inbox/` exists, but it is empty.
That means the system has a declared bus and no demonstrated traffic.

Until at least one real end-to-end task loop runs through that bus, "dispatch"
remains more declared than proven.

### 6.4 Compiled projections are lawfully described but not landed

The corrected law points toward `ION/context/*.compiled.md`.
Those surfaces do not yet appear to exist in active use.

That is fine for now if manual continuity recovery is the deliberate phase.
It is not fine if anyone quietly assumes the compiler already exists.

### 6.5 Naming splits still reveal unresolved evolution

The tree contains `relay/relay/` and `relay/amanuensis/`.
The second lane appears physically present but empty.

This is not a crisis.
But it is a sign that some role boundaries, names, or predecessor ideas are
still coexisting without final reduction.

### 6.6 The active role set is still incomplete

There is no visible `VIZIER.boot.md` in `ION/03_registry/boots/`.
There is also no formal Codex role or Codex lane, even though Codex is now
participating in system thinking.

This means some real contributors are presently operating without first-class
identity surfaces in the system they are helping define.

---

## 7. The most important considerations I would surface to the team

### 7.1 Never hide essential state inside substrate affordances

The active IDE gives agents strong hidden advantages:

- open tab context
- repository awareness
- local tool fluency
- thread-local memory
- operator steering

Those are useful.
They are also dangerous if the kernel begins to rely on them.

Anything essential to continuity, routing, trust, or delegation must be
externalized into filesystem-visible artifacts.
Otherwise the later API-native build will not be "the same system."

### 7.2 Do not confuse projections with source truth

This is the major error that already surfaced once.
It will recur unless the team treats this as a standing law.

Root or compiled views are for awareness.
Private continuity is for source truth.

### 7.3 Do not automate a law you have not yet run manually

If the manual loop does not work, the automation cannot be trusted.
Automation should be a compression of already-proven lawful manual behavior.
Not a substitute for understanding it.

### 7.4 Preserve split authority instead of flattening it

ION is strongest when it admits that authority is not singular:

- Relay is not Vizier
- Vice is not Nemesis
- human ratification is not template compliance
- current runtime truth is not historical witness

Every time the system collapses these into one neat surface, drift increases.

### 7.5 Chassis decoupling should remain constitutional

The user is likely correct that if the machine language becomes strict enough,
the same governance can later run over APIs with relatively small semantic
changes.

That only works if identity stays decoupled from chassis:

- role identity survives model switching,
- continuity objects survive model switching,
- governance does not depend on a vendor-specific affordance,
- tool use is mediated through explicit contracts.

### 7.6 Dissent and audit are not optional quality layers

Vice and Nemesis should not be treated as expensive extras.
They are part of how ION prevents premature closure.

If ION is trying to preserve future answerability, then internal opposition and
external audit are part of the kernel discipline, not post hoc bureaucracy.

### 7.7 Human sovereignty is part of the runtime

The Sovereign is not just "the user."
The Sovereign is the final boundary-condition setter for the field.

This matters because many agent systems try to automate the operator away.
ION appears to want something more lawful:

- the system can become more self-running,
- but the operator remains constitutionally meaningful,
- especially for ratification, escalation, and mission shifts.

---

## 8. What I think "ION running" means in the current phase

I do not think "running" currently means:

- full daemon infrastructure,
- API-native orchestration,
- autonomous clone scaling,
- or complete compiled-context automation.

I think "running" means something smaller and stricter.

### 8.1 Minimum credible running ION

The system is meaningfully running when one bounded task can complete through a
lawful end-to-end cycle such that a fresh session can resume without hidden chat
memory.

That cycle should include:

1. intake of intent through a lawful surface,
2. routing to an accountable role,
3. template-governed work,
4. private continuity update,
5. public visibility update,
6. optional dissent or audit,
7. successful resume from the resulting `MINI`.

If that works repeatedly, ION exists operationally even before advanced
automation lands.

### 8.2 Stronger definition

I would call the current phase successful only when:

- at least one leadership role can resume perfectly from private continuity,
- at least one relay-to-worker or relay-to-leadership path has proven traffic,
- at least one dissent/audit path has been exercised on a live artifact,
- the operator can inspect the whole transition from disk,
- and no step depends on hidden thread state to be intelligible.

---

## 9. What I would build next

If the team wants the biggest leverage with the least self-deception, I would
build in this order:

### 9.1 Prove Phase 0B manually

Run one real protocol loop end to end before more infrastructure expansion.

### 9.2 Correct the runtime truth surfaces

Bring the boot documents and active routing surfaces into explicit alignment with
the corrected continuity law.

### 9.3 Make the task bus real

Use the inbox, signals, and public artifacts for actual traffic rather than only
describing them architecturally.

### 9.4 Decide the minimum compiled-projection discipline

Either:

- root projections remain Vizier-curated temporary operator views,

or

- a provisional manual compile process is defined.

But the system should stop oscillating ambiguously between those two stories.

### 9.5 Treat model allocation as a constitutional operating problem

The Daimon protocol has already opened this door.
The next step is not just "pick best model."
It is to define lawful conditions under which:

- a role keeps its identity across chassis changes,
- same-family tier shifts are allowed,
- cross-company shifts are allowed,
- and provenance is preserved across those transitions.

### 9.6 Only then harden automation

Compilers, daemons, MCP, API-native runtime, and wider clone scaling should come
after repeated proof of the manual loop.

---

## 10. My current best wording for the team

If I had to compress the whole direction into a few lines, it would be this:

> ION is a governed cognitive operating environment whose core law is that work
> performed under the correct template and routing discipline should emit its own
> continuity, visibility, and recoverable future state.
>
> The current `ION/` root is an IDE-native reference implementation of that law,
> not a lesser fake version of the future system.
>
> The immediate task is not to outbuild the architecture. It is to prove the
> kernel loop manually and visibly enough that later automation and API execution
> are merely substrate hardening of something already real.

---

## 11. Final judgment for this pass

My present judgment is:

1. The team is converging on the right kernel.
2. The biggest danger is still false completion through beautifully written
   surfaces that have not yet been proven operationally.
3. The user's intuition is directionally right: if the current build becomes
   strict enough in machine language and governance, it can become the reference
   implementation from which the API-native production system is extracted.
4. The next decisive proof is not another schema set. It is a live end-to-end
   lawful loop that survives session loss and resume.

That is the threshold I would now optimize for.

## Upstream Reads

- `ION/05_context/comms/sovereign/directive_recalibration.md`
- `ION/PLAN.md`
- `ION/MINI.md`
- `ION/CAPSULE.md`
- `ION/STATUS.md`
- `ION/02_architecture/CONTINUITY_ARCHITECTURE.md`
- `ION/02_architecture/MULTI_CHAT_COORDINATION.md`
- `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
- `ION/02_architecture/CONJUGATE_DAIMON_PROTOCOL.md`
- `ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md`
- `ION/03_registry/boots/RELAY.boot.md`
- `ION/03_registry/boots/VICE.boot.md`
- `ION/03_registry/daimon_matrix.yaml`
- `ION/06_intelligence/audits/2026-04-03_continuity_roundtable_kickoff.md`
- `ION/06_intelligence/research/2026-04-03_TOTAL_ION_DIRECTION_vizier.md`
- `ION/06_intelligence/research/multi_model_orchestration_inventory.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`

## Downstream Expects

- Team review in lawful lanes
- Possible Codex participation in a Phase 0B proof loop if requested
- Comparison against Vice and Nemesis perspectives

## Open Questions

1. What is the thinnest possible template set that still preserves the full kernel?
2. Should compiled projections remain root-level during IDE-native phase or move
   immediately to `ION/context/` even before automation?
3. Which role should own manual projection/compilation procedure before the
   compiler exists?
4. Is Codex becoming a formal ION role, a temporary external contributor, or a
   chassis for an existing role not yet named?
