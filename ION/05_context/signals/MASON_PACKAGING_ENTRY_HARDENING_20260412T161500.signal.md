---
type: signal
from: Mason
to:
  - Codex
  - Vizier
signal: TASK_COMPLETE
status: ACTIVE
created: 2026-04-12T16:15:00-04:00
payload:
  task: "Land outsider-grade packaging hardening (01_task.md packaging slice)"
  artifacts:
    - pyproject.toml
    - ION/tests/test_packaging_entry_posture.py
  packaging_metadata_added_or_changed:
    - "Branch-root pyproject.toml: project ion-kernel, setuptools packages.find where=ION/04_packages include=kernel*, pytest.ini_options testpaths=ION/tests pythonpath=ION/04_packages"
  import_cli_entry_changes: "None (existing kernel.__main__ -> operator_cli.main remains the CLI surface after editable install)"
  tests_added_or_updated:
    - ION/tests/test_packaging_entry_posture.py
  verification_performed:
    - "cd \"<working-branch-root>\" && python3 -m venv .venv && .venv/bin/pip install -q setuptools wheel pip -U && .venv/bin/pip install -q -e . && env -u PYTHONPATH .venv/bin/python -c \"import kernel; print(kernel.__file__)\""
    - "cd \"<working-branch-root>\" && env -u PYTHONPATH .venv/bin/python -m kernel --help"
    - "cd \"<working-branch-root>\" && env -u PYTHONPATH python3 -m pytest ION/tests -q"
  summary: "Operators can pip install -e . from the working branch root and use import kernel / python -m kernel without PYTHONPATH; pytest picks up ION/04_packages via committed pytest config."
---

Mason completed the bounded packaging slice: branch-root setuptools wiring for the
`kernel` package plus pytest `pythonpath` so the full `ION/tests` suite runs with
`PYTHONPATH` unset. Kernel Python modules were not redesigned; no law or template edits.
