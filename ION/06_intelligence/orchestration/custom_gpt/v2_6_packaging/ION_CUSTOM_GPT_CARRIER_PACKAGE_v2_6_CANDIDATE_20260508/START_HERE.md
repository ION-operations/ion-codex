# Start Here — ION Full GPT Sandbox Agent Package v1

This package is for running ION inside a fresh GPT sandbox with the GPT as the carrier.

## Mount order

1. Confirm this root contains `pyproject.toml` and `ION/REPO_AUTHORITY.md`.
2. Read `ION/REPO_AUTHORITY.md`.
3. Read `ION/02_architecture/ION_MOUNT_CONTRACT.md`.
4. Read `ION/03_registry/gpt_sandbox_carrier_profile.yaml`.
5. Read `ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md`.
6. Load active ION state under `ION/05_context/current/`, or initialize from `product/starter_data/` when no project state is mounted.
7. Execute ION role phases sequentially in the GPT sandbox unless an external carrier lane is explicitly authorized.
8. Respond to the user through Persona-facing language.
9. Export an updated zip after state-bearing work.

## First user-facing prompt

```text
What are we working on?
```
