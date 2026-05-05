---
type: template
template_name: EXTERNAL_RETURN
created: 2026-04-12T11:26:36-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
---

# TEMPLATE — EXTERNAL RETURN

Use this when an external carrier returns bounded work from a snapshot, zip, or VM
surface back toward the live branch.

## Required frontmatter

```yaml
---
type: external_return
template: EXTERNAL_RETURN
created: <ISO timestamp>
status: <RETURNED|HELD|REJECTED|LANDED_AS_WITNESS>
from: <external carrier or role>
source_chassis: <browser, VM, API worker, or other carrier>
governing_packet: <task, role session, or handoff path>
workspace_snapshot: <snapshot or zip identifier>
target_owner: <live branch owner or role>
targets:
  - <file path>
---
```

## Required body sections

```markdown
# External Return: <title>

## Source Carrier

## Governing Inputs

## Produced Artifacts

## Proposed Delta or Patch

## Validation Notes

## Unresolved Drift / Risks

## Requested Landing Path
```

## Invariants

1. The return must point to one governing packet.
2. Exact target scope must be named.
3. The return must distinguish produced artifacts from already-landed truth.
4. If a full zip or snapshot is returned, the packet must still summarize bounded target
   paths and the intended landing path.
5. Any unresolved drift must remain visible.
