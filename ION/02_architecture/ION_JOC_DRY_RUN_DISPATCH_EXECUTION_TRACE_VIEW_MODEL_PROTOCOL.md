# ION/JOC Dry-Run Dispatch Execution Trace View Model Protocol

## Status

```yaml
version: V63_DRY_RUN_DISPATCH_EXECUTION_TRACE_VIEW_MODEL
authority_scope: DRY_RUN_DISPATCH_TRACE_VIEW_MODEL_RECEIPT_ONLY
production_authority: false
live_dispatch_claim: false
```

## Purpose

This protocol defines the non-executing view model that sits between operator approval and any future live dispatch. It turns the V62 dry-run handoff into a cockpit-visible execution trace showing what would happen if a future authority branch allowed dispatch.

## Required Trace Phases

```text
VALIDATE_OPERATOR_HANDOFF
RECHECK_GOVERNORS
COMPILE_CONTEXT_PREVIEW
BUILD_PROVIDER_ADAPTER_NOOP
SIMULATE_PROMPT_INJECTION
SIMULATE_RESPONSE_WAIT
SIMULATE_EXTRACTION_RECEIPT
EMIT_TRACE_RECEIPT
```

## Required UI Surfaces

```text
DRY_RUN_EXECUTION_TRACE
PROVIDER_ADAPTER_NOOP_LANE
CONTEXT_INJECTION_PREVIEW
GOVERNOR_RECHECK_SNAPSHOT
TIMELINE_EVENT_RAIL
NON_EXECUTION_BOUNDARY_STRIP
OPERATOR_HANDOFF_LINK
RECEIPT_PREVIEW
```

## Non-Execution Law

Every trace step must declare:

```yaml
live_effect: false
network_call: false
credential_touch: false
browser_mutation: false
external_model_call: false
```

If any step violates this, the trace is invalid and must be blocked.

## Future Boundary

A later branch may introduce live dispatch authority, but only after separate provider-driver gating, governor rechecks, credential boundaries, operator confirmation semantics, and execution receipts. V63 intentionally stops before that line.
