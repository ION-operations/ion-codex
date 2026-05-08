---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-03T00:00:00-04:00
status: DRAFT
task: T02
depends_on: T01
goal: Define the WorkUnitSchema — the schedulable unit of cognition issued by the daemon to an agent
connections:
  - ION/06_intelligence/specs/T01_TransitionSchema.yaml
  - SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md (K1 Boot Sequence, K2 Four Syscalls)
  - SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md (Art. 11 Agents Are Ephemeral)
  - SOS/04_packages/spawner/src/spawn_agent.py (runtime: parse_task → resolve_agent → build_prompt → dispatch)
evidence:
  - ION-016 Thoth extraction of SOS spawn_agent.py 12-step pipeline
---

# WorkUnitSchema — Schedulable Unit of Cognition

## 1. PURPOSE

A WorkUnit is what the daemon hands to an agent. It is the bounded, versioned,
trackable container for one transition's worth of work. The agent receives a
WorkUnit (via its ContextPackage), executes it, and returns a CommitDelta.

The WorkUnit is NOT a task file. Task files (`.task.md`) are human-facing input.
The daemon reads a task file, resolves it against the TransitionSchema and agent
registry, and produces a WorkUnit — which is the machine-facing execution contract.

## 2. DESIGN PRINCIPLES

From the Sovereign Kernel K1-K2:
- Agents are ephemeral consumers of pre-compiled context (Art. 11)
- One agent executes one bounded transition (GPT 5.4 blueprint §2.1)
- The daemon owns sequencing — agents do not decide what comes next (§2.3)
- Context must be versioned to detect stale execution (§2.4)

From SOS runtime evidence (ION-016):
- `spawn_agent.py` step 1-5: parse task → resolve agent → validate template → select model → build prompt
- These steps ARE the WorkUnit compilation process
- The WorkUnit is what exists after step 5 and before step 6 (API call)

## 3. SCHEMA DEFINITION

```yaml
WorkUnitSchema:
  schema_version: "1.0"

  WorkUnit:
    # --- Identity ---
    work_unit_id: string         # REQUIRED — unique ID (uuid4)
    created_at: string           # REQUIRED — ISO 8601 timestamp
    
    # --- Protocol binding ---
    protocol_id: string          # REQUIRED — which Protocol this unit belongs to (from T01)
    transition_id: string        # REQUIRED — which Transition this unit executes (from T01)
    context_version: string      # REQUIRED — version hash of the context package issued with this unit
    
    # --- Agent binding ---
    agent_personal_name: string  # REQUIRED — from agent_registry.json
    agent_role: string           # REQUIRED — functional transform
    agent_structural_id: string  # REQUIRED — Tier.Domain.Role
    agent_tier: integer          # REQUIRED — authority tier (0-5)
    agent_domain: string         # REQUIRED — operational domain
    chassis: string              # REQUIRED — which LLM/model executes this (e.g. "composer-2", "claude-opus-4.6")
    
    # --- Scope ---
    scope_type: enum             # REQUIRED — FILE | DIRECTORY | PROJECT | CROSS_PROJECT
    scope_ref: string            # REQUIRED — the primary target (file path, directory, etc.)
    bound_template: string       # REQUIRED — which template governs the agent's output format
    
    # --- Inputs ---
    input_refs: list[InputRef]   # REQUIRED — what the agent receives (artifacts, prior findings, etc.)
    context_package_id: string   # REQUIRED — ID of the compiled ContextPackage (T03)
    
    # --- Constraints ---
    allowed_writes: list[string] # REQUIRED — filesystem paths the agent may write to
    allowed_next_actions: list[string]  # REQUIRED — what signals/transitions the agent may propose
    must_not: list[string]       # OPTIONAL — explicit prohibitions (copy-on-update, protected paths, etc.)
    
    # --- Open questions in scope ---
    open_questions_in_scope: list[string]  # OPTIONAL — questions this unit is expected to address
    
    # --- Scheduling ---
    priority: enum               # REQUIRED — P0_CRITICAL | P1_HIGH | P2_NORMAL | P3_LOW
    dependencies: list[string]   # OPTIONAL — work_unit_ids that must complete before this one starts
    spawn_policy: SpawnPolicy    # OPTIONAL — whether this unit may spawn child work units
    timeout_seconds: integer     # OPTIONAL — max execution time (default: 300, per SOS heartbeat evidence)
    
    # --- Tracking ---
    status: enum                 # REQUIRED — PENDING | DISPATCHED | EXECUTING | VALIDATING | COMMITTED | FAILED | BLOCKED
    expected_output_schema: string  # OPTIONAL — reference to the output schema the agent must conform to
    parent_work_unit_id: string  # OPTIONAL — if this was spawned by another work unit
    
  InputRef:
    ref_id: string               # REQUIRED
    ref_type: enum               # REQUIRED — ARTIFACT | EVIDENCE_FINDING | SIGNAL | STATE_FILE | DOCTRINE
    ref_path: string             # REQUIRED — filesystem path or schema reference
    visibility: enum             # REQUIRED — FULL | SIGNATURES_ONLY | SUMMARY (per Art. 10 Asymmetric Visibility)
    required: boolean            # REQUIRED
    
  SpawnPolicy:
    may_spawn: boolean           # REQUIRED
    max_children: integer        # OPTIONAL — default 0
    spawn_templates: list[string]  # OPTIONAL — which templates children may use
    spawn_requires_approval: boolean  # OPTIONAL — default false
```

## 4. LIFECYCLE

```
    ┌─────────┐
    │ PENDING  │ ← daemon creates WorkUnit from task file + registry + schema
    └────┬────┘
         │ daemon dispatches to chassis
    ┌────▼──────┐
    │DISPATCHED │ ← work unit sent to agent (context package compiled)
    └────┬──────┘
         │ agent begins execution
    ┌────▼──────┐
    │ EXECUTING │ ← agent is running the bound template
    └────┬──────┘
         │ agent returns output
    ┌────▼───────┐
    │ VALIDATING │ ← gatekeeper runs W1-W10
    └────┬───────┘
         │
    ┌────▼──────┐     ┌────────┐
    │ COMMITTED │     │ FAILED │
    └───────────┘     └────────┘
    
    BLOCKED: dependencies not met, or BLOCKED signal received
```

## 5. RELATIONSHIP TO TASK FILES

Task files (`.task.md`) are the human-facing input surface:

```yaml
# .task.md (human writes this)
---
agent: Mason
template: CODE
priority: P0
target: ION/04_packages/kernel/model.py
depends_on: T01
---
Port the Ion dataclass from ION-BUILD...
```

The daemon transforms this into a WorkUnit by:
1. Resolving `agent: Mason` against `agent_registry.json` → fills agent_* fields
2. Resolving `template: CODE` against TransitionSchema → fills protocol_id, transition_id
3. Resolving `target` → fills scope_ref, allowed_writes
4. Compiling ContextPackage (T03) → fills context_package_id, input_refs
5. Checking dependencies → fills status (PENDING or BLOCKED)
6. Assigning work_unit_id (uuid4) and context_version

In IDE/manual mode (current): Vizier performs this transformation mentally.
In daemon mode (future): The scheduler performs it programmatically.

## 6. RELATIONSHIP TO T01 TransitionSchema

Every WorkUnit MUST reference a valid `protocol_id` and `transition_id` from the
TransitionSchema. The daemon validates:
- The agent's tier meets the transition's `minimum_tier`
- The agent's domain is in the transition's `allowed_domains`
- The bound template matches the transition's state template
- The allowed_writes are a subset of the transition's WriteTargets

If any check fails, the WorkUnit is not dispatched — it enters FAILED with a
validation error.

## 7. CONTEXT VERSION AND STALE DETECTION

`context_version` is a hash of the ContextPackage contents at compilation time.
If an agent returns a CommitDelta (T04) referencing a stale context_version
(because state changed while the agent was executing), the daemon may:
- Accept the delta anyway (if the changes don't conflict)
- Reject and re-dispatch with fresh context
- Downgrade the output from AUTHORITY to WITNESS

This is the mechanism described in GPT 5.4 blueprint §2.4 for preventing silent drift.

## 8. VALIDATION CRITERIA

- [ ] Every field maps to a concrete value derivable from task files + registry + TransitionSchema
- [ ] The lifecycle states match the EXECUTION.core protocol from T01
- [ ] The InputRef visibility enum implements Art. 10 Asymmetric Visibility
- [ ] SpawnPolicy enables the clone/shard model from GPT 5.4 blueprint §8
- [ ] Status enum covers all states needed for dashboard visibility
- [ ] context_version enables stale detection per GPT 5.4 blueprint §2.4
