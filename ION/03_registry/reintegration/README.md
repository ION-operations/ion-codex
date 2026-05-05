---
type: registry_index
created: 2026-04-17T00:00:00-04:00
status: WORKING
authority: A3_OPERATIONAL
canon_status: PROVISIONAL_BRIDGE_NOT_FINAL_CANON
---

# Reintegration Registry Set

This directory holds the **minimal first registry stack** for constitutional
reintegration and canon-foundry work.

It exists to support real adjudications, not to create a second planning
religion inside the registry surface.

Current scope:

- workspace root-authority adjudication,
- minimal lineage and competition visibility,
- explicit queueing of the next canonicalization questions.

Current files:

- `root_manifest.yaml`
- `lineage_registry.yaml`
- `authority_registry.yaml`
- `duplicate_competition_registry.yaml`
- `canonicalization_queue.yaml`

Current decision anchor:

- `ION/06_intelligence/decisions/2026-04-17_workspace_root_authority_canonicalization_decision.md`

Invariants:

1. The registries record decisions and competitions; they do not replace them.
2. No root is retired by registry entry alone.
3. Expansion beyond this minimal set should follow concrete adjudications, not
   speculative completeness.
