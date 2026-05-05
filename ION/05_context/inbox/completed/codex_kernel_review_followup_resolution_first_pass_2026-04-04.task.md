---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T09:45:00-04:00
from: Sovereign
target: ION/04_packages/kernel/signal_followups.py
depends_on: ION/04_packages/kernel/daemon_loop.py
status: COMPLETE
updated: 2026-04-04T10:15:00-04:00
completed_by: Codex
---

# Mission: Implement the first bounded review/follow-up resolution slice

## Goal

Widen the active signal-follow-up path just enough that later completion signals can
lawfully resolve existing `signal_followup` and `validation_review` pressure when the
current runtime has bounded completion evidence, while keeping direct child-work issuance
out of signal-follow-up for now.

## Source / Context

- `ION/03_registry/boots/CODEX.boot.md`
- `ION/agents/codex/MINI.md`
- `ION/agents/codex/CAPSULE.md`
- `ION/04_packages/kernel/signal_followups.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/daemon_loop.py`
- `ION/tests/test_kernel_signal_followups.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the pass bounded and truthful.
2. Resolve only review/follow-up pressure the current runtime can actually prove was superseded.
3. Preserve the existing review-escalation path rather than replacing it.
4. Surface the new resolution behavior in daemon-loop telemetry.
5. Make an explicit build-facing determination on whether signal follow-up may issue child work directly.
6. Add focused tests for direct helper behavior plus daemon and loop behavior.

## Deliverables

- widened `ION/04_packages/kernel/signal_followups.py`
- widened `ION/04_packages/kernel/daemon_loop.py`
- patched focused tests for signal-follow-up, daemon-actions, and daemon-loop behavior
- one research note for review/follow-up resolution plus the child-work determination
- one completion signal announcing the slice

## Constraints

1. Do not claim a full replanner, retry engine, or reviewer runtime already exists.
2. Do not let completion signals silently resolve pressure tied to the same delta that created it.
3. Do not issue child work directly from signal follow-up in this pass.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Signal

Emit one Codex signal pointing to the review/follow-up resolution first-pass result.

## Completion Record — 2026-04-04T10:15:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Widened the signal-follow-up layer so later completion signals can resolve older `signal_followup` and `validation_review` pressure with bounded completion evidence, exposed the new resolution path in daemon-loop telemetry, and kept signal follow-up pressure-only for child work in the current build.
- artifacts:
  - ION/04_packages/kernel/signal_followups.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/tests/test_kernel_signal_followups.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/06_intelligence/research/2026-04-04_codex_kernel_review_followup_resolution_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_REVIEW_FOLLOWUP_RESOLUTION_FIRST_PASS_20260404T1015.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_review_followup_resolution_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_signal_followups.py tests/test_kernel_daemon_actions.py tests/test_kernel_daemon_loop.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Keep signal follow-up pressure-only for child work until a stronger planner/manifest layer exists; next runtime work should make reviewer/follow-up answer ingestion or planner-gated retry issuance explicit instead of implicit.
- note: Completed by Codex under the explicit CODEX__CODE binding; this pass widens lawful resolution only and does not ratify a broader recovery daemon.
