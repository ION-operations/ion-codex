---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-07T23:12:00-04:00
status: ACTIVE_FIRST_PASS
connections:
  - ION/02_architecture/CONTEXT_MODE_PROTOCOL.md
  - ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md
  - ION/02_architecture/AGENT_REASONING_PROTOCOL.md
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/06_intelligence/specs/T04_ReasoningWindowSchema.spec.md
  - ION/06_intelligence/specs/T07_SignalSchema.spec.md
  - ION/06_intelligence/specs/T09_ManifestRouteStateSchema.spec.md
  - ION/07_templates/reports/MANIFEST_ROUTE_STATE_REPORT.md
lineage:
  - operation-victus/victus/protocol_manifest.py
  - ION-BUILD/src/ion/continuity/manifest.py
  - ION-BUILD/context/history/*ION_MANIFEST*.md
---

# MANIFEST AND ROUTE-STATE PROTOCOL

## Status

This protocol creates the missing bridge between bounded reasoning and future runtime execution.
It defines what manifest / route-state means in the live ION vocabulary.
It does not yet introduce a runtime implementation.

## 1. Why this layer exists

The current root already has:
- mission and doctrine surfaces,
- context package theory,
- reasoning-window governance,
- continuity law,
- signals,
- and low-burn sequential routing practice.

What it still lacked was a named surface for the system's governed traversal position:
where the organism is in its current loop,
which branch is active,
what remains merely future,
and what evidence has already changed the next step.

That is the burden of manifest / route-state.

## 2. Core law

### Law 1 — The manifest is route-state, not continuity

A manifest tells the organism where it is in governed traversal.
It is a program-counter-like surface for execution order and branch posture.
It does not replace private role continuity.

### Law 2 — Route-state is bounded, not omniscient

A route-state record should describe only the active mission/step horizon it is responsible for.
It should not pretend to be a full metaphysical map of the repository.

### Law 3 — Active, future, blocked, and completed must stay distinct

A branch that is merely thinkable is not active.
A branch that is blocked is not completed.
A branch that is completed is not the same as archived continuity.

### Law 4 — Evidence may pressure route-state, but not silently rewrite doctrine

Evidence can reorder branches, lower confidence, or trigger escalation.
It does not independently change doctrine, semantic identity, or rank.

### Law 5 — Manifest state must not be confused with automation state

Route-state answers: "where are we in the governed traversal?"
Automation-state answers: "how is this being carried out and how much autonomy is active?"
The two often interact, but they are not the same surface.

## 3. Required conceptual parts

Every manifest / route-state surface should be able to express at least:
- a manifest identity
- an owner scope (system, role, lane, packet, or work unit)
- a current loop or route position
- a bounded mission or governing objective
- branch state
- evidence trail or evidence references
- blockers / constraints
- handoff or next-route witness
- confidence / uncertainty state appropriate to routing

## 4. Minimum branch lifecycle

Current first-pass lifecycle bands:
- `FUTURE`
- `ACTIVE`
- `BLOCKED`
- `COMPLETED`
- `ABANDONED` (allowed only with explicit witness)

`ABANDONED` exists so the system can preserve truth about a route that is no longer being carried,
rather than lying by omission.

## 5. Branch burden

Each branch should identify at minimum:
- `branch_id`
- `label`
- `status`
- `priority`
- `gate_class` or equivalent traversal burden
- `governing_refs`
- `target_refs`
- `evidence_refs`
- `activation_conditions`

## 6. Relation to existing live surfaces

### In manual continuity mode

The current live root does not yet have a first-class runtime manifest file.
So route-state may be partially witnessed through:
- `ION/MINI.md`
- `ION/STATUS.md`
- reasoning journals
- signals
- migration ledgers

That is acceptable during the current phase,
as long as those surfaces do not pretend they are already the runtime manifest implementation.

### In runtime-assisted mode

A more explicit manifest surface should become the canonical route-state carrier.
That future implementation must still remain subordinate to doctrine and explicit governance.

## 7. Relation to the reasoning layer

The reasoning window asks whether one step is justified, bounded, and ready.
The manifest asks where the organism is in the larger governed traversal.

Reasoning-window outputs may update route-state.
They do not become route-state automatically.

## 8. Route-state update rules

A route-state update is legitimate when one or more of the following is true:
- a branch becomes active
- a branch becomes blocked or completed
- new evidence materially changes branch priority or confidence
- a handoff changes the next lawful carrier
- the loop position changes in a way that matters to recovery or review

A route-state update should not be made merely because prose became longer.

## 9. Current implementation target

The first ION-native schema target for this protocol is:
- `ION/06_intelligence/specs/T09_ManifestRouteStateSchema.spec.md`

Only after the target protocol/schema pair is stable should a bounded runtime module be ported.

## 10. Non-claims

This protocol does **not** yet claim:
- a final on-disk manifest format
- a broad autonomous branch-planning engine
- that every MINI update must also mutate manifest state
- that one global manifest is always superior to bounded role or work-unit manifests
