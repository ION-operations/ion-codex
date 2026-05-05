workstream: implementation
objective: Implement the first bounded daemon-loop receipt and telemetry slice.
required_surfaces_ok: True

1. codex — follow boot, MINI, CAPSULE, and the active routed kernel/runtime surfaces
   - codex.boot: ION/03_registry/boots/CODEX.boot.md
   - codex.private_mini: ION/agents/codex/MINI.md
   - codex.private_capsule: ION/agents/codex/CAPSULE.md
   - codex.directive: ION/06_intelligence/roundtable/continuity_crisis/responses/2026-04-03_sovereign_directive_manual_auto_and_model_allocation.md
   - codex.binding: ION/07_templates/bindings/CODEX__CODE.md

2. codex — choose the next bounded slice from MINI `NEXT:` without inventing a new frontier
   - chosen branch: richer loop receipts / per-step telemetry
   - deferred branch: bounded review/follow-up resolution

3. codex — widen the daemon loop truthfully
   - target: ION/04_packages/kernel/daemon_loop.py
   - supporting test surface: ION/tests/test_kernel_daemon_loop.py
   - generated-state witness lane: ION/05_context/history/system_ledger.json

4. codex — verify the widened runtime boundary
   - focused test: PYTHONPATH=04_packages pytest -q tests/test_kernel_daemon_loop.py
   - full suite: PYTHONPATH=04_packages pytest -q

5. codex — file visible continuity artifacts
   - completed task: ION/05_context/inbox/completed/codex_kernel_loop_receipts_telemetry_first_pass_2026-04-04.task.md
   - research note: ION/06_intelligence/research/2026-04-04_codex_kernel_loop_receipts_telemetry_first_pass.md
   - signal: ION/05_context/signals/CODEX_KERNEL_LOOP_RECEIPTS_TELEMETRY_FIRST_PASS_20260404T0920.signal.md
