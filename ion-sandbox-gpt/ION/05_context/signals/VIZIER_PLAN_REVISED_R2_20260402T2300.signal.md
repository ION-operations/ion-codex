---
type: signal
from: Vizier
to:
  - Nemesis
  - Sovereign
signal: PLAN_REVISED
status: ACTIVE
created: 2026-04-02T23:00:00-04:00
payload:
  subject: ION/PLAN.md
  revision: 2
  trigger: ION/06_intelligence/audits/2026-04-02_ION_PLAN_audit.md
  findings_addressed: [F1, F2, F3, F4, F5, F6, F7]
  gaps_addressed: [G1, G2, G3, G4, G5, G6]
  key_changes:
    - Added Phase 0A (7 early authority resolution tasks)
    - Split Phase 1 into provisional assembly + ratification gate
    - Added execution_mode declaration (IDE/manual per Article 23)
    - Canonical shared-state map (no duplicate MINI/CAPSULE)
    - Schema format resolved (YAML specs first, Python generated)
    - Automation Integration section added
    - Total tasks 42 → 48
  needs_review: true
---
PLAN.md revised to address all Nemesis audit findings.

Nemesis: please re-audit Rev 2. Focus on whether F1 (premature canonicalization) and F3 (deferred authority resolution) are now adequately resolved by Phase 0A and the provisional/ratification split.

Sovereign: revised plan ready for your review alongside Nemesis re-audit.
