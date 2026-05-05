---
type: canonicalization_decision
template: CANONICALIZATION_DECISION
created: 2026-04-17T00:00:00-04:00
status: WORKING
scope: packaged_root_nested_path_disambiguation
decision_class: path_authority
connections:
  - ION/06_intelligence/decisions/2026-04-17_workspace_root_authority_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
  - ION/REPO_AUTHORITY.md
  - ION/README.md
  - ION/STATUS.md
  - ION/MASTER_ORCHESTRATION_INDEX.md
  - ION/03_registry/reintegration/root_manifest.yaml
  - ION/03_registry/reintegration/lineage_registry.yaml
  - ION/03_registry/reintegration/authority_registry.yaml
  - ION/03_registry/reintegration/duplicate_competition_registry.yaml
  - ION/03_registry/reintegration/canonicalization_queue.yaml
  - ION/ION/05_context/history/daemon_service_ledger.json
  - ION/ION/05_context/history/system_ledger.json
  - ION/ION/05_context/signals/archive/ION_TASK_FAILED_bootstrap_non_idle_daemon_20260410T1835.signal.json
---

# Canonicalization Decision: Packaged-Root Nested Path Disambiguation

## Purpose

Close q006 far enough that fresh executors, carrier bundles, and future export
surfaces do not mistake the packaged root's nested `ION/` directory for a
second runnable root.

This packet does not move files. It classifies the nested path correctly and
defines the naming rules that q004 and later carrier surfaces must obey.

## Scope and competing interpretations

Primary ambiguity in scope:

1. packaged current-generation root at
   `ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/`
2. nested directory inside that root at
   `ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/ION/`
3. top-level production root at `ION/`

Competing interpretations considered:

1. the nested `ION/ION/` directory is a second runnable root
2. the nested `ION/ION/` directory is an embedded context/history residue lane
3. the nested `ION/ION/` directory is an incomplete extraction that should be
   ignored entirely

This decision is about path authority and naming discipline, not retirement or
promotion.

## Evidence considered

Primary packaged-root evidence:

- `ION/REPO_AUTHORITY.md`
- `ION/README.md`
- `ION/STATUS.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/ION/05_context/history/daemon_service_ledger.json`
- `ION/ION/05_context/history/system_ledger.json`
- `ION/ION/05_context/signals/archive/ION_TASK_FAILED_bootstrap_non_idle_daemon_20260410T1835.signal.json`

Observed structure of the nested directory:

- only `ION/05_context/history/...`
- only `ION/05_context/signals/...`
- no nested `01_doctrine/`, `02_architecture/`, `03_registry/`, `04_packages/`,
  `tests/`, or other runnable-root organs

The ledger and signal artifacts also self-reference branch-local paths such as
`ION/05_context/history/...` and `ION/06_intelligence/research/...`, which is
consistent with embedded runtime residue captured from a branch-root execution
surface, not with a second independent root.

## Decision

### 1. Nested `ION/ION/` is not a second runnable root

The nested directory at `ION/ION/` inside the packaged current-generation root
is **not** a second runnable or competing root.

It is classified as an **embedded context/history residue lane** contained
inside the packaged root.

### 2. What the nested lane actually contains

The current nested lane contains only embedded runtime evidence:

- daemon service and daemon loop ledgers / receipts
- system ledger material
- archived signal material
- kernel-store open-question residue

That is witness matter inside the packaged root, not a standalone startup
surface.

### 3. Normalized naming rules

The following names are now the required disambiguation layer for current
reintegration work:

- **packaged current-generation root** =
  `ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/`
- **packaged-root local alias** = `ION/` only when speaking from inside the
  packaged root's own documents
- **embedded residue lane** = `ION/ION/05_context/...` from the packaged-root
  local view, or the full workspace path when speaking across roots
- **top-level production root** = workspace `ION/`

### 4. Workspace-level path rule

When a document or carrier surface speaks across multiple roots, it must not
use bare `ION/` without naming which one it means.

At workspace scope:

- say **packaged current-generation root** for the packaged branch
- say **top-level production root** for workspace `ION/`
- say **embedded residue lane** for `.../ION/ION/05_context/...`

### 5. Carrier/export rule

q004 and any later carrier bundle must encode this distinction explicitly.

No carrier-facing startup surface may hand a fresh executor:

- the packaged root,
- the top-level production root,
- and the embedded residue lane

without naming each one separately and stating that only the first two are
roots while the third is internal residue.

### 6. Startup authority rule

The startup answer remains unchanged in substance:

- the packaged repository's canonical runnable root is the packaged `ION/`
  directory itself

What changes is the explicit correction:

- encountering `ION/ION/05_context/...` inside that repository does **not**
  reopen root authority
- it signals embedded runtime evidence captured under the packaged root

## Retained witnesses and deferred matter

Retained witness matter:

- the embedded residue files under `ION/ION/05_context/...`
- the root-authority split between the packaged current-generation root and the
  top-level production root

Deferred matter:

- whether any residue in `ION/ION/05_context/...` should later be rehomed into
  a cleaner witness lane
- whether q004 should export direct links into the residue lane or only name it
- whether later packaging/promotion work should physically normalize this path
  shape

## Confidence and unresolved contradictions

Confidence: **high** that the nested `ION/ION/` directory is not a second root.

Confidence: **high** that the correct present classification is embedded
context/history residue lane.

Confidence: **medium** on whether the later cleanest state is to retain this
lane in place or rehome it after carrier-export work.

Unresolved contradictions that must remain visible:

- workspace root authority is still split between the packaged
  current-generation root and the top-level production root
- the packaged root still contains historical/local documents that use `ION/`
  as a branch-local alias even when the wider workspace now contains another
  `ION/`
- q004 still has to encode this distinction into carrier-safe startup bundles

## Required follow-up

1. Update the reintegration registries to record that the nested packaged
   `ION/` path is internal residue, not a second root.
2. Update startup surfaces so fresh executors see this correction before q004
   emits carrier bundles.
3. Treat q004 as the next packet: carrier-safe root-authority export with
   explicit read modes and explicit naming of packaged root, top-level
   production root, and embedded residue lane.
