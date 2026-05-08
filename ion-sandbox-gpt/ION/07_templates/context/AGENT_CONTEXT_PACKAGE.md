# AGENT_CONTEXT_PACKAGE

## Packet metadata

- package_id:
- package_class: ROLE_BASE_CONTEXT_PACKAGE | MISSION_CONTEXT_PACKAGE | DELTA_CONTEXT_PACKAGE | RECOVERY_CONTEXT_PACKAGE | CARRIER_CONTEXT_PACKAGE
- role_id:
- mission_id:
- carrier:
- created_at:
- created_by:
- authority_ceiling:
- steward_integration_required: true

## Current ION definition for this role

State the role-relevant definition of ION in complete, compressed form. Do not use path-only references.

## Role operating boundary

- owns:
- may_read:
- may_write:
- must_not_write:
- integration_target:

## Loaded context body

Include the actual high-density context the agent needs. Use concise excerpts, summaries, invariants, and current decisions. Paths are provenance anchors only.

## Source ledger

| Path | Authority posture | SHA256 | Loaded material summary |
|---|---|---|---|

## Stale-surface warnings

Name any stale surfaces, old branch claims, old MINI/CAPSULE claims, deprecated role names, or historical donor files that must not be treated as live authority.

## Context delta since prior package

- previous_package_id:
- changes:
- newly retired surfaces:
- newly promoted surfaces:

## Return contract

The worker must begin with:

```md
### CONTEXT PROOF
```

The proof must name the required package, required files, actual loaded content summaries, and any stale surfaces detected.

## Receipt

- context_load_receipt_path:
- context_delta_receipt_path:
- proof_gate:
