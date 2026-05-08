# ION/JOC Dispatch Authorization and Governor Verdict View Model Protocol

## Status

```yaml
protocol_id: ION_JOC_DISPATCH_AUTHORIZATION_GOVERNOR_VERDICT_VIEW_MODEL_PROTOCOL
branch: V61_DISPATCH_AUTHORIZATION_GOVERNOR_VERDICT_VIEW_MODEL
authority_scope: DISPATCH_AUTHORIZATION_VIEW_MODEL_RECEIPT_ONLY
production_authority: false
live_dispatch_claim: false
```

## Purpose

This protocol defines the UI/runtime projection layer that binds a mission route preview to the model-economics, budget, and API-rate governors before the cockpit can present that route as eligible for operator approval.

It exists because ION/JOC now has two important but previously separate surfaces:

1. model/budget/API governance surfaces from the economics branch;
2. mission route preview and model-route UI surfaces from the cockpit branch.

V61 reconciles them.

## Governing Rule

```text
A visible dispatch route is not dispatch authority.
```

The cockpit may show a route preview only as one of these states:

```text
AUTHORIZATION_PREVIEW_READY
NEEDS_SUPERVISED_APPROVAL
BLOCKED_BY_BUDGET
BLOCKED_BY_API_RATE_LIMIT
BLOCKED_BY_FORBIDDEN_CAPABILITY
BLOCKED_BY_MISSING_GOVERNOR_EVIDENCE
BLOCKED_BY_CLAIM_REVIEW
BLOCKED_BY_PRODUCTION_BOUNDARY
```

## Required Inputs

A V61 authorization projection requires:

```yaml
required_inputs:
  mission_id: required
  route_preview_id: required
  selected_target: required
  compute_ring: required
  access_method: required
  task_class: required
  claim_lane: required
  estimated_cost_usd: required
  estimated_latency_band: required
  quality_band: required
  budget_governor_verdict: required
  api_rate_governor_verdict: required
  capability_policy_verdict: required
  evidence_refs: required_non_empty
```

## UI Obligations

The cockpit must render:

```text
mission id
route preview id
selected target
primary/fallback distinction
budget verdict
API-rate verdict
capability verdict
approval mode
blocked capabilities
operator-visible reason
required next action
receipt preview
non-production boundary
```

## Forbidden Inference

The UI must not imply:

```text
live dispatch occurred
external provider was called
browser was mutated
API budget was spent
cloud compute was launched
credential vault was accessed
production authority exists
```

## Approval Modes

```text
AUTO_FORBIDDEN
SUPERVISED_REQUIRED
MANUAL_ONLY
VIEW_ONLY_BLOCKED
```

V61 defaults to supervised or blocked lanes. It does not create full-auto dispatch authority.
