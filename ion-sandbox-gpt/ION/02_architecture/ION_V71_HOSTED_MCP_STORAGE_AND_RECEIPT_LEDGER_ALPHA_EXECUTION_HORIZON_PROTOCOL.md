# ION V71 Execution Horizon Protocol

## Immediate horizon

V71 converts the V69/V70 hosted account and HTTP preview work into a hosted storage and receipt-ledger alpha. The goal is to define how a mounted workspace can persist state-root snapshots, receipt events, object references, and bundle export previews without creating a live execution path.

## Current allowed work

- Define storage/ledger schemas.
- Implement local alpha ledger module.
- Generate boundary reports.
- Verify append-only receipt chain semantics.
- Verify content-addressed state-root snapshots.
- Verify bundle export preview semantics.
- Refuse forbidden live-execution event kinds.

## Current blocked work

- Public hosted endpoint deployment.
- Production OAuth certification.
- Production object storage certification.
- Kubernetes deployment certification.
- Live execution.
- Shell execution.
- Browser mutation.
- Provider dispatch.
- Credential access.
- Direct governed-write mutation.

## Next branch candidate

`V72_HOSTED_MCP_BUNDLE_IMPORT_EXPORT_AND_REPLAY_ALPHA`

V72 should define bundle import/export and replay contracts over the V71 storage/receipt substrate. It should still avoid live execution and public cloud certification.
