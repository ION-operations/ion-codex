---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-07T23:31:00-04:00
status: DRAFT
task: T10
depends_on: [T08, T09]
goal: Define the CrossModelAuditCalibration schema for comparing predicted confidence and review verdicts across builder, auditor, and escalation lanes so automation and thresholding can be calibrated against witnessed outcomes
connections:
  - ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md
  - ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md
  - ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md
  - ION/06_intelligence/specs/T09_ManifestRouteStateSchema.spec.md
  - ION/07_templates/confidence/CSR.md
lineage:
  - Project-Gemini/services/vif/calibration.py
  - Project-Gemini/services/vif/cross_model_confidence_calibrator.py
  - multi-model audit strategy referenced in production audit backlog
---

# CrossModelAuditCalibration — Confidence and Review Outcome Calibration

## 1. PURPOSE

A CSR makes confidence and concern legible.
A calibration surface asks whether those confidence claims were actually trustworthy over time,
especially when different model lanes or review roles disagree.

This schema exists to support:
- builder / auditor / reviewer comparison,
- confidence-to-outcome calibration,
- disagreement analysis,
- thresholding inputs for future runtime gates,
- and bounded escalation decisions without pretending a single model's self-report is enough.

## 2. SCHEMA DEFINITION

```yaml
CrossModelAuditCalibrationSchema:
  schema_version: "1.0"

  CalibrationRun:
    calibration_run_id: string
    created_at: string
    subject_ref: string
    scope_type: FILE | PATCH | PACKET | WORK_UNIT | ROUTE | REVIEW_CASE

    participants:
      builder: ModelAssessment | null
      auditor: ModelAssessment | null
      reviewer: ModelAssessment | null
      adjudicator: ModelAssessment | null

    observed_outcome:
      outcome_status: CORRECT | PARTIAL | INCORRECT | UNRESOLVED
      outcome_refs: list[string]
      adjudication_summary: string

    comparison:
      agreement_class: STRONG_AGREEMENT | WEAK_AGREEMENT | DIVERGENCE | DIRECT_CONTRADICTION
      dominant_failure_mode: OVERCONFIDENCE | UNDERCONFIDENCE | EVIDENCE_GAP | ROUTE_DRIFT | AUTHORITY_OVERREACH | NONE
      escalation_recommended: boolean

    calibration_metrics:
      qualitative_calibration: CALIBRATED | UNDERCALIBRATED | OVERCALIBRATED | INSUFFICIENT_DATA
      confidence_gap_band: LOW | MEDIUM | HIGH
      ece_optional: float | null
      mce_optional: float | null
      outcome_sample_size: integer

    threshold_recommendation:
      promotion_action: HOLD | ALLOW_BOUNDED_PROMOTION | REQUIRE_REVIEW | ROLL_BACK
      reasons: list[string]
      next_checks: list[string]

  ModelAssessment:
    actor_id: string
    actor_role: BUILDER | AUDITOR | REVIEWER | ADJUDICATOR
    model_family: string
    assessment_ref: string | null
    predicted_confidence_band: LOW | MEDIUM | HIGH
    predicted_direction: CLEAR | UNCERTAIN | CONFLICTED
    verdict: PASS | PASS_WITH_CONCERNS | FAIL | ESCALATE | UNKNOWN
    concerns: list[string]
```

## 3. RULES

- Calibration is comparative and witnessed; it is not a self-certification ritual.
- Numerical metrics such as `ece_optional` and `mce_optional` are allowed but not required for every case.
- A single calibration run may end `UNRESOLVED` if no trustworthy outcome witness exists yet.
- Direct contradiction between builder and auditor should bias toward review or hold, not silent promotion.
- Threshold recommendations are advisory until a future governed threshold module adopts them lawfully.

## 4. IDE/MANUAL MODE ADAPTATION

In the current live root, calibration may be assembled from:
- CSR or reasoning-journal assessments,
- audit reports,
- review signals,
- packet outcomes,
- and human/operator adjudication.

This is sufficient for first-pass calibration tracking.
A future service may compute rolling ECE/MCE style summaries once stable consumers exist.

## 5. VALIDATION CRITERIA

- [ ] The schema can compare at least builder, auditor, and reviewer/adjudicator lanes.
- [ ] Confidence claims are separable from actual outcomes.
- [ ] Disagreement class and dominant failure mode are explicit.
- [ ] Numerical calibration metrics remain optional rather than falsely required.
- [ ] The output can inform future thresholding without itself acting as threshold enforcement.
