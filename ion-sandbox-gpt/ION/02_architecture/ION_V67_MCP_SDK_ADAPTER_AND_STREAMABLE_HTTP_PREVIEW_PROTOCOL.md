# ION V67 MCP SDK Adapter and Streamable HTTP Preview Protocol

## Branch

`V67_OFFICIAL_MCP_SDK_ADAPTER_AND_STREAMABLE_HTTP_PREVIEW`

## Purpose

V67 extends the V64/V65/V66 local MCP bridge by adding a transport-preview layer and an official-SDK adapter seam. It proves that the existing local JSON-RPC stdio bridge can be projected through a Streamable-HTTP-style local `/mcp` POST envelope without changing ION authority semantics.

## Governing law

MCP remains a socket into ION, not a sovereign engine. The ION kernel, runtime session store, receipt ledger, approval queue, and dry-run handoff law remain authoritative.

V67 may compare stdio and local HTTP preview behavior, expose an SDK availability/status adapter seam, return protocol and transport certification receipts, and prove live execution remains refused across transports.

V67 may not enable OAuth, claim hosted/cloud certification, run Kubernetes or a production server, call providers, mutate browsers, read or write credentials, execute shell commands through MCP, start the daemon loop, or return `LIVE_EXECUTED`.

## Allowed execution resolutions

Every V67-facing result must resolve to one of:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

`LIVE_EXECUTED` is forbidden in V67.

## Transport preview rule

The Streamable HTTP preview is a local, in-process compatibility envelope. It models POST `/mcp` JSON-RPC request handling only. It does not claim full hosted Streamable HTTP production behavior, SSE streaming, OAuth, tenant isolation, deployment hardening, or external network exposure.

## Promotion gate

Before ION may move to hosted MCP, the following must be true:

1. stdio and HTTP preview produce equivalent boundary results;
2. live execution remains refused across both transports;
3. kernel truth mutation remains false across both transports;
4. official SDK availability is detected without making it a hard runtime dependency;
5. all transport-preview reports are receiptable and reproducible.
