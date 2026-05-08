# ION V112 Package-Runnable Status Optional Evidence Repair Report

## Purpose

Fresh extraction of the V111 full-project package proved the root mounted and `kernel.ion_status` reported `ION_STATUS_READY`, but the packaged test suite failed one assertion because `test_kernel_ion_status.py` still required the excluded safe-package sidecar to be present.

That was a real package-runnability defect. A carrier package must be able to run its own tests under the same optional-evidence law used by status.

## Implemented

- Updated `kernel.ion_status` so absent `SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json` evidence is represented as optional evidence with `path: null`.
- Added `safe_full_project_package.path_pattern` to make the discovery contract explicit without hardcoding a stale branch-number path.
- Updated status tests so they pass both in the working tree when a sidecar exists and in extracted packages when the sidecar is intentionally absent.

## Runtime Proof Target

```yaml
status: ION_STATUS_READY
missing_state_surfaces: []
safe_full_project_package.present_when_excluded_from_package: false
safe_full_project_package.path_when_absent: null
safe_full_project_package.path_pattern: ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json
production_authority: false
live_execution_authority: false
```

## Authority

V112 grants no production authority, live execution authority, file deletion authority, live MCP execution authority, or worker spawn authority.
