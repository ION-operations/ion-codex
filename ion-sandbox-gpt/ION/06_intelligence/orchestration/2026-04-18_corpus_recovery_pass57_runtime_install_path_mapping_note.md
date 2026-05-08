---
type: pass_note
authority: A1_CANONICAL
status: ACTIVE
created: 2026-04-18T00:00:00-04:00
---

# Pass 57 — runtime/session install-path mapping

## What this pass adds

This pass adds the missing install-path mapping layer for the Lane C runtime/session
joint promotion candidate.

New surfaces:
- `corpus_recovery/19_install_path_mapping/runtime_session_install_path_mapping_packet.md`
- `corpus_recovery/19_install_path_mapping/runtime_session_install_path_mapping_matrix.csv`
- `corpus_recovery/19_install_path_mapping/runtime_session_install_path_mapping.md`

## Why it matters

Before this pass, the Lane C blocker list still treated install-path mapping as
if the trio had no concrete active landing path yet.

That was no longer truthful in this branch.

The branch already carries:
- `ION/02_architecture/RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`
- `ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`
- `ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md`
- bounded kernel slices and tests that embody the same trio

This pass turns that fact into explicit install-path law for review purposes.

## Current judgment

Lane C is still not thaw-ready, but the remaining blockers are now narrower:

- receipt-linkage review
- negative-case coverage

Install-path ambiguity is no longer the main blocker.
