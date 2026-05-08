---
type: relay_steward_workpacket
mission: V76_CURSOR_CAPABILITY_INVENTORY_AND_ION_MCP_BRIDGE_ACCELERATION
date: 2026-04-27
---

# Work packet — MCP bridge acceleration (simulated Cursor cycle)

## Mount chain

1. **RELAY** — intake for mission `V76_CURSOR_CAPABILITY_INVENTORY_AND_ION_MCP_BRIDGE_ACCELERATION`; `relay_packet_id: RELAY-V76-MCP-BRIDGE-20260427`.
2. **STEWARD** — task-scoped orchestration; routes two named carriers.
3. **MASON** — inspect `ION/mcp_server/` scaffold (read-only).
4. **NEMESIS** (audit lane; packet alias **AUDITOR**) — run allowlisted MCP-related pytest selection; returns **proposal** only.
5. **STEWARD integration** — `v76_mcp_bridge_steward_integration_receipt_20260427.txt`.
6. **RELAY report** — `v76_mcp_bridge_relay_report_20260427.md`.

## Gates

- `production_authority`: false  
- `live_execution_authority`: false  
- No Cloudflare login, no tokens, no destructive filesystem operations.

## Bounded reads (MASON)

- `ION/mcp_server/README.md`
- `ION/mcp_server/security.py`
- `ION/mcp_server/tools.py`

## Bounded validation (NEMESIS / AUDITOR)

- `PYTHONPATH=ION/04_packages python3 -m pytest ION/tests/test_mcp_server_readonly_tools.py ION/tests/test_kernel_ion_mcp_hosted_bundle_replay_alpha.py -q`  
  (explicit files — **never** `pytest -k mcp` here: it can recurse with MCP server tests and freeze the host.)
