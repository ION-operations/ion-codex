# Codex CLI Carrier And Cockpit Pass

created_at: 2026-05-07
updated_at: 2026-05-07T18:56:06Z
status: implementation_pass_completed_with_codex_queue_smoke_acceptance
active_root: `/home/sev/ION - Production/ION_CODEX FULL`
carrier_context: Codex working as bounded local implementation carrier for Sev.
production_authority: false
live_execution_authority: false

## Objective

Advance the full Codex CLI carrier setup and local ION cockpit/UI path after the
Custom GPT Action Gateway and MCP JSON-RPC action surfaces became reachable.

This pass does not claim ION identity, production readiness, live execution
authority, Steward acceptance, or state inheritance from AI output.

## Context Proof

Required/current context read before implementation:

- `workpackets/ION_ACTIONS_CODEX_IDE_FULL_EXECUTION_PLAN_2026-05-07.md`
- `workpackets/ION_LOCAL_CODEX_IDE_MVP_PACKET_2026-05-07.md`
- `workpackets/ION_CODEX_CLI_PACKET_001_ACTION_GATEWAY_MVP_2026-05-07.md`
- `workpackets/ION_CUSTOM_GPT_ACTIONS_LOCAL_ION_BRIDGE_STRATEGY_2026-05-07.md`
- `ION/05_context/current/ACTIVE_WORK_PACKET.json`
- `ION/05_context/current/codex_cli/gpt55_lead_mount_prompt_v126.md`
- `ION/05_context/current/codex_cli/latest_return.md`
- `ION/04_packages/kernel/ion_codex_queue_runner.py`
- `ION/04_packages/kernel/ion_cockpit_view_model.py`
- `ION/04_packages/kernel/ion_agent_invocation_broker.py`
- `ION/04_packages/kernel/ion_local_service_status.py`
- `ION/09_integrations/cursor_extension/`
- `ION/08_ui/joc_cockpit_shell/`

Current proof observations:

- `codex --version` returns `codex-cli 0.128.0`.
- `kernel.ion_status` reports `ION_STATUS_READY`.
- `kernel.ion_codex_cli_carrier_audit` reports `ION_CODEX_CLI_CARRIER_READY`.
- `kernel.ion_codex_queue_runner --status --json` reports ready with no active run and queued request count `0`.
- The persistent local service stack is active.
- The Custom GPT action tests report Gateway auth and MCP read/status paths working against the `ION_CODEX FULL` root.

## Implementation Plan

1. Preserve the active root and avoid old `ION_CODEX` path writes.
2. Keep Codex queue and agent status reads non-mutating when projected into MCP/cockpit/UI surfaces.
3. Add a local-only cockpit app that can render ION runtime, service, Codex queue, MCP, and receipt status without depending on the unbuilt Cursor extension package.
4. Add the cockpit app to the local user-service projection and systemd template set.
5. Verify with focused Python tests and local HTTP smoke checks.
6. Start the local cockpit app as a user service if the unit renders cleanly on this host.

## Work Completed In This Pass

- Added `kernel.ion_local_cockpit_app`, a dependency-free localhost cockpit app.
- Added `ion-cockpit-app.service.template` for a persistent local UI service on `127.0.0.1:8788`.
- Added cockpit app coverage in `ION/tests/test_kernel_ion_local_cockpit_app.py`.
- Updated local service projection to include the cockpit app.
- Updated systemd user-service README to include the cockpit app and the corrected `ION_CODEX FULL` root.
- Updated cockpit projection and agent broker read paths so embedded Codex queue status uses `reconcile=False`.
- Updated Codex queue runner worker startup so the worker records its real PID in runner state.
- Tightened the Codex queue runner prompt contract to require exact `template_id`, `action_id`, `result`, and non-empty `touched_paths` fields.
- Updated focused tests for the six-service stack and read-only Codex queue projection.

## Validation So Far

Passed:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m compileall -q \
  ION/04_packages/kernel/ion_local_cockpit_app.py \
  ION/04_packages/kernel/ion_local_service_status.py \
  ION/04_packages/kernel/ion_cockpit_view_model.py \
  ION/04_packages/kernel/ion_agent_invocation_broker.py
```

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  ION/tests/test_kernel_ion_local_cockpit_app.py \
  ION/tests/test_kernel_ion_local_service_status.py \
  ION/tests/test_kernel_ion_cockpit_view_model.py \
  ION/tests/test_kernel_ion_agent_invocation_broker.py \
  ION/tests/test_kernel_ion_codex_queue_runner.py -q
```

Result:

```text
24 passed
```

Local HTML render proof:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_local_cockpit_app --ion-root . --html
```

Confirmed rendered surface includes:

- `ION LOCAL COCKPIT`
- `ION_CODEX_QUEUE_RUNNER_READY`
- `ion-cockpit-app.service`

## Final Validation

Persistent local cockpit service:

```text
ion-cockpit-app.service: active
```

Local cockpit endpoints:

```text
http://127.0.0.1:8788/health -> ION_LOCAL_COCKPIT_APP_READY
http://127.0.0.1:8788/model.json -> ion.cockpit_view_model.v1
http://127.0.0.1:8788/ -> renders ION LOCAL COCKPIT
```

Six-service local stack:

```text
ion-chatops.service: active
ion-mcp-preview.service: active
ion-mcp-tunnel.service: active
ion-action-gateway.service: active
ion-action-tunnel.service: active
ion-cockpit-app.service: active
```

Public connector health:

```text
https://ion.helixion.net/health -> accepted true
https://ion-actions.helixion.net/health -> ok true
```

Refreshed active projection:

```text
ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
shell_root: /home/sev/ION - Production/ION_CODEX FULL
service_count: 6
codex_queue_runner.reconciliation.write: false
```

## Codex Queue Runner Smoke

Three bounded read-only queue smokes were run through the MCP queue path and the
Codex CLI carrier. The first two were useful proof-gate failures; the final run
was accepted after the prompt contract was tightened.

Initial request:

```text
request: ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T163712Z0000_read_only_codex_cli_carrier_loop_smoke_for_sev_read_the_required_context_receipt.json
run: ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T163852Z0000_codex_req_2026_05_07t163712z0000_read_only_codex_cli_carrier_loop_smoke_for_sev_/run.json
result: RETURN_RECORDED_PROOF_BLOCKED
finding: missing_touched_paths
```

Second request after adding non-empty `touched_paths` instruction:

```text
request: ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T164636Z0000_read_only_codex_cli_carrier_loop_proof_contract_smoke_for_sev_after_touched_path.json
run: ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T164647Z0000_codex_req_2026_05_07t164636z0000_read_only_codex_cli_carrier_loop_proof_contract/run.json
result: RETURN_RECORDED_PROOF_BLOCKED
finding: missing_result
```

Final accepted request after adding an exact TEMPLATE ACTION PROOF shape:

```text
request: ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T165019Z0000_final_read_only_codex_cli_carrier_proof_contract_smoke_for_sev_after_exact_templ.json
run: ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T165024Z0000_codex_req_2026_05_07t165019z0000_final_read_only_codex_cli_carrier_proof_contrac/run.json
task_return: ION/05_context/current/chatgpt_connector/task_returns/2026-05-07T165325Z0000_task_return.json
result: RETURN_RECORDED_PROOF_ACCEPTED
context_proof_accepted: true
template_action_proof_accepted: true
findings: []
returncode: 0
```

Post-smoke status:

```text
active_process_running: false
active_run: null
queued_request_count: 0
latest_run.status: RETURN_RECORDED_PROOF_ACCEPTED
```

## Remaining Work After This Pass

- Package or compile the Cursor extension once npm dependencies are installed or vendored.
- Add cockpit service control docs to the broader setup runbook if the operator wants this as the permanent local UI lane.
- Use the accepted queue path for the next bounded implementation packet from the workpackets backlog.

## JOC Dual Chat Workbench Rebuild

Follow-up operator finding: the dual Codex chat was visually too monolithic and
did not follow the JOC cockpit shell pattern.

Implemented repair:

- Refactored `kernel.ion_dual_codex_chat.render_dual_codex_chat_html` into a
  JOC-style workbench with a top bar, left command rail, left context drawer,
  central dual-lane workbench, right context/evidence inspector, and bottom ION
  pipeline drawer.
- Preserved existing POST endpoints and hidden confirmation/token mechanics for
  `/turn`, `/queue`, and `/memory`.
- Kept the same shared renderer for local `/chat` and public `/cockpit/chat` so
  local and Cloudflare-served cockpit views stay aligned.
- Changed long Mini/context auto-post turns to compact previews with expandable
  full payloads, so the chat lane does not become a wall of context text.
- Added focused test coverage for the JOC shell markers and preserved form
  routes in `ION/tests/test_kernel_ion_dual_codex_chat.py`.

Authority note: this is a UI projection and queue/memory form surface only. It
does not grant production authority, live execution authority, arbitrary shell,
or git push authority.

## Non-Claims

- This pass does not submit a Gateway action.
- This pass does not claim Steward acceptance beyond the connector task-return proof gate.
- This pass does not package or publish the Cursor extension.
- This pass does not expose the cockpit app publicly.
