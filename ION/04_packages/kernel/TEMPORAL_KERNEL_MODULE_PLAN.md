# Temporal Kernel Module Plan

## Purpose

This file records the exact proposed kernel module additions for the first bounded temporal implementation.

## New proposed modules

- `temporal_model.py`
- `temporal_object_adapters.py`
- `temporal_relevance.py`
- `temporal_leases.py`
- `temporal_reconciliation.py`
- `temporal_receipts.py`
- `temporal_evaluator.py`

## Existing modules treated as input sources, not replaced

- `model.py`
- `horizon_state.py`
- `scheduler.py`
- `schedule_controls.py`
- `manifest_state.py`
- `automation_state.py`
- `runtime_state_views.py`
- `runtime_state_sync.py`
- `questions.py`
- `reviews.py`
- `signals.py`
- `signal_followups.py`
- `receipts.py`

## Implementation posture

The temporal layer should first be additive, auditable, and recommendation-oriented.
It should not mutate world state directly in its first landing.
