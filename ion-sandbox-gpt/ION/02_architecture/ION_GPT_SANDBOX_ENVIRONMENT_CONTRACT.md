# ION GPT Sandbox Environment Contract

status: ACCEPTED_SANDBOX_LINE_PROTOCOL
created_at: 2026-05-07T05:36:22+00:00
carrier_scope: GPT_SANDBOX_CARRIER
production_authority: false
live_execution_authority: false

## Purpose

This contract records the minimum operating facts a GPT sandbox carrier must surface before acting on an uploaded ION package.

A GPT sandbox carrier can usually read files, edit the mounted copy, run bounded Python/tests, and export a candidate zip. It cannot spawn external carrier slots, use MCP unless an external connector is present, mutate a live production repository, push GitHub, or continue work in the background after the response ends.

## Required distinction

```yaml
can_read_files: true
can_edit_sandbox_copy: true
can_export_candidate_zip: true
can_run_python_validation_in_sandbox: true
can_spawn_carrier_slots: false
can_use_mcp: false
can_patch_live_repo: false
can_push_git: false
production_authority: false
live_execution_authority: false
```

## Preflight requirement

Before role execution, the carrier should produce or inspect a preflight report that reconciles the carrier profile, active work packet capability projection, host-observed sandbox limits, operator-approved authority boundaries, active allowed paths, and available validation tiers.

A mismatch does not automatically authorize wider scope. It becomes a finding for Steward or human review.

## Test tiers

Use bounded validation slices first: status command, focused readiness tests, changed-surface tests, segmented pytest groups when needed, and monolithic pytest only when the host can complete it reliably.

A monolithic timeout in this host is a sandbox limitation, not proof that ION failed.

## Non-claims

This contract does not grant production authority, live external execution, MCP authority, GitHub mutation, repository push authority, or authority to treat historical archives as current root.

## Landing rule

A GPT sandbox package export is a candidate package lineage until human or Steward review accepts it and a receipt records the accepted delta.
