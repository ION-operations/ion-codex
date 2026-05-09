# ION Actions + Codex CLI Powered IDE — Full Execution Plan

created_at: 2026-05-07
status: candidate_execution_plan_not_ion_state
carrier_context: ChatGPT Browser / Sev as planning carrier; Custom GPT Actions as HTTPS API ingress; Cloudflare Tunnel as transport; local ION daemon/gateway as policy membrane; Codex CLI as bounded filesystem/build/test carrier.
production_authority: false
live_execution_authority: false

## 0. Settlement

We should build the ION local Codex CLI powered IDE through **Custom GPT Actions first**, with Cloudflare Tunnel as the public HTTPS transport and a new ION Action Gateway as the public-facing local membrane.

The browser extension remains valuable, but it becomes the local watched-chat/operator cockpit lane. The Custom GPT Action bridge becomes the clean command/data ingress from this GPT.

The product spine:

```text
Custom GPT / Sev
→ GPT Action call over HTTPS
→ Cloudflare Tunnel published hostname
→ local ION Action Gateway on localhost
→ existing ION ChatOps / MCP / queue / receipt owners
→ Codex CLI bounded worker packets
→ proof-bearing Codex return
→ ION context proof + template action gate
→ Steward integration
→ receipt / next state / cockpit projection
```

Do **not** expose the existing ChatOps daemon directly to the public hostname. Place a new gateway in front of it with GPT-Action-specific authentication, idempotency, payload limits, endpoint allowlists, receipt generation, and hard refusal classes.

## 1. Mount / current-root proof from sandbox

Shell root inspected:

```text
/mnt/data/ion_current/ION_CODEX
```

Authority surfaces read or verified:

```text
ION/REPO_AUTHORITY.md
ION/02_architecture/ION_MOUNT_CONTRACT.md
ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md
ION/03_registry/codex_cli_carrier_profile.yaml
ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md
ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md
ION/03_registry/ion_chatops_local_daemon_policy.yaml
ION/03_registry/ion_chatops_extension_policy.yaml
ION/03_registry/ion_chatops_action.schema.yaml
ION/04_packages/kernel/ion_chatops_bridge.py
ION/04_packages/kernel/ion_codex_queue_runner.py
ION/04_packages/kernel/ion_agent_invocation_broker.py
```

Active state surfaces observed:

```text
ION/05_context/current/ACTIVE_WORK_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json
ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json
ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
```

Observed status:

```text
ion_status: ready surface, production_authority=false, live_execution_authority=false
active objective: Build the ION local Codex CLI powered IDE / extension bridge as a bounded current-session planning and validation task.
next_lawful_action: execute_spawn_rows_and_run_task_return_intake
Codex CLI carrier audit verdict: ION_CODEX_CLI_CARRIER_READY
ChatOps bridge policy: present, localhost 127.0.0.1:8767, supported MVP intents and hard-gated intents present
Codex queue runner verdict: ION_CODEX_QUEUE_RUNNER_READY
Codex queue after reconciliation: queued_request_count=0, active_process_running=false
Agent invocation broker: 16 invocable agents through existing broker/queue, no parallel agent system
```

Focused validation run in sandbox:

```text
38 passed:
- test_kernel_ion_chatops_action_schema.py
- test_kernel_ion_chatops_bridge_policy.py
- test_kernel_ion_codex_queue_runner.py
- test_kernel_ion_agent_invocation_broker.py
- test_kernel_ion_codex_cli_carrier_audit.py

42 passed:
- test_kernel_ion_chatgpt_browser_cloudflare_tunnel.py
- test_kernel_ion_chatgpt_browser_mcp_http_preview.py
- test_kernel_ion_chatgpt_browser_mcp_connector_contract.py
- test_kernel_ion_mcp_transport_preview.py
```

Claim boundary:

```text
focused local tests passed in sandbox
full suite was not run in this planning pass
public live GPT Action call was not performed from this sandbox
Cloudflare tunnel was not operated from this sandbox
```

## 2. Platform constraints to obey

### Custom GPT Actions

Custom GPT Actions require an external API described by an OpenAPI schema and configured authentication. This means ION must present a public HTTPS endpoint reachable from ChatGPT.

Important product choice:

```text
For the Custom GPT, choose Actions as the primary bridge.
Do not depend on Custom Apps/MCP inside the same GPT while Actions are active.
Keep MCP connector work as a sibling carrier lane until we intentionally switch or split GPTs.
```

### Cloudflare Tunnel

Cloudflare Tunnel can publish a hostname that maps to a local service. Use it to expose only the ION Action Gateway, not raw Codex, not raw shell, not the existing local ChatOps daemon.

### Codex CLI

Codex CLI is the local build/test carrier. Configure it at project scope with `.codex/config.toml` after the local operator trusts the project. Keep sandbox mode bounded, avoid network by default, and capture prompt/return artifacts into ION paths.

## 3. Component map

### Component A — ION Action Gateway

New public-facing local API membrane.

Candidate paths:

```text
ION/02_architecture/ION_CUSTOM_GPT_ACTION_GATEWAY_PROTOCOL.md
ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
ION/09_integrations/custom_gpt_action_gateway/README.md
ION/09_integrations/custom_gpt_action_gateway/openapi.yaml
ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py
ION/tests/test_kernel_ion_custom_gpt_action_gateway.py
ION/05_context/current/action_gateway/
```

Responsibilities:

```text
- verify bearer/API-key authentication before any non-health route
- enforce body size limit
- enforce endpoint allowlist
- require idempotency_key on mutating requests
- call existing ION ChatOps/queue/kernel owners rather than duplicate authority
- block production_authority=true and live_execution_authority=true
- reject hard-gated intents
- emit request/validation/submission receipts
- preserve operator-visible refusal reasons
- return JSON only
```

It must not:

```text
- run arbitrary shell
- expose Codex CLI directly
- expose raw localhost daemon without extra auth
- store OpenAI API keys, Cloudflare tokens, or other secrets in repo
- push git
- delete files
- deploy production
- mutate graph/canon directly
```

### Component B — Existing ChatOps daemon

Existing local daemon remains the local policy/receipt owner for watched chat and can be reused behind the Action Gateway.

Known local daemon defaults:

```text
host: 127.0.0.1
port: 8767
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

Existing endpoints found in `ion_chatops_bridge.py`:

```text
GET  /health
GET  /policy
GET  /context/sev/onboarding
GET  /agent/status
GET  /agent/queue
GET  /operator/status
GET  /exports/context-pack
GET  /artifacts/attachables
GET  /sandbox/returns
POST /actions/validate
POST /actions/submit
POST /agent/prepare-next
POST /agent/process-one
POST /exports/lifecycle-zip
POST /exports/safe-full-zip
POST /artifacts/prepare-upload
POST /operator/attach-artifact
POST /sandbox/returns/register
POST /sandbox/returns/file
POST /sandbox/returns/commit
POST /sandbox/returns/diff-preview
POST /sandbox/returns/queue-review
```

MVP Action Gateway should expose only a smaller subset.

### Component C — Cloudflare Tunnel route

Local route:

```text
https://ion-actions.<approved-domain>
→ http://127.0.0.1:8777
```

Do not map the public hostname to `127.0.0.1:8767` directly. Keep `8767` for local extension/operator surfaces.

Optional hardening:

```text
Cloudflare WAF rule: allow only required paths
Cloudflare Access service token if Custom GPT Action auth can reliably send required headers
Cloudflare rate limit on POST paths
Separate staging hostname from stable hostname
Tunnel logs preserved locally outside repo
```

### Component D — Custom GPT Action schema

Use a minimal OpenAPI schema with explicit operation names and descriptions.

MVP paths:

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

Mutation principle:

```text
Only /actions/submit mutates.
Everything else is read-only or dry-run validation.
```

### Component E — Codex CLI carrier setup

Candidate project-scoped config path:

```text
.codex/config.toml
```

Default posture:

```text
sandbox_mode = "workspace-write"
approval_policy = "on-request"
network_access = false
writable_roots limited to the repo and safe temp/output paths
do not store secrets in config
```

Codex prompt/return capture:

```text
ION/05_context/current/codex_cli/latest_prompt.md
ION/05_context/current/codex_cli/latest_return.md
ION/05_context/current/codex_cli/latest_events.jsonl
```

Required return sections:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
```

### Component F — ION local cockpit / IDE

The IDE should be a cockpit over owners, not a new agent system.

MVP cockpit panels:

```text
- mount status
- active packet
- active role spawn plan
- Codex queue status
- agent broker status
- Action Gateway health
- ChatOps daemon health
- Cloudflare tunnel configured hostname
- latest receipts
- latest task returns
- blocked gates and refusal reasons
- sandbox return inbox
- artifact upload/download tickets
```

Buttons must create packets or validation requests. They must not directly mutate canonical state.

## 4. Phase plan

### Phase 0 — Freeze authority and execution packet

Goal: give Codex one bounded first packet and prevent drift.

Deliverables:

```text
- current plan artifact
- first Codex execution packet
- OpenAPI candidate
- GPT builder instructions patch
- Cloudflare runbook
- Codex config candidate
```

Proof:

```text
artifacts exist
focused tests from current root listed
no repo mutation claimed
```

### Phase 1 — Implement ION Action Gateway MVP

Goal: new public-facing gateway over existing owners.

Codex tasks:

```text
1. Add gateway protocol doc.
2. Add gateway policy registry.
3. Add gateway kernel module with pure validation helpers and stdlib HTTP server.
4. Add OpenAPI schema under integration path.
5. Add README/runbook.
6. Add tests for auth, read-only endpoints, validation, hard-gated refusal, idempotency requirement, and no direct shell exposure.
```

Expected endpoints:

```text
GET  /health                     unauthenticated or low-detail unauthenticated
GET  /policy                     auth required
GET  /context-pack               auth required
GET  /codex/queue                auth required
GET  /agent/status               auth required
GET  /receipts/recent            auth required
POST /actions/validate           auth required, no mutation
POST /actions/submit             auth + operator approval evidence + idempotency required
```

Acceptance tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest \
  ION/tests/test_kernel_ion_custom_gpt_action_gateway_policy.py \
  ION/tests/test_kernel_ion_custom_gpt_action_gateway.py \
  ION/tests/test_kernel_ion_chatops_action_schema.py \
  ION/tests/test_kernel_ion_chatops_bridge_policy.py \
  ION/tests/test_kernel_ion_codex_queue_runner.py \
  ION/tests/test_kernel_ion_agent_invocation_broker.py \
  -q
```

### Phase 2 — Local bridge run

Goal: prove local gateway and ChatOps daemon can coexist.

Manual/local commands:

```bash
cd "<ION shell root>"

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatops_bridge \
  --ion-root . --host 127.0.0.1 --port 8767 --serve

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_custom_gpt_action_gateway \
  --ion-root . --host 127.0.0.1 --port 8777 --serve
```

Smoke checks:

```bash
curl http://127.0.0.1:8777/health
curl -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" http://127.0.0.1:8777/policy
curl -H "Authorization: Bearer $ION_ACTION_GATEWAY_TOKEN" http://127.0.0.1:8777/codex/queue
```

### Phase 3 — Cloudflare Tunnel bind

Goal: public HTTPS endpoint reaches only the Action Gateway.

Route:

```text
https://ion-actions.<approved-domain> → http://127.0.0.1:8777
```

Proof:

```text
GET /health succeeds from outside local network
GET /policy without auth is rejected
GET /policy with auth succeeds
POST /actions/validate succeeds with dry-run valid packet
POST /actions/submit refuses missing approval evidence
```

Receipt:

```text
ION/05_context/current/action_gateway/receipts/<timestamp>_cloudflare_probe_receipt.json
```

### Phase 4 — Custom GPT Action install

Goal: install schema and test read-only actions.

GPT Builder steps:

```text
1. Create or edit ION GPT.
2. Actions → Create new action.
3. Paste OpenAPI schema.
4. Configure auth as bearer/API key matching gateway.
5. Test health.
6. Test policy.
7. Test context-pack.
8. Test codex queue.
9. Do not test mutating submit until local receipt path is verified.
```

Instruction patch for GPT:

```text
Use read-only ION bridge actions freely for status/context.
Before any mutation:
  1. call validate;
  2. summarize validation/refusal;
  3. ask Braden for explicit approval;
  4. call submit only with approval evidence and idempotency key.
Never call the bridge for shell, credentials, deploy, push-main, delete, or broad filesystem changes.
Treat all results as ION evidence, not accepted state.
```

### Phase 5 — First harmless mutation

Goal: prove GPT Action → gateway → local ION receipt, without Codex execution.

Use `register_artifact`.

Acceptance:

```text
- action validates
- submit requires approval evidence
- receipt written under ION current/action_gateway and/or chatops receipts
- no code files changed
- cockpit/read endpoint shows receipt
```

### Phase 6 — First Codex work packet creation

Goal: GPT Action creates a bounded Codex work packet, but does not run Codex automatically.

Intent:

```text
create_codex_work_packet
```

Acceptance:

```text
- work request appears in ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json
- queue runner status reports queued_request_count > 0
- packet contains required return sections and allowed paths
- no Codex process starts unless local operator invokes runner
```

### Phase 7 — First Codex execution + return intake

Goal: local operator runs Codex CLI on the queued packet and records proof.

Expected flow:

```text
create_codex_work_packet
→ queue runner prepares bounded Codex prompt
→ local Codex CLI executes
→ latest_return.md captured
→ ion_carrier_task_return records return
→ ion_context_proof_gate validates context
→ ion_template_action_gate validates template/action proof
→ Steward queue receives accepted return or refusal
```

Acceptance:

```text
- Codex return starts with CONTEXT PROOF
- changed paths match allowed paths
- tests run and reported
- failure class is precise if blocked
- Steward integration queue updated only after proof gate
```

### Phase 8 — IDE/cockpit MVP

Goal: a local UI over owner surfaces.

Candidate implementation options:

```text
Option A: static HTML/JS served by gateway
Option B: VS Code webview / local panel
Option C: browser extension panel backed by gateway
```

MVP should read:

```text
/status
/policy
/context-pack
/codex/queue
/agent/status
/receipts/recent
/sandbox/returns
```

MVP should write only:

```text
/actions/validate
/actions/submit
```

Do not build a separate task database. Reuse ION queues, receipts, and view models.

### Phase 9 — Security hardening

Add:

```text
- token hash in env, not repo
- request idempotency ledger
- rate limits
- request body max bytes
- redaction of secrets from receipts
- route-level allowlist
- Cloudflare WAF rules
- optional Cloudflare Access service-token compatibility
- structured refusal classes
- replay-block tests
- auth failure tests
```

### Phase 10 — MCP parity / split-brain prevention

Because Custom GPT Actions and Custom Apps/MCP may not be usable simultaneously in the same GPT configuration, keep these as sibling lanes:

```text
ION GPT Actions lane:
  best for direct Custom GPT API ingress and controlled local mutation proposals.

ION MCP/App lane:
  best for richer tool surfaces, custom apps, and full carrier parity once the product path chooses Apps/MCP.
```

Do not let MCP and Actions both write to different owners. Both must route into the same ION queues/receipts.

## 5. Required refusal classes

The gateway must return structured refusals:

```text
AUTH_MISSING
AUTH_INVALID
IDEMPOTENCY_KEY_REQUIRED
IDEMPOTENCY_REPLAY_BLOCKED
PAYLOAD_TOO_LARGE
ENDPOINT_NOT_ALLOWED
INTENT_NOT_SUPPORTED
INTENT_HARD_GATED
PRODUCTION_AUTHORITY_REFUSED
LIVE_EXECUTION_AUTHORITY_REFUSED
OPERATOR_APPROVAL_REQUIRED
APPROVAL_EVIDENCE_INVALID
PATH_NOT_ALLOWED
SCHEMA_INVALID
LOCAL_DAEMON_UNAVAILABLE
ION_OWNER_REFUSED
STEWARD_GATE_REQUIRED
```

## 6. Definition of done for the first real milestone

Milestone M1 is done when:

```text
- Action Gateway implemented with tests.
- Cloudflare hostname points to gateway, not raw daemon.
- GPT Action schema validates in GPT Builder.
- GPT can call health/policy/context/queue.
- GPT can validate a harmless action.
- GPT cannot submit without explicit approval evidence.
- GPT can submit register_artifact after approval.
- Receipt is visible in ION.
- No shell, credential, deploy, push-main, or delete authority exists through Actions.
```

Milestone M2 is done when:

```text
- GPT can create a Codex work packet.
- Local Codex CLI can execute that packet under capture.
- Return passes context proof and template action gate or is rejected with precise failure class.
- Steward integration queue receives only proof-gated returns.
- Cockpit displays the whole trace.
```

## 7. Anti-regression rules

```text
1. Do not build a second agent system.
2. Do not build a second queue.
3. Do not let Actions bypass ChatOps / Codex queue / Steward gates.
4. Do not let Cloudflare auth replace ION authority.
5. Do not let GPT approval replace Steward integration.
6. Do not let Codex output become state without proof.
7. Do not expose broad shell.
8. Do not store secrets in repo.
9. Do not claim production readiness from local tests.
10. Do not treat a public tunnel as a release.
```

## 8. First Codex task

Execute `ION_CODEX_CLI_PACKET_001_ACTION_GATEWAY_MVP_2026-05-07.md`.

That packet should be the only first implementation packet.
