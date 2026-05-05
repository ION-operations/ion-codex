---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-03T00:20:00-04:00
status: DRAFT
task: T04
depends_on: [T01, T02]
goal: Define the CommitDeltaSchema — the proposed state change returned by an agent
connections:
  - ION/06_intelligence/specs/T01_TransitionSchema.yaml
  - ION/06_intelligence/specs/T02_WorkUnitSchema.yaml
  - SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md (K2 EMIT syscall)
---

# CommitDeltaSchema — Proposed State Change

## 1. PURPOSE

A CommitDelta is what an agent returns after executing a WorkUnit. It is a
PROPOSED state change — the daemon validates it before committing. Agents do
not write directly to the filesystem. They propose deltas. The daemon commits.

This is the GPT 5.4 blueprint's core anti-drift mechanism:
> "Agents do not directly write truth. They propose a delta."

## 2. SCHEMA DEFINITION

```yaml
CommitDeltaSchema:
  schema_version: "1.0"

  CommitDelta:
    # --- Identity ---
    delta_id: string             # REQUIRED — unique ID (uuid4)
    created_at: string           # REQUIRED — ISO 8601
    
    # --- Binding ---
    work_unit_id: string         # REQUIRED — which WorkUnit produced this delta
    context_version: string      # REQUIRED — must match the WorkUnit's context_version
    protocol_id: string          # REQUIRED — from WorkUnit
    transition_id: string        # REQUIRED — from WorkUnit
    
    # --- Agent ---
    agent_personal_name: string  # REQUIRED
    agent_structural_id: string  # REQUIRED
    chassis: string              # REQUIRED — which model executed
    
    # --- Produced artifacts ---
    produced_artifacts: list[ProducedArtifact]  # REQUIRED — what the agent created
    
    # --- Ledger/state changes ---
    ledger_additions: list[LedgerEntry]  # OPTIONAL — rows to append to ledgers
    state_mutations: list[StateMutation] # OPTIONAL — changes to state files (CAPSULE, etc.)
    
    # --- Forward-looking ---
    proposed_signals: list[ProposedSignal]      # OPTIONAL — signals the agent wants emitted
    proposed_open_questions: list[string]        # OPTIONAL — questions that emerged during execution
    proposed_child_work_units: list[ChildSpec]   # OPTIONAL — work the agent thinks should happen next
    
    # --- Quality ---
    status: enum                 # REQUIRED — PROPOSED | ACCEPTED | ACCEPTED_AS_WITNESS | REJECTED | REQUIRES_REVIEW
    confidence: float            # REQUIRED — [0.0, 1.0] — agent's self-assessed confidence
    contradictions: list[string] # OPTIONAL — conflicts the agent detected with existing state
    notes: string                # OPTIONAL — agent's commentary on the work
    
  ProducedArtifact:
    path: string                 # REQUIRED — target filesystem path
    content: string              # REQUIRED — the artifact content
    operation: enum              # REQUIRED — CREATE | UPDATE | APPEND
    authority_class: enum        # REQUIRED — from T06 AuthorityClassSchema
    checksum: string             # REQUIRED — content hash for integrity
    
  LedgerEntry:
    ledger: string               # REQUIRED — which ledger to append to
    row: object                  # REQUIRED — the row data (schema varies by ledger)
    
  StateMutation:
    target: string               # REQUIRED — state file path
    operation: enum              # REQUIRED — APPEND | UPDATE_SECTION
    content: string              # REQUIRED — what to write
    
  ProposedSignal:
    signal_type: string          # REQUIRED — TASK_COMPLETE | TASK_FAILED | HANDOFF | BLOCKED | etc.
    target: string               # REQUIRED — who receives this signal
    payload: object              # OPTIONAL — signal-specific data
    
  ChildSpec:
    suggested_agent: string      # OPTIONAL — which agent should handle
    suggested_template: string   # REQUIRED — which template governs
    scope_ref: string            # REQUIRED — what to work on
    rationale: string            # REQUIRED — why this child work is needed
```

## 3. COMMIT OUTCOMES

The daemon validates a CommitDelta and produces one of:

| Outcome | Meaning | Action |
|---------|---------|--------|
| ACCEPTED | Delta is valid, context is fresh, writes are legal | Commit all artifacts and mutations |
| ACCEPTED_AS_WITNESS | Delta is useful but context was stale or authority is insufficient | Commit artifacts with authority_class downgraded to WITNESS |
| REJECTED | Delta violates schema, writes to protected paths, or fails W1-W10 | Discard. Log rejection. Optionally re-dispatch. |
| REQUIRES_REVIEW | Delta touches contested domain or has low confidence | Hold for Nemesis audit or Sovereign review |
| REQUIRES_RECONCILIATION | Delta conflicts with a parallel shard's output | Route to reconciliation pass |

## 4. STALE CONTEXT HANDLING

If `delta.context_version != current_context_version`:
1. Check if the stale fields overlap with the delta's produced artifacts
2. If no overlap → ACCEPTED (stale context didn't affect the work)
3. If overlap → ACCEPTED_AS_WITNESS (output may be based on outdated state)
4. If critical overlap → REJECTED (re-dispatch with fresh context)

## 5. VALIDATION CRITERIA

- [ ] Every field is derivable from agent output + work unit metadata
- [ ] Commit outcomes match GPT 5.4 blueprint §13
- [ ] context_version enables stale detection
- [ ] ProducedArtifact.authority_class links to T06
- [ ] ProposedSignal.signal_type links to T07
- [ ] ChildSpec enables the daemon to schedule follow-up work without human intervention
