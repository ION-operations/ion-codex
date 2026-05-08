---
type: canonicalization_decision
template: CANONICALIZATION_DECISION
created: 2026-04-17T00:00:00-04:00
status: WORKING
scope: external_transport_shell_current_phase_disposition
decision_class: disposition
connections:
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_retained_dual_center_settlement_canonicalization_decision.md
  - ION/06_intelligence/orchestration/2026-04-17_branch_root_shell_vs_content_root_clarification.md
  - ION/06_intelligence/orchestration/2026-04-17_external_service_shell_vs_runtime_entry_clarification.md
  - ION/06_intelligence/orchestration/2026-04-17_class_c_operator_docs_selective_extraction_and_reanchoring.md
  - ION/06_intelligence/orchestration/2026-04-17_post_q005_execution_phase_readiness_assessment.md
  - ION/03_registry/reintegration/root_manifest.yaml
  - ION/03_registry/reintegration/authority_registry.yaml
  - ION/03_registry/reintegration/canonicalization_queue.yaml
  - ION/04_packages/kernel/api_runtime_entry.py
  - ION/04_packages/kernel/external_execution_bridge.py
  - ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md
  - ION/tests/test_kernel_api_runtime_entry.py
  - ION/tests/test_kernel_external_execution_bridge.py
  - /home/sev/ION - Production/ION/pyproject.toml
  - /home/sev/ION - Production/ION/04_packages/kernel/preflight_cli.py
  - /home/sev/ION - Production/ION/04_packages/ion_api/main.py
  - /home/sev/ION - Production/ION/04_packages/ion_evidence_mcp/server.py
  - /home/sev/ION - Production/ION/04_packages/ion_policy_mcp/server.py
  - /home/sev/ION - Production/ION/04_packages/ion_recon_mcp/server.py
  - /home/sev/ION - Production/ION/04_packages/ion_state_mcp/server.py
  - /home/sev/ION - Production/ION/tests/test_ion_api.py
  - /home/sev/ION - Production/ION/tests/test_ion_api_integration.py
  - /home/sev/ION - Production/ION/tests/test_ion_state_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_ion_policy_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_ion_recon_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_ion_evidence_mcp_server.py
---

# Canonicalization Decision: External Transport Shell Current-Phase Disposition

## Purpose

Close the next q003 follow-up question honestly.

After the shell-root/content-root correction and the Class C operator-docs
packet, the remaining open question was whether the retained top-level
production external transport shell should now be promoted into the extracted
branch or held out of the current phase.

This packet answers that question directly.

## Scope

In scope:

1. the current-phase status of the top-level production external transport shell
2. whether that shell is required for truthful operation of the extracted branch
3. whether a promotion packet should be opened now

Out of scope:

- any future external transport implementation packet
- retirement of the top-level production root
- changes to the extracted branch internal runtime/session authority

## Evidence considered

Top-level production shell surfaces:

- `ION/pyproject.toml`
- `ION/04_packages/kernel/preflight_cli.py`
- `ION/04_packages/ion_api/main.py`
- `ION/04_packages/ion_evidence_mcp/server.py`
- `ION/04_packages/ion_policy_mcp/server.py`
- `ION/04_packages/ion_recon_mcp/server.py`
- `ION/04_packages/ion_state_mcp/server.py`

Top-level production shell proof surfaces:

- `ION/tests/test_ion_api.py`
- `ION/tests/test_ion_api_integration.py`
- `ION/tests/test_ion_state_mcp_server.py`
- `ION/tests/test_ion_policy_mcp_server.py`
- `ION/tests/test_ion_recon_mcp_server.py`
- `ION/tests/test_ion_evidence_mcp_server.py`

Extracted-branch runtime-entry and supervised external bridge surfaces:

- `ION/04_packages/kernel/api_runtime_entry.py`
- `ION/04_packages/kernel/external_execution_bridge.py`
- `ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `ION/tests/test_kernel_api_runtime_entry.py`
- `ION/tests/test_kernel_external_execution_bridge.py`

Context packets already landed:

- q003 promotion map
- shell-root/content-root clarification
- external service shell versus runtime-entry clarification
- Class C docs extraction and re-anchoring
- q005 retained dual-center settlement

Verification considered in this pass:

- the retained top-level production transport-shell proof set passes
- the extracted branch already has shell-root packaging proof and internal
  runtime/session carrier-entry law

## Decision

### 1. The top-level production external transport shell is real

This shell is not fictional or stale by default.

It is a coherent, tested family consisting of:

- top-level production `pyproject.toml`
- `kernel.preflight_cli`
- `ion_api`
- the `ion_*_mcp` server packages
- their support modules

So the decision is **not** that the shell lacks substance.

### 2. The shell is not required for truthful current-phase operation

The extracted branch already owns the current runnable center needed for
truthful operation in this phase:

- branch shell-root packaging floor
- `python -m kernel` entry posture
- internal API runtime-entry law
- supervised external execution bridge law
- re-anchored operator docs for install / verify / ratification use

That means the top-level production transport shell is **not** the missing core
of the extracted branch.

It is a separate external transport/service adjunct.

### 3. Current-phase disposition

The top-level production external transport shell is classified as:

**retained witness/support-only for the current phase**

That means:

- do not promote it now
- do not narrate it as the next automatic widening packet
- do not treat `ion-preflight`, `ion-api`, or the `ion_*_mcp` binaries as
  extracted-branch startup law
- do retain the family as a real, tested support surface under the retained
  top-level production root

### 4. Why promotion is not opened now

Promotion is not opened now because it would widen scope without closing the
most important current-phase gaps.

It would immediately bring:

- additional packaging claims
- FastAPI / Uvicorn / MCP dependency expectations
- service-shell operator expectations
- another carrier-entry surface to maintain

But the extracted branch already has the lawful runtime/session center needed
for the current reintegration phase.

So opening the transport shell now would add breadth, not close a continuity
or authority defect.

### 5. Operational rule after this decision

Routine current-phase rule:

- treat the extracted branch as the active runnable center
- treat the retained top-level production transport shell as witness/support
  matter unless a task is explicitly about that shell

Escalation rule:

- enter the top-level production transport shell only for bounded inspection,
  verification, or a deliberately opened future extraction packet

### 6. Reopen rule

This shell may be reopened only as a **new bounded packet** with an explicit
purpose such as:

- carrier-facing external service deployment needs
- deliberate MCP/API shell export for operators
- parity work proven necessary by a concrete downstream runtime requirement

Until then, it remains retained support/witness matter rather than active
promotion work.

## Retained witnesses and deferred matter

Retained support/witness matter:

- top-level production `pyproject.toml`
- `kernel.preflight_cli`
- `ion_api`
- `ion_*_mcp`
- their dedicated top-level production tests

Deferred matter:

- copied or merged service-shell code in the extracted branch
- branch-local FastAPI/Uvicorn/MCP packaging claims
- operator startup guidance centered on those service binaries

## Confidence and unresolved contradictions

Confidence: **high** that the top-level production external transport shell is
real and tested.

Confidence: **high** that it is not required for truthful current-phase
operation of the extracted branch.

Confidence: **high** that retaining it as witness/support-only is the correct
current-phase disposition.

Unresolved contradictions that must remain visible:

- the retained shell is real enough that it cannot be dismissed as junk
- the extracted branch still does not absorb that shell today
- a later operator or deployment need could justify reopening it as a bounded
  packet

## Required follow-up

1. Update q003 control surfaces so they stop implying an automatic transport-shell packet.
2. Update the authority registry and root manifest so they reflect the packaged
   branch packaging floor and the retained support-only status of the top-level
   production shell.
3. Update startup surfaces so they state that no automatic widening packet is
   currently selected after Class C.
