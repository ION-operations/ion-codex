# ION Codex CLI Execution Packet 001 — Custom GPT Action Gateway MVP

created_at: 2026-05-07
status: candidate_codex_execution_packet_not_ion_state
packet_id: ION_CODEX_CLI_PACKET_001_ACTION_GATEWAY_MVP
carrier_id: CODEX_CLI_CARRIER
production_authority: false
live_execution_authority: false

## Objective

Implement the first ION Custom GPT Action Gateway MVP over the existing ChatOps/Codex/receipt owners.

The gateway is a public-facing local API membrane intended to sit behind Cloudflare Tunnel and in front of existing ION local owners.

It must **not** become a new authority system, a new queue, a raw shell endpoint, or a replacement for Steward integration.

## Required mount

Start from shell root:

```bash
test -f pyproject.toml
test -f ION/REPO_AUTHORITY.md
```

Read in order:

```text
ION/REPO_AUTHORITY.md
ION/02_architecture/ION_MOUNT_CONTRACT.md
ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md
ION/03_registry/codex_cli_carrier_profile.yaml
ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md
ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md
ION/03_registry/ion_chatops_action.schema.yaml
ION/03_registry/ion_chatops_local_daemon_policy.yaml
ION/04_packages/kernel/ion_chatops_bridge.py
ION/04_packages/kernel/ion_codex_queue_runner.py
ION/04_packages/kernel/ion_agent_invocation_broker.py
ION/05_context/current/ACTIVE_WORK_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
```

Run preflight:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_cli_carrier_audit --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatops_bridge --ion-root . --policy --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_queue_runner --ion-root . --status --json
```

## Allowed paths

You may create or modify only:

```text
ION/02_architecture/ION_CUSTOM_GPT_ACTION_GATEWAY_PROTOCOL.md
ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
ION/09_integrations/custom_gpt_action_gateway/
ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py
ION/tests/test_kernel_ion_custom_gpt_action_gateway.py
ION/05_context/current/action_gateway/
```

You may update an index only if an existing local convention clearly requires it and the change is narrow.

## Forbidden paths / actions

```text
Do not edit REPO_AUTHORITY.md.
Do not edit ION_MOUNT_CONTRACT.md.
Do not edit existing ChatOps daemon behavior except if a tiny exported helper is clearly needed and tested.
Do not edit Codex queue runner behavior.
Do not edit agent broker behavior.
Do not touch historical_ion_aimos.
Do not create a new queue system.
Do not create a new agent system.
Do not add external Python dependencies unless already present in project policy.
Do not store secrets, tokens, Cloudflare credentials, or OpenAI credentials in repo.
Do not add shell/deploy/git push/delete endpoints.
Do not run production deploy.
Do not push to git.
```

## Implementation requirements

### 1. Protocol doc

Create:

```text
ION/02_architecture/ION_CUSTOM_GPT_ACTION_GATEWAY_PROTOCOL.md
```

Must state:

```text
- gateway is transport membrane, not authority
- Cloudflare Tunnel may expose only the gateway, not raw daemon
- mutations route through existing ChatOps / queue / proof / Steward paths
- production_authority=false
- live_execution_authority=false
- Actions approval is not Steward integration
- Codex output is proposal until proof-gated
```

### 2. Policy registry

Create:

```text
ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml
```

Minimum fields:

```yaml
schema_id: ion.custom_gpt_action_gateway_policy.v1
status: draft_non_production
production_authority: false
live_execution_authority: false
listen_host: 127.0.0.1
listen_port: 8777
public_transport: cloudflare_tunnel
auth:
  required: true
  scheme: bearer
  token_env_var: ION_ACTION_GATEWAY_TOKEN
  token_sha256_env_var: ION_ACTION_GATEWAY_TOKEN_SHA256
limits:
  max_body_bytes: 262144
  require_idempotency_key_for_mutation: true
allowed_get_paths:
  - /health
  - /policy
  - /context-pack
  - /codex/queue
  - /agent/status
  - /receipts/recent
allowed_post_paths:
  - /actions/validate
  - /actions/submit
supported_mvp_intents:
  - register_artifact
  - write_file_draft
  - create_codex_work_packet
  - create_github_issue_draft
hard_gated_intents:
  - delete_file
  - overwrite_protected_file
  - push_main
  - access_credential
  - production_deploy
  - broad_shell
```

### 3. Kernel gateway

Create:

```text
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
```

Use stdlib where possible, matching current ION kernel style.

Required pure helpers:

```text
load_gateway_policy(root) -> dict
build_gateway_health(root) -> dict
build_gateway_policy_surface(root) -> dict
validate_gateway_auth(headers, policy) -> dict
validate_gateway_request_envelope(packet, *, mutation: bool) -> dict
validate_gateway_action_packet(root, packet) -> dict
submit_gateway_action_packet(root, packet) -> dict
build_recent_gateway_receipts(root, limit=20) -> dict
```

Required CLI:

```bash
python3 -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --policy --json
python3 -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --health --json
python3 -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --openapi --json
python3 -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --validate-json packet.json --json
python3 -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --submit-json packet.json --json
python3 -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --host 127.0.0.1 --port 8777 --serve
```

Required HTTP endpoints:

```text
GET  /health
GET  /policy
GET  /context-pack
GET  /codex/queue
GET  /agent/status
GET  /receipts/recent
POST /actions/validate
POST /actions/submit
```

Endpoint ownership:

```text
/health: gateway local status
/policy: gateway policy + imported ChatOps hard gates
/context-pack: existing ChatOps context pack helper if available
/codex/queue: existing Codex queue runner status or ChatOps agent queue helper
/agent/status: existing ChatOps agent status helper
/receipts/recent: gateway receipts + ChatOps receipt pointers
/actions/validate: call existing validate_chatops_action with require_approval=false after gateway envelope validation
/actions/submit: require auth, idempotency_key, operator approval evidence; then call existing submit_chatops_action
```

Auth:

```text
- Health may return low-detail without auth.
- All other routes require Authorization: Bearer <token>.
- Accept either ION_ACTION_GATEWAY_TOKEN or sha256 comparison through ION_ACTION_GATEWAY_TOKEN_SHA256.
- Never print token values.
- Receipts must redact auth headers.
```

Mutation envelope requirement:

```json
{
  "idempotency_key": "ion-act-20260507-example",
  "operator_approval": {
    "approved_by": "Braden",
    "approved_at": "ISO-8601 timestamp",
    "approval_text": "explicit approval phrase"
  },
  "ion_action": {
    "schema": "ion.chatops.action.v1",
    "action_id": "sev-20260507-example",
    "intent": "register_artifact",
    "actor": {"callsign": "Sev", "carrier": "chatgpt_browser"},
    "authority": {
      "human_sovereign": "Braden",
      "requires_approval": true,
      "production_authority": false,
      "live_execution_authority": false
    },
    "payload": {},
    "receipts": {"requested": true}
  }
}
```

For compatibility with existing ChatOps validation, unwrap or pass through `ion_action` as needed, but the public gateway must keep idempotency and approval evidence at the gateway layer.

Receipts:

```text
ION/05_context/current/action_gateway/receipts/
ION/05_context/current/action_gateway/runtime/
```

Every submit attempt gets a receipt, including refused submits. Read-only GET requests do not need durable receipts unless debugging is enabled.

### 4. Integration README + OpenAPI

Create:

```text
ION/09_integrations/custom_gpt_action_gateway/README.md
ION/09_integrations/custom_gpt_action_gateway/openapi.yaml
```

README must include:

```text
- local launch commands
- Cloudflare route target
- Custom GPT Action setup steps
- supported endpoints
- auth env vars
- refusal classes
- no-production-authority warning
```

OpenAPI must include only MVP endpoints and clear operation names.

### 5. Tests

Create:

```text
ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py
ION/tests/test_kernel_ion_custom_gpt_action_gateway.py
```

Minimum test cases:

```text
policy file exists and declares draft_non_production
policy hard-gates dangerous intents
health returns non-production status
policy surface imports ChatOps hard gates
missing auth is rejected for protected route
valid auth accepted without token leak
mutating submit requires idempotency_key
mutating submit requires operator approval evidence
production_authority=true rejected
live_execution_authority=true rejected
hard-gated intent rejected
validate endpoint does not write receipts
submit refusal writes refusal receipt
OpenAPI file exists and contains no broad_shell/delete/push_main/deploy operation path
```

Run validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py \
  ION/tests/test_kernel_ion_custom_gpt_action_gateway.py \
  ION/tests/test_kernel_ion_chatops_action_schema.py \
  ION/tests/test_kernel_ion_chatops_bridge_policy.py \
  ION/tests/test_kernel_ion_codex_queue_runner.py \
  ION/tests/test_kernel_ion_agent_invocation_broker.py \
  ION/tests/test_kernel_ion_codex_cli_carrier_audit.py \
  -q
```

Optional second validation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  ION/tests/test_kernel_ion_chatgpt_browser_cloudflare_tunnel.py \
  ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py \
  ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py \
  ION/tests/test_kernel_ion_mcp_transport_preview.py \
  -q
```

## Required return

Codex must return:

```text
### CONTEXT PROOF
- shell root confirmed:
- carrier profile used:
- files read:
- active packet/context package used:
- existing owners reused:
- assumptions:

### TEMPLATE ACTION PROOF
- requested change:
- files changed:
- tests run:
- receipts/view models emitted:
- boundaries not crossed:
- hard gates preserved:

### RESULT
- implementation result:
- validation result:
- remaining blockers:
- next lawful move:
```

Do not claim production readiness. Do not claim live Custom GPT Action success until the GPT Builder actually calls the tunnel endpoint.
