# V70 Branch Lock

Branch: `V70_HOSTED_MCP_OAUTH_AND_STREAMABLE_HTTP_IMPLEMENTATION_PREVIEW`

This branch is locked to hosted MCP mechanics preview only.

Allowed:

- local OAuth-code/PKCE preview;
- local bearer validation preview;
- local Streamable-HTTP-style `/mcp` preview;
- read-only/dry-run/approval-required/refusal outcomes.

Forbidden:

- production OAuth certification;
- hosted cloud certification;
- public endpoint claims;
- Kubernetes claims;
- live execution;
- shell execution;
- browser mutation;
- provider dispatch;
- credential access;
- direct governed-write mutation.
