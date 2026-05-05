# V72 Branch Lock

Branch: `V72_HOSTED_MCP_BUNDLE_IMPORT_EXPORT_AND_REPLAY_ALPHA`

Locked scope: bundle import/export/replay alpha over V71 hosted storage and receipt ledger.

Allowed: read-only bundle inspection, dry-run export preview, import validation, replay preview, tamper refusal.

Forbidden: `LIVE_EXECUTED`, live daemon loop, direct governed write, provider dispatch, shell execution, browser mutation, credential access, production object-storage claims, public endpoint claims, Kubernetes claims.
