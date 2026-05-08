# Budget and API Rate Governors Protocol

**Version:** V58_BUDGET_AND_API_RATE_GOVERNORS  
**Authority:** A3 Steward model-economics candidate surface  
**Production authority:** false

## Purpose

ION must separate model selection from economic and temporal permission.

The router decides which provider/model/lane is the best candidate under work-class policy. The budget governor decides whether the candidate should run economically. The API rate governor decides whether the provider/model can be dispatched now under capacity and backoff state.

## Mandatory separation

```text
Scheduler decides what work should move and when.
Router decides who should carry it.
Budget governor decides whether the selected route is economically allowed.
API rate governor decides whether the selected provider/model can be called now.
Provider adapter executes only after explicit future authorization.
Model call receipt proves what happened.
```

## Budget governor decisions

```text
allow
require_approval
downgrade_model
batch_route
block
```

Budget decisions are based on estimated route cost, workflow budget policy, premium posture, user-visible value, and hard caps. V58 uses deterministic inputs only and treats unknown production budgets as non-authoritative placeholders.

## API rate governor decisions

```text
allow
queue
reroute
batch
throttle
block
```

Rate decisions are based on provider/model capacity state, safe parallelism, retry-after/backoff state, and estimated token pressure. V58 uses registry/intent/call-site supplied state only. It does not query providers.

## Forbidden claims

V58 does not authorize live provider calls, credentials, production rate enforcement, scheduler direct provider calls, automatic provider fallback, or model output as user-facing truth.

