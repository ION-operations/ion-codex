---
type: research
from: Codex
created: 2026-04-03T17:39:55-04:00
status: COMPLETE
topic: Sequential kernel trace executor and first replay bundle
connections:
  - ION/04_packages/kernel/sequential_kernel.py
  - ION/tests/test_sequential_kernel.py
  - ION/07_templates/actions/ROLE_SESSION.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_mason_kernel_scaffold_replay/00_trace.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_mason_kernel_scaffold_replay/01_codex_session.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_mason_kernel_scaffold_replay/01_codex_to_vizier_handoff.md
  - ION/05_context/inbox/completed/mason_kernel_scaffold.task.md
---

# Codex Trace Executor and Replay Bundle

## Why this exists

The earlier sequential-kernel work proved that the active root could render role
chains and validate runtime surfaces. This pass extends that into a generated
execution bundle so the system can inspect a whole role-to-role packet chain on disk.

## Sources or surfaces considered

- `ION/04_packages/kernel/sequential_kernel.py`
- `ION/tests/test_sequential_kernel.py`
- `ION/07_templates/actions/HANDOFF.md`
- `ION/07_templates/actions/ROLE_SESSION.md`
- `ION/05_context/inbox/completed/mason_kernel_scaffold.task.md`
- `ION/05_context/comms/kernel_router_runs/2026-04-03_mason_kernel_scaffold_replay/`

## Findings

- The sequential kernel can now generate a per-pass execution scaffold bundle with:
  one trace manifest, one role-session packet per pass, and one handoff packet
  between adjacent passes.
- A minimum `ROLE_SESSION` template now exists in the live template floor so these
  generated session packets are not undocumented ad hoc output.
- The first replay bundle is on disk at
  `ION/05_context/comms/kernel_router_runs/2026-04-03_mason_kernel_scaffold_replay/`.
  It replays the bounded Mason scaffold task across the full implementation chain:
  `codex -> vizier -> mason -> vice -> nemesis`.
- The bundle is machine-generated and explicitly marked `PLANNED`.
  It does not pretend those passes were independently executed by each role.
- The automated proof now covers twelve tests, including bundle generation through
  both the direct function path and the CLI path.

## Implications

- ION now has a real intermediate layer between static routing logic and a future
  live executor: generated role packets and handoffs can be inspected, revised, and
  later claimed by actual role passes.
- This is the first point where “Codex as sequential kernel router” becomes visible
  as a role-to-role filesystem process instead of only a conceptual routing claim.
- The right next step is no longer another bundle format change.
  It is choosing one live inbox task and letting the bundle drive actual per-pass
  execution and writeback.

## Recommended next moves

- Add a run-status update path so a role session can transition from `PLANNED` to
  `COMPLETE` without replacing the original scaffold.
- Choose one current inbox-scoped task and generate a live, not replay-only, bundle.
- After that, add the smallest possible writeback helper so completed passes can
  emit a lawful completion delta and advance the next packet.
