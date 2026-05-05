---
type: handoff
template: HANDOFF
created: 2026-04-09T15:14:00-04:00
status: ACTIVE
from: Codex
to: Next executor
objective: Start L1 executor capability registry from an explicit L0 scheduler floor
---

# Handoff: L1 Executor Capability Registry

## From

Codex

## To

Next executor

## What was completed

- L0 scheduler state, commitment gradient, horizon bridge, receipt law, and operator projection are now explicit in code.
- The full suite is green with post-L0 coverage.
- Root/orchestration surfaces now name L1 as next.

## What remains

- Formalize executor identity, carrier class, trust class, concurrency, availability, and fallback suitability.
- Rebind carrier inference away from heuristics and into explicit capability law.

## Exact artifacts to read

- `ION/README.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/06_intelligence/orchestration/2026-04-09_post_l0_state_forward_path_and_codex_handoff.md`
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`
- `ION/04_packages/kernel/scheduler.py`
- `ION/tests/test_kernel_scheduler.py`
- `ION/tests/test_kernel_operator_cli.py`

## Risks / warnings

- Do not let current carrier inference heuristics harden into hidden capability law.
- Do not widen into swarm execution before L1-L4 executor-neutrality work is materially underway.

## Requested next action

- Land L1 executor capability registry and keep the schedule layer subordinate to kernel truth and packet law.

