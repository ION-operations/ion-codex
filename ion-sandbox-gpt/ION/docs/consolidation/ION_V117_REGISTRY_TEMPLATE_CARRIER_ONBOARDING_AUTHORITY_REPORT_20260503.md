# ION V117 Registry Template Carrier Onboarding Authority Report

## Purpose

V116 made root onboarding carrier-neutral, but it still treated shell-root markdown as a required audit surface. V117 corrects that. `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md` are protected compatibility indexes only; they are not the ION carrier onboarding substrate.

The actual onboarding authority now enforced by audit is:

```text
carrier profile YAML
runtime identity mount registry YAML
role boot files
carrier mount/session/capability/execution templates
active runtime packets
```

## Implemented

- Removed root markdown from `ion_cursor_canonical_workflow_audit` required files and required phrases.
- Kept stale Cursor root wording blocked only when it appears in optional root compatibility files.
- Updated `ion_carrier_onboarding_authority_audit` to require registry/profile/template/boot surfaces instead of root markdown.
- Updated `ION_MOUNT_CONTRACT.md` so required reads no longer include `START_HERE_FOR_ANY_AGENT.md`.
- Updated `v78_ion_mount_contract_audit` to match the mount contract repair.
- Updated `CODEX_EXTENSION_EXECUTION_PACKET.md` to require Codex carrier profile/protocol/template surfaces instead of root markdown.
- Clarified `CODEX_EXTENSION_CARRIER_PROTOCOL.md` so Codex is not described as inherently inside Cursor.
- Added mount-contract regression coverage proving `START_HERE_FOR_ANY_AGENT.md` is not required mount authority.

## Validation

```text
Focused registry/cursor/codex/mount/cartography tests: 12 passed
Full test suite: 137 passed
Live carrier onboarding authority audit: ION_CARRIER_ONBOARDING_AUTHORITY_READY
authority_surface_present_count: 14/14
stale_cursor_root_patterns_present: 0
V78 mount contract audit: mount_contract_ok true
Cursor adapter audit: ION_CURSOR_CANONICAL_WORKFLOW_READY
Codex extension carrier audit: ION_CODEX_EXTENSION_CARRIER_READY
production_authority: false
live_execution_authority: false
```

## Preservation Target

V117 must be packaged only through `kernel.ion_safe_full_project_packager` against:

```text
ION/06_artifacts/packages/ION_FULL_PROJECT_V116_CARRIER_ONBOARDING_AUTHORITY_REPAIR_20260503.zip
```

Initial V117 preservation proof:

```yaml
files_before: 4879
files_after: 4883
added_files: 4
modified_files: 16
removed_files: 0
unexpected_removed_files: 0
protected_removed_files: 0
packaging_verdict: PASS
zip_root_audit: ZIP_ROOT_CONFIRMED
```

## Authority

V117 grants no production authority, live execution authority, deletion authority, worker spawn authority, or live MCP execution authority.
