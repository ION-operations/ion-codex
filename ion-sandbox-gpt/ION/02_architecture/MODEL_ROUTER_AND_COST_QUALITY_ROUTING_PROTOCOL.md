# Model Router and Cost-Quality Routing Protocol

**Version introduced:** V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING  
**Authority scope:** A3_STEWARD_MODEL_ROUTING_CANDIDATE  
**Production authority:** false  
**Live provider calls authorized:** false  
**Provider credentials authorized:** false

## Purpose

V57 implements the first pure-routing organ for API Provider Orchestration and Model Economics. The router is deliberately deterministic and registry-bound. It chooses or rejects routes; it does not call providers.

## Organ separation

The scheduler decides what should run.  
The work classifier types the work.  
The model router chooses the candidate carrier.  
The budget governor will later decide whether the cost is allowed.  
The API rate governor will later decide whether dispatch may occur now.  
The provider adapter will later execute dry-run or live provider calls.  
The model-call receipt will prove what happened.

V57 only implements the router and cost-quality scoring candidate.

## Required route filters

Before scoring, candidates must be filtered for:

1. Provider registered and dry-run safe.
2. Model registered.
3. Required capabilities present.
4. Model quality tier meets the work-class or call-intent quality requirement.
5. Context class fits or exceeds the request.
6. Privacy requirement is satisfied by provider/model data-handling profile.
7. Hard cost ceiling is not violated when cost can be estimated.
8. Explicit forbidden providers are excluded.

## Routing modes

- `cheapest_good_enough`: choose the lowest estimated cost route above threshold; unknown external prices are penalized until verified.
- `highest_quality`: choose the strongest eligible route; cost is secondary, but premium escalation remains non-authoritative until budget governance exists.
- `best_margin`: maximize quality per estimated cost, using placeholder costs only as non-production hints.
- `balanced`: combine quality, speed, cost, context fit, privacy, and availability.
- `fastest_safe`: choose low-latency eligible models above safety/quality threshold.
- `consensus_required`: return a primary route plus a note that a second reviewer route is required later.
- `batch_preferred`: prefer batch/background lanes and avoid interactive capacity where possible.

## Boundaries

A route decision is not an API call. A route decision is not a claim that the selected model is actually available, best in the market, current in price, or production-authorized. It is a deterministic policy decision over placeholder registries and must be superseded by budget/rate governors and model-call receipts in later branches.

