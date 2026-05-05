# Visual Closure Graph Projection and UI Work Surface Protocol

## Purpose

This protocol binds the real V54 visual-run closure loop to the emerging ION/JOC operator interface. It defines how ION runtime state should be projected into UI regions without flattening evidence, authority, repair obligations, or automation status into ordinary dashboard decoration.

## Core thesis

ION's UI is a maintained-work-surface renderer. It must display work state as governed state: claims, receipts, visual evidence, local runs, diagnosis bindings, model routes, session health, repair obligations, and automation events all remain inspectable.

## Projection chain

```text
V44 visual observation packet
-> V45 visual diagnosis receipt
-> V48 before/after visual verification receipt
-> V53 local browser execution run receipt
-> V54 visual run-to-diagnosis binding receipt
-> V55 UI work-surface projection receipt
-> JOC/ION operator cockpit rendering
```

## Required UI zones

V55 adopts the JOC 5-zone layout as the first ION-compatible cockpit projection:

```text
TOP_BAR                 navigation, command palette, Oracle/Steward state, claim-lane state
LEFT_RAIL               primary mode switcher and work-surface region selector
MAIN_WORK_SURFACE       active project, mission, visual closure, graph, or session surface
RIGHT_INSPECTOR         receipts, evidence, context graph, visual diagnosis, route details
BOTTOM_TIMELINE         logs, agent comms, terminal/output, automation stream, repair queue
```

## Required projection surfaces

The UI must expose at least these surfaces before it can be called ION-native:

```text
Maintained Work Surface Overview
Front-Stage Council / Steward State Strip
Claim and Receipt Rail
Visual Evidence Lens
Mission Dispatch and Model Route Panel
Context Graph / Cognitive Explorer
Reactive OS Stream
Conversational Repair Queue
Browser Session Automation Overlay
Compute and Cost Router
```

## DXL/UI canon constraints

The first UI pass must preserve the DXL matte-black instrument-panel rules:

- no emoji in actual UI controls
- custom inline SVG icons only
- mono labels, dense uppercase instrumentation, and no large casual typography
- panel radii no larger than 2px for instrument panels
- no Material Design color tokens in structural UI
- no purple/blue structural accent drift unless explicitly confined to data visualization
- no placeholder-only panels presented as finished UI
- full-width desktop-first layouts for standard and ultrawide workstations

## Automation loops visible in the UI

The UI must make ION's automations inspectable:

```text
visual_issue_closure_loop:
  observe -> diagnose -> verify_before_after -> run_local_browser_fixture -> bind_closure -> render_receipt

mission_dispatch_loop:
  compose -> package_context -> route_model_or_compute_ring -> dispatch -> monitor -> extract -> synthesize -> route_result -> receipt

session_health_loop:
  detect_session -> inspect_dom_targets -> classify_health -> repair_or_request_login -> log_action

context_projection_loop:
  filesystem_or_artifact_change -> graph/index update -> relevant-context resolution -> visible graph highlight

conversational_repair_loop:
  user_correction -> claim-class movement -> artifact repair obligation -> continuation receipt

model_cost_quality_loop:
  task_class -> risk/classification -> model/compute route -> budget/latency estimate -> evidence return
```

## Non-authorities

The V55 projection surface does not authorize browser automation beyond the permissions already granted by lower protocols. It does not grant credential access, account actions, form submission, external network operations, destructive mutation, production visual automation, or production readiness.

## Acceptance criteria

A V55 projection receipt is valid only when it records the source inputs, required zones, automation loops, DXL constraints, non-authority boundaries, and evidence lineage needed for a UI implementation agent to render ION state without overclaiming it.
