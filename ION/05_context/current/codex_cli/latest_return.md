### CONTEXT PROOF
- Root confirmed: `/home/sev/ION - Production/ION_CODEX`; `pyproject.toml` and `ION/REPO_AUTHORITY.md` present.
- Carrier profile used: `CODEX_CLI_CARRIER` from `ION/03_registry/codex_cli_carrier_profile.yaml`.
- Files read: all required first-read files, plus connector runtime/state files and `ION/09_integrations/mcp/chatgpt_connector/ion_chatgpt_browser_connector.py`.
- Active packet used: `ION/05_context/current/ACTIVE_WORK_PACKET.json`; objective is ChatGPT Browser MCP connector transport truth and carrier onboarding.
- Assumptions: I did not claim ION/STEWARD/RELAY/PERSONA authority; production/live authority remain false.

### TEMPLATE ACTION PROOF
- Commands passed:
  - root test: pass.
  - `codex --version`: `codex-cli 0.128.0` with read-only PATH update warning.
  - `PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json`: `ION_STATUS_READY`.
  - `kernel.ion_codex_cli_carrier_audit`: `ION_CODEX_CLI_CARRIER_READY`.
  - `kernel.ion_carrier_onboarding_packet --carrier codex_cli`: `ION_CARRIER_ONBOARDING_PACKET_READY`.
  - `kernel.ion_chatgpt_browser_mcp_connector_contract --write`: `ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY`.
  - `kernel.ion_mcp_bridge_audit`: `ION_MCP_CONTROL_BRIDGE_READY`.
  - focused tests: `13 passed in 0.11s`.
- Files changed:
  - [ion_chatgpt_browser_mcp_http_preview.py](</home/sev/ION - Production/ION_CODEX/ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py:310>) to make the documented `--host/--port` launch serve.
  - [test_kernel_ion_chatgpt_browser_mcp_connector_contract.py](</home/sev/ION - Production/ION_CODEX/ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py:145>) for that launch path.
  - Refreshed connector contract/tunnel state and runtime evidence under allowed current-context paths.
- Receipts/view models emitted: `CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json`, `CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json`, `ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json`, runtime PID/log/refresh/url files.
- Boundaries not crossed: no secrets read/printed, no delete, no git push, no production deploy, no arbitrary shell bridge exposed to ChatGPT.

### CODEX CLI SETTINGS / MCP READINESS
- Codex CLI available: `codex-cli 0.128.0`.
- `codex mcp list`: no MCP servers configured.
- `openaiDeveloperDocs`: not added. `codex mcp add` would mutate user-level Codex config outside this repo (`~/.codex/config.toml` per CLI help), so I blocked it under the repo-mutation boundary.
- Config limitation: current Codex MCP readiness is “CLI present, MCP config empty.”

### CHATGPT BROWSER CONNECTOR STATUS
- Connector contract verdict: `ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY`.
- Local HTTP preview: running on `http://127.0.0.1:8765/mcp`, PID `38225`; local health 200; 15 tools listed.
- Tunnel state: `TUNNEL_RUNNING_VERIFIED`; wrapper PID `38271`, `cloudflared` PID `38274`.
- Proven active connector URL: `https://attention-chrome-satisfactory-guy.trycloudflare.com/mcp`
- Tools expected in ChatGPT: `ion_carrier_onboarding_packet`, `ion_status`, `ion_current_operating_packet`, `ion_read_active_packet`, `ion_context_plan`, `ion_cockpit_view`, `ion_artifact_manifest`, `ion_receipt_search`, `ion_git_status_summary`, `ion_codex_work_queue`, plus bounded queue/receipt tools requiring confirmation.

### RESULT
Ready for ChatGPT browser connector creation. Not yet `CHATGPT_CONNECTOR_TESTED_READY`, because ChatGPT browser itself has not added the connector and called tools yet.

Remaining blocker: human must create the connector in ChatGPT and verify the advertised tools.

Smallest next technical move: paste the proven `/mcp` URL into ChatGPT connector creation, then call `ion_carrier_onboarding_packet`.

### NEXT HUMAN ACTION
In ChatGPT: enable developer mode if needed, then go to `Settings -> Connectors -> Create`, set Connector URL to:

`https://attention-chrome-satisfactory-guy.trycloudflare.com/mcp`

After creation, open a new chat, add the connector from the `+` menu, and run first tool call: `ion_carrier_onboarding_packet`.

Official OpenAI docs align with this: developer mode is under `Settings -> Apps & Connectors -> Advanced settings`, connector creation uses `Settings -> Connectors -> Create`, and the URL must be the public `/mcp` endpoint. Source: https://developers.openai.com/apps-sdk/deploy/connect-chatgpt. MCP tool listing/calling and Streamable HTTP are described here: https://developers.openai.com/apps-sdk/concepts/mcp-server.