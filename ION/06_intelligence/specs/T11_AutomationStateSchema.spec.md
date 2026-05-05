---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-07T20:20:00-04:00
status: DRAFT
task: T11
depends_on: [T08, T09, T10]
goal: Define the AutomationStateSchema — a machine-readable posture, gate, blocker, fallback, and promotion state surface that stays distinct from continuity and route-state
connections:
  - ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md
  - ION/02_architecture/CONTEXT_MODE_PROTOCOL.md
  - ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md
  - ION/07_templates/reports/AUTOMATION_STATE_REPORT.md
  - ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md
  - ION/06_intelligence/specs/T10_CrossModelAuditCalibration.spec.md
---

# AutomationStateSchema — Durable Automation Posture and Gates

## 1. PURPOSE

The automation protocol names posture, promotion, fallback, and review burden.
This schema makes that posture machine-readable so the kernel can persist it without pretending a general automation runner already exists.

## 2. SCHEMA DEFINITION

```yaml
AutomationStateSchema:
  schema_version: "1.0"

  AutomationState:
    automation_state_id: string
    created_at: string
    updated_at: string
    scope_type: SYSTEM | ROLE | LANE | WORKFLOW | PACKET | WORK_UNIT
    scope_ref: string
    current_stage: MANUAL | ASSISTED | GATED_AUTOMATION | RUNTIME_ACTIVE | SUSPENDED | DISABLED
    governing_refs: list[string]
    active_gates: list[AutomationGate]
    blockers: list[string]
    promotion_criteria: list[string]
    fallback_mode: MANUAL | ASSISTED | SUSPENDED | DISABLED
    last_transition_reason: string | null
    operator_override: string | null
    pending_actions: list[string]
    linked_manifest_id: string | null
    context_mode: IDE_MANUAL | COMPILED_RUNTIME
    calibration_status: CALIBRATED | UNTESTED | INSUFFICIENT_DATA | UNDERCALIBRATED | OVERCALIBRATED | null
    notes: string | null

  AutomationGate:
    gate_id: string
    gate_class: string
    status: PASS | BLOCKED | FAILED | UNSATISFIED | UNKNOWN
    satisfied: boolean
    detail: string | null
    evidence_refs: list[string]
    required_for_promotion: boolean
```

## 3. RULES

- `RUNTIME_ACTIVE` requires `context_mode = COMPILED_RUNTIME`.
- Gate satisfaction must be individually visible rather than flattened into one prose claim.
- Blockers may be derived from unsatisfied gates, but they must remain separately readable.
- `linked_manifest_id` binds this posture to route-state without collapsing the two records into one file.
- This schema reports posture; it does not itself execute automation.

## 4. CURRENT LIVE ADAPTATION

In the current live root this schema is the lawful machine-readable target beneath:
- `AUTOMATION_STATE_REPORT.md`
- threshold evaluation output
- governed-write promotion posture
- manual fallback witness notes

## 5. VALIDATION CRITERIA

- [ ] Current stage is explicit and queryable.
- [ ] Gate-level pass/fail state is machine-readable.
- [ ] Fallback and blockers are visible.
- [ ] Manifest linkage is optional but supported.
- [ ] Manual continuity remains distinct from automation posture.
