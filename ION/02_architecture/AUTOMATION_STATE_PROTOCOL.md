---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-07T23:18:00-04:00
status: ACTIVE_FIRST_PASS
connections:
  - ION/02_architecture/CONTEXT_MODE_PROTOCOL.md
  - ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/07_templates/reports/AUTOMATION_STATE_REPORT.md
  - ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md
  - ION/06_intelligence/specs/T10_CrossModelAuditCalibration.spec.md
  - ION/06_intelligence/specs/T11_AutomationStateSchema.spec.md
lineage:
  - ION-BUILD/context/specs/automation_unified_spec.md
  - JOC scheduler / macro / gate lineage cited by ION-BUILD
---

# AUTOMATION STATE PROTOCOL

## Status

This protocol names the missing automation-stage surface for the live root.
It makes automation posture explicit without pretending the full automation runtime is already active.

## 1. Why this layer exists

The current root already distinguishes manual continuity from future runtime support.
But it still lacked a stable way to say:
- how much automation is actually active,
- which gates are holding promotion back,
- whether the system is merely assisted or genuinely self-advancing,
- and when a fallback to manual carrying occurred.

Without this layer, automation posture gets inferred from prose or from wishful naming.

## 2. Core law

### Law 1 — Automation state must be explicit when it matters

If a workflow, lane, or system is claiming any meaningful automation posture,
it should be representable in a dedicated automation-state surface.

### Law 2 — Automation state is not continuity

Continuity records the organism's lived work trace.
Automation-state records how execution posture is staged, gated, and promoted.
These must remain distinct.

### Law 3 — Automation state is not route-state

Route-state says where the work is in traversal.
Automation-state says how that traversal is being carried and how much is delegated.

### Law 4 — Promotion is earned, not narrated

A higher automation stage must be justified by gates, observed behavior, and bounded readiness.
Narrative confidence alone is not enough.

### Law 5 — Fallbacks must be visible

If a lane or workflow falls back from assisted or automated execution to manual carrying,
that fallback is not shameful — but it must be recorded.
Hidden fallback corrupts calibration.

## 3. First-pass automation stages

These stages are deliberately conservative:

- `MANUAL` — human/role carried; no runtime delegation beyond ordinary tool use
- `ASSISTED` — structured support exists, but advancement still depends on manual carrying
- `GATED_AUTOMATION` — some advancement can occur when explicit gates pass
- `RUNTIME_ACTIVE` — bounded runtime execution is actually active for the declared scope
- `SUSPENDED` — automation was available or expected, but is intentionally halted
- `DISABLED` — automation is not permitted for the declared scope

## 4. Required dimensions

Every serious automation-state surface should be able to express at minimum:
- scope of state (system / lane / role / workflow / packet)
- current stage
- governing sources
- active gates
- blockers and promotion criteria
- fallback mode and last transition
- operator / review override status
- pending automation-capable actions or queue state (if any)

## 5. Gate classes

A first-pass automation-state record may reference gate families such as:
- confidence gate
- drift gate
- authority gate
- context sufficiency gate
- route-state readiness gate
- human approval gate
- external dependency gate

The protocol does not yet require a single universal gate grammar.
It requires that the live system stop implying gate passage without visible witness.

## 6. Reporting rule

Automation posture should become legible through a dedicated report surface when:
- the user or operator needs to understand why automation is or is not advancing
- escalation or fallback has occurred
- a packet is approaching runtime promotion
- automation claims could otherwise be mistaken for actual implemented capability

The first-pass report surface is:
- `ION/07_templates/reports/AUTOMATION_STATE_REPORT.md`

## 7. Relation to calibration

Confidence and drift surfaces describe whether the organism's self-assessment is trustworthy.
Cross-model calibration describes whether confidence claims match witnessed outcomes across review.
Automation-state uses those surfaces as inputs,
but does not replace them.

## 8. Current live default

The live April 5 integrated root is predominantly:
- `MANUAL` at the system level,
- with pockets of `ASSISTED` structure,
- and **no general `RUNTIME_ACTIVE` claim** for the missing B3 enforcement modules.

This protocol exists so the root can say that truth clearly.

## 9. Non-claims

This protocol does **not** yet claim:
- a fully implemented automation queue in the live root
- calendar/scheduler parity with lineage systems
- that all roles should carry identical automation state
- that automation promotion should happen immediately after the protocol exists
