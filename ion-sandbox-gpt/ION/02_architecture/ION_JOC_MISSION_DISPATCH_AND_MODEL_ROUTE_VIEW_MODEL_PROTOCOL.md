# ION/JOC Mission Dispatch and Model Route View Model Protocol

## Purpose

The Mission Dispatch and Model Route View Model makes routing visible before any AI provider, browser session, CLI tool, API, cloud VM, local model, or automation driver is touched.

It renders a cockpit-safe route preview for missions produced from ION maintained-work-surface state.

## Required view surfaces

```text
MISSION_DISPATCH_PANEL
MODEL_ROUTE_MATRIX
COMPUTE_RING_SELECTOR
COST_LATENCY_QUALITY_BAND
CAPABILITY_MATCH_PANEL
FALLBACK_CHAIN_PANEL
HUMAN_APPROVAL_GATE
DISPATCH_RECEIPT_PREVIEW
```

## Required compute rings

```text
RING_1_BROWSER_SESSION
RING_2_API_CLI_LOCAL
RING_3_CLOUD_COMPUTE
```

## Required route factors

```text
TASK_CLASS
CONTEXT_SIZE
QUALITY_REQUIREMENT
LATENCY_REQUIREMENT
COST_SENSITIVITY
CAPABILITY_MATCH
RISK_CLASS
FALLBACK_AVAILABILITY
```

## Allowed status values

```text
ROUTE_PREVIEW_READY
BLOCKED_NO_TARGETS
BLOCKED_MISSING_REQUIRED_RING
BLOCKED_MISSING_ROUTE_FACTOR
BLOCKED_UNAPPROVED_EXTERNAL_DISPATCH
BLOCKED_FORBIDDEN_CAPABILITY
```

## Authority boundaries

V59 may show:

```text
route recommendations
primary target
fallback chain
cost/latency/quality estimates
capability reasoning
approval requirement
blocked capabilities
receipt preview
```

V59 may not perform:

```text
external model dispatch
browser session mutation
credential access
form submission
paid cloud launch
source summary rewrite
canonical graph write
unrestricted agent activation
production release approval
```

## Cockpit rendering rule

A mission route is visible only when it preserves the distinction between **preview**, **supervised approval**, and **execution**. A route panel that visually implies live dispatch authority before such authority exists is invalid.
