# V118 No Silent Loss and Containment Preservation Lock

## Lock

V118 corrects the V107 preservation wording. The project must not freeze under
a no-deletion-ever rule. ION must evolve by moving stale, harmful, superseded,
or bulky material out of hot/runtime paths into containment, quarantine,
archive, or forensic surfaces with manifest and SHA-256 proof.

The enforceable law is:

```text
NO PROJECT FILE MAY BE SILENTLY LOST.
```

## Current Objective

```text
V118 no silent loss and containment preservation: project files can leave hot state only as generated/cache removals or hash-proven containment moves; protected or unexpected uncontained removals block packaging.
```

## Required Runtime State

```yaml
trunk_preservation_gate: V118_NO_SILENT_LOSS_AND_CONTAINMENT_PRESERVATION_GATE
policy_version: V118_NO_SILENT_LOSS_CONTAINMENT_POLICY
allowed_state_exit:
  - generated_cache_removal
  - containment_move_with_matching_sha256
blocked_state_exit:
  - protected_uncontained_removal
  - unexpected_uncontained_removal
contained_removed_files: reported
containment_moves: reported
production_authority: false
live_execution_authority: false
```

## Scope

This lock repairs preservation semantics, schema/status visibility, and safe
packager naming. It does not delete files, move files by itself, accept worker
returns, or grant production/live authority.

## Exit Condition

V118 is complete when:

- containment moves with matching SHA-256 proof are accepted
- protected uncontained removals still fail the gate
- generated/cache removals remain policy-bound
- status surfaces the latest trunk preservation report and containment move count
- safe full-project packaging emits V118 no-silent-loss evidence
- focused and full tests pass
- safe package creation against V117 reports zero protected or unexpected uncontained removals
