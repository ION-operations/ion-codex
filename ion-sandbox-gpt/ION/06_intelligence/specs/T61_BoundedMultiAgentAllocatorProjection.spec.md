---
type: specification
authority: A3_OPERATIONAL
created: 2026-04-09T23:15:00-04:00
status: ACTIVE
---

# T61 — Bounded Multi-Agent Allocator Projection

## Requirement

The kernel must be able to build one bounded branch-allocation projection for a committed parent work unit.

## The projection must

- discover child work units by explicit `parent_work_unit_id`,
- exclude non-dispatchable children,
- exclude already-claimed children,
- bind carriers through the executor capability registry when available,
- enforce effective executor capacity,
- enforce overlapping-write exclusion,
- and separate selected claims from deferred claims with explicit reasons.

## Acceptance proof

- `ION/tests/test_kernel_allocator.py`
- `ION/tests/test_kernel_operator_cli.py`
