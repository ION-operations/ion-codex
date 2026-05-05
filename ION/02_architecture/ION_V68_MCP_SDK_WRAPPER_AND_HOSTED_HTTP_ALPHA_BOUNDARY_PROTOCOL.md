# ION V68 MCP SDK Wrapper and Hosted HTTP Alpha Boundary Protocol

## Branch

`V68_OFFICIAL_MCP_SDK_WRAPPER_OR_HOSTED_HTTP_ALPHA_BOUNDARY`

## Purpose

V68 converts the V67 transport preview into a stricter product-boundary decision:

1. keep the dependency-free local MCP bridge as the canonical founder/local path;
2. define an official MCP SDK wrapper seam without making the SDK a hard dependency;
3. preview the hosted Streamable-HTTP-shaped `/mcp` boundary as an alpha contract;
4. prove that HTTP alpha projection preserves the same ION execution-resolution law as stdio.

## Non-goals

V68 does not certify:

- public hosted cloud operation;
- OAuth or account login;
- Kubernetes;
- multi-tenant isolation;
- provider dispatch;
- browser mutation;
- shell execution;
- credential access;
- live daemon loops;
- direct governed-write mutation;
- `LIVE_EXECUTED` results.

## Canonical decision

The no-dependency local bridge remains canonical for local founder/developer operation until real client certification proves that the official MCP SDK can be adopted without reducing local determinism or increasing hidden authority.

The official MCP SDK is treated as a wrapper/adaptation layer, not as a replacement kernel, scheduler, policy engine, receipt ledger, or approval queue.

## Required execution resolutions

Every V68 MCP-facing operation must resolve to one of:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

No V68 operation may resolve to `LIVE_EXECUTED`.

## Hosted HTTP alpha boundary

The hosted HTTP alpha boundary is a contract preview. It may project a local `POST /mcp` shape, but it is not a public endpoint. Before public exposure, later branches must add:

- OAuth or equivalent hosted auth;
- TLS and reverse-proxy hardening;
- Origin validation;
- tenant/workspace isolation;
- rate limiting;
- audit log retention;
- secret isolation;
- receipt durability;
- replay/rollback verification;
- abuse and prompt-injection hardening.

## ION workflow interpretation

V68 is a transport/product-boundary branch. It does not expand action authority. It exists to decide how ION should wrap MCP clients while preserving the V62 operator-approval and V64-V67 local dry-run bridge law.

## Branch invariant

`MCP transport parity is valid only if the execution boundary is unchanged.`
