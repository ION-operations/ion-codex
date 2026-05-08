---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-02T23:45:00-04:00
status: DRAFT
task: T01
goal: Define the TransitionSchema — the protocol graph that governs all legal state transitions in ION
connections:
  - SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md (K4 Template State Machine)
  - SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md (Art. 7-8 Template-First Axiom)
  - SOS/04_packages/heartbeat/src/heartbeat.py (runtime evidence)
  - SOS/04_packages/spawner/src/spawn_agent.py (runtime evidence)
  - SOS/04_packages/heartbeat/src/signal_router.py (runtime evidence)
  - ION/PLAN.md (Phase 0 T01)
evidence:
  - ION/06_intelligence/audits/2026-04-02_ION_PLAN_audit.md
  - Thoth runtime transition extraction (ION-005 through ION-007 subagent findings)
---

# TransitionSchema — ION Kernel Protocol Graph

## 1. PURPOSE

The TransitionSchema defines the **protocol graph** — the set of all legal state transitions
in the ION cognitive kernel. Every operation in the system must be expressible as a sequence
of transitions in this graph. Operations that cannot be expressed as legal transitions are
unconstitutional and must be rejected.

This schema synthesizes three sources:
- **Constitutional law** (K4): The template state machine with 8 nodes
- **GPT 5.4 kernel blueprint**: Protocol graphs with per-transition I/O, authority, and write constraints
- **SOS runtime evidence**: The actual execution transitions in heartbeat.py, spawn_agent.py, signal_router.py

## 2. CORE CONCEPTS

### 2.1 Protocol

A protocol is a named graph of transitions that governs a specific class of work.
Protocols are not prompts — they are law. Each protocol defines which transitions
are legal, what inputs are required, what outputs are valid, and who may execute them.

### 2.2 Transition

A transition is an atomic, bounded unit of state change. One agent executes one
transition, producing one output. The kernel validates the output and commits it
(or rejects it). Transitions are the fundamental unit of work.

### 2.3 Protocol Family

Protocols are grouped into families. Each family governs a domain of work:

| Family | Purpose | Constitutional Basis |
|--------|---------|---------------------|
| RECONNAISSANCE | Surface discovery, file manifests, batch planning | Art. 7 (Template-First) |
| EVIDENCE | Atomic file-level forensic inspection | Art. 7, Art. 10 (Asymmetric Visibility) |
| CONSOLIDATION | Cross-file synthesis: fingerprints, lineage, competition | Art. 7 |
| EXECUTION | Code writing, debugging, refactoring | Art. 7, Art. 8 (FSM) |
| GOVERNANCE | Audit, review, approval, compliance | Art. 7, Art. 19 (Inspector General) |
| PLANNING | Task decomposition, sequencing, dependency mapping | Art. 7 |
| COMMUNICATION | Signals, handoffs, broadcasts | Art. 7, K7 (Signal Protocol) |
| SYSTEM | Evolution, template development, agent spawn | Art. 7, Art. 22 (Amendment) |

## 3. SCHEMA DEFINITION

```yaml
# TransitionSchema v1.0
# Every field marked REQUIRED must be present. Fields marked OPTIONAL may be omitted.

TransitionSchema:
  schema_version: "1.0"
  
  Protocol:
    protocol_id: string          # REQUIRED — unique identifier (e.g. "EXECUTION.code")
    protocol_family: string      # REQUIRED — one of the 8 families above
    display_name: string         # REQUIRED — human-readable name
    description: string          # REQUIRED — one-sentence purpose
    version: string              # REQUIRED — semver
    status: enum                 # REQUIRED — DRAFT | ACTIVE | DEPRECATED
    authority: enum              # REQUIRED — A0_SUPREME through A7_QUARANTINE
    states: list[State]          # REQUIRED — the nodes of this protocol's graph
    transitions: list[Transition] # REQUIRED — the edges of this protocol's graph
    entry_states: list[string]   # REQUIRED — which states may be entered from outside
    terminal_states: list[string] # REQUIRED — which states end the protocol
    escalation_conditions: list[EscalationCondition]  # OPTIONAL
    clone_permissions: ClonePolicy  # OPTIONAL — when parallel shards are allowed

  State:
    state_id: string             # REQUIRED — unique within this protocol
    display_name: string         # REQUIRED
    template: string             # REQUIRED — which template governs output at this state
    minimum_tier: integer        # REQUIRED — lowest agent tier that may execute this state
    allowed_domains: list[string] # REQUIRED — which domains may execute
    description: string          # OPTIONAL

  Transition:
    transition_id: string        # REQUIRED — unique within this protocol
    from_state: string           # REQUIRED — source state_id
    to_state: string             # REQUIRED — target state_id
    trigger: enum                # REQUIRED — what causes this transition
    required_inputs: list[InputSpec]   # REQUIRED — what must exist before transition fires
    required_outputs: list[OutputSpec]  # REQUIRED — what the transition must produce
    allowed_writes: list[WriteTarget]  # REQUIRED — filesystem paths the agent may write to
    authority_check: AuthorityCheck    # REQUIRED — permission validation
    validation_rules: list[string]     # OPTIONAL — additional W1-W10 checks
    description: string                # OPTIONAL

  # --- Supporting types ---

  InputSpec:
    input_id: string             # REQUIRED
    input_type: enum             # REQUIRED — ARTIFACT | SIGNAL | STATE | CONTEXT_PACKAGE
    source_ref: string           # REQUIRED — where to find this input
    required: boolean            # REQUIRED — true = hard prerequisite, false = soft/optional
    description: string          # OPTIONAL

  OutputSpec:
    output_id: string            # REQUIRED
    output_type: enum            # REQUIRED — ARTIFACT | SIGNAL | LEDGER_ROW | OPEN_QUESTION
    target_ref: string           # REQUIRED — where the output goes
    schema_ref: string           # OPTIONAL — schema the output must conform to
    description: string          # OPTIONAL

  WriteTarget:
    path_pattern: string         # REQUIRED — glob or exact path the agent may write to
    operation: enum              # REQUIRED — CREATE | UPDATE | APPEND | DELETE
    requires_lock: boolean       # REQUIRED — true if D44 file lock is needed
    protected: boolean           # REQUIRED — true if path is constitutionally protected

  AuthorityCheck:
    minimum_tier: integer        # REQUIRED
    required_domain: string      # OPTIONAL — null means any domain
    requires_sovereign: boolean  # REQUIRED — true if T0 approval needed

  EscalationCondition:
    condition: string            # REQUIRED — when this fires
    escalate_to: enum            # REQUIRED — SOVEREIGN | INSPECTOR_GENERAL | CHIEF_OF_STAFF
    reason: string               # REQUIRED

  ClonePolicy:
    parallel_allowed: boolean    # REQUIRED
    max_clones: integer          # OPTIONAL — default 1
    shard_mode: enum             # OPTIONAL — SEQUENTIAL | BIDIRECTIONAL | TOPOLOGICAL
    reconciliation_required: boolean  # REQUIRED — must clones be reconciled?

  # --- Trigger enum ---
  # TASK_RECEIVED — a .task.md file arrived in inbox
  # SIGNAL_RECEIVED — a signal file matched this transition's input
  # PRIOR_COMPLETE — the from_state's work was committed successfully
  # HUMAN_DIRECTIVE — sovereign instruction
  # TIMER — scheduled/periodic
  # FAILURE — a prior transition failed and this is the error path
```

## 4. THE CORE EXECUTION PROTOCOL

This is the primary protocol that governs task execution — the ION equivalent of
the SOS heartbeat → spawn → validate → write → signal loop.

```yaml
protocol_id: "EXECUTION.core"
protocol_family: "EXECUTION"
display_name: "Core Task Execution"
description: "The primary loop: receive task, compile context, execute template, validate, write, signal."
version: "1.0.0"
status: DRAFT
authority: A1_KERNEL

states:
  - state_id: RECEIVED
    display_name: "Task Received"
    template: null  # daemon state, not agent-executed
    minimum_tier: 0
    allowed_domains: ["*"]
    
  - state_id: CONTEXT_COMPILED
    display_name: "Context Compiled"
    template: null  # daemon state
    minimum_tier: 0
    allowed_domains: ["*"]
    
  - state_id: EXECUTING
    display_name: "Agent Executing"
    template: "{bound_template}"  # determined by task metadata
    minimum_tier: 5
    allowed_domains: ["{task_domain}"]
    
  - state_id: VALIDATING
    display_name: "Output Validating"
    template: null  # gatekeeper, not agent
    minimum_tier: 0
    allowed_domains: ["*"]
    
  - state_id: COMMITTED
    display_name: "Output Committed"
    template: null  # daemon state
    minimum_tier: 0
    allowed_domains: ["*"]
    
  - state_id: FAILED
    display_name: "Execution Failed"
    template: null
    minimum_tier: 0
    allowed_domains: ["*"]

entry_states: [RECEIVED]
terminal_states: [COMMITTED, FAILED]

transitions:
  - transition_id: "compile_context"
    from_state: RECEIVED
    to_state: CONTEXT_COMPILED
    trigger: TASK_RECEIVED
    required_inputs:
      - input_id: task_file
        input_type: ARTIFACT
        source_ref: "05_context/inbox/*.task.md"
        required: true
      - input_id: agent_registry
        input_type: STATE
        source_ref: "03_registry/agent_registry.json"
        required: true
    required_outputs:
      - output_id: context_package
        output_type: CONTEXT_PACKAGE
        target_ref: "{compiled_context}"
    allowed_writes: []  # daemon compiles in memory
    authority_check:
      minimum_tier: 0
      requires_sovereign: false

  - transition_id: "execute_template"
    from_state: CONTEXT_COMPILED
    to_state: EXECUTING
    trigger: PRIOR_COMPLETE
    required_inputs:
      - input_id: context_package
        input_type: CONTEXT_PACKAGE
        source_ref: "{compiled_context}"
        required: true
    required_outputs:
      - output_id: agent_output
        output_type: ARTIFACT
        target_ref: "{task_target_path}"
        schema_ref: "{bound_template_output_schema}"
    allowed_writes:
      - path_pattern: "{task_target_path}"
        operation: CREATE
        requires_lock: false
        protected: false
    authority_check:
      minimum_tier: 5
      required_domain: "{task_domain}"
      requires_sovereign: false

  - transition_id: "validate_output"
    from_state: EXECUTING
    to_state: VALIDATING
    trigger: PRIOR_COMPLETE
    required_inputs:
      - input_id: agent_output
        input_type: ARTIFACT
        source_ref: "{task_target_path}"
        required: true
    required_outputs:
      - output_id: validation_receipt
        output_type: ARTIFACT
        target_ref: "{provenance_path}"
    allowed_writes:
      - path_pattern: "{task_target_path}.provenance.json"
        operation: CREATE
        requires_lock: false
        protected: false
    authority_check:
      minimum_tier: 0
      requires_sovereign: false

  - transition_id: "commit_success"
    from_state: VALIDATING
    to_state: COMMITTED
    trigger: PRIOR_COMPLETE
    required_inputs:
      - input_id: validation_receipt
        input_type: ARTIFACT
        source_ref: "{provenance_path}"
        required: true
        description: "Validation must have passed all W1-W10 gates"
    required_outputs:
      - output_id: completion_signal
        output_type: SIGNAL
        target_ref: "05_context/signals/{agent}_{task_id}_COMPLETE.signal.json"
      - output_id: ledger_entry
        output_type: LEDGER_ROW
        target_ref: "05_context/history/system_ledger.json"
    allowed_writes:
      - path_pattern: "05_context/signals/*.signal.json"
        operation: CREATE
        requires_lock: false
        protected: false
      - path_pattern: "05_context/history/system_ledger.json"
        operation: APPEND
        requires_lock: true
        protected: false
      - path_pattern: "05_context/inbox/completed/*"
        operation: CREATE
        requires_lock: false
        protected: false
    authority_check:
      minimum_tier: 0
      requires_sovereign: false

  - transition_id: "commit_failure"
    from_state: VALIDATING
    to_state: FAILED
    trigger: FAILURE
    required_inputs:
      - input_id: validation_receipt
        input_type: ARTIFACT
        source_ref: "{provenance_path}"
        required: true
        description: "Validation failed one or more W1-W10 gates"
    required_outputs:
      - output_id: failure_signal
        output_type: SIGNAL
        target_ref: "05_context/signals/{agent}_{task_id}_FAILED.signal.json"
    allowed_writes:
      - path_pattern: "05_context/signals/*.signal.json"
        operation: CREATE
        requires_lock: false
        protected: false
      - path_pattern: "05_context/inbox/failed/*"
        operation: CREATE
        requires_lock: false
        protected: false
    authority_check:
      minimum_tier: 0
      requires_sovereign: false

escalation_conditions:
  - condition: "Agent output references files outside allowed_writes"
    escalate_to: INSPECTOR_GENERAL
    reason: "Zone violation — agent attempted to write outside authorized paths"
  - condition: "Agent output modifies constitutionally protected path"
    escalate_to: SOVEREIGN
    reason: "Protected path mutation requires T0 authorization"
  - condition: "Validation fails 3 consecutive times for same task"
    escalate_to: CHIEF_OF_STAFF
    reason: "Repeated failure — task may need redesign or different agent"

clone_permissions:
  parallel_allowed: false
  reconciliation_required: false
```

## 5. THE TEMPLATE FSM PROTOCOL

This maps the constitutional state machine (K4) as a protocol graph,
governing how templates chain into each other.

```yaml
protocol_id: "FSM.template_chain"
protocol_family: "EXECUTION"
display_name: "Template State Machine"
description: "Governs legal template-to-template transitions per Constitution Art. 8 and Kernel K4."
version: "1.0.0"
status: DRAFT
authority: A0_SUPREME

states:
  - {state_id: RESEARCH, template: RESEARCH, minimum_tier: 5, allowed_domains: ["Intelligence"], display_name: "Research"}
  - {state_id: PLAN, template: PLAN, minimum_tier: 3, allowed_domains: ["Communications"], display_name: "Plan"}
  - {state_id: CODE, template: CODE, minimum_tier: 5, allowed_domains: ["Source"], display_name: "Code"}
  - {state_id: AUDIT, template: AUDIT, minimum_tier: 4, allowed_domains: ["Governance"], display_name: "Audit"}
  - {state_id: REFACTOR, template: REFACTOR, minimum_tier: 5, allowed_domains: ["Source"], display_name: "Refactor"}
  - {state_id: DEBUG, template: DEBUG, minimum_tier: 5, allowed_domains: ["Source"], display_name: "Debug"}
  - {state_id: DONE, template: null, minimum_tier: 0, allowed_domains: ["*"], display_name: "Done"}

  # Extended template vocabulary (from _MASTER registry, pending FSM promotion in T16)
  - {state_id: SPEC, template: SPEC, minimum_tier: 3, allowed_domains: ["Intelligence", "Source"], display_name: "Specification"}
  - {state_id: EVIDENCE, template: EVIDENCE, minimum_tier: 5, allowed_domains: ["Intelligence"], display_name: "Evidence"}
  - {state_id: CONSOLIDATION, template: CONSOLIDATION, minimum_tier: 3, allowed_domains: ["Intelligence"], display_name: "Consolidation"}
  - {state_id: RECONNAISSANCE, template: RECONNAISSANCE, minimum_tier: 5, allowed_domains: ["Intelligence"], display_name: "Reconnaissance"}
  - {state_id: TEST, template: TEST, minimum_tier: 5, allowed_domains: ["Source"], display_name: "Test"}
  - {state_id: APPROVAL, template: APPROVAL, minimum_tier: 1, allowed_domains: ["Communications", "Governance"], display_name: "Approval"}

entry_states: [RESEARCH, PLAN, RECONNAISSANCE, EVIDENCE, SPEC]
terminal_states: [DONE]

transitions:
  # Core K4 transitions
  - {transition_id: "research_to_plan", from_state: RESEARCH, to_state: PLAN, trigger: PRIOR_COMPLETE}
  - {transition_id: "plan_to_code", from_state: PLAN, to_state: CODE, trigger: PRIOR_COMPLETE}
  - {transition_id: "code_to_audit", from_state: CODE, to_state: AUDIT, trigger: PRIOR_COMPLETE}
  - {transition_id: "code_to_test", from_state: CODE, to_state: TEST, trigger: PRIOR_COMPLETE}
  - {transition_id: "audit_to_refactor", from_state: AUDIT, to_state: REFACTOR, trigger: PRIOR_COMPLETE}
  - {transition_id: "audit_to_done", from_state: AUDIT, to_state: DONE, trigger: PRIOR_COMPLETE}
  - {transition_id: "debug_to_code", from_state: DEBUG, to_state: CODE, trigger: PRIOR_COMPLETE}
  - {transition_id: "refactor_to_audit", from_state: REFACTOR, to_state: AUDIT, trigger: PRIOR_COMPLETE}
  - {transition_id: "test_to_audit", from_state: TEST, to_state: AUDIT, trigger: PRIOR_COMPLETE}
  - {transition_id: "test_to_debug", from_state: TEST, to_state: DEBUG, trigger: FAILURE}

  # Forensic pipeline transitions
  - {transition_id: "recon_to_plan", from_state: RECONNAISSANCE, to_state: PLAN, trigger: PRIOR_COMPLETE}
  - {transition_id: "evidence_to_consolidation", from_state: EVIDENCE, to_state: CONSOLIDATION, trigger: PRIOR_COMPLETE}
  - {transition_id: "consolidation_to_plan", from_state: CONSOLIDATION, to_state: PLAN, trigger: PRIOR_COMPLETE}
  - {transition_id: "consolidation_to_done", from_state: CONSOLIDATION, to_state: DONE, trigger: PRIOR_COMPLETE}

  # Specification transitions
  - {transition_id: "spec_to_code", from_state: SPEC, to_state: CODE, trigger: PRIOR_COMPLETE}
  - {transition_id: "spec_to_approval", from_state: SPEC, to_state: APPROVAL, trigger: PRIOR_COMPLETE}
  - {transition_id: "research_to_spec", from_state: RESEARCH, to_state: SPEC, trigger: PRIOR_COMPLETE}
  
  # Approval transitions
  - {transition_id: "approval_to_code", from_state: APPROVAL, to_state: CODE, trigger: PRIOR_COMPLETE}
  - {transition_id: "approval_to_plan", from_state: APPROVAL, to_state: PLAN, trigger: PRIOR_COMPLETE}
  - {transition_id: "approval_to_done", from_state: APPROVAL, to_state: DONE, trigger: PRIOR_COMPLETE}

  # Plan can enter many states
  - {transition_id: "plan_to_spec", from_state: PLAN, to_state: SPEC, trigger: PRIOR_COMPLETE}
  - {transition_id: "plan_to_research", from_state: PLAN, to_state: RESEARCH, trigger: PRIOR_COMPLETE}
  - {transition_id: "plan_to_recon", from_state: PLAN, to_state: RECONNAISSANCE, trigger: PRIOR_COMPLETE}
  - {transition_id: "plan_to_evidence", from_state: PLAN, to_state: EVIDENCE, trigger: PRIOR_COMPLETE}
```

## 6. KNOWN ISSUES FROM SOS RUNTIME EVIDENCE

Thoth's extraction of the live SOS runtime revealed these transition-relevant findings
that the schema must account for:

1. **Signal naming inconsistency:** `spawn_agent.py` emits `"type": "SPAWN_COMPLETE"` but
   `signal_router.py` checks for `"signal_type": "TaskCompleteSignal"`. The unified
   SignalSchema (T07) must standardize signal type naming.

2. **Two task creation paths:** `signal_router.py` creates tasks from `TaskRequestSignal` JSON;
   `task_spawner.py` creates tasks from `` ```task `` blocks in markdown. Both produce
   inbox `.task.md` files. The schema must allow multiple triggers for the RECEIVED state.

3. **Budget/circuit-breaker transitions:** The heartbeat daemon has budget exhaustion and
   consecutive-failure circuit breakers that halt execution. These map to escalation
   conditions in the TransitionSchema.

4. **Code extraction side-effect:** After CODE template execution, `code_extractor.py` may
   materialize code blocks to disk. This is a post-commit side-effect, not a separate
   transition. The schema should model it as a hook on the COMMITTED state.

## 7. VALIDATION CRITERIA

This schema spec is valid when:
- [ ] Every template in `_MASTER` registry can be placed as a State in at least one Protocol
- [ ] Every transition in the K4 FSM is represented
- [ ] The EXECUTION.core protocol faithfully models the SOS heartbeat→spawn→validate→write→signal loop
- [ ] Signal types are consistent across all transition trigger/output references
- [ ] No transition allows writes to constitutionally protected paths without T0 authority
- [ ] Escalation conditions cover the failure modes documented in SOS runtime evidence
