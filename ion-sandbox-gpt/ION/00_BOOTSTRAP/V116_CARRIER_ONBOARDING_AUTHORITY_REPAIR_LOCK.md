# V116 Carrier Onboarding Authority Repair Lock

## Lock

V116 repairs root-level carrier onboarding authority.

The root files `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md` must not present stale Cursor-specific V94 workflow as universal ION law. Cursor remains a supported adapter, but root onboarding must be carrier-neutral and must point carriers to active runtime packets, carrier ids, current protocols, and preservation gates.

## Current Objective

```text
V116 carrier onboarding authority repair: root onboarding is carrier-neutral, Codex is mounted as codex_extension, Cursor is scoped as one adapter, and stale V94 Cursor root wording is audit-blocked.
```

## Required Runtime State

```yaml
root_confirmed: true
carrier_onboarding_authority_audit: ION_CARRIER_ONBOARDING_AUTHORITY_READY
stale_cursor_root_patterns_present: 0
root_onboarding_files_present: 2
production_authority: false
live_execution_authority: false
```

## Scope

This lock changes root onboarding authority and adds an audit. It does not remove Cursor adapter support, delete protected files, spawn workers, materialize deferred role bundles, or grant production/live authority.

## Exit Condition

V116 is complete when:

- root onboarding is carrier-neutral
- Cursor `/ion` is scoped as a Cursor adapter shortcut, not universal ION law
- Codex carrier id is explicit as `codex_extension`
- stale V94 Cursor root-onboarding patterns are blocked by test and live audit
- full tests pass
- safe full-project packaging compares against V115 and reports zero protected or unexpected removals
