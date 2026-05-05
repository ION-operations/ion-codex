# MCP Carrier Profile

carrier_id: MCP_CARRIER
host_family: mcp
default_level: L0
candidate_levels: [L1, L4]
default_return_agent: CURRENT_CARRIER

## Host-specific principle

MCP is an adapter/runtime carrier only when actual callable ION operations exist and call proofs are produced.

## L4 requirements

An MCP Carrier may request L4 only when it can prove:
- runtime operation names;
- input/output schemas;
- call proof;
- journal or receipt path;
- fallback manual template.

## Forbidden

- Do not equate an MCP server with ION runtime authority unless it exposes ION-owned operations.
