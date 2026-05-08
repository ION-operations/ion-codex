---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-07T22:21:00-04:00
status: ACTIVE_FIRST_PASS
connections:
  - ION/01_doctrine/SOVEREIGN_CONSTITUTION.md
  - ION/02_architecture/INTELLIGENT_DOMAIN_PROTOCOL.md
  - ION/02_architecture/NAME_LINEAGE_REGISTRY_PROTOCOL.md
  - ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md
  - ION/03_registry/name_lineage_registry.yaml
  - ION/06_intelligence/orchestration/2026-04-22_codex_current_phase_role_and_boot_retirement_note.md
  - ION/03_registry/semantic_identities/VIZIER.semantic.yaml
  - ION/06_intelligence/research/2026-04-03_codex_ion_centering_response.md
---

# TRUE NAME AND SEMANTIC LAYER PROTOCOL

## Status

This protocol formalizes the minimum semantic layer needed to stop casual rename drift in the live `ION/` root.
It is not yet a total ontology.
It is the first active naming law required for the current migration.

## 1. Why this layer exists

The live root already carries structurally meaningful names in boots, doctrine, protocols, and research.
Those names are load-bearing.
Without an explicit semantic layer, weaker execution passes can flatten them into style choices,
retrofit cleaner names without provenance, or confuse historical names with active structural names.

## 2. Semantic stack

Each governed entity may carry multiple naming layers.
The current minimum stack is:

### A. Registry identifier

The stable machine-oriented identifier used in registry surfaces.
This should be the least ambiguous reference for file-backed governance.

### B. Display name

The ordinary visible name used in current operational prose.
Examples: `Steward`, `Vizier`, `ION`.

### C. Structural identity

The doctrinal or architectural identity string that describes the entity's deeper role placement.
Examples already exist in boot records.

### D. Historical naming truth

A preserved older name, acronym, spelling, or witness form that should remain visible as lineage.
Historical naming truth is not automatically the active governing name.

### E. True-name status

A statement of whether the entity's active name is:

- `SETTLED_CURRENT_PHASE`
- `HISTORICAL_ONLY`
- `PROVISIONAL`
- `DEEP_NAME_HELD`

This lets the system distinguish active naming from suggestive but unratified depth-language.

## 3. Naming law

### Law 1 — Naming is load-bearing

No governed entity should be casually renamed in a patch unless the packet explicitly concerns semantic identity,
true-name review, or protocol cleanup.

### Law 2 — Historical truth must be preserved, not silently normalized away

If an older acronym, spelling, or witness form matters for lineage, it should remain visible with provenance.
It must not be erased merely because a cleaner present-tense form exists.

### Law 3 — Deep names must not be over-activated

A deeper or more metaphysical naming layer may be discussed in research,
but it should not silently become active registry truth unless the current protocol or doctrine adopts it.

### Law 4 — Display name and structural identity must remain distinguishable

A person or role may be referred to by display name in ordinary use,
but the structural identity remains the stronger semantic anchor for governance work.

## 4. Required fields for a semantic identity record

Each semantic identity file should include:

- `entity_id`
- `display_name`
- `structural_identity`
- `historical_truth`
- `true_name_status`
- `primary_domain`
- `secondary_domains`
- `governing_sources`
- `rename_constraints`

## 5. Current first-pass semantic decisions

### ION

`ION` should preserve two truths simultaneously:

- historical acronym truth as filed in lineage
- converged current structural naming truth in the active organism

This protocol does not expand that into a final total ontology.

### Steward

`Steward` is the settled current-phase orchestration truename for the active production-build branch.
This names orchestration truth rather than chassis convenience.

### Historical carrier alias (retired IDE token)

This retired token is preserved as a historical carrier/display alias for older IDE-native branch artifacts.
It is not a live current-phase role name and should not be revived as a workflow distinction among IDE, browser, API, or other lawful carriers.

### Vizier

`Vizier` remains the active display name.
Its burden-bearing continuity architecture role remains the stronger registry anchor.
No deeper renaming is activated here beyond what already exists in boot law.

## 6. Registry rule

The live semantic layer for current-phase governance is carried by:

- `ION/03_registry/semantic_identities/*.semantic.yaml`
- `ION/03_registry/name_lineage_registry.yaml`

When prose, task memory, or witness artifacts conflict with a semantic identity record,
the identity record governs for current-phase operational work unless a higher-authority doctrine surface explicitly overrides it.

The semantic identities answer "what is this governed entity?"
The name-lineage registry answers "which older names still mean something, and what may or may not happen when they re-enter live paths?"

## 7. Non-claims

This protocol does **not** yet define:

- a full semantic dictionary engine
- all deep-name stacks across all lineages
- automated rename linting
- final constitutional doctrine for every semantic class
