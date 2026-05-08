---
type: canonicalization_decision
template: CANONICALIZATION_DECISION
created: 2026-04-17T00:00:00-04:00
status: WORKING
scope: workspace_root_authority
decision_class: primary_selection
connections:
  - ION/06_intelligence/orchestration/2026-04-17_reintegration_state_and_canonical_root_assessment.md
  - ION/06_intelligence/orchestration/corpus_recovery/11_grand_picture/era2_controlled_reintegration.md
  - ION/06_intelligence/orchestration/corpus_recovery/24_orchestration_board/current_era2_orchestration_board.md
  - ION/06_intelligence/orchestration/corpus_recovery/26_constitutional_reintegration_foundry/04_canon_foundry_operating_model_and_registry_stack.md
  - ION/06_intelligence/orchestration/corpus_recovery/26_constitutional_reintegration_foundry/06_decision_gates_open_questions_and_first_execution_order.md
  - ION/03_registry/reintegration/root_manifest.yaml
  - ION/03_registry/reintegration/lineage_registry.yaml
  - ION/03_registry/reintegration/authority_registry.yaml
  - ION/03_registry/reintegration/duplicate_competition_registry.yaml
  - ION/03_registry/reintegration/canonicalization_queue.yaml
---

# Canonicalization Decision: Workspace Root Authority

## Purpose

Close Decision Gate 2 far enough that current reintegration work can proceed
without pretending the workspace already has one undisputed center.

The estate currently contains two serious ION roots:

- the top-level production `ION/`,
- and the packaged current-generation root at
  `ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/`.

This decision does not claim that the split is solved forever. It does make the
split explicit, partitions authority lawfully, and defines where current
reintegration work should land.

## Scope and competing candidates

Primary competing candidates:

1. `ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/`
2. `ION/`

Important adjacent but non-primary candidates in this decision:

- `AIM-ION/` as a sibling universe pending a separate classification packet
- `ION-BUILD/` as historical runtime/API witness
- `operation-victus/` and `Project-Gemini/` as manager/orchestrator witnesses

This decision is about **workspace root authority**, not full-estate retirement.
No archive family is retired by this document.

## Evidence considered

Primary local evidence:

- `ION/06_intelligence/orchestration/2026-04-17_reintegration_state_and_canonical_root_assessment.md`
- `ION/06_intelligence/orchestration/corpus_recovery/26_constitutional_reintegration_foundry/02_ion_estate_build_lines_and_root_status_assessment.md`
- `ION/06_intelligence/orchestration/corpus_recovery/26_constitutional_reintegration_foundry/04_canon_foundry_operating_model_and_registry_stack.md`
- `ION/06_intelligence/orchestration/corpus_recovery/26_constitutional_reintegration_foundry/06_decision_gates_open_questions_and_first_execution_order.md`
- `ION/README.md`
- `ION/STATUS.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/03_registry/current_phase_template_surface_registry.yaml`

Independent witness evidence from the Opus / Composer bridge:

- `/home/sev/ION - Production/_opus_composer_bridge/30_deliverables_for_opus/001_foundry_suite_brief.md`
- `/home/sev/ION - Production/_opus_composer_bridge/30_deliverables_for_opus/002_estate_survey.md`

Local verification also corrects one minor witness miss from the bridge:
`ION/03_registry/current_phase_template_surface_registry.yaml` does exist in the
packaged root and should not be treated as missing.

## Decision

### 1. Present primary operational center

For the current Era 2 reintegration cycle, the packaged current-generation root
at `ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/`
is the **provisional primary operational center** for:

- controlled reintegration orchestration,
- corpus recovery,
- constitutional reintegration / canon foundry planning,
- current-phase template governance,
- root-authority adjudication surfaces,
- and future carrier-facing canon-export work.

### 2. Retained live extraction center

The top-level production `ION/` root is retained as an
**active witness and extraction center**, not as retired matter.

It remains the operative source for production-facing surfaces that the packaged
center does not yet fully absorb, especially:

- MCP-facing package surfaces,
- `ion_api`,
- `docs/` and `docs/program/` style material,
- and other production/preflight-facing entry surfaces still unique to that root.

### 3. No false single-root claim

No workspace-wide claim of final single-root unification is authorized yet.

The truthful current state is:

- one provisional primary center,
- one retained live extraction center,
- and an explicit promotion burden between them.

### 4. Landing rule for new work

New work about reintegration, foundry, adjudication, recovery atlases, and
current-phase orchestration should land in the packaged current-generation root
unless a packet is explicitly scoped to retained production-only surfaces in the
top-level `ION/` root.

### 5. Promotion rule for production surfaces

Any attempt to declare the packaged root the sole workspace canon must first
carry a bounded promotion packet for the still-separated production surfaces in
top-level `ION/`.

At minimum that promotion burden includes:

- MCP package surfaces,
- `ion_api`,
- `docs/`,
- program docs and preflight-facing support surfaces,
- and any remaining runtime entry material that is still uniquely production-side.

### 6. Export rule

The first generated canon export should be a **root-authority bundle** that
states this split explicitly for carriers, rather than handing a fresh worker
both roots without adjudication.

## Retained witnesses and deferred matter

Retained live or historical witnesses:

- `ION/`
- `ION-BUILD/`
- `operation-victus/`
- `Project-Gemini/`
- `ATLAS/`
- `AIM-ION/`

Deferred matter:

- final workspace-wide single-root ratification,
- promotion or merge of the top-level `ION/` production surfaces,
- retirement or tombstoning of any primary root,
- AIM-ION / AIM-OS family classification,
- and carrier-specific export packaging beyond the first root-authority bundle.

## Confidence and unresolved contradictions

Confidence: **high** that a real split-center condition exists.

Confidence: **medium** that the current partition is complete enough to survive
all near-term work without revision.

Unresolved contradictions that must remain visible:

- the two ION roots still carry materially different `README.md` / `STATUS.md`
  narratives and therefore different self-understandings of current phase,
- the packaged center carries the later recovery/orchestration spine,
- the top-level production center still carries important MCP/API/docs surfaces
  absent from the packaged root,
- and the packaged root's nested `ION/` subdirectory remains a path-legibility
  hazard for agents and future export tooling.

This decision therefore closes the immediate ambiguity operationally, but it does
not erase the contradiction history.

## Required follow-up

1. Seed the minimal reintegration registries and keep them aligned with this
   decision.
2. Open the AIM-ION / AIM-OS classification packet as the next major
   canonicalization question. Historical bridge material may be consulted as
   archived witness evidence, but no active Opus/Composer review dependency
   remains after bridge deactivation.
3. Produce a bounded promotion map for the top-level `ION/`-only
   MCP/API/docs/preflight surfaces, treating docs/program and preflight-facing
   support as the highest-variance domains inside that packet.
4. Open the packaged-root nested-path disambiguation packet before carrier
   export, so fresh workers do not have to infer path truth across the
   packaged root, its nested `ION/` directory, and the top-level production
   `ION/`.
5. Emit the first root-authority export bundle for carriers with explicit
   per-carrier read modes and explicit treatment of the current STATUS
   narrative divergence.
6. Reassess whether the provisional primary center can become sole workspace
   canon only after steps 2-5 are complete enough to judge honestly.
