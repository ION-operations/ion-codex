---
type: orchestration_verification
authority: A3_OPERATIONAL
created: 2026-04-17T18:03:49-04:00
status: ACTIVE
purpose: Record the first durable current-carrier exercise receipt for the q004 root-authority startup bundle
connections:
  - ION/06_intelligence/decisions/2026-04-17_root_authority_carrier_export_bundle_canonicalization_decision.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/CURSOR_CODEX_READ_MODE.md
  - ION/05_context/history/kernel_store/root_authority_bundle_exercise_receipts/root-authority-bundle-exercise-cursor-codex-2026-04-17t18-03-49-04-00.json
  - ION/04_packages/kernel/root_authority_bundle.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_root_authority_bundle.py
  - ION/tests/test_root_authority_bundle_cli.py
---

# Root-authority bundle current-carrier exercise receipt

## Purpose

Move q004 past modeled read-test only.

The bundle was already stable as a startup export and already had static and CLI
proof. This pass adds one real stored exercise receipt from the current carrier
posture so the branch no longer depends on notes alone to prove that the bundle
has been entered successfully under its intended local packaging mode.

## Exercise performed

The exercise was run from the extracted branch shell root under branch-local
editable-install posture.

Command class:

- `python -m kernel bundle --workspace-root . --format json record-exercise --carrier-key cursor_codex --execution-mode BRANCH_LOCAL_EDITABLE_INSTALL --executor CODEX`

Result:

- receipt id: `root-authority-bundle-exercise-cursor-codex-2026-04-17t18-03-49-04-00`
- bundle status: `READ_TESTED_STABLE_STARTUP_EXPORT`
- carrier key: `cursor_codex`
- execution mode: `BRANCH_LOCAL_EDITABLE_INSTALL`
- valid: `true`
- missing paths: none

Persisted receipt:

- `ION/05_context/history/kernel_store/root_authority_bundle_exercise_receipts/root-authority-bundle-exercise-cursor-codex-2026-04-17t18-03-49-04-00.json`

## What this proves

This proves that the current branch can:

- resolve the emitted q004 bundle from the lawful shell-root position
- validate that bundle through the operator CLI
- persist one durable kernel receipt proving successful current-carrier startup
  exercise

## What this does not prove

This does not prove:

- browser or Claude execution parity
- top-level production transport-shell promotion
- final single-root canon

Those remain separate bounded packets.
