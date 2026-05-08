# ION V69 Execution Horizon

## Current branch

`V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_PROTOCOL`

## Purpose

Define the hosted-MCP account/workspace/state-root/auth boundary before ION exposes any hosted mutation or live execution route.

## Required implementation surfaces

- `kernel.ion_mcp_hosted_auth_alpha`
- `ion_mcp_hosted_alpha_boundary_report.schema.json`
- `ion_mcp_hosted_auth_alpha_policy.yaml`
- focused tests proving token/session/workspace separation

## Exit criteria

1. Baseline hosted alpha dry-run mount is accepted.
2. Wrong token audience is refused.
3. Elevated/live scopes require approval and are not granted.
4. Token identifiers cannot be used as ION session identifiers.
5. Transport sessions cannot become ION authority.
6. No decision authorizes live execution.
7. No decision mutates kernel truth.

## Next branch

`V70_HOSTED_MCP_OAUTH_AND_STREAMABLE_HTTP_IMPLEMENTATION_PREVIEW`

V70 should still remain non-production and should prove actual HTTP/OAuth mechanics without granting live execution.
