# V59 Mission Dispatch and Model Route View Model Lock

```yaml
version: V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL
status: A3_UI_RUNTIME_VIEW_MODEL
production_authority: false
live_dispatch_authority: false
external_model_dispatch_authority: false
credential_authority: false
purpose:
  - project ION/JOC mission dispatch decisions into the cockpit
  - make model/resource routing reasons visible before execution
  - separate route preview from live dispatch
  - expose cost, latency, capability, fallback, and blocked-capability boundaries
predecessors:
  - V57_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL
  - V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL
```

V59 binds the Cognitive Explorer route to the next cockpit question: **where does this context go, through what compute ring, under what cost/quality/latency policy, and with which authority boundary?**

This lock does not authorize live browser automation, direct API calls, credential use, model dispatch, source-summary rewrite, canonical graph write, or unrestricted agent activation. It creates a view-model receipt only.

The lawful chain is:

```text
operator intent
→ V58 context route preview
→ V59 mission dispatch route preview
→ human/supervised approval boundary
→ later live driver execution if separately authorized
```

The branch remains non-production-authoritative.
