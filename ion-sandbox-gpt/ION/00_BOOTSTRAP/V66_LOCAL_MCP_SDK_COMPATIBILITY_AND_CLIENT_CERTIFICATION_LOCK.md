# V66 Local MCP SDK Compatibility and Client Certification Lock

Branch: `V66_LOCAL_MCP_SDK_COMPATIBILITY_AND_CLIENT_CERTIFICATION`

This branch promotes the V64/V65 local MCP bridge from smoke-tested bridge to contract-certified local client socket.

## Lock

ION may certify local MCP client profiles only if every certified path remains bounded to:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

This branch may not produce, imply, or simulate `LIVE_EXECUTED` authority.

## Certified profile class

The lock covers contract-level profiles for:

- generic stdio MCP;
- Cursor-style local stdio;
- VS Code-style local stdio;
- Codex-style local stdio.

This is not live attestation from those products. It is ION's local compatibility contract proving that the bridge is shaped correctly for them.

## Hard prohibitions

V66 may not authorize:

- shell execution;
- provider dispatch;
- browser mutation;
- credential access;
- direct governed-write mutation;
- daemon loop activation;
- live job execution;
- hosted ChatGPT app claims;
- cloud/Kubernetes production claims.
