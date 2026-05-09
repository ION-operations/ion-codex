### CONTEXT PROOF

Read required work request and context receipt first.

- `ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T164636Z0000_read_only_codex_cli_carrier_loop_proof_contract_smoke_for_sev_after_touched_path.json` sha256 `c2ac1970c74168fa7f0cc0bab35eb35ec1d8b3ac5bda6648316cc0bbeac81e29`; lines 7-9: no live/prod authority objective and packet path; lines 14-16: schema/status `CLAIMED_BY_CODEX_QUEUE_RUNNER`.
- `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T164647Z0000_codex_req_2026_05_07t164636z0000_read_only_codex_cli_carrier_loop_proof_contract/context_receipt.json` sha256 `37fe5987e0209880bf32451df1f7f81af17aa5ceee2350f3f72fa3cbf993cfd2`; lines 2-57 list required context reads; line 59 schema `ion.context_load_receipt.v1`.

Receipt-required paths inspected:

- `ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json` sha256 `e8d660990b1fd27b174a8e39698dde4a64f6c69fed5f08ccbb9fe8d70d6755b3`; lines 2-4 no live/prod authority and queue path; lines 12-16 current smoke objective/status.
- `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json` sha256 `813e2d6ed5a620fcb608554d667b70db569388a79c5378cc54cb4451cd644dae`; lines 3-4 live authority false/messages; lines 130-131 production false and schema.
- `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py` sha256 `700c56d23a0f61afc568c0628cbcd17a1227315a1a6486aa50f79107a20f4b17`; lines 3-5 forbid arbitrary shell/writes/deletion/git push/credentials; lines 1136-1156 evaluate context/template proof; lines 1297-1308 route `ion_codex_queue_process_once`.
- `ION/04_packages/kernel/ion_carrier_task_return.py` sha256 `516e39db4f44d5aaf85023b7fa94713f8d2fb018597f01e86c6dc9c82f0e8a28`; lines 229-238 run context/template proof gates; lines 265-267 record template/action/touched_paths.
- `ION/04_packages/kernel/ion_carrier_continue.py` sha256 `761797140d37a38fd1ca2a3c2da5239a4e2e08169d825af9f50c9f01c05bb72f`; lines 3-6 safe continuation, no live execution or production authority; lines 650-659 return queue/status paths.
- `ION/04_packages/kernel/ion_codex_queue_runner.py` sha256 `387b6eeb1ef7df1195473873e87ce8d990af3b2048ac49f42fa9ba3204542c21`; lines 1-6 bounded runner over existing queue; lines 56-67 default required context reads; lines 283-293 required proof/touched_paths contract.
- `ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md` sha256 `53fdd493c216c3974c826ef80473aa359d7a600791d72c37e2531e20fa7b555e`; lines 17-20 no production/live/shell/credential/delete/git-push grant; lines 350-360 define queue automation owner and run receipts.
- `ION/03_registry/chatgpt_browser_carrier_profile.yaml` sha256 `74d56f18f94b0b92d289f6f063717fc8c1cc5702b6c7c0e6aec161df4e949181`; lines 1-6 carrier/callsign only; lines 29-32 no shell/delete/git-push/credentials; lines 58-60 no authority.
- `ION/03_registry/codex_cli_carrier_profile.yaml` sha256 `b83c081562482ebd44399830722784f5a09f293964dea8f7dd75c9afa3c8b0c6`; lines 1-3 Codex CLI carrier identity; lines 17-20 identity/proof gates; lines 32-43 forbidden claims and no authority.
- `ION/04_packages/kernel/ion_cockpit_view_model.py` sha256 `384a2a51ad477dd379b8539edafb6535071fad453b858627cfd40e2572e3f8f8`; lines 345-407 read carrier queue/work queue and queue runner status; lines 410-412 adapter gap plus no production/live authority.

Supporting run packet inspected: `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T164647Z0000_codex_req_2026_05_07t164636z0000_read_only_codex_cli_carrier_loop_proof_contract/run.json` sha256 `eb0c904a852e3fa4d0709bd2914a1fe55f74443aebb050a1fb88186f71012598`; lines 14-16 no live/prod authority; lines 17-22 prompt/request/run packet paths; line 25 `CODEX_CLI_RUNNING`.

### TEMPLATE ACTION PROOF

template_id: ion.template.autonomous_loop.local_worker.v1
action_id: codex_queue_runner_process_once
touched_paths:
  - ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-07T164636Z0000_read_only_codex_cli_carrier_loop_proof_contract_smoke_for_sev_after_touched_path.json
  - ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T164647Z0000_codex_req_2026_05_07t164636z0000_read_only_codex_cli_carrier_loop_proof_contract/context_receipt.json
  - ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-07T164647Z0000_codex_req_2026_05_07t164636z0000_read_only_codex_cli_carrier_loop_proof_contract/run.json
  - ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
  - ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json
  - ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py
  - ION/04_packages/kernel/ion_carrier_task_return.py
  - ION/04_packages/kernel/ion_carrier_continue.py
  - ION/04_packages/kernel/ion_codex_queue_runner.py
  - ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md
  - ION/03_registry/chatgpt_browser_carrier_profile.yaml
  - ION/03_registry/codex_cli_carrier_profile.yaml
  - ION/04_packages/kernel/ion_cockpit_view_model.py

### VALIDATION

Read-only validation performed with `nl -ba`, `rg`, `wc -l`, `sha256sum`, and `git status --short --untracked-files=no`. No tests were run because this packet requested a read-only proof-contract smoke, not code execution or edits.

`git status` shows existing modified tracked files in the repo, including some inspected paths. I did not edit, delete, reset, push, deploy, or access secrets.

### RESULT

Touched paths are the inspected evidence paths listed under `touched_paths`. Tests: not run, read-only proof only. Remaining blockers: none for this smoke proof. Next lawful moves: submit/record this return through the existing task-return intake path, then let the queue runner update the work request status through the established proof gates.