# ION MCP Control Bridge

This directory contains ION's bounded MCP server for Cursor.

## What this bridge is

`ion_mcp_server.py` exposes a small set of ION kernel commands as MCP tools so Cursor can call ION state transitions directly instead of relying on the Auto mode model to remember the workflow from prose.

Project-level Cursor configuration lives at:

```text
.cursor/mcp.json
```

Cursor should show a project MCP server named:

```text
ion-control
```

## Tools exposed

```text
ion_status
ion_continue
ion_context_plan
ion_cockpit_view
ion_workflow_audit
ion_read_active_packet
ion_task_return
```

## Safety model

The MCP server is intentionally bounded. It does not expose arbitrary shell, arbitrary file write, credentials, network access, or destructive operations. It runs only named ION kernel commands and reads only whitelisted active packet/report surfaces.

## Local smoke test

From the ION shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S ION/09_integrations/mcp/ion_mcp_server.py --ion-root . --self-test
```

Then run the audit:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_mcp_bridge_audit --ion-root . --json
```

## Important limitation

This local stdio MCP bridge lets **Cursor** call ION tools. It does not automatically let this ChatGPT conversation command your private local Cursor process. For ChatGPT to call ION directly, ION must also be exposed as a remote HTTPS MCP app/server and connected through ChatGPT Apps/developer/workspace settings with explicit action controls.
