# Visual Fixture Runner Local Sandbox Review Protocol

Version: V50_VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW  
Authority: A3 visual-agent sandbox/security review gate  
Production status: NOT_PRODUCTION_AUTHORIZED

## Purpose

V50 introduces a mandatory sandbox/security review receipt before the Visual Agent line can move from plan-only fixture receipts toward any executable local browser or visual fixture harness.

The protocol continues the Visual Agent sequence:

1. V44 records visual observations.
2. V45 records visual diagnoses and browser harness planning.
3. V46 records local/dev supplied artifact capture receipts.
4. V47 defines a local browser capture adapter stub without execution.
5. V48 records before/after visual verification.
6. V49 records repeatable visual regression fixture suite plans and pre-captured outcomes.
7. V50 reviews whether future fixture execution can even be discussed safely under local/dev sandbox constraints.

## Principle

Sandbox review must precede sandbox execution.

ION shall not add browser execution authority, DOM injection authority, credential-sensitive action, network side effects, destructive action, form submission, purchase/submission action, persistent DOM mutation, or production visual automation until the relevant local sandbox constraints are explicitly reviewed and receipted.

## Review verdicts

Permitted V50 verdicts:

- `SANDBOX_REVIEW_PASSED_PLAN_ONLY`
- `SANDBOX_REVIEW_NEEDS_REMEDIATION`
- `SANDBOX_REVIEW_BLOCKED_BY_STEWARD`
- `SANDBOX_REVIEW_REJECTED_FOR_FORBIDDEN_CAPABILITY`

Only `SANDBOX_REVIEW_PASSED_PLAN_ONLY` is a clean pass, and even that does not authorize browser execution. It only authorizes a later sandbox specification branch.

## User-facing implication

Persona may say that ION has reviewed a local visual fixture runner plan for sandbox readiness only when a V50 receipt exists. Persona must not say that V50 ran a browser, controlled a computer, mutated a DOM, or performed production visual automation.
