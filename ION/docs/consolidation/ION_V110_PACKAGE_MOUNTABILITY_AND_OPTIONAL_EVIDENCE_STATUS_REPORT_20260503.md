# ION V110 Package Mountability and Optional Evidence Status Report

## Purpose

Fresh extraction of the V109 package confirmed the archive root was canonical, but `kernel.ion_status` reported `ION_STATUS_PARTIAL` because generated package evidence sidecars were intentionally excluded from the archive.

V110 fixes that false degradation.

## Change

`kernel.ion_status` now treats package proof sidecars as optional evidence:

- `TRUNK_PRESERVATION_REPORT_V107.json`
- `SAFE_FULL_PROJECT_PACKAGE_RESULT_V109.json`

The status command still surfaces those reports when present. It does not require them for mount readiness after extraction.

The V72 MCP donor reconciliation audit remains a required active state surface because it is stable evidence about restored donor substrate, not self-referential package output.

## Why

A package cannot include its own final package hash proof and remain stable. The final package proof must remain an external sidecar emitted by the safe packager. Requiring that sidecar inside the package makes every valid extracted package look partially broken.

## Validation Target

```text
fresh package extraction -> pyproject.toml present
fresh package extraction -> ION/REPO_AUTHORITY.md present
fresh package extraction -> kernel.ion_status returns ION_STATUS_READY
full test suite passes
safe packager returns PASS
removed_files = 0
protected_removed_files = 0
unexpected_removed_files = 0
```

## Authority

```yaml
production_authority: false
live_execution_authority: false
```
