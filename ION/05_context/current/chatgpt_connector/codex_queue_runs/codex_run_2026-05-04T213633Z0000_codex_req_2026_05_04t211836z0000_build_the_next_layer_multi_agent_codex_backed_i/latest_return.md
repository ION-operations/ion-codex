### CONTEXT PROOF

Read required packet and receipt before edits. Evidence includes read-time sha256.

| Path | Evidence |
|---|---|
| [work request](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T211836Z0000_build_the_next_layer_multi_agent_codex_backed_ion_swarm_control_from_sev_gpt_bro.json:10>) | line 10 objective requests Codex-backed swarm broker; sha256 `381e120ca293cf2779c387eb90ad92b3ab2404ecd3bef948551ea8d626c3f987` |
| [context receipt](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-04T213633Z0000_codex_req_2026_05_04t211836z0000_build_the_next_layer_multi_agent_codex_backed_i/context_receipt.json:2>) | lines 2-57 list required context reads; sha256 `7d8900c1b0770eea233caf7c6f0c077853eb3a04b8291b6e6449688f9eb0335c` |
| [ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json:1>) | lines 1-6 queue metadata, lines 7-17 prepared MASON smoke; read-time sha256 `6c817d694c22336a800da7475a7c327386880db5a33fb244a70515f7fb567088` |
| [ACTIVE_CARRIER_MESSAGE_QUEUE.json](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json:1>) | lines 1-4 queue metadata, lines 107-108 Sev callsign note; sha256 `813e2d6ed5a620fcb608554d667b70db569388a79c5378cc54cb4451cd644dae` |
| [MCP connector contract](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py:95>) | lines 95-141 expose status/write tools, lines 1277-1301 route agent invoke/cancel/swarm; sha256 `a4b2d46aa5e6ec6aafbbd13c1d074a1df97733746a30f88308a530c2caff136d` |
| [task return gate](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_carrier_task_return.py:229>) | lines 229-238 run context/template proof gates; sha256 `516e39db4f44d5aaf85023b7fa94713f8d2fb018597f01e86c6dc9c82f0e8a28` |
| [carrier continue](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_carrier_continue.py:401>) | lines 401-414 require proof-gated returns; sha256 `761797140d37a38fd1ca2a3c2da5239a4e2e08169d825af9f50c9f01c05bb72f` |
| [Codex queue runner](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_codex_queue_runner.py:1>) | lines 1-6 bounded runner owner, lines 551-565 submit output through task-return intake; sha256 `ce8eb142fe50890c56fa90f6adbc916898c16f109fd860620336d648bfdb8a0b` |
| [full-carrier parity protocol](</home/sev/ION - Production/ION_CODEX/ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md:363>) | lines 363-381 define agent broker slice and failure classes; sha256 `53fdd493c216c3974c826ef80473aa359d7a600791d72c37e2531e20fa7b555e` |
| [ChatGPT browser carrier profile](</home/sev/ION - Production/ION_CODEX/ION/03_registry/chatgpt_browser_carrier_profile.yaml:2>) | lines 2-6 carrier/callsign boundaries, lines 36-38 proof gates; sha256 `74d56f18f94b0b92d289f6f063717fc8c1cc5702b6c7c0e6aec161df4e949181` |
| [Codex CLI carrier profile](</home/sev/ION - Production/ION_CODEX/ION/03_registry/codex_cli_carrier_profile.yaml:2>) | lines 2-10 backend carrier capabilities, lines 17-24 proof gate owners; sha256 `b83c081562482ebd44399830722784f5a09f293964dea8f7dd75c9afa3c8b0c6` |
| [cockpit view model code](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_cockpit_view_model.py:18>) | lines 18-19 import broker/runner, lines 372-406 project agent tools/state; sha256 `cdcabe13a1233cc3e5e19a7b2724225ab8964b18952aff896769bf5a8618808c` |

### TEMPLATE ACTION PROOF

template_id: `ion.template.autonomous_loop.local_worker.v1`  
action_id: `codex_queue_runner_process_once`

Implemented the narrow guardrail patch in [ion_agent_invocation_broker.py](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_agent_invocation_broker.py:52>): cancel now only accepts prepared/queued invocation and work-request statuses, and `ion_swarm_step_once` now refuses non-agent or non-queued Codex request paths before calling the queue runner.

Touched paths:
- [ion_agent_invocation_broker.py](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_agent_invocation_broker.py:749>)
- [test_kernel_ion_agent_invocation_broker.py](</home/sev/ION - Production/ION_CODEX/ION/tests/test_kernel_ion_agent_invocation_broker.py:149>)
- [ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json:1>)
- [agent_invocation_broker_state.json](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/chatgpt_connector/runtime/agent_invocation_broker_state.json:1>)
- [ACTIVE_COCKPIT_VIEW_MODEL.json](</home/sev/ION - Production/ION_CODEX/ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json:1>)
- New prepare-only smoke invocation/work request under `chatgpt_connector/agent_invocations/` and `codex_work_requests/`.

### VALIDATION

- `pytest ION/tests/test_kernel_ion_agent_invocation_broker.py -q`: 6 passed.
- `pytest ION/tests/test_kernel_ion_agent_invocation_broker.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py -q`: 19 passed.
- `pytest ION/tests/test_kernel_ion_full_carrier_capability_audit.py -q`: 2 passed.
- `kernel.ion_status --json`: `ION_STATUS_READY`.
- MCP connector audit: `ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY`, 42 tools exposed.
- Full-carrier capability audit: `ION_FULL_CARRIER_CAPABILITY_AUDIT_READY`; no missing agent/queue/visibility tools.
- Prepare-only smoke: `ion_agent_invoke` with `steward_review` produced invocation `agent_inv_2026-05-04T213935Z0000_steward_prepare_only_broker_regression_smoke_after_cancellation_and_swarm_step_g`, status `PREPARED_NOT_QUEUED`, no Codex backend started.
- Negative guard smoke: `ion_swarm_step_once` against that non-queued prepared request blocked with `agent_invocation_work_request_not_queued`, as intended.

### RESULT

The broker slice is in place and tighter: Sev/ChatGPT Browser can invoke role packets through MCP into existing ION queue owners, Codex remains the backend carrier, and raw backend output still only enters state through `ion_submit_task_return` proof gates.

Exposed agent/swarm tools verified: `ion_agent_list`, `ion_agent_status`, `ion_agent_result`, `ion_agent_queue`, `ion_agent_spawn_plan`, `ion_swarm_status`, `ion_agent_invoke`, `ion_agent_cancel`, `ion_swarm_step_once`.

Remaining blockers: no production deploy, no git push, no live backend execution beyond prepare-only smoke. Audit still records direct shell/git/process MCP as `CAPABILITY_NOT_YET_IMPLEMENTED`, not `ION_CORE_FAILURE`. Next lawful move is to queue a real agent invocation and use `ion_swarm_step_once` in prepare-only or explicitly bounded execution mode, then intake any Codex return through the existing context/template proof gates.