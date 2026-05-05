---
type: research
authority: A3_OPERATIONAL
created: 2026-04-07T17:55:00-04:00
status: ACTIVE_WORKING_PLAN
topic: Consolidated evolution plan for the live ION root based on the April 5 integrated build, audit bundle v3, and production lineage archive
connections:
  - ION/PLAN.md
  - ION/05_context/comms/migration_ledgers/domain_semantic_runtime_migration.md
  - ION/01_doctrine/SOVEREIGN_CONSTITUTION.md
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/02_architecture/AGENT_REASONING_PROTOCOL.md
  - ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
---

# ION Evolution — Consolidated Plan (2026-04-07)

## Executive determination

The uploaded project state already consolidates into a clean three-layer frame:

1. **Live target root** — the April 5 integrated `ION/` tree
2. **Canonical backlog** — audit bundle v3
3. **Lineage witness archive** — `ION - Production.zip`

That means the next correct move is not another abstract consolidation memo.
The correct move is a controlled evolution of the live root in place.

## What the live root already has

The current integrated root already contains a real operating floor:

- provisional doctrine bridge in `01_doctrine/`
- continuity and context framing in `02_architecture/`
- active boot registry in `03_registry/boots/`
- first-pass kernel runtime in `04_packages/kernel/`
- active spec range `T01` through `T07`
- a shared template floor and first bindings in `07_templates/`
- projection, signals, and run-trace comms infrastructure in `05_context/`

The new work must extend this organism rather than replace it.

## What is missing and now load-bearing

### A. Semantic governance is still under-realized

The root has boots and roles, but not yet a stable domain-governance lattice.
Missing surfaces include:

- `ION/02_architecture/INTELLIGENT_DOMAIN_PROTOCOL.md`
- `ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`
- `ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md`
- `ION/03_registry/domains/`
- `ION/03_registry/semantic_identities/`

### B. Confidence and route-state are not yet first-class

The root has reasoning-window governance, but not yet the stronger operator-facing
confidence / drift family or the bridge to explicit route-state and automation-state.
Missing surfaces include:

- `ION/07_templates/confidence/CSR.md`
- `ION/07_templates/bindings/CODEX__CSR.md`
- confidence / drift schema
- manifest / route-state protocol and schema
- automation-state protocol and report template
- cross-model audit calibration spec

### C. Runtime enforcement parity is still partial

The live kernel already has model/store/index/graph/review/planner scaffolds, but it still
lacks several bounded enforcement supports identified by the audit:

- `ION/04_packages/kernel/threshold.py`
- `ION/04_packages/kernel/governed_write.py`
- `ION/04_packages/kernel/capsule_manager.py`

## Planning correction: do not reuse stale spec numbering

The audit bundle names some desired future specs with older ordinals such as manifest at
`T06`, confidence at `T07`, and calibration at `T08`.
That numbering collides with the live integrated root, which already occupies `T01`-`T07`.

Therefore the correct implementation rule is:

- keep existing `T01`-`T07` untouched
- allocate newly landed specs from the next free ordinals onward
- keep semantic filenames explicit so later renumbering, if ever ratified, can be done
  as a separate constitutional cleanup rather than inside this migration

Recommended safe sequence:

- `T08_ConfidenceAndDriftSchema.spec.md`
- `T09_ManifestRouteStateSchema.spec.md`
- `T10_CrossModelAuditCalibration.spec.md`

## Constitutional direction for the next evolution cycle

### Numbering adjustment after live packet landing

The first live packet sequence chose the confidence/drift surface as the earliest next-free spec because `B1` landed before the manifest packet.
The numbering now in effect is:

- `T08_ConfidenceAndDriftSchema.spec.md`
- `T09_ManifestRouteStateSchema.spec.md`
- `T10_CrossModelAuditCalibration.spec.md`

This keeps the integrated root sequential from the next free ordinal onward while preserving the same conceptual bridge order.


### Rule 1 — live ION governs

Nothing in the archive outranks the live constitution, continuity architecture, current
boots, active specs, or current template bindings unless the live root explicitly adopts it.

### Rule 2 — domains first, then stronger automation

The system already has roles and runtime slices, but domains are still implicit.
Making domains explicit is the next stabilizing move.

### Rule 3 — confidence / route-state before runtime authority growth

The current root is strongest where it recently repaired drift through doctrine and bounded
reasoning. The next step is to make that self-monitoring and route-state explicit enough
that future automation can be inspected rather than guessed.

### Rule 4 — runtime ports follow targets

Do not port threshold, governed-write, or capsule modules until their protocol/spec targets
exist in live ION-native form.

### Rule 5 — extraction must stay traceable

Every imported subsystem should carry source-lineage notes or packet references showing why
that subsystem was adopted and from which production roots it was synthesized.

---

## Proposed phase structure

## Phase 0 — migration frame establishment

### Objective
Create the live migration spine and cross-link it from the root plan.

### Deliverables
- migration ledger
- consolidated evolution plan
- brief plan addendum that declares the new execution frame

### Status
Started in this working session.

## Phase 1 — explicit domain governance and semantic identity

### Objective
Make domain law and semantic identity real in repository state.

### New surfaces
- `ION/02_architecture/INTELLIGENT_DOMAIN_PROTOCOL.md`
- `ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`
- `ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md`
- `ION/03_registry/domains/`
- `ION/03_registry/domains/activation_witness/`
- `ION/03_registry/semantic_identities/`

### First active domains
1. `Construction, Routing, and Integration`
2. `Continuity, Context, and Resumability`

### First placements
- **Codex** → primary inside Construction / Routing / Integration
- **Vizier** → primary inside Continuity / Context / Resumability
- **Vice** and **Nemesis** → held for explicit placement in Phase 2

### Why now
The root already has strong role boots and execution slices, but those surfaces are still
not held inside a sufficiently explicit domain lattice.

## Phase 2 — activate Confidence, Drift, and Review

### Objective
Land the first explicit review organ before more aggressive runtime promotion.

### New surfaces
- `ION/07_templates/confidence/CSR.md`
- `ION/07_templates/bindings/CODEX__CSR.md`
- next-free confidence / drift schema spec
- `ION/03_registry/domains/domain.confidence_drift_review.domain.yaml`
- corresponding activation witness

### Role placement
- **Vice** → internal pressure / contradiction / future-answerability guardian
- **Nemesis** → independent audit and bounded release gate posture
- **Codex** → may emit CSR as builder/operator witness but does not become review authority

### Critical distinction
A `REASONING_JOURNAL` and a `CSR` are related but not identical.

- `REASONING_JOURNAL` = internal bounded reasoning witness for an execution window
- `CSR` = explicit confidence / direction / concern / calibration report surface

### Phase 2 implementation note

Phase 2 registry activation is now in place at first-pass level:

- `domain.confidence_drift_review.domain.yaml` exists
- activation witness exists
- `VICE` and `NEMESIS` now have explicit semantic placement inside the review organ
- `CODEX` is marked secondary only through bounded witness/reporting relation

The next lawful move is now `B2`: context mode, manifest/route-state, and automation-state bridge surfaces.

## Phase 3 — protocol bridge completion

### Objective
Create semantics-first targets for context mode, route-state, and automation-state.

### New surfaces
- `ION/02_architecture/CONTEXT_MODE_PROTOCOL.md`
- `ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md`
- `ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md`
- next-free manifest / route-state schema spec
- next-free cross-model calibration spec
- `ION/07_templates/reports/AUTOMATION_STATE_REPORT.md`

### Best lineage authorities by target
- context mode → `SOS` and `SOS-OPUS` context protocol lineage
- CSR family → `SOS`, `SOS-OPUS`, `ION-BUILD`
- manifest / route-state → `operation-victus` conceptual framing + `ION-BUILD` runtime semantics + `IONv2` sanity checks
- automation state → `ION-BUILD/context/specs/automation_unified_spec.md`
- cross-model calibration → `Project-Gemini/services/vif/*`

## Phase 4 — bounded runtime parity after gate pass

### Objective
Port only the runtime modules that now have live targets.

### Runtime sequence
1. `ION/04_packages/kernel/threshold.py`
2. `ION/04_packages/kernel/governed_write.py`
3. `ION/04_packages/kernel/capsule_manager.py`

### Gate
No Phase 4 port should start until the live root contains:

- context mode protocol
- manifest / route-state protocol
- automation state protocol
- confidence / drift schema
- cross-model calibration spec

## Phase 5 — operational truthfulness and tests

### Objective
Make the new surfaces inspectable and truthful in operator flow.

### Work class
- wire new surfaces into planner / context / review flow where appropriate
- add or update tests
- update projections only when they truthfully reflect live state
- keep constitutional claims exactly matched to what has landed

---

## Two-role execution split to keep the migration lawful

## Constitutional Integrator
Owns doctrine-facing, registry-facing, and semantic identity work:

- domain protocols
- domain registry
- semantic identity files
- activation witness
- review-role placement
- small constitutional notes

## Runtime Extractor
Owns bridge protocols, schemas, templates, and later bounded runtime ports:

- CSR family
- confidence / drift spec
- context mode protocol
- manifest / route-state protocol and spec
- automation state protocol and report
- later threshold / governed-write / capsule support ports

---

## Immediate execution order

1. establish migration frame and ledger
2. create domain-governance and semantic-identity floor
3. land CSR + confidence / drift surfaces
4. activate Confidence / Drift / Review as a domain
5. land context-mode, route-state, and automation-state bridge surfaces
6. port one bounded runtime enforcement module at a time

## Whole-cycle acceptance criteria

The next evolution cycle should count as successful only when all of the following are true:

- the first active domains exist as real registry state
- semantic identity is explicit enough to prevent casual rename drift
- Confidence / Drift / Review exists as a visible review organ
- confidence, route-state, and automation-state bridges exist in live ION-native form
- runtime parity work begins only after those targets exist
- all extraction remains traceable to lineage rather than silently transplanted

## Bottom line

The live April 5 root is already a real organism.
Its next evolution should not be another broad rewrite.
It should be a packetized maturation that makes semantic governance explicit, restores
confidence / route-state visibility, and then adds only the runtime enforcement layers
that now have lawful targets.
