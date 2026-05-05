# Model Call Receipt Protocol


**Authority:** A3 Steward implementation candidate  
**Production authority:** false  
**Live provider calls authorized:** false  
**Provider credentials authorized:** false

This protocol belongs to the API Provider Orchestration and Model Economics lane. It is a planning/runtime-policy surface only until later routed through deterministic tests, dry-run provider adapters, receipts, and Steward review.

Core law:

> ION must not merely call models. ION must govern model selection as an economic, epistemic, temporal, and evidentiary act.

The scheduler must not call providers directly. Model calls must pass through typed intent, routing, budget/rate governance, adapter normalization, and model-call receipt logic.


## V56 scope

Defines the future model-call receipt as proof of route, cost/tokens/latency if known, retry/backoff state, result status, and claim boundary. V59 should implement the receipt surface.

## Forbidden in V56

- live provider API calls
- provider credential loading
- production model-routing authority
- scheduler-to-provider direct dispatch
- unreceipted model outputs
- exact pricing claims as current truth

## Required later integration

The later implementation lane must preserve organ separation:

```text
Scheduler -> work classification -> call intent -> model router -> budget governor -> API rate governor -> scheduler lane placement -> provider adapter -> model call receipt -> front-stage / repair / artifact path
```

