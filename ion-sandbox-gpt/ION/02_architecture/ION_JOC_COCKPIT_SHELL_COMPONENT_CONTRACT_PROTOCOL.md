# ION/JOC Cockpit Shell Component Contract Protocol

## Purpose

This protocol defines the first concrete UI component contract for rendering ION's maintained work surface in a JOC-style cockpit. It bridges V55 projection receipts into implementation-facing React/Electron shell components while preserving ION's authority boundaries.

## Core thesis

The cockpit is not a dashboard placed beside ION. The cockpit is a projection organ. Every primary component must correspond to a governed ION surface: work state, claim state, receipt state, visual evidence state, mission route state, context graph state, automation stream state, repair state, session automation state, or compute/cost route state.

## Required shell regions

```text
TOP_BAR
LEFT_RAIL
MAIN_WORK_SURFACE
RIGHT_INSPECTOR
BOTTOM_TIMELINE
```

These regions inherit the V55 layout zones. A component set missing any one of them is not an ION-native cockpit shell.

## Required component contracts

```text
IonTopBar
IonLeftRail
IonMainWorkSurface
IonRightInspector
IonBottomTimeline
ReceiptRail
VisualEvidenceLens
ReactiveOsStream
MissionRoutePanel
ContextGraphExplorer
ConversationalRepairQueue
BrowserAutomationOverlay
ComputeCostRouter
```

A minimal shell may render some of these as embedded sections rather than separate routes, but each contract must be represented and named.

## Required bindings

Each component must declare:

```text
layout_zone
projection_surfaces
receipts_rendered
automation_loops
claim_lanes
evidence_lanes
forbidden_authorities_preserved
```

## Required UI behavior

The shell must expose:

```text
1. Steward/Front-Stage Council state in the top bar.
2. Primary mode selection in the left rail.
3. Current maintained work surface in the main region.
4. Receipts, evidence, and claim classes in the right inspector.
5. Automation/reaction/repair activity in the bottom timeline.
6. A command-palette mount point.
7. A no-placeholder finished-state rule.
8. DXL matte-black instrument-panel constraints.
```

## DXL constraints

The first ION/JOC shell must preserve:

```text
no emoji in controls
custom inline SVG icons only
mono dense uppercase labels
panel radius <= 2px for instrument panels
no Material Design structural colors
no casual large typography
full-width desktop-first layout
```

## Non-authority boundaries

A component contract may render forbidden capabilities as blocked, unavailable, gated, or requiring Steward/VZ escalation. It may not mark them as authorized.

Forbidden capabilities remain:

```text
production_authority
unrestricted_browser_control
credential_access
external_network_authority
account_operation
destructive_action
form_submission
purchase_or_submission
persistent_dom_mutation
production_visual_automation
```

## Acceptance criteria

A V56 component contract is valid only when it contains all required shell regions, all required component contracts, at least one binding to the V55 visual closure projection lineage, DXL constraints, and explicit false values for all forbidden authorities.
