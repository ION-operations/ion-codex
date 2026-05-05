# T38 — Supervised Automation Policy Matrix

## Intent

Provide the first bounded decision matrix for supervised automation actions in the live ION root.

## Required Behaviors

1. Accept one bounded automation action request.
2. Consider operator stop / hold state.
3. Consider context mode, automation stage, calibration status, threshold action, and review pressure.
4. Return one of:
   - `ALLOW`
   - `REQUIRE_APPROVAL`
   - `HOLD`
   - `BLOCK`
5. Preserve explicit reasons and required controls.
6. Optionally convert `REQUIRE_APPROVAL` into `ALLOW` only when explicit approval is supplied.

## Non-Goals

- autonomous scheduling
- mutation of kernel truth
- external execution
