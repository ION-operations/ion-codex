# V112 Package-Runnable Status Optional Evidence Repair Lock

## Lock

V112 repairs a package-runnability defect found by testing the V111 full-project zip after fresh extraction.

The extracted package mounted correctly, but one included status test still assumed the generated safe-package sidecar existed inside the package. That contradicted the V110/V111 mount law: generated package sidecars are optional evidence and may be excluded from carrier packages.

## Current Objective

```text
V112 package-runnable status repair: optional safe-package evidence no longer fails fresh extracted package tests, while preservation proof and no live or production authority remain in force. Current preservation semantics are governed by V118 no-silent-loss containment preservation.
```

## Required Runtime State

```yaml
kernel_status: ION_STATUS_READY
fresh_package_tests: pass
safe_full_project_package_sidecar_required_for_mount: false
missing_state_surfaces: []
production_authority: false
live_execution_authority: false
```

## Scope

This lock does not make generated safe-package result sidecars authoritative mount surfaces. It makes their optional nature explicit in `kernel.ion_status` and in package-runnable tests.

## Exit Condition

V112 is complete when:

- status reports absent safe-package sidecar evidence with `present: false`
- status exposes the package sidecar search pattern without a stale branch-number path
- full tests pass in the working tree
- full tests pass from a fresh extraction of the V112 full-project zip
- preservation report shows zero protected and unexpected removals
