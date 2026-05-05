---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-03T00:25:00-04:00
status: DRAFT
task: T05
depends_on: [T01]
goal: Define the OpenQuestionSchema — first-class kernel state for unresolved questions
---

# OpenQuestionSchema — First-Class Unresolved Questions

## 1. PURPOSE

Open questions are how meaning survives distributed work. When an agent encounters
something it cannot resolve within its bounded scope, it records an OpenQuestion.
The daemon tracks these as first-class kernel state — they influence scheduling,
block transitions, and prevent premature closure.

## 2. SCHEMA DEFINITION

```yaml
OpenQuestionSchema:
  schema_version: "1.0"

  OpenQuestion:
    question_id: string          # REQUIRED — unique ID (uuid4)
    created_at: string           # REQUIRED — ISO 8601
    
    # --- Origin ---
    origin_work_unit: string     # REQUIRED — which work unit produced this question
    origin_agent: string         # REQUIRED — who asked it
    origin_transition: string    # REQUIRED — during which transition
    
    # --- Content ---
    domain: string               # REQUIRED — which domain this question concerns
    scope_ref: string            # REQUIRED — file, directory, or system the question is about
    question_text: string        # REQUIRED — the actual question
    context: string              # OPTIONAL — background needed to understand the question
    
    # --- Resolution ---
    needed_from: string          # REQUIRED — what role/agent/resource can answer this
    priority: enum               # REQUIRED — P0_BLOCKING | P1_HIGH | P2_NORMAL | P3_LOW
    status: enum                 # REQUIRED — OPEN | ASSIGNED | RESOLVED | DEFERRED | CANCELLED
    blocking: list[string]       # OPTIONAL — work_unit_ids or transition_ids this question blocks
    
    # --- Resolution data (filled when answered) ---
    resolved_by: string          # OPTIONAL — who answered
    resolved_at: string          # OPTIONAL — when
    resolution: string           # OPTIONAL — the answer
    resolution_evidence: list[string]  # OPTIONAL — evidence supporting the answer
    
    # --- Linking ---
    linked_artifacts: list[string]     # OPTIONAL — related evidence/research/audit files
    linked_competitions: list[string]  # OPTIONAL — 05A competition rows this relates to
    parent_question_id: string         # OPTIONAL — if this was spawned from another question
```

## 3. PRIORITY SEMANTICS

| Priority | Meaning | Daemon behavior |
|----------|---------|----------------|
| P0_BLOCKING | Cannot proceed without answer | Daemon will not schedule dependent work units |
| P1_HIGH | Should be resolved soon | Daemon prioritizes resolution work units |
| P2_NORMAL | Answer when convenient | Standard queue priority |
| P3_LOW | Nice to know | Deferred indefinitely |

## 4. VALIDATION CRITERIA

- [ ] Questions can be created by any agent via CommitDelta.proposed_open_questions
- [ ] Blocking questions actually prevent dependent work unit scheduling
- [ ] Resolution evidence links to real artifacts
- [ ] Questions survive across sessions (persisted to filesystem)
