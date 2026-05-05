# ION Branch Consolidation: UI + Model-Governor Binding Protocol

## Consolidation thesis

ION/JOC mission dispatch cannot be only a UI object, and model-economics governance cannot remain invisible backend logic.

The correct merged architecture is:

```text
Cognitive Explorer selects visible context route
→ Mission Dispatch Router previews target lanes
→ Model Router selects dry-run provider/model candidate
→ Budget Governor classifies economic permission
→ API Rate Governor classifies capacity/backoff permission
→ Front-Stage Council classifies user-facing claims
→ only then may a future live dispatch adapter be considered
```

## Parallel branch namespace settlement

Duplicate V55-V58 labels are retained as historical branch-lane labels:

```text
budget/economics lane:
  V56 model economics registry skeletons
  V57 model router and cost-quality routing
  V58 budget and API-rate governors

ui/cockpit lane:
  V55 visual closure graph projection and UI work surface
  V56 JOC cockpit shell component contracts
  V57 Reactive OS Stream
  V58 Cognitive Explorer/context-route view model
  V59 mission dispatch/model route view model
```

Future docs should not describe one lane as replacing the other. V60 binds them.

## Required guarantees

A valid V60 receipt must assert both branch families are present, the UI mission dispatch remains route-preview only, future live dispatch is blocked pending governor chain, model router cannot bypass budget/rate checks, cockpit surfaces blocked capabilities, and production authority remains false.

## Recommended successor

`V61_DRY_RUN_MODEL_CALL_RECEIPTS_AND_GOVERNED_DISPATCH_PREVIEW`.
