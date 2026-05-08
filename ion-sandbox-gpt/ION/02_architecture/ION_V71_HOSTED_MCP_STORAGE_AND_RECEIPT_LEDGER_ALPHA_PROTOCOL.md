# ION V71 Hosted MCP Storage and Receipt Ledger Alpha Protocol

## Branch identity

`V71_HOSTED_MCP_STORAGE_AND_RECEIPT_LEDGER_ALPHA`

V71 defines the hosted storage and receipt-ledger substrate required after the V70 hosted OAuth and Streamable HTTP preview. It remains an alpha boundary branch. It does not certify production OAuth, a public hosted endpoint, cloud tenancy, Kubernetes, live execution, provider dispatch, browser mutation, shell execution, credential access, or direct governed-write mutation.

## Core law

Storage is not execution.

A hosted state root is a content-addressed continuity object. It is not an MCP-mutable live workspace. A receipt ledger is append-only evidence. It is not an alternate execution authority. A bundle export is a preview unless later certified by product packaging and release gates. Any result entering the ledger from MCP remains a receipt, proposal, dry-run artifact, or approval projection until it passes the normal ION governance path.

## Required invariants

Every V71 storage-facing action must resolve to one of:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

No V71 action may resolve to `LIVE_EXECUTED`.

Every ledger event must be hash-linked to the previous event, where applicable. Every state-root snapshot must be content-addressed. Every bundle export in V71 must be marked preview-only. Every hosted storage report must explicitly say that public hosted cloud, Kubernetes, production object storage, and live execution are not certified.

## Authorized alpha events

V71 may model these event kinds:

- `MOUNT_RECEIPT`
- `STATE_ROOT_SNAPSHOT`
- `DRY_RUN_PLAN`
- `DRY_RUN_SUBMISSION`
- `APPROVAL_QUEUE_PROJECTION`
- `BUNDLE_EXPORT_PREVIEW`
- `ROLLBACK_PREVIEW`
- `REPLAY_PREVIEW`

## Forbidden events

V71 must refuse:

- `LIVE_EXECUTION`
- `SHELL_EXECUTION`
- `BROWSER_MUTATION`
- `PROVIDER_DISPATCH`
- `SECRET_READ`
- `SECRET_WRITE`
- `GOVERNED_WRITE_DIRECT`
- `DAEMON_LOOP_ACTIVATION`

## Hosted storage alpha model

The hosted storage alpha model consists of:

- account metadata;
- workspace metadata;
- state-root metadata;
- object references carrying content hashes;
- append-only receipt events;
- state-root snapshots;
- bundle export previews;
- replay/export validation reports.

This model intentionally avoids selecting the final production storage provider. The production implementation may use Postgres, object storage, a vault, queue infrastructure, and isolated workers, but V71 only defines and validates the boundary contract.

## Promotion gate

V71 may promote to the next branch only when:

1. The alpha ledger can produce a deterministic report.
2. The report verifies receipt-chain continuity.
3. State-root snapshots are content-addressed.
4. Bundle export is preview-only.
5. Forbidden event kinds are refused.
6. `LIVE_EXECUTED` is impossible.
7. Hosted cloud and Kubernetes remain uncertified unless explicitly certified by later branches.
