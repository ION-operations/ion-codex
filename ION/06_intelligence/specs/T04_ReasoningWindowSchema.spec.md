---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-05T09:40:00-04:00
status: DRAFT
task: T04
depends_on: [T03]
goal: Define the ReasoningWindowSchema — the governed reasoning chamber an agent uses before and after one bounded step
connections:
  - ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md
  - ION/02_architecture/AGENT_REASONING_PROTOCOL.md
  - ION/07_templates/reports/REASONING_JOURNAL.md
---

# ReasoningWindowSchema — Governed Reasoning Chamber

## 1. PURPOSE

A ContextPackage tells an agent what it may see.
A ReasoningWindow tells an agent how it must reason over that bounded visibility before and after one step.

The ReasoningWindow exists to make agent reasoning inspectable, anti-drift, and continuity-safe.
It is the formal chamber for:

- authority interpretation,
- template / protocol interpretation,
- confidence / drift journaling,
- issue detection,
- and next-step proposal without silent self-authorization.

## 2. SCHEMA DEFINITION

```yaml
ReasoningWindowSchema:
  schema_version: "1.0"

  ReasoningWindow:
    reasoning_window_id: string
    reasoning_version: string
    created_at: string

    role: string
    work_unit_id: string
    context_package_id: string | null
    governing_artifact: string

    identity_and_authority:
      boot_ref: string
      structural_identity: string
      authority_bounds: list[string]
      forbidden_silent_decisions: list[string]

    active_inputs:
      template_ref: string
      binding_ref: string | null
      protocol_refs: list[string]
      doctrine_refs: list[string]
      target_refs: list[string]
      dependency_refs: list[string]
      prior_finding_refs: list[string]

    timeline_witness:
      recent_receipt_refs: list[string]
      recent_trace_refs: list[string]
      unresolved_issue_refs: list[string]
      recent_route_refs: list[string]

    candidate_routes:
      manifests: list[CandidateRoute]

    preflight:
      bounded_objective: string
      in_scope: list[string]
      out_of_scope: list[string]
      load_bearing_grounding: list[string]
      template_obligations: list[string]
      protocol_constraints: list[string]
      issues_seen: list[ReasoningIssue]
      confidence: string
      semantic_novelty: string
      recursion_risk: string
      grounding_sufficiency: string
      new_abstraction_family: boolean
      new_runtime_family: boolean
      independent_consumer_exists: boolean | null
      recommendation: string

    postflight:
      actual_changes: list[string]
      verification_run: list[string]
      unresolved_risks: list[string]
      issues_emitted: list[string]
      next_step_proposal: string
      next_step_grounding: list[string]
      authorization_required: list[string]

  CandidateRoute:
    route_id: string
    description: string
    conditions_to_adopt: list[string]
    status: HYPOTHETICAL

  ReasoningIssue:
    class: string
    summary: string
    severity: LOW | MEDIUM | HIGH
    affects_self: boolean
    affects_other: boolean
    evidence_refs: list[string]
```

## 3. RULES

- Candidate routes are hypothetical only.
- The ReasoningWindow may summarize future route options, but it may not record them as active continuity unless a lawful transition adopts them.
- A low-confidence or high-recursion preflight should recommend stop or escalate rather than silent continuation.
- If `new_runtime_family` is true and `independent_consumer_exists` is false or unknown, the step should not auto-continue.

## 4. IDE/MANUAL MODE ADAPTATION

In current IDE/manual mode, the ReasoningWindow is explicit rather than daemon-compiled.
Its live artifact is a `REASONING_JOURNAL` plus any short issue signals emitted alongside it.

## 5. VALIDATION CRITERIA

- [ ] The schema distinguishes active, witnessed, and hypothetical route state.
- [ ] The schema forces explicit authority and forbidden-decision handling.
- [ ] Confidence / novelty / recursion are first-class fields.
- [ ] Issue reporting can target self or other lanes.
- [ ] Next-step proposal does not imply self-authorization.
