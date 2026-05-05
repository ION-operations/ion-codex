---
type: research
from: Codex
created: 2026-04-04T09:20:00-04:00
status: COMPLETE
topic: First bounded daemon-loop receipt and per-step telemetry slice
connections:
  - ION/04_packages/kernel/daemon_loop.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/05_context/inbox/completed/codex_kernel_loop_receipts_telemetry_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_loop_receipts_telemetry_first_pass/00_trace.md
  - ION/05_context/signals/CODEX_KERNEL_LOOP_RECEIPTS_TELEMETRY_FIRST_PASS_20260404T0920.signal.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_followup_automation_first_pass.md
---

# Codex Kernel Loop Receipts + Telemetry First Pass

## Why this exists

Codex MINI left the next runtime choice explicitly open between:

- richer loop receipts / per-step telemetry
- or bounded review/follow-up resolution

This pass lands the first option first.

The goal is narrow and truthful: repeated daemon runs should now be able to emit a
bounded generated-state receipt plus one system-ledger append that makes the run
inspectable without pretending that the daemon is already a fully autonomous service.

## Sources or surfaces considered

- `ION/04_packages/kernel/daemon_loop.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_signal_followup_automation_first_pass.md`

## Findings

- `ION/04_packages/kernel/daemon_loop.py` now widens `DaemonLoopResult` with:
  - `run_id`
  - `started_at`
  - `completed_at`
  - `receipt_path`
  - `ledger_path`
- `run_until_blocked(...)` now accepts bounded generated-state output lanes:
  - `history_dir`
  - `loop_receipts_dir`
- When `workspace_root` is provided, one daemon run now writes:
  - one durable loop receipt JSON under `ION/05_context/history/daemon_loop_receipts/`
  - one appended `daemon_loop_run` row into `ION/05_context/history/system_ledger.json`
- The receipt includes explicit step telemetry per daemon step:
  - chosen action type
  - step status and reason
  - work/delta identifiers when present
  - dispatch packet path when dispatch occurred
  - signal interpretation / archive data when signal consumption occurred
  - created review or follow-up question identifiers when they were materialized
- `ION/tests/test_kernel_daemon_loop.py` now proves the widened boundary directly:
  - a signal -> dispatch -> idle run can emit a durable loop receipt
  - the same run appends one bounded `system_ledger.json` row
  - the receipt exposes the per-step action trace rather than only the terminal status
- The combined kernel suite is now at **114 passing tests**.

## Boundary

- This is generated-state runtime witness material, not governing authority.
- It does not resolve review or follow-up pressure by itself.
- It does not yet create a long-running service ledger or broad observability stack.
- It keeps the first pass at the daemon-loop boundary rather than widening every helper
  into its own telemetry system.

## Implications

- Repeated daemon runs now leave a bounded machine-readable witness trail.
- The runtime frontier narrows again:
  - bounded review/follow-up resolution should now land next
  - then the field can decide whether signal follow-up may ever issue child work
    directly instead of remaining pressure-only
- The new receipt/ledger surfaces also make future MCP or service extraction safer,
  because loop behavior can be inspected without overreading chat narration as proof.

## Recommended next moves

- Build bounded review/follow-up resolution next.
- After that, decide whether signal follow-up should ever issue child work directly
  or remain a pressure-only bridge until the planner layer is stronger.
