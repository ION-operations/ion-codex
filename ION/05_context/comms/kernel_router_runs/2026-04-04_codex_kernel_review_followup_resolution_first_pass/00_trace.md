workstream: implementation
objective: Implement the first bounded review/follow-up resolution slice and file the build-facing child-work policy.
required_surfaces_ok: True

1. codex — follow boot, MINI, CAPSULE, directive, and the routed kernel/runtime surfaces
   - codex.boot: ION/03_registry/boots/CODEX.boot.md
   - codex.private_mini: ION/agents/codex/MINI.md
   - codex.private_capsule: ION/agents/codex/CAPSULE.md
   - codex.directive: ION/06_intelligence/roundtable/continuity_crisis/responses/2026-04-03_sovereign_directive_manual_auto_and_model_allocation.md
   - codex.binding: ION/07_templates/bindings/CODEX__CODE.md

2. codex — take the next runtime slice exactly from MINI `NEXT:`
   - chosen branch: bounded review/follow-up resolution
   - companion determination: signal follow-up remains pressure-only for child work in the current build

3. codex — widen the signal-follow-up truthfully
   - target: ION/04_packages/kernel/signal_followups.py
   - supporting runtime witness: ION/04_packages/kernel/daemon_loop.py
   - supporting tests:
     - ION/tests/test_kernel_signal_followups.py
     - ION/tests/test_kernel_daemon_actions.py
     - ION/tests/test_kernel_daemon_loop.py

4. codex — keep the boundary explicit
   - completion signals may resolve existing `signal_followup` and `validation_review` questions when they lawfully supersede older pressure
   - signal follow-up does not issue child work directly in this pass

5. codex — verify the widened runtime boundary
   - focused test: PYTHONPATH=04_packages pytest -q tests/test_kernel_signal_followups.py tests/test_kernel_daemon_actions.py tests/test_kernel_daemon_loop.py
   - full suite: PYTHONPATH=04_packages pytest -q

6. codex — file visible continuity artifacts
   - completed task: ION/05_context/inbox/completed/codex_kernel_review_followup_resolution_first_pass_2026-04-04.task.md
   - research note: ION/06_intelligence/research/2026-04-04_codex_kernel_review_followup_resolution_first_pass.md
   - signal: ION/05_context/signals/CODEX_KERNEL_REVIEW_FOLLOWUP_RESOLUTION_FIRST_PASS_20260404T1015.signal.md
