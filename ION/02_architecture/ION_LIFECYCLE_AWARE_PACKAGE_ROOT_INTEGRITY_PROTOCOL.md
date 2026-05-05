# ION Lifecycle-Aware Package Root Integrity Protocol

```yaml
schema_id: ion.lifecycle_aware_package_root_integrity_protocol.v1
version_line: V106_LIFECYCLE_AWARE_PACKAGE_ROOT_INTEGRITY
production_authority: false
mutation_authority: source_immutable_manifest_audit_and_package_zip_creation
```

## Purpose

ION packages must be mountable without the next carrier guessing which nested
folder is the real shell root. The required shell-root files are:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

If those files are under a wrapper such as `CURSOR- ION/`, the archive may
contain the project, but it is not a canonical ION carrier package until it is
repacked with those files at archive root.

## Package Classes

```text
FULL_PROJECT      current project state for broad inspection
COMPACT_RUNTIME   hot runtime state for fast lawful carrier mount
FORENSIC_ARCHIVE  historical evidence, cold context, and reconciliation material
```

## Required Gate

Before a package is used as an ION runtime root, run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_lifecycle_packager --ion-root . --package-class COMPACT_RUNTIME --audit-zip <package.zip> --json
```

Accepted package root verdict:

```text
ZIP_ROOT_CONFIRMED
```

Review/block verdicts:

```text
WRAPPED_ROOT_DETECTED
MULTIPLE_WRAPPED_ROOTS_DETECTED
ROOT_INVARIANT_FAILED
ZIP_NOT_FOUND
```

## Materialization Command

To emit a canonical-root compact runtime package:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_lifecycle_packager --ion-root . --package-class COMPACT_RUNTIME --create-zip --zip-output ION/06_artifacts/packages/ION_COMPACT_RUNTIME_V106_20260502.zip --json
```

Materialization writes a zip artifact and sidecar manifest. It must not move,
delete, or rewrite source evidence. Packaged file permissions are normalized to
`0644` so extraction-damaged unreadable files are not copied forward.

## Non-Claims

This protocol does not grant deletion, archival mutation of source evidence,
external transfer, production deployment, or full release authority. It is a
packaging integrity, lifecycle manifest, and source-immutable zip creation gate.
