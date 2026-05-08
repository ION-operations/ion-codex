# ChatGPT Browser Legacy Cloudflare Tunnel Reuse V124

## Current Verdict

V124 confirms that the older AIMOS Cloudflare tunnel system is useful as donor
evidence for one thing only:

```text
cloudflared tunnel --url <local-http-service>
```

It is not current ION authority. The old `/sse` endpoint and AIMOS identity are
not carried forward.

## Current Connector URL

Use this shape for ChatGPT browser connector setup:

```text
https://<cloudflare-host>/mcp
```

Do not use:

```text
https://<cloudflare-host>/sse
```

## Prerequisite

Install `cloudflared` and make sure it is on `PATH`.

ION does not auto-install `cloudflared` because package installation is
host-level setup, not an ION runtime mutation.

If `cloudflared` exists outside `PATH`, pass its absolute path:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel --ion-root . --start --port 8765 --cloudflared-binary /absolute/path/to/cloudflared
```

## Terminal 1: Start Local HTTP MCP Preview

From the ION shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_mcp_http_preview --ion-root . --host 127.0.0.1 --port 8765 --serve
```

Local endpoint:

```text
http://127.0.0.1:8765/mcp
```

## Terminal 2: Start Cloudflare Tunnel

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel --ion-root . --start --port 8765
```

Cloudflare targets the local service root:

```text
http://127.0.0.1:8765
```

ION appends `/mcp` when it records the public connector URL.

## Status Files

Runtime tunnel status:

```text
ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json
```

Legacy donor reuse audit:

```text
ION/05_context/current/CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json
```

## Audit Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_legacy_tunnel_reuse_audit --ion-root . --write --json
```

Expected current state before `cloudflared` is installed:

```text
ION_CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_SETUP_REQUIRED
```

That state is acceptable when the donor reuse contract is safe and only host
setup remains.
