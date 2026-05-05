# Contributing

This repository is public for collaboration, but ION state is still governed by
packets, receipts, proof gates, and bounded carrier authority.

## Before You Change Files

1. Read `ION/REPO_AUTHORITY.md`.
2. Use a scoped branch:
   - `docs/<short-topic>`
   - `work/<short-topic>`
   - `agent/<short-topic>`
   - `data-plane/<short-topic>`
3. Keep changes narrow and explain the owner surface you reused.
4. Run the smallest meaningful validation for the change.
5. Open a pull request with evidence.

## Pull Request Evidence

Include:

- objective
- touched paths
- validations run
- known blockers or skipped checks
- relevant ION packet, receipt, issue, branch, or artifact references

## What Not To Submit

- secrets, credentials, tokens, private browser profiles, tunnel credentials, or
  `.env` files
- production deployment changes unless explicitly authorized by ION policy and
  Braden
- broad rewrites that bypass existing architecture, registry, packet, or
  receipt owners
- raw AI output as accepted state without proof-gated integration

## Validation Commands

Useful defaults from the shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q
```

