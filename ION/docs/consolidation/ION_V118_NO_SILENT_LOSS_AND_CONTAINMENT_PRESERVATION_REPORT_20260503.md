# ION V118 No Silent Loss and Containment Preservation Report

## Verdict

```yaml
line: V118_NO_SILENT_LOSS_AND_CONTAINMENT_PRESERVATION
accepted: true
production_authority: false
live_execution_authority: false
```

## Correction

V107's emergency preservation wording was too blunt. The correct ION law is not
"no deletion ever." That would freeze a still-evolving project and conflict with
V102 context metabolism.

The corrected law is:

```text
NO PROJECT FILE MAY BE SILENTLY LOST.
```

Files may leave hot/runtime paths through generated/cache removal or through
hash-proven movement into containment, quarantine, archive, or forensic
surfaces. Protected or unexpected files that vanish without containment proof
remain blocking loss events.

## Implemented Surfaces

```text
ION/00_BOOTSTRAP/V118_NO_SILENT_LOSS_AND_CONTAINMENT_PRESERVATION_LOCK.md
ION/02_architecture/ION_NO_SILENT_LOSS_AND_CONTAINMENT_PRESERVATION_PROTOCOL.md
ION/02_architecture/ION_NO_SILENT_DELETION_AND_TRUNK_PRESERVATION_PROTOCOL.md
ION/03_registry/ion_trunk_preservation_policy.yaml
ION/03_registry/ion_trunk_preservation_report.schema.json
ION/04_packages/kernel/ion_trunk_preservation_gate.py
ION/04_packages/kernel/ion_safe_full_project_packager.py
ION/04_packages/kernel/ion_status.py
ION/tests/test_kernel_ion_trunk_preservation_gate.py
```

The old no-silent-deletion protocol filename is retained only as a compatibility
alias and points to the V118 protocol.

## Runtime Behavior

The trunk preservation gate now classifies removed paths as:

```text
generated/cache removal
containment move with matching SHA-256
protected uncontained removal
unexpected uncontained removal
```

The package gate passes only when:

```yaml
protected_removed_files: 0
unexpected_removed_files: 0
```

Contained movement is visible through:

```yaml
contained_removed_files: integer
contained_removed_paths: list
containment_moves:
  - from_path: string
    to_path: string
    sha256: string
    movement_class: CONTAINMENT_MOVE
```

## Validation

Focused preservation/status validation:

```text
12 passed
```

Full current test suite:

```text
138 passed
```

## Authority Boundary

V118 does not move or delete files by itself. It is a gate and evidence layer.
Actual lifecycle movement still belongs to bounded apply actions, donor
reconciliation, quarantine/containment tooling, and future Steward-reviewed
integration.
