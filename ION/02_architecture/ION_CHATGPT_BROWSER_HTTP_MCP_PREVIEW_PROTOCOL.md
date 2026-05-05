# ION ChatGPT Browser HTTP MCP Preview Protocol

## Version

V121

## Purpose

V121 adds a local HTTP MCP preview for the V120 ChatGPT browser connector
contract. This preview proves the connector can expose an MCP-shaped `/mcp`
surface with only bounded ION tools before any public HTTPS connector is
claimed.

This is not production deployment authority.

## Official Platform Frame

OpenAI Apps SDK documentation describes MCP servers as exposing tool listing
and tool calling capabilities, and says the transport may be Server-Sent Events
or Streamable HTTP, with Streamable HTTP recommended for hosted servers.

OpenAI's ChatGPT connector setup requires the MCP server to be reachable over
HTTPS and registered through ChatGPT connector settings. It also notes that
write tools require manual confirmation in ChatGPT unless approvals are
remembered for the conversation.

Security guidance requires server-side input validation, human confirmation for
irreversible operations, minimal data exposure, and scoped authentication for
hosted connectors.

## V121 Preview Boundary

```text
connector_state: LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR
endpoint_path: /mcp
default_bind_host: 127.0.0.1
production_authority: false
live_execution_authority: false
deployment_authority: false
```

The preview handles:

```text
initialize
tools/list
tools/call
ping
```

It also exposes:

```text
GET /health
```

## Write Confirmation Gate

All bounded queue/receipt tools require:

```json
{"confirmation": "ION_BOUNDED_WRITE_CONFIRMED"}
```

without which the tool call returns:

```text
bounded_write_confirmation_required
```

The preview still does not allow arbitrary shell, arbitrary file write, delete,
git push, credential access, provider calls, browser/computer control, or
production deployment.

## Validation

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_mcp_http_preview --ion-root . --self-test --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py -q
```

