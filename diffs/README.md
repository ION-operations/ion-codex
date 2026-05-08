# ION Diffs Lane

Status: patch evidence and candidate patch intake lane, not applied state.

This folder stores patch files that may represent older work, candidate changes,
or portable-package deltas. A diff is not active until it is inspected, applied
selectively or intentionally superseded, validated, and receipted.

Processing rule:

```text
diff -> inspect touched paths -> compare to active build -> apply selected hunks only if still relevant -> validate -> receipt
```

Do not apply a patch blindly. Some diffs may target stale paths, older package
layouts, or work already implemented differently in `ION/`.

## Current Inventory

See:

```text
DIFF_INDEX_20260508T190626Z.json
```

The current lane has 4 patch files.

## Non-Claims

- A diff is not applied state.
- A diff is not accepted ION law.
- A diff does not override current code, tests, receipts, or explicit operator
  instruction.
