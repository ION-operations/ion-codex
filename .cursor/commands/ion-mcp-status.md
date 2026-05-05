# /ion-mcp-status

Use the `ion-control` MCP server if available.

1. Call MCP tool `ion_status`.
2. Call MCP tool `ion_workflow_audit`.
3. If MCP is unavailable, run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_mcp_bridge_audit --ion-root . --json
```

Do not summarize from memory. Report packet-backed state only.
