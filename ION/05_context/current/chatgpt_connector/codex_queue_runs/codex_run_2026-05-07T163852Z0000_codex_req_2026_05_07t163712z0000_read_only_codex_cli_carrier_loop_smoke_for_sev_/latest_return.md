### CONTEXT PROOF

| Required path | sha256 | line/excerpt evidence |
|---|---|---|
| `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T163852Z0000_codex_req_2026_05_07t163712z0000_read_only_codex_cli_carrier_loop_smoke_for_sev_/context_receipt.json` | `029c6dc0389ca9ae074759cc950a71c732fbc530c4882b70983b555047ec9c2c` | lines 2-57 list all required context reads. |
| `ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T163712Z0000_read_only_codex_cli_carrier_loop_smoke_for_sev_read_the_required_context_receipt.json` | `313124a84a218df1ee339fb71cc87250436063cb6f28dba09899f958b8b30fb5` | lines 10-12 show latest return/objective; lines 18-20 show `RETURN_RECORDED_PROOF_BLOCKED`. |
| `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` | `61536a9c0d1bd7e47e3a85fd8e25e271c4497c703251d42d3cf903294798a274` | lines 2-5 show no authority and `request_count: 25`; lines 10-18 show current return path and blocked status. |
| `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json` | `813e2d6ed5a620fcb608554d667b70db569388a79c5378cc54cb4451cd644dae` | lines 2-4 show queue/messages; lines 24, 52, 79, 102, 126 show pending/acked statuses. |
| `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py` | `700c56d23a0f61afc568c0628cbcd17a1227315a1a6486aa50f79107a20f4b17` | lines 96-123 list status tools; lines 125-140 list bounded queue/receipt tools. |
| `ION/04_packages/kernel/ion_carrier_task_return.py` | `516e39db4f44d5aaf85023b7fa94713f8d2fb018597f01e86c6dc9c82f0e8a28` | lines 229-238 evaluate context/template gates; lines 250-269 record template/action/touched path proof. |
| `ION/04_packages/kernel/ion_carrier_continue.py` | `761797140d37a38fd1ca2a3c2da5239a4e2e08169d825af9f50c9f01c05bb72f` | lines 1-5 state no live external execution/production authority; lines 401-413 list proof-gated carrier actions. |
| `ION/04_packages/kernel/ion_codex_queue_runner.py` | `96fc22d578df124ec77a401527d4c6dd1ecfe6a85637af69a7e287cfac5bf0e9` | lines 1-6 define bounded runner/no arbitrary shell; lines 278-292 define required sections/template/action requirement. |
| `ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md` | `53fdd493c216c3974c826ef80473aa359d7a600791d72c37e2531e20fa7b555e` | lines 17-20 deny authority grants; lines 350-361 define Codex queue automation owner and limits. |
| `ION/03_registry/chatgpt_browser_carrier_profile.yaml` | `74d56f18f94b0b92d289f6f063717fc8c1cc5702b6c7c0e6aec161df4e949181` | lines 2-6 define `CHATGPT_BROWSER_CARRIER`/Sev as continuity label only; lines 28-33 forbid direct shell/delete/push/credentials. |
| `ION/03_registry/codex_cli_carrier_profile.yaml` | `b83c081562482ebd44399830722784f5a09f293964dea8f7dd75c9afa3c8b0c6` | lines 2-10 define `CODEX_CLI_CARRIER` capabilities; lines 17-24 bind proof gates/profile; lines 38-41 forbid push/credential/unbounded/delete paths. |
| `ION/04_packages/kernel/ion_cockpit_view_model.py` | `384a2a51ad477dd379b8539edafb6535071fad453b858627cfd40e2572e3f8f8` | lines 341-407 read queue/message/service inputs; lines 437-530 build the cockpit model. |

### TEMPLATE ACTION PROOF

```yaml
template_id: ion.template.autonomous_loop.local_worker.v1
action_id: codex_queue_runner_process_once
result: READ_ONLY_CONTEXT_SMOKE_COMPLETED
touched_paths: []
production_authority: false
live_execution_authority: false
```

### VALIDATION

Read-only checks run: `nl`, `sed`, `rg`, `jq`, `sha256sum`, `stat`, and `ps -p 436387 -o pid=,stat=`. No edits, deletes, git pushes, deployments, or secret reads were performed.

Current Codex queue: 25 requests. Status counts are 13 `RETURN_RECORDED_PROOF_ACCEPTED`, 2 `RETURN_RECORDED_PROOF_BLOCKED`, 1 `FULFILLED_BY_LOCAL_BRANCH_WORK_PENDING_TASK_RETURN`, 2 `PREPARED_FOR_CODEX_CARRIER_NOT_QUEUED`, 2 invalid placeholders, and 5 superseded/archive statuses. The smoke request is now `RETURN_RECORDED_PROOF_BLOCKED`.

Runner state: `active_run: null`; latest run is `RETURN_RECORDED_PROOF_BLOCKED` with `returncode: 0`, `failure_classification: BACKEND_CODEX_FAILURE`, context proof accepted, template action proof rejected for missing `template_id`, `action_id`, `result`, and `touched_paths` in the already-recorded return.

Local cockpit/service status: cockpit runtime is `ready`; top bar reports `local_service_status: configured`, 6 services, 0 missing templates. Runtime debug overlay is `degraded` with SSE/watcher `NOT_CONNECTED`. Local services are configured but HTTP probing is disabled.

### RESULT

Touched paths by this read-only inspection: `[]`.

Observed queue-runner outputs already present/updated during the run: the work request, active Codex work queue, runner state, run packet, `stdout.log`, `stderr.log`, `latest_return.md`, and `ION/05_context/current/chatgpt_connector/task_returns/2026-05-07T164245Z0000_task_return.json`.

Tests: none run; this was a read-only smoke/status packet.

Remaining blockers: the recorded task return is proof-blocked on template-action fields; cockpit projection appears stale versus the latest queue run; runtime debug overlay is not connected; 3 carrier messages remain pending for `CHATGPT_BROWSER_CARRIER`.

Next lawful moves: resubmit or rerun the task return with the required template/action/result/touched-path proof fields, refresh cockpit projection under an explicit write-authorized action, optionally run read-only service probes, and acknowledge/poll pending carrier messages.