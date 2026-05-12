# ION Local Port Routing Truth

Status: candidate local routing truth for `PCKT-ION-MCP-PORT-ROUTING-TRUTH-001`.

This document separates ION MCP, ION Action Gateway, local cockpit, and the
sibling dAimon Gemini bridge so local services do not silently collide.

## Canonical Local Owners

| Port | Owner | Surface | Public/tunnel route |
| --- | --- | --- | --- |
| `8765` | ION | ChatGPT browser MCP HTTP preview, `/mcp` | `ion-browser` tunnel to `https://ion.helixion.net/mcp` |
| `8777` | ION | Custom GPT Action Gateway | `ion-actions` tunnel to `https://ion-actions.helixion.net` |
| `8788` | ION | local cockpit app | local only |
| `8767` | ION | ChatOps local bridge | local only |
| `8795` | dAimon Gemini | sibling websocket bridge | local only |
| `8796` | dAimon Gemini | reserved secondary dAimon surface | local only |

## Current Collision

Observed on 2026-05-12:

```text
127.0.0.1:8765 -> /home/sev/ION - Production/dAimon_gemini/scripts/ion_bridge_server.py
127.0.0.1:8777 -> kernel.ion_custom_gpt_action_gateway
127.0.0.1:8788 -> kernel.ion_local_cockpit_app
ion-browser tunnel -> http://127.0.0.1:8765
```

That means the public `ion-browser` tunnel is aimed at the dAimon Gemini bridge
instead of ION MCP preview. ION must not run MCP preview and dAimon Gemini on
the same port.

## Routing Decision

Keep:

```text
ION MCP preview: 127.0.0.1:8765
ION Action Gateway: 127.0.0.1:8777
ION local cockpit: 127.0.0.1:8788
```

Move:

```text
dAimon Gemini websocket bridge: 127.0.0.1:8795
```

## dAimon Migration Patch Shape

The sibling dAimon repo currently hardcodes the collision:

```text
/home/sev/ION - Production/dAimon_gemini/scripts/ion_bridge_server.py
  websockets.serve(handler, "localhost", 8765)

/home/sev/ION - Production/dAimon_gemini/extension/src/background.js
  ws://localhost:8765
```

The safe migration is:

```text
scripts/ion_bridge_server.py:
  read DAIMON_GEMINI_BRIDGE_HOST, default 127.0.0.1
  read DAIMON_GEMINI_BRIDGE_PORT, default 8795
  bind websockets.serve(handler, host, port)

extension/src/background.js:
  default websocket URL becomes ws://localhost:8795
```

Do not apply that sibling patch from an ION packet unless Braden explicitly
approves editing `/home/sev/ION - Production/dAimon_gemini`.

Candidate sibling diff, not applied by this packet:

```diff
diff --git a/scripts/ion_bridge_server.py b/scripts/ion_bridge_server.py
--- a/scripts/ion_bridge_server.py
+++ b/scripts/ion_bridge_server.py
@@
 import sys
 import os
@@
+BRIDGE_HOST = os.environ.get("DAIMON_GEMINI_BRIDGE_HOST", "127.0.0.1")
+BRIDGE_PORT = int(os.environ.get("DAIMON_GEMINI_BRIDGE_PORT", "8795"))
+
@@
 async def main():
-    async with websockets.serve(handler, "localhost", 8765):
-        print("ION Kernel Bridge running on ws://localhost:8765")
+    async with websockets.serve(handler, BRIDGE_HOST, BRIDGE_PORT):
+        print(f"ION Kernel Bridge running on ws://{BRIDGE_HOST}:{BRIDGE_PORT}")
         await asyncio.Future()
diff --git a/extension/src/background.js b/extension/src/background.js
--- a/extension/src/background.js
+++ b/extension/src/background.js
@@
-const socket = new WebSocket('ws://localhost:8765');
+const ION_DAIMON_BRIDGE_WS_URL = globalThis.ION_DAIMON_BRIDGE_WS_URL || 'ws://localhost:8795';
+const socket = new WebSocket(ION_DAIMON_BRIDGE_WS_URL);
```

## Refresh Sequence After Approval

Stop only the dAimon Gemini bridge currently occupying `8765`:

```sh
kill <daimon-gemini-bridge-pid>
```

Start dAimon on `8795` after the sibling patch exists:

```sh
cd "/home/sev/ION - Production/dAimon_gemini"
DAIMON_GEMINI_BRIDGE_HOST=127.0.0.1 DAIMON_GEMINI_BRIDGE_PORT=8795 \
  python3 scripts/ion_bridge_server.py
```

Start ION MCP preview on `8765`:

```sh
cd "/home/sev/ION - Production/ION_CODEX FULL"
PYTHONPATH=ION/04_packages \
  python3 -S -m kernel.ion_chatgpt_browser_mcp_http_preview \
  --ion-root . --host 127.0.0.1 --port 8765 --serve
```

Keep the `ion-browser` tunnel pointed to:

```text
http://127.0.0.1:8765
```

## Read-only Verification

```sh
PYTHONPATH=ION/04_packages python3 -m kernel.ion_local_port_routing --ion-root . --json
ss -ltnp | rg ':(8765|8777|8788|8795|8796)\b'
curl -fsS http://127.0.0.1:8765/health
curl -fsS http://127.0.0.1:8777/health
curl -fsS http://127.0.0.1:8788/health
```

## Non-claims

This routing truth does not deploy production, start queue workers, re-enable
live Action/MCP mutation, delete evidence, or claim accepted state.
