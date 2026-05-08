---
type: audit
authority: A3_OPERATIONAL
template: AUDIT
created: 2026-04-12T11:44:01-04:00
subject: Phase 1 browser mount boundary disagreement
status: CONDITIONAL
---

# Audit: Phase 1 Browser Mount Boundary

## Scope

Audit whether direct browser role mount is currently lawful in Phase 1, or whether the
branch must keep browser ChatGPT external and unmounted.

## Sources Examined

- `ION/AGENT_CONTRACT.md`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- `ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/05_browser_external_unmounted_role_chassis_mount.md`
- `ION/06_intelligence/research/2026-04-12_phase1_browser_mount_boundary_research.md`

## Findings

1. Direct browser role mount does not currently have stronger active branch authority
   than the explicit `EXTERNAL_UNMOUNTED` default in the mount protocol.
2. Skipping the external-return boundary would violate the executor contract and the
   external bridge law that returned work must re-enter as bounded artifacts rather than
   direct live truth.
3. The branch already has one real packet proving the browser default posture. Reversing
   that posture would require stronger evidence, not operator preference alone.

## Recommendations

- treat browser ChatGPT as `EXTERNAL_UNMOUNTED` for the current phase
- require `EXTERNAL_RETURN` plus `PATCH_PACKAGE` for the first real browser drill
- keep the mount question open as a future possible refinement rather than silently
  settling it today

## Verdict

Law converged for the current phase: browser ChatGPT should remain external and
unmounted by default. Recovery is not complete yet because the browser zip-return drill
and the broader integrated packet-flow proof still remain open.
