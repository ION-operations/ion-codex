---
type: research
authority: A3_OPERATIONAL
created: 2026-04-10T20:30:00-04:00
status: ACTIVE
---

# Bootstrap-init landed

## Goal

Eliminate manual authoring of the first bootstrap packet in fresh extracted roots while preserving the now-explicit bootstrap layering:

1. init writes packet
2. bridge writes canonical signal
3. daemon consumes signal

## What landed

### New kernel surface

- `ION/04_packages/kernel/bootstrap_init.py`

This module adds the smallest lawful earlier bootstrap surface the current stack can support:

1. write one canonical bootstrap `task` packet into `ION/05_context/inbox/bootstrap/`
2. validate that packet against the canonical packet law before accepting it
3. persist one bootstrap-init receipt under `ION/05_context/history/bootstrap_init_receipts/`
4. leave daemon law unchanged
5. leave the existing bootstrap bridge unchanged

### New operator surface

- `python -m kernel bootstrap init ...`

This command mints the first visible bootstrap packet without requiring manual markdown authoring.
It does **not** emit daemon pressure directly.
It preserves the packet lane.

### Current path after this landing

A fresh extracted root can now reach lawful first daemon pressure through the following truthful chain:

1. `python -m kernel bootstrap init ...`
2. `python -m kernel bootstrap emit ...`
3. `python -m kernel daemon run --approval --max-steps 1`

## Why this is the correct order

The branch already had:

- visible bootstrap packet lane
- bridge into canonical daemon signal lane
- supervised daemon follow-up behavior

The remaining manual seam was packet authoring.
Bootstrap-init removes only that seam.
It does not collapse the constitutional layers.

## Proof

The relevant targeted regressions now pass:

```text
PYTHONPATH=04_packages pytest -q \
  tests/test_kernel_bootstrap_init.py \
  tests/test_kernel_bootstrap_bridge.py \
  tests/test_kernel_daemon_bootstrap.py \
  tests/test_kernel_daemon.py \
  tests/test_kernel_daemon_actions.py \
  tests/test_kernel_daemon_loop.py \
  tests/test_kernel_operator_cli.py
```

Result:

```text
65 passed in 2.18s
```

The proof now covers:

- bootstrap init packet writing
- packet validation
- bootstrap bridge emission
- daemon consumption
- durable `signal_followup` pressure creation
- operator CLI coverage for both `bootstrap init` and `bootstrap emit`

## Architectural significance

This landing means a fresh extracted root no longer requires manual signal authoring or manual packet authoring to reach the first lawful daemon action.

That is important because it makes ION’s native self-use posture more truthful:

- visible bootstrap packet law remains explicit
- canonical signal law remains explicit
- daemon law remains explicit
- no hidden carrier state is invented to achieve first activation

## Next pressure

The next frontier is not “can fresh roots wake the daemon?”
That answer is now yes.

The next frontier is:

**how should the three-step bootstrap chain be packaged as one lawful supervised activation protocol without collapsing the constitutional layers?**

That suggests a next packet around either:

- bootstrap activation orchestration (`init -> emit -> daemon`) with explicit receipts, or
- a visible initialization manifest that can mint one or more bootstrap packets declaratively.
