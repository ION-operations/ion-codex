# Local MCP Transport Preview Guide

V67 provides a local transport-preview harness for ION MCP bridge work.

Run:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_transport_preview --ion-root ION --json
```

The preview compares:

1. stdio JSON-RPC handling through `handle_jsonrpc_message`;
2. local Streamable-HTTP-style JSON-RPC handling through `handle_streamable_http_preview_request`.

The HTTP preview is not a hosted server. It is a boundary test for the future hosted MCP branch. It supports only local POST `/mcp` semantics and refuses to claim OAuth, cloud, streaming/SSE, production deployment, or live execution.

A passing report must show:

- `passed: true`
- `live_execution_authorized_seen: false`
- `kernel_truth_mutation_seen: false`
- live execution requests refused with `REFUSED`
