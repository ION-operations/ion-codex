# ION Self-Knowledge Registry Promotion Candidate

Generated: `2026-05-08T04:05:23+00:00`  
Status: `promotion_proposal_pending_human_steward_acceptance`

This directory is a **promotion mirror**, not accepted registry law.

It prepares the exact registry-shaped files that would land under:

```text
ION/03_registry/self_knowledge/
```

after explicit human/Steward acceptance and settlement receipt.

## Why this mirror exists

The active sandbox work packet allows writes under `ION/05_context/current/` and `ION/tests/`, but does not authorize direct mutation of `ION/03_registry/`.

Therefore this work prepares a reviewable apply tree:

```text
ION/05_context/current/self_knowledge/promotion_candidate/apply_tree/ION/03_registry/self_knowledge/
```

## Non-claims

- The files here are not accepted canon.
- The target namespace has not been mutated.
- The registry status remains pending acceptance.
- This mirror is not proof of production readiness.
- A future acceptance act must decide whether to copy, revise, or reject this mirror.

## Prepared target files

- `ION/03_registry/self_knowledge/domain_registry.yaml` from `ION/05_context/current/self_knowledge/candidate_registries/domain_registry.candidate.yaml`
- `ION/03_registry/self_knowledge/route_registry.yaml` from `ION/05_context/current/self_knowledge/candidate_registries/route_registry.candidate.yaml`
- `ION/03_registry/self_knowledge/node_registry.yaml` from `ION/05_context/current/self_knowledge/candidate_registries/node_registry.candidate.yaml`
- `ION/03_registry/self_knowledge/node_schema.yaml` from `ION/05_context/current/self_knowledge/candidate_registries/node_schema.candidate.yaml`
- `ION/03_registry/self_knowledge/state_classification.yaml` from `ION/05_context/current/self_knowledge/candidate_registries/state_classification.candidate.yaml`
- `ION/03_registry/self_knowledge/authority_ranking.yaml` from `ION/05_context/current/self_knowledge/candidate_registries/authority_ranking.candidate.yaml`

## Required settlement before landing

1. Human/Steward acceptance of candidate self-knowledge domain-state layer.
2. Focused test pass for candidate registries, routes, mount packet, and anti-drift guards.
3. State-surface sync report showing candidate/accepted boundary remains consistent.
4. Settlement receipt naming the exact files promoted.
