# ION V116 Carrier Onboarding Authority Repair Report

## Purpose

V116 repairs a root-level authority problem: `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md` were still framed as V94 Cursor carrier onboarding. That made a stale Cursor-specific adapter workflow look like universal ION protocol.

The repair keeps Cursor support, but scopes it correctly. Cursor is one adapter. Codex is the current carrier as `codex_extension`. Root onboarding now points carriers to shell-root proof, active runtime packets, carrier-neutral continuation, return intake, and preservation-proof packaging. Current preservation semantics are governed by V118 no-silent-loss containment preservation.

## Implemented

- Rewrote `START_HERE_FOR_ANY_AGENT.md` as `ION Carrier Mount Index`.
- Rewrote `AGENTS.md` as `ION Carrier Onboarding And Return Contract`.
- Added `ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md`.
- Added `kernel.ion_carrier_onboarding_authority_audit`.
- Added tests proving stale V94 Cursor root onboarding is blocked.
- Wrote live audit report to `ION/05_context/current/CARRIER_ONBOARDING_AUTHORITY_AUDIT_V116.json`.

## Validation

```text
Focused onboarding authority tests: 3 passed
Focused Cursor/onboarding audit compatibility tests: 4 passed
Full test suite: 136 passed
Live onboarding authority audit: ION_CARRIER_ONBOARDING_AUTHORITY_READY
stale_cursor_root_patterns_present: 0
root_onboarding_files_present: 2
production_authority: false
live_execution_authority: false
```

## Preservation Target

V116 must be packaged only through `kernel.ion_safe_full_project_packager` against:

```text
ION/06_artifacts/packages/ION_FULL_PROJECT_V115_AUDIT_TRUTH_RECONCILIATION_20260503.zip
```

Initial V116 preservation proof:

```yaml
files_before: 4873
files_after: 4879
added_files: 6
modified_files: 9
removed_files: 0
unexpected_removed_files: 0
protected_removed_files: 0
packaging_verdict: PASS
zip_root_audit: ZIP_ROOT_CONFIRMED
```

## Authority

V116 grants no production authority, live execution authority, deletion authority, worker spawn authority, or live MCP execution authority.
