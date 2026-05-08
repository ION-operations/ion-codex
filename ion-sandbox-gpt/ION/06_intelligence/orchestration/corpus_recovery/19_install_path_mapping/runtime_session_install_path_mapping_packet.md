---
type: install_path_mapping_packet
authority: A1_CANONICAL
status: ACTIVE
created: 2026-04-18T00:00:00-04:00
---

# Runtime/session install-path mapping packet

## Purpose

The Lane C runtime/session promotion candidate is now mature enough to require
a concrete install-path map.

Unlike the earlier activation/lifecycle candidate, the key install paths are
not hypothetical in this branch. The current line already carries bounded
active-law and kernel slices for the runtime/session trio.

This packet names:

- where the trio already lives in active architecture
- which kernel modules embody the bounded current slice
- what adjacent surfaces they border
- what they must not silently replace
- and what blockers remain after install-path ambiguity is removed

This packet is **not** a new installation.
It is a truthful install-path clarification for future thaw review.

## Scope

Covered:
- active-architecture landing paths already present
- adjacent current-law surfaces
- supporting kernel modules and tests
- non-replacement boundaries
- current remaining blockers after install-path clarification

Not covered:
- final ratification
- direct new edits under `ION/02_architecture/`
- broad runtime/server refactor
- claim that the current bounded slice equals the whole historical runtime shell

## Candidate surfaces under consideration

Review-layer source set:
- `../14_quarantined_runtime_review/RUNTIME_SESSION_AUTHORITY_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/API_RUNTIME_ENTRY_PROTOCOL.review_draft.md`
- `../16_promotion_candidate_review/runtime_session_joint_promotion_candidate_packet.md`

## Active landing paths already present

Primary active-law surfaces already present:
- `ION/02_architecture/RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`
- `ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`
- `ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md`

Primary bounded kernel slices already present:
- `ION/04_packages/kernel/runtime_session_store.py`
- `ION/04_packages/kernel/runtime_session_dispatch_binding.py`
- `ION/04_packages/kernel/api_runtime_entry.py`

Primary proof surfaces already present:
- `ION/tests/test_kernel_runtime_session_store.py`
- `ION/tests/test_kernel_runtime_session_dispatch_binding.py`
- `ION/tests/test_kernel_api_runtime_entry.py`

## Active neighbors

The trio already sits adjacent to, but must not replace:
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`
- `ION/02_architecture/RUNTIME_STATE_BINDING_PROTOCOL.md`
- `ION/02_architecture/RUNTIME_STATE_QUERY_PROTOCOL.md`
- `ION/02_architecture/RUNTIME_STATE_REPORTING_PROTOCOL.md`
- `ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md`
- `ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`
- `ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`

## Non-replacement law

The current install map must not be misread as any of the following false
moves:

- scheduler law now owns session identity or queue ownership
- runtime-state witness/reporting now becomes runtime/session authority
- supervised daemon or external execution shells now become the runtime center
- API runtime entry now equals the whole center because transport entry exists
- continuation or settlement now replaces session identity, persistence, or
  queue ownership
- activation law has now been silently reloaded through queue readiness or API
  attachment

## Bounded active slice judgment

The present active slice is real but deliberately narrow:

- session authority is active enough to name session identity, persistence,
  carrier binding, and queue existence
- queue/dispatch is active enough to bind session queue items to kernel
  dispatch law
- API runtime entry is active enough to attach an external/API carrier into an
  existing or explicitly allowed new session

The present slice is **not**:

- a full server or transport shell
- a daemon runtime controller
- the whole historical runtime organism

## Root-map consequence

Because the install paths already exist, the real root-map obligation is not
"where would these go?" but:

"which startup and orchestration surfaces must acknowledge that they already
exist as bounded active law?"

The minimum affected root/orchestration surfaces are:
- `ION/README.md`
- `ION/STATUS.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/SYSTEM_MAP.md`
- current Lane C board / selection surfaces

## Remaining blockers after mapping

Install-path ambiguity is no longer the main blocker.

The remaining pre-thaw blockers are now narrower:
- explicit receipt-linkage review across session authority, queue/dispatch,
  API entry, and settlement/continuation witnesses
- explicit negative-case coverage for invalid session, stale binding, blocked
  queue, refusal, cancellation, and re-entry

## Current judgment

The Lane C set now has:
- review drafts
- seam pressure
- worked examples
- joint promotion-candidate framing
- and install-path clarity tied to already-present active-law and kernel slices

That is enough to remove install-path ambiguity as the main blocker.
It is **not** enough for thaw review yet.
