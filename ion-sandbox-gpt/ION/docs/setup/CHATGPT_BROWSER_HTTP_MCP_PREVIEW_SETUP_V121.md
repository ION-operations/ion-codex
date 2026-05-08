# ChatGPT Browser HTTP MCP Preview Setup V121

## Status

```yaml
version_line: V121_CHATGPT_BROWSER_HTTP_MCP_PREVIEW
connector_state: LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR
endpoint_path: /mcp
default_bind_host: 127.0.0.1
default_port: 8765
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Purpose

This preview lets ION exercise an MCP-shaped HTTP connector locally before any
public HTTPS connector is configured in ChatGPT.

It is intentionally not exposed as a public connector by default.

## Run Local Preview

From shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S ION/09_integrations/mcp/chatgpt_connector/ion_chatgpt_browser_http_mcp_preview.py --ion-root . --serve --host 127.0.0.1 --port 8765
```

Health check:

```bash
curl http://127.0.0.1:8765/health
```

MCP endpoint:

```text
http://127.0.0.1:8765/mcp
```

Do not use this localhost URL as a ChatGPT connector URL. ChatGPT connector
registration requires a public HTTPS `/mcp` endpoint.

## Write Tool Confirmation

Every bounded queue/receipt tool must include:

```json
{"confirmation": "ION_BOUNDED_WRITE_CONFIRMED"}
```

Read/status tools do not require this marker.

## Still Forbidden

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

## Public Connector Gate

Before a public ChatGPT connector may be claimed:

```text
HTTPS transport must exist
authentication/scopes must be explicit
write tools must preserve confirmation semantics
server-side input validation must pass
logs must avoid secrets/raw prompt overcollection
production_authority=false remains preserved
live_execution_authority=false remains preserved unless separately ratified
```

