# ION Python Packages

This directory contains the Python package source for the ION kernel.

Package discovery is configured in the repository-root `pyproject.toml`:

```text
where = ["ION/04_packages"]
include = ["kernel*"]
```

## Main Package

```text
kernel/
```

The kernel package contains status tools, carrier audits, packet processing,
ChatOps bridge support, GitHub data-plane audits, MCP previews, and other local
runtime helpers.

## Common Commands

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_github_data_plane_audit --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q
```

## Rule

Kernel modules may emit receipts, packets, or projections. Raw tool output is
not accepted ION state unless an owning packet, receipt, or integration path
records it.

