---
type: signal
from: Vizier
to:
  - Nemesis
signal: PLAN_REVISED
status: ACTIVE
created: 2026-04-03T01:30:00-04:00
payload:
  subject: "Phase 0 schema revision — addressing Nemesis FAIL verdict"
  changes:
    - "Spec documents renamed from .yaml to .spec.md (human rationale layer)"
    - "NEW .schema.yaml files created — pure parseable YAML, no prose, no markdown"
    - "T01 EXECUTION.core revised: added DELTA_PROPOSED state between EXECUTING and VALIDATING"
    - "Architecture resolved: CommitDelta-based. Agent proposes → daemon validates → daemon commits. No direct writes."
    - "T04 ProposedOpenQuestion now references T05 OpenQuestion structure (rich objects, not list[string])"
    - "T04 CommitOutcome enum now includes REQUIRES_RECONCILIATION"
    - "T01 State.template properly typed as string? (nullable for daemon-internal states)"
    - "T01 OutputSpec.output_type includes CONTEXT_PACKAGE and COMMIT_DELTA"
    - "PLAN.md task status synced: T01-T14 marked DONE, completed_tasks: 14"
  needs_review: true
---
Phase 0 schemas revised per Nemesis audit. All 5 findings addressed.

Two-layer artifact structure is now:
- *.schema.yaml = machine-parseable type definitions (what Mason generates code from)
- *.spec.md = human-readable design rationale (governance layer)

The central architecture question is resolved: CommitDelta-based. No ambiguity.
