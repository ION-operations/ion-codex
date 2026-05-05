# V61 Dispatch Authorization Governor Verdict View Model Lock

```yaml
branch_id: V61_DISPATCH_AUTHORIZATION_GOVERNOR_VERDICT_VIEW_MODEL
base_line: V60_BRANCH_CONSOLIDATION_UI_MODEL_GOVERNOR_BINDING
purpose:
  - bind V59 mission route previews to V56-V58 model economics, budget, and API-rate governor evidence
  - produce an operator-visible dispatch authorization view model
  - prevent visible route preview from being confused with permission to dispatch
production_authority: false
live_dispatch_claim: false
external_model_call_claim: false
credential_access_claim: false
paid_cloud_launch_claim: false
```

V61 is a cockpit-binding branch. It does not execute missions, call external providers, mutate browser sessions, spend API budget, or launch cloud compute. It creates the governed view model that lets ION/JOC display whether a proposed mission route is clear for supervised approval, blocked by budget, blocked by API/rate limits, blocked by forbidden capability, or waiting on claim/evidence review.

Core settlement:

```text
V59 shows where a mission could go.
V61 shows whether that route is governable enough to request approval.
```

A dispatch route is not operationally valid merely because the UI can display it. The route must be bound to budget posture, API-rate posture, capability policy, claim lane, approval mode, evidence references, and repair obligations.
