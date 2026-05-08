---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-07T22:27:00-04:00
status: DRAFT
task: T08
goal: Define the ConfidenceAndDriftSchema — the live schema target for operator-facing confidence, concern, and calibration reporting
lineage:
  - SOS/07_templates/confidence/CSR.md
  - SOS-OPUS/07_templates/confidence/CSR.md
  - ION-BUILD/context/templates/confidence/CSR.md
  - ion_production_audit/manifest_confidence_reintegration_audit.md
connections:
  - ION/02_architecture/AGENT_REASONING_PROTOCOL.md
  - ION/07_templates/confidence/CSR.md
  - ION/07_templates/reports/REASONING_JOURNAL.md
---

# ConfidenceAndDriftSchema — Operator-Facing Confidence and Pressure Surface

## 1. PURPOSE

The live root already has a reasoning-window protocol.
What it still lacks is a stronger outward-facing surface for confidence, drift pressure, and calibration.

This schema exists to formalize that surface.
It is not a replacement for the `REASONING_JOURNAL`.
It is the companion artifact that makes direction, execution posture, concerns, and calibration legible to the wider organism.

## 2. RELATION TO THE REASONING JOURNAL

- `REASONING_JOURNAL` = governed internal reasoning chamber for one bounded step
- `CSR` / ConfidenceAndDriftSchema = outward-facing confidence, concern, and calibration witness

A journal may be richer and more procedural.
A CSR should be easier to scan, compare, route, and pressure.

## 3. SCHEMA DEFINITION

```yaml
ConfidenceAndDriftSchema:
  schema_version: "1.0"

  ConfidenceReport:
    report_id: string
    created_at: string
    role: string
    responding_to: string
    mode: FULL | MINI

    direction:
      narrative: string
      summary: CLEAR | UNCERTAIN | CONFLICTED
      evidence_refs: list[string]

    execution:
      narrative: string
      summary: CAPABLE | PARTIAL | UNABLE
      evidence_refs: list[string]

    intent:
      narrative: string
      summary: DEFINED | VAGUE | UNDEFINED
      evidence_refs: list[string]

    concerns:
      narrative: string
      summary: NONE | MANAGEABLE | BLOCKING
      items: list[ConcernItem]

    context_gaps:
      narrative: string
      summary: COMPLETE | GAPS_RESEARCHABLE | GAPS_NEED_USER
      missing_items: list[string]
      proposed_next_sources: list[string]

    calibration:
      narrative: string
      summary: CALIBRATED | UNTESTED | HISTORICALLY_OVERCONFIDENT
      comparison_refs: list[string]

    drift_assessment:
      semantic_drift_risk: LOW | MEDIUM | HIGH
      recursion_risk: LOW | MEDIUM | HIGH
      authority_overreach_risk: LOW | MEDIUM | HIGH
      notes: string

    recommendation:
      action: CONTINUE | NARROW_AND_CONTINUE | RESEARCH_FIRST | ASK_USER | ESCALATE | STOP
      reasons: list[string]
      requires_external_authority: list[string]

  ConcernItem:
    concern: string
    severity: LOW | MEDIUM | HIGH | BLOCKING
    mitigation: string | null
```

## 4. RULES

- The schema uses qualitative bands rather than fake decimal certainty.
- A favorable execution summary does not itself authorize a wider lane.
- `ASK_USER` and `ESCALATE` are first-class recommendations, not failure states.
- Drift assessment must remain distinct from execution confidence.

## 5. VALIDATION CRITERIA

- [ ] The schema distinguishes internal reasoning from outward confidence reporting.
- [ ] Concerns and context gaps can pressure routing explicitly.
- [ ] Calibration is a first-class field rather than an afterthought.
- [ ] Drift risk is recorded separately from execution capability.
- [ ] Recommendation does not imply silent self-ratification.
