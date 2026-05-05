# Visual Run Receipt to Diagnosis Binding Protocol

## Purpose

The Visual Run Receipt to Diagnosis Binding Protocol closes the first Visual Agent evidence loop. It requires a visual diagnosis lineage, a before/after verification lineage, and a fixture-bound local browser execution run lineage before ION may describe a visual issue as diagnostically closed.

## Core rule

A visual issue is not closed merely because an implementation agent changed code or a screenshot appears different. It is closed only when diagnosis, before/after verification, and a gated local run receipt agree that the issue is resolved without persistent findings, regressions, forbidden events, or Steward/VZ blocks.

## Inputs

- V44 visual observation packet identifiers
- V45 visual diagnosis receipt identifiers
- V48 before/after verification identifiers
- V53 local browser execution run receipt identifiers
- evidence references including screenshots, capture artifacts, run references, or DOM/capture references
- resolved, persistent, and regression findings
- Steward/VZ closure gate status

## Verdicts

- VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE
- VISUAL_ISSUE_CLOSURE_NEEDS_REVIEW
- VISUAL_ISSUE_CLOSURE_NEEDS_FOLLOWUP
- VISUAL_ISSUE_CLOSURE_REGRESSION_REQUIRES_REVIEW
- VISUAL_ISSUE_CLOSURE_REJECTED_FOR_FORBIDDEN_EVENT
- VISUAL_ISSUE_CLOSURE_BLOCKED_BY_STEWARD

## Non-authorities

This protocol does not authorize unrestricted browser control, external network access, credential/session import, account operation, destructive action, form submission, purchase/submission action, persistent DOM mutation, production visual automation, production readiness, or production authority.
