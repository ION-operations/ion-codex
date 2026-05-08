---
type: task
agent: Mason
template: CODE
priority: P2
target: ION/04_packages/kernel/__init__.py
depends_on: none
created: 2026-04-03T19:00:00-04:00
from: Vizier
---

# Mission: Create kernel package scaffold

Create the initial Python package structure for the ION kernel at `ION/04_packages/kernel/`.

## Requirements

1. Create `ION/04_packages/__init__.py` (empty, marks packages root)
2. Create `ION/04_packages/kernel/__init__.py` with a docstring: "ION Kernel — core object model, store, index, graph."
3. Create `ION/04_packages/kernel/model.py` with ONLY a module docstring and a placeholder comment: "# Port from ION-BUILD src/ion/kernel/model.py and IONv2 ion/model.py per T22"
4. No actual implementation yet — just the scaffold.

## Lane

Write ONLY to `ION/04_packages/kernel/`. Nothing else.

## On Completion

1. Update your private `ION/agents/mason/MINI.md` and `ION/agents/mason/CAPSULE.md`
2. Emit signal: `MASON_TASK_COMPLETE_scaffold.signal.md`
3. Move this task file to `ION/05_context/inbox/completed/`

## Verification

- `python3 -c "import sys; sys.path.insert(0, 'ION/04_packages'); import kernel"` should not error
