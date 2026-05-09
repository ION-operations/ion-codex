# ION MCP Custom GPT Action

This folder contains an OpenAPI schema for connecting the existing ION MCP
HTTP preview to a Custom GPT as a second Action.

This Action is explicit-use only. It is not the default ION mount path. Do not
use it to boot the uploaded sandbox/package, answer from files, satisfy
`/guest-mode`, satisfy `/what is ION?`, or start first-time context. Use it only
when the user asks for live MCP/local hub status, tool listing, runtime reads,
or a connector-backed action.

Use this when the GPT Builder accepts OpenAPI Actions but does not expose the
normal ChatGPT Apps/Connectors MCP setup inside the Custom GPT configuration.

## Endpoint

The schema targets the existing ION MCP tunnel:

```text
https://ion.helixion.net/mcp
```

It does not create a new server. It wraps the existing JSON-RPC MCP methods:

- `initialize`
- `tools/list`
- `tools/call`
- `ping`

## Custom GPT Setup

Add this as a separate Action from the Action Gateway:

- Action Gateway schema: `ION/09_integrations/custom_gpt_action_gateway/openapi.yaml`
- MCP schema: `ION/09_integrations/chatgpt_browser_mcp_action/openapi.yaml`

The MCP Action is useful for explicit broad ION read/status/tool access. The
Action Gateway remains the approval-gated path for bounded submits, receipts,
and work-packet creation. Uploaded package/sandbox files remain the default
source for ordinary Custom GPT work.

## Example Bodies

List tools:

```json
{
  "jsonrpc": "2.0",
  "id": "tools-list-1",
  "method": "tools/list",
  "params": {}
}
```

Call `ion_status`:

```json
{
  "jsonrpc": "2.0",
  "id": "ion-status-1",
  "method": "tools/call",
  "params": {
    "name": "ion_status",
    "arguments": {}
  }
}
```

Bounded write tools require:

```json
{
  "confirmation": "ION_BOUNDED_WRITE_CONFIRMED"
}
```
