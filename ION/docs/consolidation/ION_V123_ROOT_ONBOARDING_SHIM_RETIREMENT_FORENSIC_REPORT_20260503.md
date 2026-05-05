# ION V123 Root Onboarding Shim Retirement Forensic Report

## Verdict

The user's alarm was correct.

`START_HERE_FOR_ANY_AGENT.md` and `AGENTS.md` were still functioning as hot-root
onboarding surfaces even after the project had already corrected the doctrine
to ION-native carrier onboarding.

The failure was not only stale wording. It was a structural authority leak:
root-visible markdown containing commands and protocol anchors becomes de facto
onboarding authority no matter how many times other documents call it
compatibility-only.

## How The Failure Persisted

The previous repair was too weak because it treated the root files as
compatibility indexes instead of retiring the hot-root mechanism.

Concrete causes found:

- `START_HERE_FOR_ANY_AGENT.md` carried current operating packet anchors,
  command sequences, and protocol links at shell root.
- `AGENTS.md` carried onboarding and return contract language at shell root.
- `.cursor/hooks/ion_session_start_persona_mount.py` still instructed carriers
  to read `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md`.
- `ION/02_architecture/ION_PRODUCTIZED_RUNTIME_BOUNDARY_PROTOCOL.md` still
  treated the root shims as runtime package contents.
- `ION/04_packages/kernel/ion_lifecycle_packager.py` still included the root
  shims in the compact runtime package set.
- `ION/04_packages/kernel/ion_carrier_onboarding_authority_audit.py` blocked a
  few old Cursor V94 phrases, but did not block procedural root onboarding
  patterns or active hooks requiring retired root files.
- `ION/REPO_AUTHORITY.md` still pointed carriers to the April 17 exported
  `START_HERE.md` bundle as a preferred first startup surface.
- `ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md` was an old April 27
  witness run in current context that still listed the retired root shims as
  required reads.
- `ION/05_context/current/_tmp_onboard.json` was a generated April 27 onboarding
  artifact with the same stale required-read path.

## Corrected Authority

Carrier onboarding authority is ION-native:

```text
ION/REPO_AUTHORITY.md
ION/02_architecture/ION_MOUNT_CONTRACT.md
ION/03_registry/*carrier_profile.yaml
ION/03_registry/*runtime_identity_mount_registry.yaml
ION/03_registry/boots/*.boot.md
ION/07_templates/carriers/*.md
ION/05_context/current/ACTIVE_WORK_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
task return / context proof / template-action proof gates
```

Former root convenience files are not current onboarding authority.

## Custody Transition

The root files were not deleted silently. They were retired to containment with
matching SHA-256 proof:

```text
AGENTS.md
sha256 cbf437330e35b58beb5f8068bd602df3d5faef46ae5c5f6092e0d801df279d69
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/AGENTS.md

START_HERE_FOR_ANY_AGENT.md
sha256 fa92e38097d872d4fc005b1980b763fc09c425511d4e142485e2de0b989c9a38
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/START_HERE_FOR_ANY_AGENT.md
```

Receipt:

```text
ION/05_context/current/CONTAINMENT_RECEIPT_V123_ROOT_ONBOARDING_SHIMS.json
```

A second stale startup surface was found after the initial root-file repair:

```text
ION/05_context/exports/2026-04-17_root_authority_bundle/
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/root_authority_bundle_2026-04-17/
```

That bundle contained `START_HERE.md` and carrier read-mode files that still
said to read the bundle first. It was also retired to containment with hash
proof:

```text
ION/05_context/current/CONTAINMENT_RECEIPT_V123_ROOT_AUTHORITY_BUNDLE_START_HERE.json
```

The stale current-context operator-visible last run was also retired:

```text
ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md
sha256 27569d526f2983a9fc589263ea73e68a8d9adf8f14785997a51f4d2b92872ed3
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/OPERATOR_VISIBLE_LAST_RUN_20260427_STALE_START_HERE.md

ION/05_context/current/_tmp_onboard.json
sha256 f29c84910b6717a88c4af2341350c6be6e4171a94ddbff9f1b7d7c2ddb2f412d
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/_tmp_onboard_20260427_STALE_START_HERE.json
```

Receipt:

```text
ION/05_context/current/CONTAINMENT_RECEIPT_V123_STALE_OPERATOR_VISIBLE_LAST_RUN.json
```

## Repairs Made

V123 changes:

- retired `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md` from shell root
- updated the Cursor session hook to require ION-native mount surfaces only
- updated carrier onboarding protocol to define root shim retirement law
- updated mount contract to state former root shims are retired from hot mount authority
- updated current operating packet to identify V123 root shim retirement as current state
- updated repo authority so the April 17 `START_HERE.md` export is historical
  containment evidence, not first-read startup law
- removed root shims from productized runtime package authority
- removed root shims from compact runtime package roots
- moved the April 17 root authority bundle out of hot exports and pointed its
  legacy kernel helper at the containment path
- moved the stale April 27 operator-visible last-run witness out of current context
- strengthened carrier onboarding audit to block procedural root markdown,
  active hooks that require retired root files, and repo authority language
  that crowns the old `START_HERE.md` bundle as first read
- added tests for the reproduced failure modes

## Why This Matters

This is the difference between preserving evidence and preserving stale
authority.

ION's containment law is:

```text
No unreceipted disappearance of authority-bearing state.
No stale authority preserved in hot state merely from fear of deletion.
```

V123 applies that law to root onboarding.

## Validation

Validation is recorded in:

```text
ION/05_context/current/CARRIER_ONBOARDING_AUTHORITY_AUDIT_V123.json
ION/05_context/current/TRUNK_PRESERVATION_REPORT_V123.json
ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V123.json
```

Validation results:

```text
carrier_onboarding_authority_audit: ION_CARRIER_ONBOARDING_AUTHORITY_READY
focused regression tests: 24 passed
full test suite: 163 passed
ion_status: ION_STATUS_READY
package: ION_FULL_PROJECT_V123_ROOT_ONBOARDING_SHIM_RETIREMENT_20260503.zip
package_root: ZIP_ROOT_CONFIRMED
trunk_preservation: PASS
contained_removed_files: 13
unexpected_removed_files: 0
protected_removed_files: 0
production_authority: false
live_execution_authority: false
```

The safe package report proves the old root shims, old exported
`START_HERE.md` bundle, and stale current-context onboarding artifacts moved to
containment with matching hashes.

## Authority Ceiling

Production authority remains `false`.

Live execution authority remains `false`.
