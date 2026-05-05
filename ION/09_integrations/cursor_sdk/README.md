# ION Cursor SDK Carrier Adapter

This directory is a conservative TypeScript SDK integration scaffold for Cursor's public beta SDK.

It is not live production authority. It exists so ION can evolve from manual Cursor parent-chat control into programmatic local/cloud carrier runs without changing ION's core law.

## Intended flow

1. Run `kernel.ion_carrier_continue` in the repository root.
2. Read `ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json`.
3. For each `spawn=true` row, send the generated `context_package_path` material to a Cursor SDK agent.
4. Save the agent's full response as markdown.
5. Run `kernel.ion_carrier_task_return` against the captured markdown.
6. Steward integrates only accepted returns.

## Install sketch

```bash
cd ION/09_integrations/cursor_sdk
npm install
CURSOR_API_KEY=... npm run carrier:continue
```

The adapter intentionally defaults to local runtime and `composer-2`. Higher models or cloud runtime require explicit operator configuration.
