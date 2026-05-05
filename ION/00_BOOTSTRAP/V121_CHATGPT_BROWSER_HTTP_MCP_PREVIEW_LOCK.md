# V121 ChatGPT Browser HTTP MCP Preview Lock

## Lock

V121 adds a local HTTP MCP preview for the ChatGPT browser connector. It proves
the MCP-shaped tool surface without claiming public connector deployment.

## Authority Boundary

```text
connector_state: LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Required Surfaces

```text
ION/02_architecture/ION_CHATGPT_BROWSER_HTTP_MCP_PREVIEW_PROTOCOL.md
ION/03_registry/ion_chatgpt_browser_http_mcp_preview.schema.json
ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py
ION/09_integrations/mcp/chatgpt_connector/ion_chatgpt_browser_http_mcp_preview.py
ION/docs/setup/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_SETUP_V121.md
ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py
```

