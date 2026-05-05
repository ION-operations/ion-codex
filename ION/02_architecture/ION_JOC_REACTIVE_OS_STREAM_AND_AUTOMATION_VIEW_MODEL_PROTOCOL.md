# ION/JOC Reactive OS Stream and Automation View Model Protocol

## Purpose

This protocol defines the V57 contract for rendering ION automation loops inside the JOC cockpit. It extends the V56 component-contract shell by requiring every visible automation stream event to carry loop identity, phase, status, claim lane, evidence references, rendered surface, authority scope, and repair/blocked-capability state.

## Governing principle

```text
Automation is not visible because a log line exists. Automation is visible when the UI can show what loop ran, what phase it reached, what evidence supports it, what claim class it occupies, what action is blocked, and what repair remains.
```

## Required loops

```text
VISUAL_ISSUE_CLOSURE_LOOP
MISSION_DISPATCH_LOOP
SESSION_HEALTH_LOOP
CONTEXT_PROJECTION_LOOP
CONVERSATIONAL_REPAIR_LOOP
MODEL_COST_QUALITY_LOOP
```

## Required event fields

Each event must provide:

```yaml
event_id: stable identifier
occurred_at: ISO-8601 or HH:MM:SS display time
loop_id: one required automation loop
phase: loop-local phase name
status: OK | WATCH | BLOCKED | REPAIR
claim_lane: C0 | C1 | C2 | C3 | C4 | C5
rendered_surface: cockpit surface receiving the event
authority_scope: bounded scope for the event
evidence_refs: non-empty list unless the event is a purely blocked warning
repair_required: boolean
blocked_capabilities: list of forbidden capabilities implicated by the event
detail: short operator-readable detail
```

## UI projection requirements

The V57 cockpit must render:

```text
1. loop coverage summary
2. event stream grouped or filterable by loop
3. status class per event
4. evidence references per event
5. blocked capability rail
6. repair queue count
7. authority boundary statement
8. no production authority claim
```

## Forbidden capabilities

The following remain false in V57:

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

## Non-authority boundary

V57 may validate and render an automation view model. It may not claim the UI is live in production, may not operate browser sessions, may not submit forms, and may not mutate accounts or credentials.
