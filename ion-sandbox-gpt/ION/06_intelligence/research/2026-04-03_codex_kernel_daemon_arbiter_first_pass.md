---
type: research
from: Codex
created: 2026-04-03T21:49:49-04:00
status: COMPLETE
topic: First bounded daemon arbitration slice
connections:
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_daemon.py
  - ION/05_context/inbox/codex_kernel_daemon_arbiter_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_daemon_arbiter_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T01_TransitionSchema.spec.md
  - ION/06_intelligence/specs/T07_SignalSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_child_work_issuance_first_pass.md
---

# Codex Kernel Daemon Arbiter First Pass

## Why this exists

The active kernel stack could now schedule, dispatch, execute, validate, apply,
route questions, emit and archive signals, and issue child work, but it still
lacked one explicit daemon-level object that could inspect the whole current
state and say what should happen next.

Without that, the stack had pieces but not a truthful decision surface.

This pass adds that first decision layer.

## Sources or surfaces considered

- `ION/04_packages/kernel/scheduler.py`
- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/children.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_daemon.py`
- `ION/06_intelligence/specs/T01_TransitionSchema.spec.md`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/daemon.py` now provides the first bounded daemon
  arbitration helper for the active kernel stack.
- The helper introduces:
  `KernelDaemonArbiter`, `IonDaemonArbiter`, `DaemonActionType`,
  `DaemonActionCandidate`, and `DaemonArbitrationResult`.
- The arbiter intentionally does not claim a full autonomous loop. It returns the
  next highest-priority lawful action from current state rather than executing a
  hidden controller pass.
- The current action order is now explicit in code:
  1. `CONSUME_ACTIVE_SIGNAL`
  2. `ESCALATE_REVIEW`
  3. `ROUTE_OPEN_QUESTIONS`
  4. `ISSUE_CHILD_WORK`
  5. `DISPATCH_WORK`
  6. `IDLE`
- Active daemon-targeted canonical signals now count as top-level runtime
  pressure even though signal-type-specific interpretation is still not built.
  This is a deliberate boundary: the daemon can now see that signal pressure
  exists before it knows how to semantically route every signal kind.
- Review-held deltas now surface as explicit daemon work instead of remaining only
  as a status on a `CommitDelta`.
- Accepted deltas with unrouted open questions or unissued child work now surface
  as explicit daemon work instead of remaining dead intent inside persisted state.
- Dispatchable pending work is still visible through the existing scheduler and is
  now folded into the same ordered arbitration surface rather than living as a
  separate helper-only concept.
- `ION/tests/test_kernel_daemon.py` proves:
  - active daemon-targeted signals outrank everything else
  - review-held validation outranks question routing and dispatch
  - unrouted questions outrank child issuance and dispatch
  - child issuance outranks dispatch when questions are absent
  - pure dispatchable state still resolves cleanly
  - empty state returns `IDLE`
- The combined kernel suite is now at **90 passing tests**.

## Boundary

- This is not the full daemon loop.
- It does not yet execute the chosen action.
- It does not yet interpret canonical signal types semantically.
- It does not yet expire stale signals.
- It does not yet reconcile multiple accepted deltas from the same parent work
  unit beyond the current bounded heuristics.

## Implications

- The active kernel now has a truthful daemon decision surface.
- The system can now express the daemon’s next-step judgment as visible structured
  state instead of relying on an operator to mentally arbitrate across separate
  helpers.
- This materially reduces orchestration guesswork and makes the next runtime step
  much clearer: either execute chosen actions, or deepen signal semantics before
  execution.

## Recommended next moves

- Build the first bounded `act_once` helper that can execute at least the
  non-signal daemon decisions already surfaced here.
- Or, if active signal pressure becomes the dominant live surface, build
  type-specific signal interpretation and stale-signal expiry before action
  execution.
