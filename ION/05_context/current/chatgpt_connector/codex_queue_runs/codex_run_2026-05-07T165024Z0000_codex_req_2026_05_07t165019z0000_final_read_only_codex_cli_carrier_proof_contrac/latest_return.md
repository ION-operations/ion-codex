### CONTEXT PROOF

Read-only context paths inspected with SHA-256 and line evidence:

- `ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T165019Z0000_final_read_only_codex_cli_carrier_proof_contract_smoke_for_sev_after_exact_templ.json` sha256 `11eefcc5317fa0e3ede5cfb70d69f82a08f62ce1eb7b580dfa4cd9b2d44a1df8`; lines 8, 14-15 show read-only objective, schema `ion.chatgpt_browser_connector_codex_work_request.v1`, status `CLAIMED_BY_CODEX_QUEUE_RUNNER`.
- `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T165024Z0000_codex_req_2026_05_07t165019z0000_final_read_only_codex_cli_carrier_proof_contrac/context_receipt.json` sha256 `38d4c356fab5e97dd8ad3412eece25abfcb9046f8027817bcdb561155430ca76`; lines 2, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55 enumerate required reads; line 59 schema `ion.context_load_receipt.v1`.
- `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` sha256 `56f725f2a32afce3ccb3baffe11bc6db16d534aeca9a60b8430292ea968763c7`; lines 12, 14, 16 show this objective, request id, and claimed status; line 377 schema.
- `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json` sha256 `813e2d6ed5a620fcb608554d667b70db569388a79c5378cc54cb4451cd644dae`; lines 4 and 131 show messages queue and schema `ion.carrier_message_queue.v1`.
- `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py` sha256 `700c56d23a0f61afc568c0628cbcd17a1227315a1a6486aa50f79107a20f4b17`; lines 42-44 define connector state/work/carrier-message queues; lines 127-138 include bounded queue tools including `ion_codex_queue_process_once`.
- `ION/04_packages/kernel/ion_carrier_task_return.py` sha256 `516e39db4f44d5aaf85023b7fa94713f8d2fb018597f01e86c6dc9c82f0e8a28`; lines 229-235 evaluate context/template proof; lines 265-267 record `template_id`, `action_id`, `touched_paths`.
- `ION/04_packages/kernel/ion_carrier_continue.py` sha256 `761797140d37a38fd1ca2a3c2da5239a4e2e08169d825af9f50c9f01c05bb72f`; lines 3-5 describe safe continue behavior without production authority; lines 440-441 set authorities false.
- `ION/04_packages/kernel/ion_codex_queue_runner.py` sha256 `7b8be86fe3f463f126922f509614587e61f2eb9d44eb25ba39a0882b822f8475`; lines 285-301 embed required return sections plus exact `template_id`, `action_id`, `result`, `touched_paths` prompt shape.
- `ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md` sha256 `53fdd493c216c3974c826ef80473aa359d7a600791d72c37e2531e20fa7b555e`; lines 17-20 deny production/live/credential/delete/git-push authority; lines 350-361 describe Codex queue automation.
- `ION/03_registry/chatgpt_browser_carrier_profile.yaml` sha256 `74d56f18f94b0b92d289f6f063717fc8c1cc5702b6c7c0e6aec161df4e949181`; lines 1-2 identify schema/carrier; lines 58-60 set authorities false.
- `ION/03_registry/codex_cli_carrier_profile.yaml` sha256 `b83c081562482ebd44399830722784f5a09f293964dea8f7dd75c9afa3c8b0c6`; lines 1-2 identify schema/carrier; lines 42-43 set authorities false.
- `ION/04_packages/kernel/ion_cockpit_view_model.py` sha256 `384a2a51ad477dd379b8539edafb6535071fad453b858627cfd40e2572e3f8f8`; lines 345-347 read carrier/work queues; line 407 includes Codex runner status; lines 411-412 set authorities false.
- Run packet also inspected: `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T165024Z0000_codex_req_2026_05_07t165019z0000_final_read_only_codex_cli_carrier_proof_contrac/run.json` sha256 `eec61283a52045e1e23b1b695ce151e99fb94787e3a8f594fd89e5552aa80399`; lines 14, 16, 23, 25 show authorities false, schema, and `CODEX_CLI_RUNNING`.

### TEMPLATE ACTION PROOF
template_id: ion.template.autonomous_loop.local_worker.v1
action_id: codex_queue_runner_process_once
result: read_only_proof_contract_smoke_completed_no_edits
touched_paths:
  - ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T165019Z0000_final_read_only_codex_cli_carrier_proof_contract_smoke_for_sev_after_exact_templ.json
  - ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T165024Z0000_codex_req_2026_05_07t165019z0000_final_read_only_codex_cli_carrier_proof_contrac/context_receipt.json
  - ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T165024Z0000_codex_req_2026_05_07t165019z0000_final_read_only_codex_cli_carrier_proof_contrac/run.json
  - ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
  - ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json
  - ION/04_packages/kernel/ion_codex_queue_runner.py

### VALIDATION

Read-only validation completed. `sha256sum` was run on all required context paths plus the run packet. `jq -e type` succeeded for the JSON work request, context receipt, run packet, active Codex work queue, and active carrier message queue. `rg -n`/`nl -ba` were used for line evidence. `git status --short` was read-only and showed an already dirty/untracked worktree; I made no edits, deletions, commits, pushes, deployments, or secret reads.

### RESULT

Touched paths are the inspected evidence paths listed in `touched_paths`; no changed paths were created by this carrier. Tests: no test suite was run because this was a read-only proof-contract smoke; validation was limited to parse/hash/line-evidence checks. Remaining blockers: none for this read-only return. Next lawful moves: existing queue/task-return intake can record and proof-gate this response; if intake rejects formatting, rerun the same read-only smoke with the same required sections and non-empty `touched_paths`.