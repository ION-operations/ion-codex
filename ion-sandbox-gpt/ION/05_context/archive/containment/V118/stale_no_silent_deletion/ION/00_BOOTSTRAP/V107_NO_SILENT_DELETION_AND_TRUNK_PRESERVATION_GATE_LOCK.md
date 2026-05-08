# V107 No Silent Deletion and Trunk Preservation Gate Lock

**Version line:** `V107_NO_SILENT_DELETION_AND_TRUNK_PRESERVATION_GATE`

**Authority posture:** mutation-safety gate / non-production-authoritative

## Governing Law

```text
NO FILE MAY DISAPPEAR SILENTLY.
```

Every future full-project artifact must be paired with a preservation report
that compares a baseline file manifest against the post-mutation or
post-package manifest.

## Protected Organs

The protected organ floor is registered in:

```text
ION/03_registry/ion_trunk_preservation_policy.yaml
```

Protected file loss or unexpected file loss blocks packaging and trunk
acceptance. Cache and generated temporary removal is allowed only under policy.

## Runtime Surfaces

```text
ION/04_packages/kernel/ion_trunk_preservation_gate.py
ION/04_packages/kernel/ion_safe_full_project_packager.py
ION/03_registry/ion_trunk_preservation_report.schema.json
ION/05_context/current/TRUNK_PRESERVATION_REPORT_V107.json
```

## Exit Condition

```text
protected_removed_files = 0
unexpected_removed_files = 0
packaging_verdict = PASS
```

This lock does not claim live execution authority or production authority.
