# V49 Visual Regression Fixture Runner Plan Lock

Version: V49_VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN  
Authority: A3 Visual Agent planning/reporting surface  
Production status: NOT_PRODUCTION_AUTHORIZED

V49 introduces a local/dev-only visual regression fixture runner plan and receipt layer. It exists to make repeated visual checks describable, auditable, and comparable before granting any real browser-execution or autonomous computer-control authority.

## Authority boundary

The V49 surface may:

- define visual regression fixture suites,
- load local fixture manifests inside the workspace root,
- classify planned or pre-captured before/after verification outcomes,
- emit fixture-run receipts,
- route failures/regressions to Steward/VZ and implementation agents.

The V49 surface may not:

- launch browsers,
- control a live browser,
- perform network actions,
- access credentials,
- submit forms,
- click purchase/commit/destructive controls,
- mutate DOM persistently,
- claim production visual automation authority.

V49 remains a proof and repeatability planning layer only.
