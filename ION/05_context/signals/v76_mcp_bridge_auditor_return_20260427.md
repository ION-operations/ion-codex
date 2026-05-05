---
type: role_carrier_proposal
role: NEMESIS
packet_alias: AUDITOR
carrier: cursor_subagent
status: PROPOSAL
---

# NEMESIS return — MCP-focused test sweep (AUDITOR lane)

## Command executed (allowlisted pattern)

- `PYTHONPATH=ION/04_packages python3 -m pytest ION/tests/test_mcp_server_readonly_tools.py ION/tests/test_kernel_ion_mcp_hosted_bundle_replay_alpha.py -q` (explicit paths; avoids `pytest -k mcp` nesting hazard).

## Posture

- Read-only validation lane; no production authority.
- No live external connector invoked.

## Integration

- Awaiting Steward receipt.
