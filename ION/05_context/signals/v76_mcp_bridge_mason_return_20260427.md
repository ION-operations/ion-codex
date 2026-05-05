---
type: role_carrier_proposal
role: MASON
carrier: cursor_subagent
status: PROPOSAL
---

# MASON return — MCP server scaffold inspection

## Summary

- `ION/mcp_server/` present: `security.py` allowlists, `tools.py` adapter-neutral handlers, `server.py` catalog/invoke CLI, `README.md` tier table.
- No arbitrary shell tool; `ion.run_approved_check` maps to fixed `APPROVED_CHECKS` only.

## Risks

- MCP reference SDK not pinned; stdio session bridge is future work.

## Integration

- Awaiting Steward receipt for witness merge.
