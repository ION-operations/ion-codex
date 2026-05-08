# V117 Registry Template Carrier Onboarding Authority Lock

## Lock

V117 corrects the remaining V116 overreach: shell-root markdown is not the ION carrier onboarding substrate.

The enforceable carrier onboarding surface is registry profiles, runtime identity mount registries, role boot files, carrier execution templates, and active runtime packets. Root files such as `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md` may remain protected compatibility indexes, but kernel audits must not require them as carrier authority.

## Current Objective

```text
V117 registry/template carrier onboarding authority: carrier onboarding is enforced through profiles, mount registries, role boots, templates, and active packets; root markdown is optional compatibility only.
```

## Required Runtime State

```yaml
carrier_onboarding_authority_audit: ION_CARRIER_ONBOARDING_AUTHORITY_READY
authority_surface_present_count: authority_surface_count
stale_cursor_root_patterns_present: 0
v78_mount_contract_requires_start_here: false
cursor_adapter_audit: ION_CURSOR_CANONICAL_WORKFLOW_READY
codex_extension_carrier_audit: ION_CODEX_EXTENSION_CARRIER_READY
production_authority: false
live_execution_authority: false
```

## Scope

This lock changes authority classification and audits only. It does not delete root compatibility files, remove Cursor adapter support, spawn workers, materialize deferred role bundles, or grant production/live authority.

## Exit Condition

V117 is complete when:

- `ion_cursor_canonical_workflow_audit` no longer requires root markdown files
- `ion_carrier_onboarding_authority_audit` gates on registry/profile/template/boot surfaces
- `ION_MOUNT_CONTRACT.md` no longer requires `START_HERE_FOR_ANY_AGENT.md`
- `CODEX_EXTENSION_EXECUTION_PACKET.md` requires Codex carrier profile/protocol/template surfaces instead of root markdown
- focused and full tests pass
- safe full-project packaging compares against V116 and reports zero protected or unexpected removals
