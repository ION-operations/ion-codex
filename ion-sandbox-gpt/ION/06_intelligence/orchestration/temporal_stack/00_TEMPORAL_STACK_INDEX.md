# Temporal Stack Index

## Purpose

This directory is the proposed import-ready landing zone for the temporal development work in the current canonical ION tree.

## Files

1. `01_ION_TEMPORAL_DEVELOPMENT_FRAMEWORK_EXPANDED.md`
2. `02_TEMPORAL_WORKED_SCENARIOS_FOR_ION.md`
3. `03_TEMPORAL_STACK_MAPPING_INTO_CURRENT_ION.md`
4. `04_FIRST_PASS_TEMPORAL_EVALUATOR_DESIGN.md`
5. `05_TEMPORAL_EVALUATOR_PSEUDOCODE_AND_DATA_STRUCTURES.md`
6. `06_EXACT_CURRENT_ION_MODULE_MAPPING.md`
7. `context/CURRENT_BRANCH_IMPORT_LEDGER_AND_SIBLING_AUTHORITIES.md`

## Expected companion doctrine files

The following doctrine/schema files are intended to live in `ION/02_architecture/` and are part of this same temporal stack:

- `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL.md`
- `TEMPORAL_CONTEXT_LEASE_PROTOCOL.md`
- `TRIPLE_TIME_RECONCILIATION_PROTOCOL.md`
- `TEMPORAL_OBJECT_SCHEMA.md`

## Next implementation layer

These documents point toward a later bounded kernel implementation in:

- `ION/04_packages/kernel/temporal_model.py`
- `ION/04_packages/kernel/temporal_object_adapters.py`
- `ION/04_packages/kernel/temporal_relevance.py`
- `ION/04_packages/kernel/temporal_leases.py`
- `ION/04_packages/kernel/temporal_reconciliation.py`
- `ION/04_packages/kernel/temporal_receipts.py`
