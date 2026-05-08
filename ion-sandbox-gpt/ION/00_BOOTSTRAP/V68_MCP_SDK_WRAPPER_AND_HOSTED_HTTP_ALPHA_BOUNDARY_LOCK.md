# V68 Branch Lock — MCP SDK Wrapper and Hosted HTTP Alpha Boundary

Branch: `V68_OFFICIAL_MCP_SDK_WRAPPER_OR_HOSTED_HTTP_ALPHA_BOUNDARY`

This lock authorizes only a boundary/adapter expansion over the existing local MCP bridge.

## Authorized

- add SDK-wrapper decision surfaces;
- add hosted HTTP alpha contract preview;
- add report schema and policy;
- add focused tests proving no live authority;
- preserve V64/V65/V66/V67 local bridge semantics.

## Forbidden

- live execution;
- public cloud certification;
- OAuth certification;
- Kubernetes certification;
- provider dispatch;
- shell execution;
- browser mutation;
- credential access;
- live daemon loop activation;
- direct governed-write mutation;
- treating official SDK presence as kernel authority.

## Required result set

All actions must resolve to one of:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

`LIVE_EXECUTED` is forbidden in V68.
