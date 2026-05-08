# Start Here - ION Sandbox GPT

This package is for running ION inside a fresh Custom GPT/browser GPT sandbox
with the GPT as the carrier.

Release posture:

```text
custom_gpt_portable_sandbox
non-production
non-live
no secrets authority
no deployment authority
```

## Mount order

1. Confirm this root contains `pyproject.toml` and `ION/REPO_AUTHORITY.md`.
2. Read `ION/REPO_AUTHORITY.md`.
3. Read `ION/02_architecture/ION_MOUNT_CONTRACT.md`.
4. Read `ION/03_registry/gpt_sandbox_carrier_profile.yaml`.
5. Read `ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md`.
6. Read `ION/02_architecture/SINGLE_CARRIER_SEQUENTIAL_RUNTIME_PROTOCOL.md`.
7. Load active ION state under `ION/05_context/current/`, or initialize from `product/starter_data/` when no project state is mounted.
8. Execute ION role phases sequentially in the GPT sandbox unless an external carrier lane is explicitly authorized.
9. Keep Persona Interface as ingress and final user-facing response boundary.
10. Export an updated zip after state-bearing work.

## First user-facing prompt

```text
What are we working on?
```
