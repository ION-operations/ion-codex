---
type: research
from: Codex
created: 2026-04-03T19:12:00-04:00
status: COMPLETE
topic: Future orchestration blueprint for the active IDE-native ION build
connections:
  - ION/PLAN.md
  - ION/06_intelligence/research/multi_model_orchestration_inventory.md
  - ION/06_intelligence/research/2026-04-03_codex_total_ion_deep_dive.md
  - ION/06_intelligence/research/2026-04-03_codex_end_to_end_law_protocol_template_review_and_kernel_router_transition.md
  - ION/04_packages/kernel/sequential_kernel.py
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/context_compiler.py
---

# Codex Future Orchestration Blueprint

## What this document is

This is the next large-body blueprint for how ION should be orchestrated from here,
given the system that now actually exists on disk.

It is not a ratification artifact.
It is not a claim that the daemon already exists.
It is not a claim that the premium-parallel swarm is the present default.

It is a build-facing blueprint that tries to answer:

1. what the current active runtime really is,
2. what the next orchestration layers should look like,
3. what must remain manual or explicit for now,
4. and how the current IDE-native build can evolve into the later extracted system
   without changing semantic law.

---

## 1. Current governing reality

The active `ION/` root is now best understood as:

> an IDE-native reference implementation of ION running in low-burn sequential mode,
> with Codex acting as the practical kernel router by default.

That statement matters because it stabilizes several layers at once:

- the semantic kernel is real enough to build against,
- the active execution substrate is the IDE,
- the orchestration default is sequential rather than many-chat parallel,
- and the later API-native system should be treated as an extraction target, not as
  the thing the active root already is.

This means the system should now be designed in two simultaneously valid frames:

1. **present orchestration frame**
   what can actually run lawfully today in the IDE

2. **future orchestration frame**
   what can later be moved into daemon/API/MCP service layers with minimal semantic drift

---

## 2. The orchestration stack

ION is now far enough along that it helps to name the orchestration stack explicitly.

### 2.1 Layer A: Human constitutional field

This remains above everything else.

Functions:

- preserve overall intent
- hold the whole
- authorize ratification
- prevent local subsystem optimization from hijacking the system

In current practice, the Sovereign is not a lone decision oracle.
The role is closer to:

- convergence steward
- final closer of visible field-made decisions
- keeper of whole-system coherence

### 2.2 Layer B: Semantic kernel

This is the substrate-independent law layer.

Functions:

- continuity law
- authority law
- routing law
- output law
- template law
- trust and release law

Artifacts:

- doctrine
- boots
- templates
- schema specs
- continuity architecture
- role law

This is the layer that must survive any substrate shift.

### 2.3 Layer C: Operational coordination layer

This is where the field becomes actually runnable.

Functions:

- task packet creation
- session sequencing
- packet handoff
- lane updates
- signal emission
- audit/review/release routing

Current active form:

- task packets under `ION/05_context/inbox/`
- signals under `ION/05_context/signals/`
- root projections for operator visibility
- private continuity lanes
- Codex-led sequential kernel routing

### 2.4 Layer D: Kernel data/runtime substrate

This is the data-bearing and machine-bearing floor that now exists in first pass.

Current landed modules:

- `kernel/model.py`
- `kernel/store.py`
- `kernel/index.py`
- `kernel/graph.py`
- `kernel/context_compiler.py`
- `kernel/sequential_kernel.py`

These are not full legacy ports.
They are the beginning of a new stack aligned with the current schema law.

### 2.5 Layer E: Future extracted services

These are not yet the active default, but they should already be visible in design.

Expected service families:

- scheduler
- dispatch/spawner helper
- signal service
- gatekeeper / write authority service
- MCP exposure
- control-plane API
- dashboard / IDE bridge surfaces

The design rule is:

> extracted services should consume the semantic kernel and the kernel data/runtime
> substrate, not redefine them.

---

## 3. Runtime modes

ION needs explicit runtime modes so the team stops mixing present truth and future
target in one undifferentiated story.

### 3.1 Mode A: IDE-native low-burn sequential

This is the current default.

Properties:

- one high-capability session acts as router
- auxiliary roles are invoked selectively
- continuity is private and explicit
- task packets and signals remain visible on disk
- packet creation and completion are deliberate
- cost is treated as a first-class operational constraint

This mode should remain the default until the later runtime surfaces prove themselves.

### 3.2 Mode B: IDE-native assisted multi-role

This is still valid, but no longer the default.

Properties:

- multiple live chats or role lanes
- more direct role-authored passes
- still grounded in private continuity and disk artifacts
- higher coordination cost
- higher spend risk

Use only when the work materially benefits from distributed cognition.

### 3.3 Mode C: Extracted daemon-assisted runtime

This is the next real target, not the present default.

Properties:

- scheduler creates or advances work units
- compiler creates context packages explicitly
- dispatch helper mounts identities to chassis
- signals become more machine-readable and less purely narrative
- state moves from human packet handling to lawful service handling

This mode should be introduced only after each helper is independently proven in the
IDE-native reference implementation.

### 3.4 Mode D: API-native / service-native orchestration

This is the later extraction horizon.

Properties:

- adapters replace IDE assumptions
- governed MCP surfaces expose state and actions
- dispatch may target API providers rather than IDE tabs
- runtime state becomes more continuously maintained

This mode should reuse the same semantic contracts.

---

## 4. Codex’s leadership function

If Codex is taking lead in the present phase, the role should be described precisely.

Codex is not replacing the whole field.
Codex is not becoming private supreme law.
Codex is not becoming the sole author of ION.

The leadership function in the present phase is:

- route the field in low-burn sequential form
- preserve provenance while compressing orchestration cost
- externalize decisions, risks, and next steps to disk
- keep current runtime truth separate from future-architecture aspiration
- build the kernel/runtime substrate in order, without skipping enabling layers
- decide when auxiliary roles are worth invoking
- avoid premature daemon myths

In short:

> Codex should act as the practical kernel router and construction lead for the
> current phase, while keeping doctrine, ratification, and field legitimacy
> distributed and explicit.

---

## 5. Role activation blueprint

The team should stop treating all roles as ambiently active.
Roles should be activated by clear need classes.

### 5.1 Always-on practical roles

- Codex
  function: routing, integration, build execution, continuity maintenance

### 5.2 Governance/architecture activation

- Vizier
  activate when architecture, doctrine, or multi-step strategic shaping is needed

- Vice
  activate when future-answerability pressure is needed or when a neat solution feels
  too easy

- Nemesis
  activate when release, canonicalization, ratification, or hidden failure pressure is relevant

### 5.3 Delivery/courier activation

- Relay
  activate when the artifact must be packaged for Sovereign or for wide field visibility

### 5.4 Research/lineage activation

- Thoth
  activate for focused evidence sweeps or bounded research passes

- Atlas
  activate when outside reference pressure or comparative grounding matters

- Vestige
  activate when stale lineage, contradictions, or archaeology matters

### 5.5 Implementation specialization

- Mason
  activate when a bounded implementation slice is delegated, or when the system wants
  a distinct implementation pass separated from route design

This role activation blueprint should later become machine-routable.

---

## 6. Packet and transition blueprint

The current packet surfaces should be treated as the embryo of the future runtime,
not as throwaway scaffolding.

### 6.1 Core packet classes

- task packet
  bounded instruction + target + deliverables + constraints

- role session packet
  one role’s bounded pass for one objective

- handoff packet
  transfer surface between passes

- signal packet
  machine-visible state or event notification

- continuity update
  private lane mutation and shared projection implications

### 6.2 Desired mature transition

Future runtime transitions should look like:

1. a task packet becomes a work unit
2. the compiler helper produces a context package
3. the scheduler selects the next role or chassis
4. execution emits a commit delta
5. validation/gatekeeper decides acceptance class
6. continuity and visibility surfaces update
7. next work is either queued or stopped explicitly

The active root now has enough substrate to start implementing this incrementally.

---

## 7. Budget governance blueprint

The recent spend spike was not just a usage problem.
It forced the architecture to tell the truth.

ION should now treat budget as a governing dimension, not an afterthought.

### 7.1 Budget rules

- premium multi-chat parallelism is not the default
- expensive role duplication requires explicit reason
- low-burn sequential routing is the baseline safe posture
- role activation must be justified by real value, not stylistic completeness

### 7.2 Budget-aware orchestration implications

- the best architecture is not the one that assumes infinite premium cognition
- orchestration packets should work in degraded and nominal conditions
- logs and continuity should preserve enough context that the field can recover after
  a forced contraction in active cognition

### 7.3 Future extraction rule

When the daemon exists, it should not assume premium models everywhere.
It should encode:

- role/chassis separation
- quality thresholds
- escalation rules
- degraded fallback
- explicit witness/review downgrades when cheaper paths are used

---

## 8. The extracted future runtime

The future extracted runtime should not be imagined as “replace the IDE with APIs.”
It should be imagined as:

> preserve the semantic kernel and replace the execution adapter.

### 8.1 What should stay identical

- continuity law
- authority classes
- work unit concept
- context package concept
- commit delta concept
- review and release gates
- role activation logic
- packet/handoff semantics

### 8.2 What should change

- who compiles contexts
- who dispatches execution
- where state is read from during execution
- how signals are propagated
- whether the execution adapter is IDE, API, local runtime, or hybrid

### 8.3 Extraction constraint

Do not migrate a layer out of the IDE-native reference implementation until it has
already been proven there in bounded form.

That means:

- first prove the helper inside `ION/04_packages/kernel/`
- then build the service wrapper around it
- then add adapter-specific behavior

---

## 9. Build sequence from here

The next major build sequence should be:

1. scheduler helper
   reason: now that the compiler exists, the next missing coordination primitive is
   deciding and advancing work in machine-usable form

2. dispatch helper
   reason: once scheduling is explicit, execution mounting becomes the next missing bridge

3. signal helper
   reason: runtime transitions need a machine-visible event channel that is more than
   hand-authored markdown alone

4. write authority helper / gatekeeper bridge
   reason: once real deltas and transitions move, acceptance class must become explicit

5. store/index/graph/compiler integration surfaces
   reason: runtime helpers should consume the actual kernel stack rather than re-derive it

### What should not be rushed

- control plane
- UI/dashboard
- MCP fan-out
- broad agent-autonomy claims
- full API-native runtime

Those become meaningful after the runtime helpers above exist in credible first pass.

---

## 10. What future agents may trust

Future agents may trust:

- the system is no longer only in abstract planning
- the current kernel stack is real in first pass
- the active default runtime is Codex-led sequential low-burn
- the active root is an IDE-native reference implementation
- private continuity and root projections are now stable enough to design against

Future agents must not trust without revalidation:

- that the daemon exists
- that the scheduler/dispatch/gatekeeper runtime loop is real
- that the full doctrine/template canon is ratified
- that parallel premium staffing is the active norm
- that the extracted API-native runtime is already designed cleanly enough to skip the
  current reference phase

---

## 11. Core orchestration principle

The strongest orchestration principle I trust now is:

> Every future automation layer in ION should be born as an explicit bounded helper
> inside the IDE-native reference implementation first, and only later be extracted
> into service form.

That principle keeps the build honest.
It is why the current sequence has worked:

- model
- store
- index
- graph
- compiler

If that principle holds, the future runtime will not be imagined into existence.
It will be lifted out of proven local machinery.
