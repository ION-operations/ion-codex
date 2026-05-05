# V124 Legacy Cloudflare Tunnel Reuse Lock

## Authority

V124 classifies the older AIMOS Cloudflare tunnel scripts as donor evidence for
the ChatGPT browser connector lane.

## Problem

The older tunnel system carried a useful transport pattern:

```text
cloudflared tunnel --url http://localhost:<port>
```

But that older system also carried stale authority for this branch:

```text
AIMOS identity
legacy /sse endpoint
legacy data/mcp status path
host-level install hints
legacy default port assumptions
```

ION must reuse the proven Cloudflare quick-tunnel transport without restoring
the older AIMOS MCP surface as current authority.

## Law

The old tunnel is donor substrate, not current ION identity.

Reusable:

```text
cloudflared quick tunnel transport
trycloudflare.com public URL discovery
status JSON evidence pattern
```

Forbidden as current authority:

```text
AIMOS identity
/sse endpoint
data/mcp/active_tunnel.json as current ION status
auto-installing cloudflared as an ION runtime mutation
production or live execution authority claims
```

## Current Connector Shape

The current ChatGPT browser connector must use:

```text
local preview: http://127.0.0.1:8765/mcp
Cloudflare target: http://127.0.0.1:8765
public connector URL: https://<cloudflare-host>/mcp
```

## Status Evidence

V124 writes its donor reuse audit to:

```text
ION/05_context/current/CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json
```

## Authority Ceiling

Production authority remains `false`.

Live execution authority remains `false`.

Deployment authority remains `false`.
