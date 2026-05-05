# Cursor / Codex Read Mode

Use this mode when the carrier has rich local filesystem access and can inspect
both roots directly.

## Read order

1. `START_HERE.md`
2. `ION/REPO_AUTHORITY.md`
3. `ION/06_intelligence/decisions/2026-04-17_retained_dual_center_settlement_canonicalization_decision.md`
4. `ION/06_intelligence/decisions/2026-04-17_workspace_root_authority_canonicalization_decision.md`
5. `ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md`
6. `ION/06_intelligence/decisions/2026-04-17_packaged_root_nested_path_disambiguation_canonicalization_decision.md`
7. `ION/03_registry/reintegration/canonicalization_queue.yaml`
8. `ION/06_intelligence/orchestration/2026-04-17_post_reintegration_canonicalization_state_forward_path_and_codex_handoff.md`

## Operating rule

Start in the packaged current-generation content root for ordinary reading and
code navigation.

When the task is package-aware, switch to the extracted branch shell root one
level above `ION/`. That shell root is where `pyproject.toml` lives.

Open the top-level production root only when the task is explicitly about:

- production packaging/preflight surfaces now coupled to the service layer
- `ion_api`
- `ion_*_mcp`
- production docs / runbook / ratification surfaces

Ignore the embedded residue lane unless the task is specifically about prior
daemon/runtime witness matter.

## STATUS handling

Do not begin from either `STATUS.md`.

After the read order above, STATUS may be used as a projection surface, not as
the first authority answer.
