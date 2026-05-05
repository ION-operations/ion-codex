# /ion-health — Canonical workflow health audit

Run the V94 canonical workflow audit from shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_cursor_canonical_workflow_audit --ion-root . --json
```

If findings appear, do not continue role work until canonical workflow surfaces are repaired.
