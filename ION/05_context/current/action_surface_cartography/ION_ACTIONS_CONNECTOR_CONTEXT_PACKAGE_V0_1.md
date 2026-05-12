# ION Actions Connector Context Package v0.1

Status: candidate context package (not settled law).

## Scope
This package materializes Action Surface Context Package 001 as candidate-only repo artifacts under `ION/05_context/current/action_surface_cartography/`.

Boundaries held:
- `production_authority=false`
- `live_execution_authority=false`
- No shared Capsule/Mini/HOT_CONTEXT/STATUS/ROUTE mutation
- No C-number assigned by this agent

## Live Surfaces Tested by ChatGPT Browser (documented)
- Action Gateway health/policy
- MCP preview health/tools list
- ChatOps context-pack validation-only path
- ION status/context-plan/cockpit read surfaces
- Daemon/Codex queue status surfaces
- Browser queue status
- Action Gateway validate-only action checks

## Key Findings (required record)
- Action Gateway verdict `ION_CUSTOM_GPT_ACTION_GATEWAY_READY`, status `draft_non_production`, public_transport `cloudflare_tunnel`, local listen `127.0.0.1:8777`, max_body_bytes `262144`, idempotency required for mutation, `production_authority=false`, `live_execution_authority=false`.
- MCP preview verdict `ION_CHATGPT_BROWSER_HTTP_MCP_PREVIEW_READY`, version `V121_CHATGPT_BROWSER_HTTP_MCP_PREVIEW`, endpoint `/mcp`, default `127.0.0.1:8765`, connector_state `LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR`, write confirmation token `ION_BOUNDED_WRITE_CONFIRMED`, production/live/deployment authority false.
- Forbidden capability classes: arbitrary shell, arbitrary file write, browser/computer control, credential access, direct delete, git push, production deployment, provider API calls, unbounded filesystem access, direct accept of unproofed worker output.
- MCP tools/list exposed 44 tools; classify into read/status and bounded queue/receipt/write tools.
- Action Gateway validation tests: `ion.action.v1` schema failed `SCHEMA_INVALID`; `ion.chatops.action.v1` `create_codex_work_packet` passed validation-only; `register_artifact` passed validation-only; `write_file_draft` passed validation-only; `create_github_issue_draft` has a schema mismatch/gap around `github_owner`/`github_repo`/`github_title`/`github_body`.
- Assistant-work route compiler degraded: `pyyaml_unavailable`, `route_registry_missing_or_invalid`, `lifecycle_registry_missing_or_invalid`.
- Large response pressure: `ion_context_plan` large/truncated, `ion_cockpit_view` response too large, queue reads need low limits/pagination.
- Browser queue: pending_count 2, queued 1, needs_operator 1, max_queue_length 25, max_autoplay_turns 10, one echo packet queued and one `B01_RUNTIME_CONNECTORS` packet needs operator.
- Direct MCP `file_put_text` attempt to target `action_surface_cartography` was blocked by path policy `target_path_not_in_artifact_transfer_roots`.

## Evidence Anchors
- Action Gateway policy/source: `ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml`, `ION/04_packages/kernel/ion_custom_gpt_action_gateway.py`
- MCP preview snapshot: `ION/05_context/current/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json`
- Connector contract capability classes and bounded write token handling: `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py`, `ION/03_registry/chatgpt_browser_carrier_profile.yaml`
- Browser queue state: `ION/05_context/current/action_gateway/runtime/browser_queue.json`
- Queue work request and context receipt: 
  - `ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-11T190651Z0000_action_surface_context_package_001_materialize_live_repo_candidate_goal_material.json`
  - `ION/05_context/current/chatgpt_connector/codex_queue_runs/codex_run_2026-05-11T190656Z0000_codex_req_2026_05_11t190651z0000_action_surface_context_package_001_materialize_/context_receipt.json`
- Validate-only test traces: `ION/05_context/current/action_surface_cartography/ACTION_SURFACE_TEST_LOG_V0_1.json`

## Drift Note
- Local V121 snapshot currently enumerates 42 allowed tools.
- Current connector contract audit currently enumerates 48 allowed tools.
- The required packet finding above preserves the ChatGPT-authored live-test record statement of 44 tools.

## Candidate Posture
This package is witness/candidate material only. It is not accepted shared state and does not settle law without explicit parent settlement intake.
