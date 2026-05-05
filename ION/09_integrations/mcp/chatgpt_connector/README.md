# ION ChatGPT Browser MCP Connector

V120 defines this directory as the ChatGPT-browser-facing connector lane.

This is not the existing local Cursor stdio bridge. The local bridge remains:

```text
ION/09_integrations/mcp/ion_mcp_server.py
```

The ChatGPT browser lane is intended to become an HTTPS MCP/custom connector
reachable from ChatGPT. V120 creates the safe contract and local self-test
surface before any hosted deployment is claimed.

## Current State

```text
CONTRACT_READY_NOT_DEPLOYED
```

No production connector is claimed. No live ChatGPT browser access to the local
machine is claimed.

## Allowed Tool Families

Read/status tools may expose bounded ION state:

```text
ion_status
ion_current_operating_packet
ion_read_active_packet
ion_context_plan
ion_cockpit_view
ion_artifact_manifest
ion_receipt_search
ion_git_status_summary
```

Queue/receipt tools may write only bounded packets:

```text
ion_queue_operator_message
ion_request_codex_work_packet
ion_submit_task_return
ion_record_chatgpt_decision
ion_create_containment_receipt
```

## Forbidden Capabilities

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
```

## Contract Self-Test

From shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S ION/09_integrations/mcp/chatgpt_connector/ion_chatgpt_browser_connector.py --ion-root . --self-test
```

