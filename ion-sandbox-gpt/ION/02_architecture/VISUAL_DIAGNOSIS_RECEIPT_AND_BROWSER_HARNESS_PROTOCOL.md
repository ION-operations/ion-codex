# Visual Diagnosis Receipt and Browser Harness Protocol

## Purpose

V45 converts the Visual Agent line from isolated observation packets into bounded diagnosis receipts and a planned browser/screenshot/DOM harness architecture.

The purpose is to let ION treat rendered truth as receipted continuity state while preserving a strict authority boundary: observe, diagnose, report, and recommend only.

## Doctrine

Rendered behavior is part of truth. A source tree can compile while the rendered product is visually wrong, confusing, inaccessible, or semantically misleading. ION therefore needs a visual receipt layer that can record what was observed, what was diagnosed, what evidence supports the diagnosis, what action is recommended, and what authority boundary applies.

## Receipt chain

A V45 visual diagnosis receipt may bind:

1. one or more V44 visual observation packets;
2. screenshot references;
3. DOM references;
4. viewport state;
5. before/after references;
6. issue findings;
7. recommended implementation-agent actions;
8. browser harness plan status;
9. human/steward review requirements;
10. forbidden action flags.

## Browser harness plan

The browser harness remains a plan surface in V45. It may describe local-dev screenshot, DOM snapshot, accessibility-tree, console-summary, and before/after capture workflows. It does not execute arbitrary browser control.

## Authority boundary

The Visual Agent may observe, diagnose, compare, explain, and request patches. It may not perform unrestricted navigation, persistent DOM mutation, credential-sensitive action, purchase/submission, deletion, or production action without future explicit authority and Steward/VZ review.

## User-facing representation

Persona may truthfully say that a visual diagnosis receipt was produced when Relay can supply the receipt and Steward/VZ permits the claim class. Persona must not claim the visual agent performed actions beyond the receipt's authority scope.

## Next step

The expected next step is V46: a local visual harness prototype that can operate against authorized local/dev previews using screenshot/DOM capture only.
