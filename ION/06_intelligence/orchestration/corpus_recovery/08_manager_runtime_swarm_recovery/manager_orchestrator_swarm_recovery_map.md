# Manager / orchestrator / swarm recovery map

## Strongest preserved lines
- `ION - Production/operation-victus/`
- `ION - Production/Project-Gemini/`

## Key evidence paths
- `ION - Production/operation-victus/victus/ion/orchestrator.py`
- `ION - Production/Project-Gemini/ion-core/ion/orchestrator.py`
- `ION - Production/Project-Gemini/ion-core/swarm.py`
- `ION - Production/Project-Gemini/ion-core/mesh_orchestrator.py`
- `ION - Production/Project-Gemini/ion-core/tests/system/test_swarm_cycle.py`

## First-pass conclusion
The current branch does not by itself preserve the full manager/orchestrator/swarm center.
That center lived more explicitly in the Victus/Gemini line.


## Pass 3 executable strengthening
See: `2026-04-13_project_gemini_swarm_cycle_receipt.md` for a stronger executable receipt showing the Project-Gemini/Victus swarm cycle witness can still run when the Victus runtime is made available on `PYTHONPATH`.
