---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-07T23:10:00-04:00
status: DRAFT
task: T12
depends_on: [T08, T09, T10, T11]
goal: Define bounded event-to-state binding for governed-write and capsule PRE/POST so manifest route-state and automation-state update from live kernel events without collapsing continuity into runtime state
connections:
  - ION/02_architecture/RUNTIME_STATE_BINDING_PROTOCOL.md
  - ION/04_packages/kernel/runtime_state_sync.py
  - ION/04_packages/kernel/governed_write.py
  - ION/04_packages/kernel/capsule_manager.py
---

# RuntimeStateBindingEvents — Bounded Event-to-State Synchronization

## 1. PURPOSE

C1 created durable `manifest_route_state` and `automation_state` families.
C2 binds those families to actual event edges already present in the live root.

## 2. SUPPORTED EVENT SOURCES

```yaml
RuntimeStateBindingEvents:
  schema_version: "1.0"

  EventSources:
    GovernedWrite:
      source_kind: governed_write
      source_ref: CommitDelta.delta_id
      inputs:
        - GovernedWriteReceipt
        - ThresholdEvaluation
        - WorkUnit
        - optional ContextPackage
      outputs:
        - AutomationState upsert
        - ManifestRouteState upsert

    Capsule:
      source_kind: capsule
      source_ref: CapsuleRecord.capsule_id
      inputs:
        - CapsuleRecord
        - scope binding
      outputs:
        - AutomationState upsert
        - ManifestRouteState upsert
```

## 3. BINDING RULES

### Governed-write

- On blocked or invalid evaluation, persist blocking machine state rather than nothing.
- On successful bounded apply, persist delivery posture.
- Failed route or authority gates must appear as machine-readable blockers or gates.
- Illegal `RUNTIME_ACTIVE` in manual context must normalize to a lawful persisted witness posture.

### Capsule PRE

- Default route loop position: `PLAN`
- Default branch status: `ACTIVE`
- Pending action: capsule `next_action`

### Capsule POST

- Default route loop position: `DELIVER`
- Default branch status: `COMPLETED`
- Pending action: capsule `next_action`
- Handoff summary may populate manifest route-frame handoff surface

## 4. REQUIRED OUTPUT FIELDS

```yaml
RuntimeStateSyncResult:
  source_kind: governed_write | capsule
  source_ref: string
  manifest_id: string
  automation_state_id: string
  notes: list[string]
```

## 5. NON-GOALS

- No autonomous daemon claim
- No hidden singleton manifest
- No continuity markdown reclassification
- No authority escalation beyond existing write law

## 6. VALIDATION CRITERIA

- [ ] Governed-write apply updates both state families.
- [ ] Governed-write blocked posture still updates both state families.
- [ ] Capsule PRE/POST can update both state families when scope binding is provided.
- [ ] Invalid runtime posture is normalized lawfully, not silently stored as valid.
- [ ] Continuity remains distinct from route-state and automation-state.
