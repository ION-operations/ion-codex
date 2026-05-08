---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-07T22:22:00-04:00
status: ACTIVE_FIRST_PASS
connections:
  - ION/01_doctrine/SOVEREIGN_CONSTITUTION.md
  - ION/02_architecture/INTELLIGENT_DOMAIN_PROTOCOL.md
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
  - ION/03_registry/semantic_identities/VIZIER.semantic.yaml
  - ION/06_intelligence/orchestration/2026-04-22_codex_current_phase_role_and_boot_retirement_note.md
  - ION/03_registry/boots/VIZIER.boot.md
  - ION/03_registry/boots/VICE.boot.md
  - ION/03_registry/boots/NEMESIS.boot.md
---

# RANK AND PRECEDENCE PROTOCOL

## Status

This protocol defines the minimum precedence rules needed to prevent semantic and governance ambiguity during the current migration.
It is a first-pass operational rule set.
It is not a final constitutional hierarchy of all possible entities.

## 1. Why precedence must be explicit

The live root already contains multiple classes of authority:

- sovereign/human lead authority,
- doctrine and constitution,
- protocol surfaces,
- boots,
- bindings and templates,
- runtime code,
- witness artifacts,
- and archive lineage.

Without a precedence rule, a weaker execution pass can accidentally let later prose outrank doctrine,
or let archive lineage outrank current live law.

## 2. Primary precedence order

For the current migration, interpret conflicts in this order:

1. Sovereign / explicit human lead direction in the active session
2. Constitution and kernel doctrine in `ION/01_doctrine/`
3. Current active protocols in `ION/02_architecture/`
4. Registry state in `ION/03_registry/`
5. Active specs in `ION/06_intelligence/specs/`
6. Shared templates and bindings in `ION/07_templates/`
7. Runtime implementation in `ION/04_packages/`
8. Research, audits, signals, and other witness surfaces in `ION/05_context/` and `ION/06_intelligence/`
9. External lineage archives and production predecessor roots

## 3. Interpretation rules

### Law 1 — Higher law constrains lower surfaces

A runtime module may not silently widen what a protocol forbids.
A binding may not redefine what a boot or doctrine already settled.
A research note may not silently ratify itself into law.

### Law 2 — Live-root law outranks archive lineage

Production lineage is extraction witness.
It is valuable because it shows proven subsystems and earlier control surfaces.
It does not outrank the current active organism unless the live root explicitly adopts it.

### Law 3 — Registry outranks casual role prose

Where role placement, domain membership, or semantic identity are concerned,
registry state is the current operational source of truth.

### Law 4 — Active protocols outrank local convenience

A local code shortcut or patch-package suggestion does not outrank a protocol gate.
If a module wants to exist, its target law should exist first.

## 4. Rank classes for current roles

This migration uses rank classes only as coordination guidance, not as personal prestige.

- `BURDEN_BEARER_ARCHITECTURAL` — strategic continuity burden and architecture carriage
- `BOUNDED_CONSTRUCTION_LEAD` — active implementation and routing burden
- `BOUNDED_ORCHESTRATION_STEWARD` — current-phase orchestration, packet sequencing, status, and proposal burden
- `HISTORICAL_CARRIER_ALIAS` — preserved witness class for retired carrier labels; not a live current-phase operational rank
- `BOUNDED_INTENT_RELAY` — bounded front-door relay, digest, and courier burden without hidden orchestration or ratification power
- `INTERNAL_CONTRADICTION_PRESSURE` — internal pressure against hidden defect
- `INDEPENDENT_AUDIT_GATE` — bounded external audit and release gate posture
- `STANDING_ARCHAEOLOGY_DAEMON` — persistent excavation, stale-authority watch, and evidence-bound archaeology without adjudicative authority

Current first-pass mapping:

- `VIZIER` → `BURDEN_BEARER_ARCHITECTURAL`
- `STEWARD` → `BOUNDED_ORCHESTRATION_STEWARD`
- `RELAY` → `BOUNDED_INTENT_RELAY`
- `VICE` → `INTERNAL_CONTRADICTION_PRESSURE`
- `NEMESIS` → `INDEPENDENT_AUDIT_GATE`
- `VESTIGE` → `STANDING_ARCHAEOLOGY_DAEMON`

Interpretation note:
- `STEWARD` names current-phase orchestration truth.
- carrier or mount specificity belongs to chassis/mount law rather than a separate current-phase roster rank.
- historical carrier witness does not outrank truename settlement.

## 5. Scope of this protocol

This protocol governs:

- conflict interpretation,
- active packet review,
- semantic identity work,
- domain placement,
- and archive extraction discipline.

It does not yet define personnel law for every historical or future role.
