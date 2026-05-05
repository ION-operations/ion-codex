# ION V106 Core Telemetry Triad And Runtime Floor Repair Report

## Scope

V106 converts the user-requested telemetry triad and the immediate runtime-status blocker into repeatable ION surfaces.

## Implemented Surfaces

- Lane timeline projection and JOC panel:
  - `ION/04_packages/kernel/ion_lane_timeline_view_model.py`
  - `ION/08_ui/joc_cockpit_shell/LaneTimelinePanel.tsx`
  - `ION/tests/test_kernel_ion_lane_timeline_view_model.py`
- Receipt hydration projection and JOC panel:
  - `ION/04_packages/kernel/ion_receipt_hydration_mapper.py`
  - `ION/08_ui/joc_cockpit_shell/ReceiptHydrationPanel.tsx`
  - `ION/tests/test_kernel_ion_receipt_hydration_mapper.py`
- Runtime debug overlay projection and JOC panel:
  - `ION/04_packages/kernel/ion_runtime_debug_overlay.py`
  - `ION/08_ui/joc_cockpit_shell/RuntimeDebugOverlayPanel.tsx`
  - `ION/tests/test_kernel_ion_runtime_debug_overlay.py`
- Cursor hook state projection:
  - `ION/04_packages/kernel/ion_cursor_hook_state.py`
  - `ION/03_registry/ion_cursor_hook_state.schema.json`
  - `ION/tests/test_kernel_ion_cursor_hook_state.py`
- Codex extension carrier mount proof:
  - `ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md`
  - `ION/03_registry/codex_extension_carrier_profile.yaml`
  - `ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md`
  - `ION/04_packages/kernel/ion_codex_extension_carrier_audit.py`
  - `ION/tests/test_kernel_ion_codex_extension_carrier_audit.py`
  - `ION/05_context/current/CODEX_EXTENSION_CARRIER_AUDIT_V106.json`
- Lifecycle package materialization:
  - `ION/04_packages/kernel/ion_lifecycle_packager.py`
  - `ION/06_artifacts/packages/ION_COMPACT_RUNTIME_V106_20260502.zip`
  - `ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json`
- Front-door deterministic proof trace:
  - `ION/04_packages/kernel/ion_front_door_proof_trace.py`
  - `ION/03_registry/ion_front_door_proof_trace.schema.json`
  - `ION/08_ui/joc_cockpit_shell/FrontDoorProofTracePanel.tsx`
  - `ION/tests/test_kernel_ion_front_door_proof_trace.py`
  - `ION/05_context/current/ACTIVE_FRONT_DOOR_PROOF_TRACE.json`
- Active-state integrity audit:
  - `ION/04_packages/kernel/ion_active_state_integrity_audit.py`
  - `ION/tests/test_kernel_ion_active_state_integrity_audit.py`
  - `ION/05_context/current/ACTIVE_STATE_INTEGRITY_AUDIT.json`

## Runtime Floor Result

`kernel.ion_status` now reports:

- `verdict`: `ION_STATUS_READY`
- `missing_state_surfaces`: `[]`
- `objective`: `V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection`
- `cursor_hook_state.status`: `projected_not_connected`
- `cursor_hook_state.cursor_hook_bridge_verdict`: `ION_CURSOR_HOOK_BRIDGE_READY`
- `next_lawful_action`: `continue_or_queue_new_work`
- `codex_extension_carrier_audit`: `ION_CODEX_EXTENSION_CARRIER_READY`
- `compact_runtime_package`: `PACKAGE_ZIP_READY_WITH_EXCLUSIONS`
- `compact_runtime_zip_root_audit`: `ZIP_ROOT_CONFIRMED`
- `compact_runtime_manifest`: `ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json`
- `front_door_proof_trace`: `ION_FRONT_DOOR_PROOF_TRACE_READY`
- `active_state_integrity`: `ION_ACTIVE_STATE_INTEGRITY_READY`

The hook state deliberately separates bridge readiness from live host observation. This shell did not observe a live Cursor sessionStart event, so `live_hook_event_seen` remains `false` and `live_execution_authority` remains `false`.

The front-door proof trace materializes a deterministic path through existing runtime surfaces: operator message, Persona Interface ingress, Relay semantic-boundary packet, Steward routing envelope, runtime session entry, Steward work unit/context package, dispatch packet, Relay return, Persona response, front-stage council receipt, and conversational receipt. It does not claim live autonomous Steward reasoning or production authority.

## Test Hygiene Repair

`ION/tests/test_kernel_ion_operator_queue_human_gate_status.py` now preserves and restores active runtime files during tests. This prevents focused/full test runs from rolling the active objective back to stale V88 packets.

`ION/tests/test_kernel_ion_compiled_role_context_bundle_audit.py` now preserves and restores `ACTIVE_ROLE_SPAWN_PLAN.json`. This prevents compiled-bundle audit tests from leaking `/tmp/pytest-*` context package paths into active runtime projections.

`kernel.ion_active_state_integrity_audit` now scans active runtime JSON for test/temp path contamination and is surfaced by `kernel.ion_status`. If a future test leaks `/tmp/pytest-*` paths into active state, status degrades to `ION_STATUS_DEGRADED` with `next_lawful_action: repair_active_state_integrity`.

Two old synthetic V88 queue items were closed through `kernel.ion_operator_message_queue` with status `superseded_test_residue`.

Five unreadable extraction-damaged files were restored to user-readable permissions before package materialization. The packager now normalizes packaged file permissions to `0644` so unreadable files are not copied forward into newly emitted zips.

## Verification

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q
67 passed in 0.56s
```

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
verdict: ION_STATUS_READY
missing_state_surfaces: []
active_state_integrity: ION_ACTIVE_STATE_INTEGRITY_READY
```

Compact package root proof:

```text
pyproject.toml at archive root: true
ION/REPO_AUTHORITY.md at archive root: true
ACTIVE_FRONT_DOOR_PROOF_TRACE.json included: true
wrapped root entries: 0
execution cycle entries: 0
final zip hash: recorded in LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json
```

## Remaining Boundaries

- Live SSE metrics are not connected in this compact tree; runtime debug overlay marks them `NOT_CONNECTED`.
- Live DB hydration is not connected in this compact tree; receipt hydration is fixture/JSON-adapter ready and forbids recency attachment.
- Codex is mounted as a tool-assisted carrier; host-native subagents remain unproven and gated.
- Full-project and forensic-archive package materialization still need operator-approved receipts; compact runtime materialization is now proven.
- Front-door Relay -> Steward -> Persona -> receipt path is deterministically proven; live host/SSE/DB binding through that same path remains unproven.
- Production authority remains `false`.
