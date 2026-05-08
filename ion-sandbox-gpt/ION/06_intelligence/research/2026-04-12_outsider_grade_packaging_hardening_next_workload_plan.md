---
type: research
authority: A3_OPERATIONAL
from: Codex
created: 2026-04-12T15:13:15-04:00
status: COMPLETE
ratification: SUPERSEDED_BY_COMPLETION
topic: Next workload plan for outsider-grade packaging hardening after current-generation ratification was withheld
completion_artifact: ION/05_context/signals/MASON_PACKAGING_ENTRY_HARDENING_20260412T161500.signal.md
connections:
  - ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_assessment.md
  - ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_record.md
  - ION/06_intelligence/orchestration/2026-04-12_ion_acceptance_evidence_bundle_current_state.md
  - ION/06_intelligence/orchestration/2026-04-09_ion_current_state_vs_end_state_roadmap.md
  - ION/04_packages/kernel/operator_cli.py
  - ION/04_packages/kernel/__init__.py
---

# Outsider-Grade Packaging Hardening Next Workload Plan

## Why this is next

The current-generation ratification assessment withheld final ratification not because
the branch lacks proof, but because entry still depends on extracted-root execution
posture:

- `PYTHONPATH=ION/04_packages pytest -q`
- `PYTHONPATH=ION/04_packages python -m kernel ...`

That posture is workable for current development, but it is weaker than outsider-grade
entry and therefore keeps `Extension readiness` at partial status.

## Bounded objective

Land the minimum install/import/CLI surface required so a fresh operator or executor can
use the branch without mandatory manual `PYTHONPATH` wiring.

## Expected target surfaces

- branch-root packaging metadata if that proves to be the cleanest lawful entry surface
- minimal import / module-resolution adjustments only if packaging metadata alone is not
  sufficient
- bounded proof coverage for install/import/CLI entry

## Non-goals

This workload should **not**:

- widen bridge packet canon or validator law
- alter packet semantics
- change scheduler or orchestration behavior
- repack the entire estate outside the current working branch

## Required reads before implementation

1. `ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_assessment.md`
2. `ION/06_intelligence/orchestration/2026-04-12_ion_acceptance_evidence_bundle_current_state.md`
3. `ION/06_intelligence/orchestration/2026-04-09_ion_current_state_vs_end_state_roadmap.md`
4. `ION/04_packages/kernel/operator_cli.py`
5. `ION/04_packages/kernel/__init__.py`

## Verification target

The slice succeeds when the branch can prove a truthful improvement in entry posture,
ideally reducing or removing mandatory manual `PYTHONPATH` setup for:

- importing `kernel`
- running `python -m kernel ...`
- and the bounded test entry surface

without changing kernel behavior.

## Carrier posture

This is now a valid `Mason` workload once packetized.

## Outcome

This workload is now complete.

Completion surface:

- `ION/05_context/signals/MASON_PACKAGING_ENTRY_HARDENING_20260412T161500.signal.md`
