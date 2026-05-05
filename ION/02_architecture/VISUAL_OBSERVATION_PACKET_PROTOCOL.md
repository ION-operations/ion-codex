# Visual Observation Packet Protocol

## Purpose

ION must be able to inspect rendered truth. Source-code correctness is not product
correctness. Rendered behavior, layout, interaction state, avatar expression, and
simulation output must be observable and receiptable.

## Scope

V44 grants only observe, diagnose, compare, explain, patch-request, and verify packet
formation authority. It does not grant unrestricted computer control.

## Packet duties

A visual observation packet must record target, mode, viewport, visual/DOM evidence,
findings, severity, confidence, recommended actions, and authority limits.

## Forbidden actions

- unrestricted_computer_control
- credential_sensitive_action
- destructive_action
- purchase_or_submission
- persistent_dom_mutation_without_authority
- production_authority

