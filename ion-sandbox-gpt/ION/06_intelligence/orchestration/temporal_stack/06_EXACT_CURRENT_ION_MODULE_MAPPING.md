# Exact Current ION Module Mapping

## Purpose

This document answers the concrete question:

**Where do the temporal drafts land in the current canonical ION tree, and which current modules should they extend rather than replace?**

This mapping is based on the current canonical merged ION tree structure already examined during the consolidation work.

---

## 1. Exact repository landing paths for documents

### 1.1 Doctrine / protocol files

These should land directly in the current protocol surface:

- `ION/02_architecture/ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL.md`
- `ION/02_architecture/TEMPORAL_CONTEXT_LEASE_PROTOCOL.md`
- `ION/02_architecture/TRIPLE_TIME_RECONCILIATION_PROTOCOL.md`
- `ION/02_architecture/TEMPORAL_OBJECT_SCHEMA.md`

### 1.2 Working paper and design files

These should land under a new current-tree design cluster:

- `ION/06_intelligence/orchestration/temporal_stack/00_TEMPORAL_STACK_INDEX.md`
- `ION/06_intelligence/orchestration/temporal_stack/01_ION_TEMPORAL_DEVELOPMENT_FRAMEWORK_EXPANDED.md`
- `ION/06_intelligence/orchestration/temporal_stack/02_TEMPORAL_WORKED_SCENARIOS_FOR_ION.md`
- `ION/06_intelligence/orchestration/temporal_stack/03_TEMPORAL_STACK_MAPPING_INTO_CURRENT_ION.md`
- `ION/06_intelligence/orchestration/temporal_stack/04_FIRST_PASS_TEMPORAL_EVALUATOR_DESIGN.md`
- `ION/06_intelligence/orchestration/temporal_stack/05_TEMPORAL_EVALUATOR_PSEUDOCODE_AND_DATA_STRUCTURES.md`
- `ION/06_intelligence/orchestration/temporal_stack/06_EXACT_CURRENT_ION_MODULE_MAPPING.md`

This path is correct for the current canonical tree because `ION/06_intelligence/orchestration/` already exists and is the proper home for design/intelligence papers, while `ION/03_schema/` does not currently exist in the canonical tree.

### 1.3 Supplemental lineage / import context

- `ION/06_intelligence/orchestration/temporal_stack/context/CURRENT_BRANCH_IMPORT_LEDGER_AND_SIBLING_AUTHORITIES.md`

---

## 2. Exact current kernel modules the evaluator should anchor to

The evaluator work should not begin as a replacement of existing kernel modules. It should anchor to them.

### 2.1 Existing kernel modules that provide temporal inputs

These are the most important current input modules:

- `ION/04_packages/kernel/horizon_state.py`
- `ION/04_packages/kernel/scheduler.py`
- `ION/04_packages/kernel/schedule_controls.py`
- `ION/04_packages/kernel/manifest_state.py`
- `ION/04_packages/kernel/automation_state.py`
- `ION/04_packages/kernel/runtime_state_views.py`
- `ION/04_packages/kernel/runtime_state_sync.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/signal_followups.py`
- `ION/04_packages/kernel/receipts.py`
- `ION/04_packages/kernel/model.py`

### 2.2 Exact new kernel modules recommended for temporal implementation

The cleanest initial implementation should add new focused modules rather than overloading existing ones:

- `ION/04_packages/kernel/temporal_model.py`
- `ION/04_packages/kernel/temporal_object_adapters.py`
- `ION/04_packages/kernel/temporal_relevance.py`
- `ION/04_packages/kernel/temporal_leases.py`
- `ION/04_packages/kernel/temporal_reconciliation.py`
- `ION/04_packages/kernel/temporal_receipts.py`
- `ION/04_packages/kernel/temporal_runtime_bridge.py` *(later, not first landing)*

### 2.3 Why these should be new files first

This avoids bloating:

- `model.py`
- `scheduler.py`
- `manifest_state.py`
- `automation_state.py`

before the temporal evaluator is proven. The first implementation should be additive and overlay-based.

---

## 3. Exact role of each current module in the temporal landing path

### 3.1 `model.py`

Current role:
- base enums and record types
- work units, horizons, schedules, automation, questions, receipts

Temporal landing role:
- remain largely unchanged in the first landing
- later absorb only truly canonical shared enums if the temporal layer stabilizes

### 3.2 `horizon_state.py`

Current role:
- immediate / near / far horizon persistence and tightening

Temporal landing role:
- source of horizon inputs for orchestration heat
- should not be replaced

### 3.3 `scheduler.py`

Current role:
- lawful orchestration scheduler surfaces
- commitment gradients and schedule states

Temporal landing role:
- source of commitment/state inputs into temporal relevance
- should not own heat/lease/reconciliation by itself

### 3.4 `manifest_state.py`

Current role:
- manifest / route-state persistence

Temporal landing role:
- source of activation conditions, branch posture, and route readiness
- should inform temporal relevance and reconciliation

### 3.5 `automation_state.py`

Current role:
- automation posture and promotion/demotion surfaces

Temporal landing role:
- source of budget/feasibility-adjacent posture and fallback implications
- may later consume temporal recommendations

### 3.6 `runtime_state_views.py`

Current role:
- view layer over manifest and automation runtime posture

Temporal landing role:
- likely first consumer-side bridge for turning temporal recommendations into runtime-readable posture

### 3.7 `runtime_state_sync.py`

Current role:
- writes manifest/automation state based on governed write results

Temporal landing role:
- should remain downstream at first
- later may consume temporal receipts or recommendation envelopes

### 3.8 `questions.py` and `reviews.py`

Current role:
- open-question routing and held-review escalation

Temporal landing role:
- likely early destinations for reconfirmation / escalation outputs from reconciliation logic

### 3.9 `receipts.py`, `signals.py`, and `signal_followups.py`

Current role:
- validation receipts, signal emission, follow-up interpretation

Temporal landing role:
- ideal downstream homes for temporal evaluation receipts and temporal recommendation signals
- should not be bypassed once temporal outputs become live

---

## 4. Exact first implementation order in the current tree

1. Land the four doctrine/schema files in `ION/02_architecture/`.
2. Land the working-paper cluster in `ION/06_intelligence/orchestration/temporal_stack/`.
3. Add the new kernel files:
   - `temporal_model.py`
   - `temporal_object_adapters.py`
   - `temporal_relevance.py`
   - `temporal_leases.py`
   - `temporal_reconciliation.py`
4. Bind those new files to existing current modules as read-only consumers of:
   - horizon state
   - scheduler state
   - manifest/route state
   - automation posture
5. Emit recommendation/receipt envelopes before any live mutation path is attempted.
6. Only later integrate with runtime-facing calendar/reminder/automation expression surfaces.

---

## 5. Strongest conclusion

Yes: the evaluator types and the temporal stack now have an exact current-ION anchoring path.

The correct approach is:

- **new focused temporal kernel modules first**,
- **existing scheduler / horizon / manifest / automation modules as inputs**,
- **receipt/signal modules as downstream audit surfaces**,
- and **no early monolithic rewrite**.
