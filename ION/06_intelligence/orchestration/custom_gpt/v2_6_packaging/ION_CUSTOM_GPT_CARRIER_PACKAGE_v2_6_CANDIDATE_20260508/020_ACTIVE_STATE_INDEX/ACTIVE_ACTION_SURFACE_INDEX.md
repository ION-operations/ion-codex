# Active Action Surface Index

## Action 1 — ION Action Gateway

Schema:

`060_ACTION_SCHEMAS/action_gateway/openapi.yaml`

Use for:

- `/health`
- `/policy`
- `/context-pack`
- `/codex/queue`
- `/agent/status`
- `/receipts/recent`
- `/actions/validate`
- `/actions/submit`

Privacy Policy URL:

`https://helixion.net/privacy`

## Action 2 — ION MCP JSON-RPC Action

Schema:

`060_ACTION_SCHEMAS/mcp_json_rpc/openapi.yaml`

Use for:

- health/status;
- JSON-RPC ping;
- tools/list;
- tools/call for bounded read/status;
- current operating packet;
- tool manifest;
- local hub status.

Privacy Policy URL:

`https://helixion.net/privacy`

## Extension / YAML Bridge

Reference:

`070_BROWSER_EXTENSION_YAML_BRIDGE/`

Use fenced `ion_action:` YAML only as proposal text until extension/user approval
and daemon/gateway receipt.
