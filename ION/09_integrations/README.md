# ION Integrations

This directory contains carrier and transport integrations around the ION
kernel.

## Integration Map

```text
browser_extension/   ChatOps browser carrier extension surfaces
cursor_extension/    Cursor extension carrier surface
cursor_sdk/          Cursor SDK carrier adapter
local_daemon/        localhost daemon bridges
mcp/                 MCP servers, previews, and ChatGPT connector surfaces
```

## Current High-Value Surfaces

- `browser_extension/ion_chatops_bridge/README.md`
- `local_daemon/ion_chatops_bridge/README.md`
- `mcp/README.md`
- `mcp/chatgpt_connector/README.md`

## Boundary

Integrations are carrier adapters. They do not become ION identity, Steward
authority, production authority, or broad shell authority by existing in this
directory.

