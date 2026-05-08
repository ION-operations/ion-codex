# ION V70 Execution Horizon

## Active horizon

Build the hosted MCP auth/HTTP mechanics preview without granting hosted authority.

## Completion criteria

- OAuth authorization-code + PKCE preview works.
- Wrong PKCE verifier is refused.
- Bearer-header validation is required for `/mcp`.
- `/mcp` POST can reach the local bridge contract.
- Hosted mount still evaluates through V69 account/workspace/state-root law.
- Live execution remains impossible.

## Blocked until later branches

- real OAuth provider integration;
- public endpoint deployment;
- tenant database;
- object storage;
- Kubernetes;
- microVM execution;
- provider credentials;
- live dispatch.
