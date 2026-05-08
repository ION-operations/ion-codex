---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T03:07:00-04:00
status: ACTIVE
---

# T68 — Branch-control CLI and status

Canonical operator surface additions:
- `python -m kernel allocator assess-branch-posture ...`
- `python -m kernel status ...` latest branch-control receipt projection

Minimum expectations:
- CLI persists one explicit branch-control receipt
- optional stale-claim decay remains explicit through flag and receipt
- status rediscovery shows the latest branch-control receipt without inventing a second control plane
