# Visual Regression Fixture Runner Plan Protocol

Version: V49_VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN  
Authority: A3 Visual Agent planning/reporting protocol  
Production status: NOT_PRODUCTION_AUTHORIZED

## Purpose

The Visual Regression Fixture Runner Plan gives ION a repeatable way to describe, load, classify, and receipt visual regression fixture suites without granting the Visual Agent live browser-control authority.

This protocol continues the Visual Agent line:

1. V44 visual observation packets establish what was seen.
2. V45 visual diagnosis receipts establish what the observation means.
3. V46 local visual harness receipts bind local/dev artifacts into evidence.
4. V47 browser capture adapter stubs define an adapter interface without execution.
5. V48 before/after verification receipts classify visual repair evidence.
6. V49 visual regression fixture runner receipts make repeated fixture checks auditable.

## Principle

Repeatability must arrive before autonomy.

The Visual Agent shall not be granted stronger browser or computer-control authority until ION can first describe repeatable visual fixtures, classify expected versus actual outcomes, and leave a receipt for every suite run or planned run.

## Fixture suite

A fixture suite is a bounded local/dev artifact that may specify:

- suite id,
- target/project surface,
- fixture cases,
- expected visual verdicts,
- before/after evidence references,
- related V48 before/after verification receipt ids,
- required Steward/VZ review flags,
- tags and implementation hints.

## Runner modes

Permitted V49 modes:

- `STATIC_ARTIFACT_REFERENCE_CHECK`
- `PRECAPTURED_BEFORE_AFTER_VERIFICATION`
- `HARNESS_PLAN_ONLY`
- `STEWARD_REVIEW_REQUIRED`

Forbidden in V49:

- live browser execution,
- unrestricted screenshot capture,
- network browsing,
- credential-sensitive action,
- form submission,
- purchase or destructive action,
- persistent DOM mutation,
- production visual automation.

## Receipt requirements

Every fixture runner output must include:

- suite id,
- fixture count,
- per-fixture result,
- expected and actual verdicts,
- pass/fail/review/blocked counts,
- overall suite verdict,
- authority scope,
- forbidden capability flags,
- recommended next actions.

## User-facing implication

Persona may truthfully report that a visual regression suite is planned, passed, failed, blocked, or needs review only from a V49 receipt or stronger successor authority. Persona must not imply that V49 actually controlled a browser or performed live visual automation.
