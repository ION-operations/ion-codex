# V30 Summary Refresh Demo Evidence Bundle Plan

Adds a portable evidence-bundle command for the certified summary-refresh demo.

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_evidence_bundle --workspace-root .
```

The command packages certification, doctor, replay reports, operator commands, and boundaries. It does not widen mutation.

## Verification

```text
Ran 6 tests in 0.999s
OK
```

Live evidence-bundle smoke produced a certified bundle with one isolated bounded commit, two committed nodes, and four committed edges.
