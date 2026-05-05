carrier_mount:
  title: "ION V126 Codex CLI Carrier Mount, MCP Setup, and ChatGPT Connector Bring-Up"
  working_root_hint: "ION - Production/ION_CODEX"
  issued_by: "ChatGPT browser / GPT-5.5 Pro lead-dev reasoning lane"
  carrier: "Codex CLI"
  carrier_identity: "CODEX_CLI_CARRIER"
  ion_identity_claim: false
  production_authority: false
  live_execution_authority: false

mission:
  primary_goal: >
    Mount Codex CLI as the bounded local ION worker carrier, verify it understands
    the V125 Codex CLI carrier lane, configure/inspect its own Codex/MCP readiness
    without exposing secrets, and advance the ChatGPT-browser MCP connector path
    toward a live bounded bridge that GPT-5.5 can use from browser chat.
  immediate_outcome: >
    Produce a proof-bearing return that says exactly what is ready, what is not
    ready, what commands passed, what connector URL/state exists, and what the
    next human action is to make ChatGPT browser connect to ION.

hard_boundaries:
  - "Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority."
  - "You are a carrier/chassis only. ION roles are mounted through packets and templates."
  - "Do not push git."
  - "Do not deploy production."
  - "Do not read, print, store, or request secrets/API keys/tokens."
  - "Do not delete files. If removal seems needed, propose lifecycle transition only."
  - "Do not mutate outside the current repo shell root."
  - "Do not create broad new doctrine unless a concrete runtime blocker proves it is needed."
  - "Prefer repair/wiring/proof over explanation."

required_first_reads:
  - "ION/REPO_AUTHORITY.md"
  - "ION/02_architecture/ION_MOUNT_CONTRACT.md"
  - "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md"
  - "ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md"
  - "ION/03_registry/codex_cli_carrier_profile.yaml"
  - "ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md"
  - "ION/docs/setup/CODEX_CLI_ION_DOGFOOD_SETUP_V125.md"
  - "ION/docs/setup/CHATGPT_BROWSER_MCP_CONNECTOR_SETUP_V120.md"
  - "ION/02_architecture/ION_CHATGPT_BROWSER_MCP_CONNECTOR_PROTOCOL.md"
  - "ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml"
  - "ION/05_context/current/ACTIVE_WORK_PACKET.json"
  - "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json"

preflight_commands:
  - command: "test -f pyproject.toml && test -f ION/REPO_AUTHORITY.md"
    purpose: "prove shell root"
  - command: "codex --version"
    purpose: "record Codex CLI version only; do not expose credentials"
    allowed_to_fail: true
  - command: "codex mcp list"
    purpose: "inspect Codex MCP server configuration"
    allowed_to_fail: true
  - command: "codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp"
    purpose: "add OpenAI docs MCP if missing; skip if already present"
    allowed_to_fail: true
  - command: "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json"
    purpose: "prove ION status"
  - command: "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_cli_carrier_audit --ion-root . --json"
    purpose: "prove Codex CLI carrier audit"
  - command: "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_onboarding_packet --ion-root . --carrier codex_cli --json"
    purpose: "prove carrier onboarding packet"
  - command: "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_mcp_connector_contract --ion-root . --write --json"
    purpose: "refresh ChatGPT-browser connector contract"
  - command: "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_mcp_bridge_audit --ion-root . --json"
    purpose: "prove MCP control bridge audit"
  - command: "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_cli_carrier_audit.py ION/tests/test_kernel_ion_carrier_onboarding_packet.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py -q"
    purpose: "focused carrier and connector test proof"

chatgpt_connector_bringup:
  inspect_paths:
    - "ION/05_context/current/chatgpt_connector/runtime/"
    - "ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json"
    - "ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json"
    - "ION/05_context/current/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json"
    - "ION/09_integrations/mcp/chatgpt_connector/ion_chatgpt_browser_connector.py"
  tasks:
    - "Determine whether the local HTTP MCP preview is running."
    - "Determine whether a Cloudflare tunnel is running or stale."
    - "Determine whether active_connector_url exists and ends in /mcp."
    - "Do not start long-running processes unless the setup guide explicitly supports it and you can record pid/log paths."
    - "If starting local HTTP preview is needed, use the exact setup-guide command and write pid/log evidence under ION/05_context/current/chatgpt_connector/runtime/."
    - "If starting Cloudflare tunnel is needed and cloudflared exists locally, use the exact setup-guide command and write pid/log evidence under ION/05_context/current/chatgpt_connector/runtime/."
    - "If cloudflared is missing, do not install globally without asking; report the exact missing dependency and next command."
    - "Print the connector URL only if the ION state file proves it. Do not fabricate it."

allowed_changes:
  - "ION/05_context/current/codex_cli/"
  - "ION/05_context/current/chatgpt_connector/runtime/"
  - "ION/05_context/current/CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json"
  - "ION/05_context/current/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json"
  - "ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json"
  - "ION/05_context/signals/"
  - "Small tests or kernel patches only if a preflight command fails and the cause is concrete."

forbidden_changes:
  - "No broad file reorganization."
  - "No package zipping unless explicitly asked later."
  - "No doctrine expansion."
  - "No deletion."
  - "No credential files."
  - "No production deployment."
  - "No arbitrary shell bridge exposed to ChatGPT."

return_contract:
  required_sections:
    - "### CONTEXT PROOF"
    - "### TEMPLATE ACTION PROOF"
    - "### CODEX CLI SETTINGS / MCP READINESS"
    - "### CHATGPT BROWSER CONNECTOR STATUS"
    - "### RESULT"
    - "### NEXT HUMAN ACTION"
  section_requirements:
    context_proof:
      - "root confirmed"
      - "carrier profile used"
      - "files read"
      - "active packet used"
      - "assumptions"
    template_action_proof:
      - "commands run"
      - "files changed"
      - "tests run"
      - "receipts/view models emitted"
      - "boundaries not crossed"
    codex_cli_settings_mcp_readiness:
      - "codex version or unavailable"
      - "codex mcp list result"
      - "openaiDeveloperDocs MCP present/added/blocked"
      - "any config limitation"
    chatgpt_browser_connector_status:
      - "connector contract verdict"
      - "local HTTP preview state"
      - "tunnel state"
      - "active_connector_url if proven"
      - "tools expected in ChatGPT"
    result:
      - "ready/not ready verdict"
      - "remaining blockers"
      - "smallest next technical move"
    next_human_action:
      - "exact ChatGPT settings step if connector URL is ready"
      - "exact terminal command if local process/dependency is missing"
      - "do not include vague advice"
