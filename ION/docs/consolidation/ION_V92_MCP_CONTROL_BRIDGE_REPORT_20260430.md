# ION V92 — MCP Control Bridge Report

## Summary

V92 adds a bounded MCP control bridge so Cursor can call ION kernel commands directly instead of relying on the Auto mode agent to remember the workflow.

## Why this exists

The main failure is not lack of architectural prose. The failure is that the Cursor parent model drifts. It forgets to refresh active packets, asks the user to manage internal ION routing, and collapses carrier-control into ordinary assistant behavior.

MCP gives Cursor explicit tools:

```text
ion_status
ion_continue
ion_context_plan
ion_cockpit_view
ion_workflow_audit
ion_read_active_packet
ion_task_return
```

## Added files

```text
.cursor/mcp.json
.cursor/commands/ion-mcp-status.md
.cursor/rules/ion-mcp-control-bridge.mdc
ION/09_integrations/mcp/ion_mcp_server.py
ION/09_integrations/mcp/README.md
ION/04_packages/kernel/ion_mcp_bridge_audit.py
ION/tests/test_kernel_ion_mcp_bridge_audit.py
ION/02_architecture/ION_MCP_CONTROL_BRIDGE_PROTOCOL.md
ION/05_context/current/ACTIVE_MCP_BRIDGE_STATE.json
ION/05_context/current/PRODUCTIZED_RUNTIME_MANIFEST_V92.json
ION/05_context/signals/v92_mcp_control_bridge_receipt_20260430.txt
```

## Correct interpretation

This bridge helps Cursor command ION. It does not magically let this hosted ChatGPT conversation reach a private local Cursor process.

For this ChatGPT conversation to directly command ION, a second layer is required:

```text
remote HTTPS MCP app/server
+ authentication
+ ChatGPT app/developer/workspace connection
+ explicit action approvals
+ no arbitrary shell
```

## Validation commands

From the shell root after applying this update:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S ION/09_integrations/mcp/ion_mcp_server.py --ion-root . --self-test
```

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_mcp_bridge_audit --ion-root . --json
```

Expected:

```text
ION_MCP_CONTROL_BRIDGE_READY
```

## Safety posture

The bridge does not expose arbitrary shell, credentials, production authority, or destructive actions. It only exposes bounded ION control tools.
