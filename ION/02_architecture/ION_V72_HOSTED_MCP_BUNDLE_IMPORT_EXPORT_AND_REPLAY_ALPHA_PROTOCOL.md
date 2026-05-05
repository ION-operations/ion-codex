# ION V72 Hosted MCP Bundle Import/Export and Replay Alpha Protocol

## Branch

`V72_HOSTED_MCP_BUNDLE_IMPORT_EXPORT_AND_REPLAY_ALPHA`

## Purpose

V72 extends the V71 hosted storage and receipt-ledger substrate into a deterministic bundle import/export/replay alpha. It defines how ION-over-MCP can package account/workspace/state-root evidence, validate imported bundle material, generate a replay plan, and refuse tampered or authority-inflating bundles.

## Law

Bundle handling is not execution. Export is preview-only. Import is untrusted until validation succeeds. Replay is a projected plan, not mutation. No imported bundle, replay step, or manifest may authorize `LIVE_EXECUTED`, direct governed write, shell execution, browser mutation, provider dispatch, credential access, or daemon loop activation.

## Required V72 resolutions

Every V72 operation resolves to one of:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

`LIVE_EXECUTED` is forbidden.

## Required validation gates

An imported bundle must verify:

1. bundle format version;
2. manifest hash;
3. workspace binding;
4. state-root binding;
5. receipt-event chain ordering;
6. preview-only export flag;
7. absence of forbidden event kinds;
8. absence of forbidden tools;
9. absence of forbidden execution resolutions;
10. absence of kernel-truth mutation and live-execution authorization claims.

## Replay rule

Replay in V72 is a dry-run plan over receipt events. Replay steps may read, verify, project a state root, project a bundle, or queue an approval preview. Replay may not execute.

## Non-goals

V72 does not certify public cloud hosting, production OAuth, production object storage, Kubernetes, live execution, provider dispatch, browser automation, direct governed write, or credential access.
