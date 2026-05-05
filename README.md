# ION Codex

ION Codex is the public collaboration repository for the current runnable ION
kernel branch, carrier integrations, context artifacts, and proof-gated local
automation work.

This repository is public so outside users and AI collaborators can inspect,
discuss, and contribute. It is not a production deployment surface and it does
not grant authority to publish secrets, credentials, private logs, or unsafe
runtime state.

## Start Here

The authoritative content root is:

```text
ION/
```

The shell root is this repository root. Run commands from here when they rely
on `pyproject.toml`, package discovery, or pytest configuration.

Recommended first reads:

1. `ION/REPO_AUTHORITY.md`
2. `ION/README.md`
3. `ION/02_architecture/ION_MOUNT_CONTRACT.md`
4. `ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md`
5. `ION/docs/README.md`

## Quick Proof Commands

```bash
test -f pyproject.toml && test -f ION/REPO_AUTHORITY.md
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q
```

## Public Collaboration Boundaries

- Do not commit secrets, API keys, tokens, private `.env` files, browser
  profiles, tunnel credentials, or production infrastructure state.
- Do not treat issue comments, GitHub comments, or raw AI output as accepted
  ION state. Durable work should pass through ION packets, receipts, or PRs.
- Do not push directly to `main` for normal work. Use scoped branches such as
  `docs/*`, `work/*`, `agent/*`, or `data-plane/*` and open a pull request.
- Do not claim ION identity, Steward authority, production authority, or live
  external execution authority through this repository.

## Main Directory Map

```text
ION/00_BOOTSTRAP      bootstrap and historical mount surfaces
ION/01_doctrine       doctrine floor and workflow law
ION/02_architecture   protocols and architecture authority
ION/03_registry       carrier, tool, capability, and policy registries
ION/04_agents         role and carrier agent surfaces
ION/04_packages       Python kernel package
ION/05_context        active context, queues, receipts, runtime evidence
ION/06_intelligence   reports, audits, research, orchestration maps
ION/07_templates      packet, receipt, carrier, and action templates
ION/08_ui             UI/cockpit surfaces
ION/09_integrations   MCP, browser extension, daemon, Cursor integrations
ION/docs              setup guides, consolidation reports, public docs
ION/examples          examples and harness inputs
ION/tests             pytest suite
```

## GitHub Data Plane

The canonical public repository is:

```text
https://github.com/ION-operations/ion-codex
```

GitHub is a durable collaboration/data plane. ION remains the authority layer
for packets, context, receipts, proof gates, and carrier boundaries.

See:

- `ION/02_architecture/ION_GITHUB_DATA_PLANE_PROTOCOL.md`
- `ION/02_architecture/ION_GITHUB_WORK_DAEMON_PROTOCOL.md`
- `ION/03_registry/ion_github_data_plane_registry.yaml`

