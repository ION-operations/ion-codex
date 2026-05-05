# ChatGPT Browser MCP Connector Setup V120

## Status

```yaml
connector_id: ION_CHATGPT_BROWSER_CONNECTOR
version_line: V120_CHATGPT_BROWSER_MCP_CONNECTOR_AND_CORRECT_CARRIER_ONBOARDING
connector_state: CONTRACT_READY_NOT_DEPLOYED
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Purpose

V120 creates the safe connector contract for a future ChatGPT-browser-facing ION
connector. It does not claim that ChatGPT can currently command the local ION
tree.

The local Cursor/Codex lane remains the heavy build lane. The ChatGPT browser
lane is for continuity, coordination, current-state inspection, bounded queue
packets, decision receipts, and proof-gated task-return packets.

## Official Platform Constraint

OpenAI's current Apps SDK documentation describes MCP as the backbone for Apps
SDK tool integration, with servers listing tools, handling tool calls, and
optionally returning UI resources. It also says Apps SDK supports SSE and
Streamable HTTP, recommending Streamable HTTP for hosted servers.

OpenAI's ChatGPT connection guide says a ChatGPT connector requires an MCP
server reachable over HTTPS, with the connector URL pointing at the public
`/mcp` endpoint. Local servers can be exposed for development through a tunnel,
but that is a deployment decision, not current ION authority.

Sources:

```text
https://developers.openai.com/apps-sdk/concepts/mcp-server
https://developers.openai.com/apps-sdk/deploy/connect-chatgpt
https://developers.openai.com/apps-sdk/guides/security-privacy
```

## Current Local Validation

From shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_mcp_connector_contract --ion-root . --write --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S ION/09_integrations/mcp/chatgpt_connector/ion_chatgpt_browser_connector.py --ion-root . --self-test
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py -q
```

Expected:

```text
ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY
```

## Allowed MVP Tools

Read/status:

```text
ion_status
ion_current_operating_packet
ion_carrier_onboarding_packet
ion_read_active_packet
ion_context_plan
ion_cockpit_view
ion_artifact_manifest
ion_receipt_search
ion_git_status_summary
```

## Correct Carrier Onboarding Tool

The ChatGPT browser connector must start with:

```text
ion_carrier_onboarding_packet
```

That tool returns the ION-native mount path:

```text
pyproject.toml + ION/REPO_AUTHORITY.md
ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md or later
carrier profile under ION/03_registry/
ION/02_architecture/ION_MOUNT_CONTRACT.md
active packets under ION/05_context/current/
role boot/context surfaces
compiled context bundles
execution packet templates
context proof, template-action proof, task return, and receipt flow
```

Root-level `START_HERE_FOR_ANY_AGENT.md` and `AGENTS.md` are not connector
onboarding authority.

Bounded queue/receipt:

```text
ion_queue_operator_message
ion_request_codex_work_packet
ion_submit_task_return
ion_record_chatgpt_decision
ion_create_containment_receipt
```

## Forbidden MVP Capabilities

```text
arbitrary shell
arbitrary file write
direct delete
git push
credential access
browser/computer control
provider API calls
unbounded local filesystem access
production deployment
direct acceptance of unproofed worker output
```

## Deployment Gate

A future hosted connector must not become active until it proves:

```text
HTTPS MCP endpoint reachable
auth/scopes explicit
tool policy matches V120 registry
write tools require confirmation or bounded receipt queueing
task-return packets require CONTEXT PROOF and TEMPLATE ACTION PROOF
no arbitrary shell/file/delete/git/credential/provider/browser control
production_authority=false
live_execution_authority=false unless separately ratified
```

## First ChatGPT Connector Trial

This is a bounded operator trial, not production deployment. The connector state
must remain conservative until ChatGPT actually adds the connector and calls
tools successfully.

Current transport truth values:

```text
NOT_INSTALLED
INSTALLED_NOT_RUNNING
LOCAL_HTTP_RUNNING_ONLY
TUNNEL_RUNNING_NOT_VERIFIED
TUNNEL_RUNNING_VERIFIED
CHATGPT_CONNECTOR_ADDED_NOT_TESTED
CHATGPT_CONNECTOR_TESTED_READY
```

From shell root, start the local HTTP MCP preview:

```bash
mkdir -p ION/05_context/current/chatgpt_connector/runtime
setsid env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
  python3 -S -m kernel.ion_chatgpt_browser_mcp_http_preview \
  --ion-root . --host 127.0.0.1 --port 8765 \
  > ION/05_context/current/chatgpt_connector/runtime/http_preview.log 2>&1 &
echo $! > ION/05_context/current/chatgpt_connector/runtime/http_preview.pid
```

Refresh local transport truth:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
  python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel \
  --ion-root . --cloudflared-binary /home/sev/.local/bin/cloudflared \
  --write --json
```

Expected before a public tunnel:

```text
transport_state: LOCAL_HTTP_RUNNING_ONLY
active_connector_url: null
production_authority: false
live_execution_authority: false
deployment_authority: false
```

Start the Cloudflare quick tunnel:

```bash
setsid env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
  python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel \
  --ion-root . --cloudflared-binary /home/sev/.local/bin/cloudflared \
  --start \
  > ION/05_context/current/chatgpt_connector/runtime/cloudflare_tunnel.log 2>&1 &
echo $! > ION/05_context/current/chatgpt_connector/runtime/cloudflare_tunnel.pid
```

Refresh and print the public connector URL:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
  python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel \
  --ion-root . --cloudflared-binary /home/sev/.local/bin/cloudflared \
  --write --json
python3 - <<'PY'
import json
from pathlib import Path
path = Path("ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json")
data = json.loads(path.read_text())
print(data.get("active_connector_url") or "")
PY
```

Paste only the printed HTTPS URL ending in `/mcp` into ChatGPT custom connector
settings.

First expected ChatGPT tool calls:

```text
1. ion_carrier_onboarding_packet
2. ion_status
3. ion_request_codex_work_packet
```

The bounded write test must include explicit confirmation:

```text
confirmation: ION_BOUNDED_WRITE_CONFIRMED
```

Without that confirmation, the connector must return:

```text
bounded_write_confirmation_required
```

After ChatGPT has actually connected and called tools successfully, record that
as a connector receipt before changing state beyond
`CHATGPT_CONNECTOR_ADDED_NOT_TESTED`.

Stop / rollback:

```bash
kill "$(cat ION/05_context/current/chatgpt_connector/runtime/cloudflare_tunnel.pid)" 2>/dev/null || true
kill "$(cat ION/05_context/current/chatgpt_connector/runtime/http_preview.pid)" 2>/dev/null || true
pkill -f 'cloudflared tunnel --url http://127.0.0.1:8765' 2>/dev/null || true
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S - <<'PY'
from kernel.ion_chatgpt_browser_cloudflare_tunnel import write_tunnel_status
write_tunnel_status(
    ".",
    tunnel_url=None,
    running=False,
    local_url="http://127.0.0.1:8765",
    endpoint_path="/mcp",
    error="operator_stop",
)
PY
```

Do not claim `CHATGPT_CONNECTOR_TESTED_READY` until ChatGPT browser itself has
called the connector and the returned state/receipt is inspected.
