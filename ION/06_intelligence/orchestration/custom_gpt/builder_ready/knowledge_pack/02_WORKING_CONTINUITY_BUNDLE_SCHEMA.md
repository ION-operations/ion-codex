# WORKING_CONTINUITY_BUNDLE_SCHEMA

## Purpose

This document defines the canonical schema for the **working continuity bundle** used by the ION custom GPT.

This is the bundle the GPT reads and updates during active use.

## Design goals

The working bundle must be:

- uploadable
- compact
- human-auditable
- machine-parseable
- stable in structure
- rich enough to resume serious work
- disciplined enough not to grow without bound

## Canonical top-level layout

```text
ION_WORKING_CONTINUITY_BUNDLE/
  00_manifest/
    bundle_manifest.yaml
    integrity_manifest.yaml
    export_notes.md

  01_identity/
    project_identity.yaml
    continuity_profile.yaml

  02_state/
    current_state.yaml
    active_mission.md
    active_constraints.md
    current_priorities.md

  03_context/
    project_summary.md
    key_entities.yaml
    relevant_artifacts.yaml
    project_overrides.md

  04_temporal/
    temporal_objects.yaml
    active_leases.yaml
    recurrence_registry.yaml
    upcoming_reconfirmations.yaml

  05_budget/
    budget_posture.yaml
    forecast_bundles.yaml
    estimate_receipts.yaml

  06_continuity/
    continuity_summary.md
    recent_decisions.md
    unresolved_questions.md
    drift_watch.md

  07_receipts/
    recent_receipts.yaml
    transition_receipts.yaml

  08_history/
    compact_timeline.md
    archive_lineage.yaml

  09_handoff/
    restart_instructions.md
    next_session_bootstrap.md
```

## Minimum required files

### `00_manifest/bundle_manifest.yaml`
Must include:
- bundle_id
- bundle_version
- schema_version
- continuity_generation
- export_timestamp
- project_id
- project_name
- compaction_level
- included_sections
- excluded_sections

### `01_identity/project_identity.yaml`
Must include:
- project_id
- project_name
- continuity_shell
- continuity_owner
- current_status

### `02_state/current_state.yaml`
Must include:
- current_phase
- active_objectives
- current_branch_state
- next_expected_actions

### `06_continuity/continuity_summary.md`
Must summarize:
- where work currently stands
- what remains live
- what changed recently
- how to resume conservatively

### `06_continuity/unresolved_questions.md`
Must preserve live unresolved questions.

### `09_handoff/next_session_bootstrap.md`
Must provide a compact restart bridge for the next session.

## Compaction rules

The working bundle should preserve:
- active identity
- live obligations
- unresolved questions
- recent decisions
- recent receipts
- active temporal objects
- current budget posture

The working bundle should compress:
- cold history
- bulky prior logs
- deep archives already reflected in summaries
- large raw artifacts that are externally referenced

## Export rule

The GPT should always export a new working bundle with:
- incremented continuity generation
- updated timestamps
- refreshed continuity summary
- refreshed next-session bootstrap
- updated recent receipts
- preserved lineage references

## Present conclusion

The working bundle is the GPT-facing mutable operational state.
It must stay compact, explicit, and resumable.
