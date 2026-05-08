---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-03T00:35:00-04:00
status: DRAFT
task: T07
depends_on: [T01]
goal: Define the SignalSchema — machine-readable inter-agent and inter-phase notifications
evidence:
  - ION-016 Thoth finding: spawn_agent.py emits SPAWN_COMPLETE but signal_router.py expects TaskCompleteSignal
  - SOS-OPUS/07_templates/actions/SIGNAL.md
  - ION-BUILD/context/specs/inter_agent_signal_protocol.md (D44)
---

# SignalSchema — Machine-Readable Notifications

## 1. PURPOSE

Signals are the machine-readable coordination layer. They carry state-change
notifications between agents, between phases, and between the daemon and agents.
Signals are NOT human prose — they are structured, typed, parseable artifacts.

This schema resolves a known SOS bug: `spawn_agent.py` emits `"type": "SPAWN_COMPLETE"`
but `signal_router.py` expects `"signal_type": "TaskCompleteSignal"` for dependency
checking. The unified schema standardizes all signal type names.

## 2. SCHEMA DEFINITION

```yaml
SignalSchema:
  schema_version: "1.0"

  Signal:
    # --- Identity ---
    signal_id: string            # REQUIRED — unique ID (uuid4)
    created_at: string           # REQUIRED — ISO 8601
    
    # --- Source ---
    source_agent: string         # REQUIRED — who emitted this signal
    source_work_unit: string     # OPTIONAL — which work unit produced it
    source_role: string          # OPTIONAL — structural identity of emitter
    
    # --- Target ---
    target: string               # REQUIRED — agent name, role, "ALL", or "DAEMON"
    target_domain: string        # OPTIONAL — domain filter
    
    # --- Content ---
    signal_type: enum            # REQUIRED — one of the canonical types below
    payload: object              # OPTIONAL — signal-type-specific data
    priority: enum               # REQUIRED — P0_CRITICAL | P1_HIGH | P2_NORMAL | P3_LOW
    
    # --- Lifecycle ---
    status: enum                 # REQUIRED — ACTIVE | CONSUMED | ARCHIVED | EXPIRED
    ttl_seconds: integer         # OPTIONAL — time to live (default: 86400 = 24h)
    consumed_by: string          # OPTIONAL — who consumed this signal
    consumed_at: string          # OPTIONAL — when it was consumed
    
    # --- Linking ---
    parent_signal_id: string     # OPTIONAL — if this is a response to another signal
    related_artifacts: list[string]  # OPTIONAL — paths to related files

  # --- Canonical signal types ---
  SignalType:
    # Task lifecycle
    TASK_COMPLETE:
      description: "Agent finished work unit successfully"
      required_payload: {work_unit_id: string, output_path: string, confidence: float}
      emitted_by: "Any agent"
      consumed_by: "Daemon, signal_router"
      
    TASK_FAILED:
      description: "Agent could not complete work unit"
      required_payload: {work_unit_id: string, error: string, recoverable: boolean}
      emitted_by: "Any agent"
      consumed_by: "Daemon, Praetor"
      
    TASK_REQUEST:
      description: "Request for a new work unit to be scheduled"
      required_payload: {suggested_agent: string, suggested_template: string, scope_ref: string, dependencies: list[string]}
      emitted_by: "Any agent (via CommitDelta.proposed_child_work_units)"
      consumed_by: "Daemon, signal_router"
      
    # Coordination
    HANDOFF:
      description: "Work transfer from one agent to another"
      required_payload: {from_agent: string, to_agent: string, handoff_ref: string}
      emitted_by: "Any agent"
      consumed_by: "Daemon, target agent"
      
    BLOCKED:
      description: "Agent cannot proceed — needs input or resolution"
      required_payload: {work_unit_id: string, blocker: string, needed_from: string}
      emitted_by: "Any agent"
      consumed_by: "Daemon, Vizier"
      
    READY:
      description: "Agent has completed boot and is ready for work"
      required_payload: {agent: string, chassis: string}
      emitted_by: "Any agent"
      consumed_by: "Daemon"
      
    # File coordination (D44)
    FILE_LOCK:
      description: "Agent claims exclusive write access to a file"
      required_payload: {target_file: string, reason: string, expected_duration: string}
      emitted_by: "Any agent with write authorization"
      consumed_by: "All agents, daemon"
      
    FILE_RELEASE:
      description: "Agent releases write lock on a file"
      required_payload: {target_file: string}
      emitted_by: "Lock holder"
      consumed_by: "All agents, daemon"
      
    FILE_CHANGED:
      description: "Notification that a shared file was modified"
      required_payload: {target_file: string, change_summary: string, changed_by: string}
      emitted_by: "Any agent after modifying a shared file"
      consumed_by: "All agents"
      
    # Governance
    AUDIT_COMPLETE:
      description: "Nemesis completed an audit"
      required_payload: {subject: string, verdict: string, drift_score: integer, audit_path: string}
      emitted_by: "Nemesis (Inspector General)"
      consumed_by: "Vizier, Sovereign"
      
    ESCALATION:
      description: "Issue requires higher-authority intervention"
      required_payload: {issue: string, escalate_to: string, severity: string}
      emitted_by: "Any agent"
      consumed_by: "Target authority"
      
    # System
    CHASSIS_FAILED:
      description: "LLM chassis exhausted or errored"
      required_payload: {chassis: string, error: string}
      emitted_by: "Daemon"
      consumed_by: "Daemon (retry logic)"
      
    PLAN_REVISED:
      description: "Plan document was revised"
      required_payload: {plan_path: string, revision: integer, key_changes: list[string]}
      emitted_by: "Vizier"
      consumed_by: "All agents"
```

## 3. FILESYSTEM FORMAT

Signals are persisted as JSON files (not markdown with YAML frontmatter — this
resolves the format inconsistency between SOS's `.signal.md` and `.signal.json`):

```
ION/05_context/signals/{source}_{signal_type}_{id_short}_{timestamp}.signal.json
```

Example:
```
ION/05_context/signals/MASON_TASK_COMPLETE_a1b2c3_20260403T0100.signal.json
```

During IDE/manual mode, signals may also be `.signal.md` with YAML frontmatter
for human readability. The daemon, when built, normalizes to JSON.

## 4. SIGNAL ROUTING RULES

1. Signals with `target: "DAEMON"` are consumed by the scheduler only
2. Signals with `target: "ALL"` are broadcast — every agent reads on next session
3. Signals with a specific agent name are point-to-point
4. `TASK_REQUEST` signals are always consumed by the daemon/signal_router
5. `FILE_LOCK` signals block all other agents from writing the target file
6. Stale signals (`status: ACTIVE` older than `ttl_seconds`) auto-expire to ARCHIVED
7. Consumed signals are moved to `05_context/signals/archive/`

## 5. VALIDATION CRITERIA

- [ ] Every signal type has required_payload documented
- [ ] Signal type names are consistent (no SPAWN_COMPLETE vs TaskCompleteSignal confusion)
- [ ] FILE_LOCK/RELEASE implements D44 concurrent access protocol
- [ ] TASK_COMPLETE payload enables dependency checking in signal_router
- [ ] Signal lifecycle (ACTIVE → CONSUMED → ARCHIVED) is clear
- [ ] JSON format resolves the SOS .signal.md vs .signal.json inconsistency
