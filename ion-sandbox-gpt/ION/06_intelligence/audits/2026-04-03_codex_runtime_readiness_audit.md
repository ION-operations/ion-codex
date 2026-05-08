---
type: audit
from: Codex
created: 2026-04-03T19:18:00-04:00
status: COMPLETE
topic: Runtime readiness audit after the first kernel stack buildout
connections:
  - ION/PLAN.md
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/context_compiler.py
  - ION/04_packages/kernel/sequential_kernel.py
  - ION/tests/test_sequential_kernel.py
  - ION/tests/test_context_compiler.py
---

# Codex Runtime Readiness Audit

## Summary judgment

ION is no longer blocked on the absence of a kernel substrate.
ION is still blocked on the absence of a real runtime loop.

That is the cleanest current sentence.

### What is now genuinely landed

- private continuity law
- root projections as projections
- minimal doctrine floor
- minimal template floor
- visible task/signal packet discipline
- sequential kernel router
- typed kernel records
- durable kernel record store
- in-memory kernel index
- bounded causal graph
- explicit context compiler helper

### What is still partial or missing

- scheduler
- dispatch/spawner helper for the new kernel stack
- signal protocol implementation for runtime transitions
- explicit commit-delta validation / gatekeeper bridge
- broader doctrine/template ratification
- extracted daemon/service loop

---

## Layer audit

| Layer | Status | Evidence | Readiness | Main blocker |
|---|---|---|---|---|
| Continuity law | LANDED | `02_architecture/CONTINUITY_ARCHITECTURE.md`, private lanes, normalized boots | High | ratification not yet final |
| Root projection model | LANDED | `ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md` corrected as projections | High | projection curation still manual |
| Doctrine floor | PARTIAL | `01_doctrine/README.md`, `SOVEREIGN_CONSTITUTION.md`, `SOVEREIGN_KERNEL.md` | Medium | not full canon, not fully ratified |
| Template floor | PARTIAL | `07_templates/` minimal stack | Medium | fuller reviewed registry still absent |
| Task/signal packet discipline | LANDED | `05_context/inbox/`, `05_context/signals/`, lifecycle helpers | High | signal semantics still partly narrative |
| Sequential orchestration | LANDED | `04_packages/kernel/sequential_kernel.py`, live bundles, retired tasks | High | still session-driven, not scheduler-driven |
| Typed kernel model | LANDED | `04_packages/kernel/model.py` | High | broader legacy object model not yet ported |
| Durable store | LANDED | `04_packages/kernel/store.py` | High | runtime root policy still future work |
| Indexed lookup | LANDED | `04_packages/kernel/index.py` | High | broader query catalog still future work |
| Causal graph | LANDED | `04_packages/kernel/graph.py` | High | no broad semantic bond system yet |
| Context compiler helper | LANDED | `04_packages/kernel/context_compiler.py` | High | explicit inputs only; no daemon loading |
| Scheduler | MISSING | no scheduler helper yet | Low | next required runtime helper |
| Dispatch/spawner | MISSING | no new-stack dispatch helper yet | Low | depends on scheduler shape |
| Runtime signal service | MISSING | no new-stack signal implementation yet | Low | depends on runtime transition model |
| Gatekeeper bridge | MISSING | no new-stack validation helper yet | Low | depends on commit/delta transition path |
| MCP surface | MISSING | no new-stack MCP helpers yet | Low | depends on stable runtime services |

---

## Readiness by phase

### Phase: Construction substrate

Status: READY

Reason:

- the kernel data/lookup/compiler floor is now sufficiently real to support runtime helpers

### Phase: Runtime-helper construction

Status: READY TO START

Reason:

- the next missing helpers can now be built on top of real local machinery

Required next order:

1. scheduler helper
2. dispatch helper
3. signal helper
4. validation/gatekeeper helper

### Phase: Extracted daemon runtime

Status: NOT READY

Reason:

- too many runtime helpers are still missing
- doctrine/template canon is not stable enough for broad extraction claims

### Phase: API-native / MCP-facing orchestration

Status: NOT READY

Reason:

- extracted service loop does not yet exist
- current compiler is explicit-input-driven rather than daemon-driven

---

## Main risks

### 1. Myth of completion

Risk:

- the visible progress may tempt the field to speak as if the runtime already exists

Reality:

- the stack exists
- the loop does not yet

### 2. Premature extraction

Risk:

- moving too quickly into API/MCP/service language before scheduler/dispatch/validation
  helpers exist

Reality:

- extraction should follow proven local helpers

### 3. Canon drift

Risk:

- blueprint and research surfaces can outpace ratified law surfaces

Reality:

- current law floor is strong enough to build against, but not strong enough to stop
  explicit provisional labeling

### 4. Budget drift

Risk:

- architecture may quietly slide back toward many-live-premium-chat assumptions

Reality:

- low-burn sequential remains the present safest governing posture

---

## Current best next move

Build the scheduler helper next.

Reason:

- the compiler now exists
- packets already exist
- the kernel stack can now support actual machine-usable work advancement logic

Without the scheduler, the system remains a strong substrate without a true runtime loop.

---

## Plan drift note

`ION/PLAN.md` is still useful as the strategic execution map, but it is no longer an
accurate completion ledger for the first kernel passes already landed on April 3, 2026.

Specifically, the following surfaces now exist in bounded first pass even though the
plan table still marks their broader tasks as `TODO`:

- `T22` model floor
- `T23` store floor
- `T24` index floor
- `T25` graph floor
- `T34` context compiler helper floor

That mismatch is not fatal as long as future agents treat the plan as a strategic map
and this audit as the more current runtime readiness witness.
