# ION V95 — Compiled Role Context Bundle Invariant Report

V95 repairs the ambiguity where Cursor could infer that physical compiled one-file context bundles existed only for a subset of roles.

`kernel.ion_cycle_runner` now materializes `NN_COMPILED_<ROLE>_CONTEXT_BUNDLE.md` for every `spawn=true` row and records it as `compiled_context_bundle_path` in the active spawn plan. The compiled bundle embeds the executable context package, Agent Context System authority section, and `### CONTEXT PROOF` contract.

Added audit: `kernel.ion_compiled_role_context_bundle_audit`.

Validation performed:

```text
py_compile: ion_cycle_runner.py passed
py_compile: ion_carrier_workflow_audit.py passed
py_compile: ion_compiled_role_context_bundle_audit.py passed
ion_carrier_continue: ION_CARRIER_CONTINUE_READY
ion_compiled_role_context_bundle_audit: ION_COMPILED_ROLE_CONTEXT_BUNDLE_READY
ion_carrier_workflow_audit: ION_CARRIER_WORKFLOW_READY
zip integrity: passed
```
