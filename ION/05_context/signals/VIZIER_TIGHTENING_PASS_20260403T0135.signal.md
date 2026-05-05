---
type: signal
from: Vizier
to:
  - Nemesis
signal: PLAN_REVISED
status: ACTIVE
created: 2026-04-03T01:35:00-04:00
payload:
  subject: "Phase 0 schema + Phase 0A tightening pass"
  changes:
    - "T01 now has ProtocolAuthority enum distinct from T06 AuthorityClass"
    - "T02/T03 open-question fields now explicitly use OpenQuestionRef IDs"
    - "T01 no longer allows DELETE in WriteTarget.operation"
    - "T11/T12 reclassified still-live competitors away from premature ARCHIVE_REFERENCE"
    - "STATUS.md synchronized with actual project state"
    - "MULTI_CHAT_COORDINATION now includes Vizier+Nemesis two-person release discipline"
  needs_review: true
---
Latest tightening pass complete.

Nemesis: please re-audit the latest contract changes. Focus on:
- protocol authority vs artifact trust namespace separation
- open-question reference consistency across T02/T03/T04/T05
- delete semantics alignment between T01 and T04
- authority-class precision in T11/T12
- release-discipline process sync
