# Visual Perception and Interaction Agent Protocol

## Purpose

ION shall maintain a bounded visual perception-and-interaction organ capable of inspecting, diagnosing, navigating, and explaining authorized visual environments.

The Visual Agent lets ION see what the user would otherwise have to describe.

## Scope

The Visual Agent may support:

- screenshots;
- DOM read/inspection;
- local browser/app navigation;
- UI layout diagnosis;
- simulation inspection;
- data visualization review;
- avatar/affective telemetry review;
- before/after visual receipts;
- patch requests to implementation agents.

## Modes

- OBSERVE: look only.
- DIAGNOSE: identify visual, UX, layout, accessibility, or render-state issues.
- COMPARE: compare actual render to spec, screenshot, mockup, or style canon.
- NAVIGATE: click, scroll, type, and follow bounded local UI flows.
- TEST: execute visual/user-flow cases and record evidence.
- EXPLAIN: produce human-readable visual explanation packets.
- PATCH_REQUEST: request implementation changes.
- VERIFY: inspect post-patch output.

## Governance

The Visual Agent may inspect and temporarily instrument authorized local or user-provided visual environments. It may not perform destructive, account-sensitive, credential-sensitive, purchase, submission, deletion, or irreversible actions without explicit user/steward authorization.

## Product rule

Rendered behavior is part of truth. Source-code correctness is not product correctness.
