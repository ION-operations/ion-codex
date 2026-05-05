# ION V107 No Silent Deletion and Trunk Preservation Report

## Purpose

V107 turns the project trust crisis into an enforceable gate:

```text
NO FILE MAY DISAPPEAR SILENTLY.
```

## Implemented Surfaces

```text
ION/00_BOOTSTRAP/V107_NO_SILENT_DELETION_AND_TRUNK_PRESERVATION_GATE_LOCK.md
ION/02_architecture/ION_NO_SILENT_DELETION_AND_TRUNK_PRESERVATION_PROTOCOL.md
ION/03_registry/ion_trunk_preservation_policy.yaml
ION/03_registry/ion_trunk_preservation_report.schema.json
ION/04_packages/kernel/ion_trunk_preservation_gate.py
ION/04_packages/kernel/ion_safe_full_project_packager.py
ION/04_packages/kernel/ion_steward_integrate.py
ION/tests/test_kernel_ion_trunk_preservation_gate.py
ION/tests/test_kernel_ion_safe_full_project_packager.py
ION/tests/test_kernel_ion_steward_integrate.py
ION/05_context/current/TRUNK_PRESERVATION_REPORT_V107.json
ION/05_context/current/TRUNK_FILE_MANIFEST_BASELINE_V107.json
ION/05_context/current/TRUNK_FILE_MANIFEST_POSTPATCH_V107.json
ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V107.json
ION/06_artifacts/packages/ION_FULL_PROJECT_V107_NO_SILENT_DELETION_20260502.zip
```

## Gate Behavior

The V107 gate records file path, byte size, and SHA-256 hash for every
manifested project file. It emits added, modified, removed, allowed-removed,
unexpected-removed, and protected-removed counts.

Packaging blocks when:

```text
protected_removed_files > 0
unexpected_removed_files > 0
```

Allowed removals are limited to registered generated cache or temporary
surfaces.

## Generated Package Proof

Baseline:

```text
/home/sev/ION - Production/ION most recent/ION_CURSOR_V105_FULL_PROJECT_CONSOLIDATED_20260502.zip
```

New full-project package:

```text
ION/06_artifacts/packages/ION_FULL_PROJECT_V107_NO_SILENT_DELETION_20260502.zip
```

Preservation comparison:

```yaml
files_before: 4242
files_after: 4659
added_files: 417
modified_files: 27
removed_files: 0
allowed_removed_files: 0
unexpected_removed_files: 0
protected_removed_files: 0
packaging_verdict: PASS
accepted: true
```

Package root proof:

```yaml
zip_root_audit: ZIP_ROOT_CONFIRMED
wrapped_entries: 0
pytest_cache_entries: 0
zip_sha256_source: ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V107.json
```

The V107 preservation manifests, preservation report, package result, package
zips, and cache files are sidecar/generated evidence and are excluded from the
safe full-project archive to avoid stale or recursive package contents.

## Steward Queue Closure

V107 also closes the accepted-return boundary that was left visible after
carrier task return intake. `kernel.ion_steward_integrate` now supports
`--integrate-queue`, which consumes `PENDING_STEWARD_INTEGRATION` items, reruns
the template/action proof gate against each captured task return, writes a
Steward integration receipt, and marks each item as integrated or rejected.

Current queue result:

```yaml
processed_count: 2
accepted_count: 2
rejected_count: 0
pending_count: 0
verdict: ION_STEWARD_QUEUE_INTEGRATION_COMPLETE
```

## Authority Boundary

This is not production authority. It is a mutation-safety and packaging
integrity layer for future trunk acceptance.
