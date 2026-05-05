---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-07T22:20:00-04:00
status: ACTIVE_FIRST_PASS
connections:
  - ION/01_doctrine/SOVEREIGN_CONSTITUTION.md
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
  - ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md
  - ION/03_registry/domains/README.md
  - ION/03_registry/domains/domain.construction_routing_integration.domain.yaml
  - ION/03_registry/domains/domain.continuity_context_resumability.domain.yaml
  - ION/03_registry/semantic_identities/STEWARD.semantic.yaml
  - ION/03_registry/semantic_identities/VIZIER.semantic.yaml
---

# INTELLIGENT DOMAIN PROTOCOL

## Status

This protocol establishes the first explicit domain-governance layer for the live `ION/` root.
It is an active first-pass operational surface.
It does not claim that every runtime or doctrine surface is already fully domain-governed.

## 1. Why domains exist

The live root already has roles, boots, templates, and runtime slices.
What it has lacked is a stable layer that says which families of work those roles are primarily carrying,
which backlog belongs where, and how new work should be placed without casual semantic drift.

Domains exist to solve that.
A domain is not a person, and it is not merely a folder.
A domain is a governed work-field with:

- a stable identifier,
- a declared burden,
- owned or stewarded surfaces,
- role placements,
- activation status,
- and explicit witness of why the activation is real.

## 2. Core law

### Law 1 — Domains are governance surfaces, not decorative tags

A domain record exists to carry real burden, placement, and backlog orientation.
If a domain is named but no work, roles, or surfaces are held inside it, the record is not yet truthful.

### Law 2 — Activation does not imply completeness

A domain may be active in constitutional or registry state while only partially realized in runtime enforcement.
The registry must keep that distinction visible.

### Law 3 — Role placement is primary, not exclusive

A role may have one primary domain and zero or more secondary relations.
Primary placement identifies the role's main standing burden in the current phase.
It does not forbid bounded cross-domain work when routing or doctrine explicitly permits it.

### Law 4 — Domain records outrank casual prose references

When a domain name, identifier, or membership appears in ordinary prose and conflicts with the registry,
the registry governs unless a higher-authority doctrine surface explicitly says otherwise.

### Law 5 — Witness of activation must be separate from the domain record

The domain file states the governed current truth.
Activation witness records why that truth was adopted, by what packet, and with what constraints.

## 3. Domain status classes

Current first-pass status bands:

- `PROPOSED` — named but not yet active in the live root
- `ACTIVE_FIRST_PASS` — active for the current phase, but still incomplete or unratified
- `ACTIVE` — active and considered stable for the current organism
- `ARCHIVED_REFERENCE` — preserved as witness only

## 4. Required parts of a domain record

Each domain record should declare at minimum:

- `domain_id`
- `display_name`
- `true_name_status`
- `status`
- `authority`
- `mission`
- `scope`
- `primary_roles`
- `secondary_roles`
- `owned_or_stewarded_surfaces`
- `open_edges`
- `activation_witness`

## 5. Current phase active domains

The first active domains of this migration are:

1. `Construction, Routing, and Integration`
2. `Continuity, Context, and Resumability`
3. `Confidence, Drift, and Review`

These are intentionally modest first activations.
They make the existing root more truthful without pretending the full domain lattice is complete.

## 6. Placement rule for the first active phase

### Construction, Routing, and Integration

Primary role:
- `STEWARD`

Working burden:
- bounded implementation
- sequential routing
- integration synthesis
- scoped execution and verification

### Continuity, Context, and Resumability

Primary role:
- `VIZIER`

Working burden:
- continuity law
- context discipline
- resumability and governance memory
- phase framing and burden-bearing architecture


### Confidence, Drift, and Review

Primary roles:
- `VICE`
- `NEMESIS`

Secondary role:
- `STEWARD`

Working burden:
- confidence-state reporting
- drift and contradiction pressure
- bounded audit posture
- review gating without silent constitutional self-ratification


## 7. Backlog placement rule

A missing feature or unresolved burden should now be placed into one of three classes:

- domain-owned backlog
- cross-domain bridge work
- witness-only lineage material

This prevents anonymous backlog drift.

## 8. Current file law

The first-pass domain layer lives at:

- `ION/03_registry/domains/`
- `ION/03_registry/domains/activation_witness/`
- `ION/03_registry/semantic_identities/`

The registry is the live operational source for active domain truth.
It is not the final doctrine canon, but it is more authoritative than unstated habit.

## 9. Non-claims

This protocol does **not** yet claim:

- a complete ministry/cabinet/domain ontology
- a final true-name stack for every role
- fully automated enforcement of domain ownership
- that every file in the repository already has a settled domain home
