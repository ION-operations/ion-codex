# ION Compiled Role Context Bundle Invariant Protocol — V95

Every `spawn=true` row in `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json` must include `context_package_path`, `compiled_context_bundle_path`, and `context_load_receipt_path`.

The `compiled_context_bundle_path` must point to a physical file named `NN_COMPILED_<ROLE>_CONTEXT_BUNDLE.md`. It is a law-complete alias of the executable context package, not an optional Steward/Relay-only surface.

If a role is present with `spawn=false`, no bundle is required for that inactive row. If that role becomes spawned, the bundle must materialize.

Forbidden fallback: carriers and subagents must not fall back to boot/MINI/CAPSULE/session-only onboarding when a compiled bundle is missing. Regenerate with the V95 kernel or stop with a missing-bundle finding.

Audit:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_compiled_role_context_bundle_audit --ion-root . --json
```
