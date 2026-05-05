# V64 Provider Adapter Readiness and Selector Health View Model Lock

```yaml
version: V64_PROVIDER_ADAPTER_READINESS_AND_SELECTOR_HEALTH_VIEW_MODEL
branch_class: ui_runtime_governance_view_model
base_branch: V63_DRY_RUN_DISPATCH_EXECUTION_TRACE_VIEW_MODEL
production_authority: false
live_dispatch_authority: false
external_model_call_authority: false
browser_session_mutation_authority: false
credential_access_authority: false
purpose:
  - render provider adapter readiness before any live dispatch branch exists
  - bind dry-run dispatch trace evidence to provider/session selector health
  - preserve no-op adapter boundary
  - surface missing provider evidence, degraded session health, unsupported access method, and forbidden capability drift
```

V64 does **not** execute dispatch. It creates a cockpit-visible readiness receipt for the selected provider adapter and compute/access lane after V63 has produced a non-executing dry-run trace.

The lock rule is:

```text
A no-op trace may show provider readiness.
Provider readiness is not live provider authority.
```
