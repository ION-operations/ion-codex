# Temporal Implementation Starter

This directory contains bounded starter modules for the first temporal evaluator landing.

These files are intended to be imported into ION later, then adapted to read from real current ION records through object adapters.

## Included starter modules

- `temporal_model.py`
- `temporal_object_adapters.py`
- `temporal_relevance.py`
- `temporal_leases.py`
- `temporal_reconciliation.py`
- `temporal_receipts.py`
- `temporal_evaluator.py`

## Included starter tests

See `ION/tests/test_temporal_evaluator.py`.

## Important posture

- rule-based, not learned
- recommendation-oriented, not world-mutating
- auditable, with traces and receipts
- narrow initial object-family support
