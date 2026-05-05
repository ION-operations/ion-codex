---
type: roundtable_response
from: Builder Perspective (Mason + Scribe synthesis by Nemesis)
created: 2026-04-03T11:25:20-04:00
responding_to:
  - ION/06_intelligence/roundtable/continuity_crisis/INDEX.md
  - ION/06_intelligence/audits/2026-04-03_continuity_stabilization_audit.md
  - ION/06_intelligence/roundtable/continuity_crisis/responses/2026-04-03_sovereign_directive_manual_auto_and_model_allocation.md
status: FILED
---

# Builder Continuity Roundtable Response

## Role Posture

This response represents the implementation/operations perspective the execution-tier
roles would need if they are going to participate safely in continuity recovery.

The key builder principle is simple:

> Do not automate meaning first. Automate integrity first.

## 1. What physical scaffolding must exist before worker dispatch is real?

### 1.1 The bus must physically exist

Before builders can honestly say they are task-driven by the protocol, the active `ION/`
root needs the physical surfaces the docs already assume:

- `ION/05_context/inbox/`
- clear task filename conventions
- a known place for completed/failed task markers if those are going to exist

Right now the older docs and boots assume these surfaces. They should stop being imaginary.

### 1.2 Private continuity roots must exist per role

If private per-agent continuity is the true ION law, then builders need explicit,
real places to maintain it.

For each active role, at minimum:

- `ION/agents/{role}/MINI.md`
- `ION/agents/{role}/CAPSULE.md`

Without those, builders remain trapped in the wrong shared-root continuity model.

### 1.3 Manual update obligations must be written into templates

The biggest builder problem right now is not “forgetting” to update continuity.
It is that the templates do not yet say exactly what must be updated when work completes.

Every action template that matters operationally should eventually state:

- what must be written into private `MINI`
- what must be written into private `CAPSULE`
- what public artifact must be emitted
- what signal must be sent
- whether any shared projection may be updated and by whom

That turns manual continuity into lawful work, not memory-dependent behavior.

## 2. What can be automated safely now?

### Safe now

- directory scaffolding
- placeholder file creation
- CI setup
- lint/test execution
- syntax and schema validation
- projection-building in shadow mode
- task-file conventions and validation

### Not safe now

- automatic compilation of authoritative shared continuity from unstable sources
- automatic dispatch of workers based on signals that may still be semantically inconsistent
- automatic mutation of `MINI` / `CAPSULE` if the source/compiled distinction is not yet ratified
- any automation that assumes the current unified ION runtime already exists

## 3. Safe manual + automatic side-by-side model

Builders strongly endorse a staged validation loop:

### Stage A — Manual source truth

Agents update their own private continuity by hand after every lawful action.

### Stage B — Shadow projection compiler

Simple tools read private continuity and emit root-level projections or validation reports,
but do not become authoritative yet.

### Stage C — Drift comparison

Compare:

- private continuity
- emitted public artifacts
- compiled projections

If they diverge, the automation is wrong or the manual protocol is not being followed.

### Stage D — Automation promotion

Only after repeated clean cycles should automation graduate from observer to primary
for any part of the continuity flow.

## 4. Clone onboarding for execution-tier chats

Execution-tier clone onboarding should be much simpler than leadership onboarding.

### Required

1. Correct boot file
2. Correct private lane
3. Correct inbox path
4. Correct task packet
5. Correct completion signal
6. Correct private continuity update

### Not required

- broad architectural authority
- editing shared continuity root files
- guessing from public projections what their private state should be

### Execution-tier law

Builders should read projections to orient themselves,
but they should update only:

- their own continuity
- their assigned output artifact
- their own completion signal

## 5. Concrete builder recommendations

### P0

1. create `ION/05_context/inbox/`
2. define task packet filename rules
3. create private continuity directories for active roles
4. update boots so execution-tier roles point first at private continuity once it exists

### P1

5. create minimal projection builder in shadow mode
6. create validation script for private continuity shape and required fields
7. create simple task lifecycle markers (`created`, `claimed`, `completed`, `failed`) if desired

### P2

8. only then begin discussing automated scheduling and compiled context as an active runtime

## Bottom Line

The builder view is that the system does not need more brilliance right now.
It needs:

- directories
- files
- explicit obligations
- validation
- one proven work cycle

If that exists, the deeper ION design can start becoming real again.
If not, more automation will just accelerate the wrong model.
