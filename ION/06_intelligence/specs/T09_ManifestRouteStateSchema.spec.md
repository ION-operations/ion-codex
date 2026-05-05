---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-07T23:24:00-04:00
status: DRAFT
task: T09
depends_on: [T04, T07, T08]
goal: Define the ManifestRouteStateSchema — the governed route-state surface that records loop position, branch posture, evidence pressure, and handoff state without collapsing into continuity or automation state
connections:
  - ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md
  - ION/02_architecture/CONTEXT_MODE_PROTOCOL.md
  - ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md
  - ION/06_intelligence/specs/T04_ReasoningWindowSchema.spec.md
  - ION/06_intelligence/specs/T07_SignalSchema.spec.md
  - ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md
---

# ManifestRouteStateSchema — Governed Traversal and Branch State

## 1. PURPOSE

A ReasoningWindow governs one bounded act of reasoning.
A ManifestRouteState governs the larger traversal position that the organism can recover and review.

This schema exists to formalize:
- current loop position,
- active versus future versus blocked branch posture,
- evidence pressure on routing,
- handoff state,
- and next-route visibility,

without pretending that route-state is the same thing as private continuity or automation posture.

## 2. SCHEMA DEFINITION

```yaml
ManifestRouteStateSchema:
  schema_version: "1.0"

  ManifestRouteState:
    manifest_id: string
    manifest_version: string
    created_at: string
    updated_at: string

    owner_scope:
      scope_type: SYSTEM | ROLE | LANE | WORK_UNIT | PACKET
      scope_id: string
      steward: string

    mode_binding:
      context_mode: IDE_MANUAL | COMPILED_RUNTIME
      automation_stage: MANUAL | ASSISTED | GATED_AUTOMATION | RUNTIME_ACTIVE | SUSPENDED | DISABLED

    route_frame:
      mission: string
      governing_refs: list[string]
      loop_position: CONTEXTUALIZE | REFLECT | PLAN | GATE | EXECUTE | AUDIT | DELIVER
      active_branch_id: string | null
      handoff_summary: string | null
      next_route_proposal: string | null

    branches:
      catalog: list[RouteBranch]

    evidence_pressure:
      recent_evidence_refs: list[string]
      unresolved_issue_refs: list[string]
      blocker_refs: list[string]
      drift_flags: list[string]

    routing_assessment:
      route_confidence: LOW | MEDIUM | HIGH
      branching_stability: STABLE | SHIFTING | FRAGILE
      recommended_action: CONTINUE | NARROW_AND_CONTINUE | PAUSE | ESCALATE | HANDOFF
      reasons: list[string]

  RouteBranch:
    branch_id: string
    label: string
    status: FUTURE | ACTIVE | BLOCKED | COMPLETED | ABANDONED
    priority: P0_CRITICAL | P1_HIGH | P2_NORMAL | P3_LOW
    gate_class: G0_TRIVIAL | G1_BOUNDED | G2_MULTI_STEP | G3_ARCHITECTURAL | G4_SELF_MODIFYING
    target_refs: list[string]
    governing_refs: list[string]
    activation_conditions: list[string]
    evidence_refs: list[string]
    confidence_band: LOW | MEDIUM | HIGH
    started_at: string | null
    completed_at: string | null
    abandonment_reason: string | null
```

## 3. RULES

- Route-state is a bounded traversal surface, not a substitute for private continuity.
- `active_branch_id` must correspond to exactly one branch with status `ACTIVE`, or be null.
- `ABANDONED` requires an explicit `abandonment_reason`.
- Evidence pressure may lower confidence or recommend pause/escalation without deleting witness.
- `automation_stage` is included only as mode binding context; it does not make this schema the automation record.

## 4. IDE/MANUAL MODE ADAPTATION

In the current live root, the schema may be witnessed indirectly through:
- `ION/MINI.md`
- `ION/STATUS.md`
- migration ledgers
- reasoning journals
- signals

That is an adaptation layer, not full parity.
The schema exists so future runtime support has a stable target instead of inventing its own meaning.

## 5. VALIDATION CRITERIA

- [ ] The schema distinguishes route-state from continuity and automation state.
- [ ] Active/future/blocked/completed/abandoned branch posture is explicit.
- [ ] Loop position is recoverable without rereading all continuity prose.
- [ ] Evidence pressure and unresolved issues can influence routing visibly.
- [ ] Handoff and next-route state are visible without silently self-authorizing the next step.
