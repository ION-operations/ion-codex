# PCKT-LOCAL-PC-VM-GATEWAY-001 — Codex Work Packet

Status: ready_for_codex_candidate  
Date: 2026-05-08  
Parent route: ION Custom GPT → local PC-as-VM gateway demo  
Authority: candidate implementation packet; no production authority; no live external mutation without local approval

## Objective

Build a local ION Gateway demo on the operator PC. The PC acts as the first VM/sandbox cell. The gateway must support local user login, workspace routing, read-only connection status, dry-run action proposals, bounded Codex work-packet creation, and receipts.

The GPT and extension must never receive raw passwords, API keys, local secrets, SSH keys, or broad filesystem authority.

## Required implementation shape

Create a new local project directory, suggested:

```text
ion-local-gateway/
```

Recommended Python/FastAPI layout:

```text
ion-local-gateway/
  README.md
  pyproject.toml
  .env.example
  openapi/ion_local_gateway_actions.openapi.yaml
  ion_local_gateway/
    __init__.py
    app.py
    config.py
    db.py
    models.py
    security.py
    receipts.py
    codex_bridge.py
    schemas.py
    routers/
      __init__.py
      health.py
      auth.py
      connect.py
      workspaces.py
      tools.py
      actions.py
      codex.py
      exports.py
  tests/
    test_health.py
    test_auth.py
    test_connect.py
    test_actions.py
    test_codex_workpack.py
    test_secret_redaction.py
```

Accept equivalent structure only if simpler and well tested.

## Dependencies

Prefer small, standard dependencies:

```text
fastapi
uvicorn[standard]
pydantic
sqlmodel or sqlalchemy
argon2-cffi or passlib[bcrypt]
python-dotenv
pytest
httpx
pyyaml
```

Do not add heavy auth frameworks unless needed. Do not implement production OAuth in this first packet unless the rest of the MVP is complete.

## Local auth requirements

Implement local user auth for demo use:

- `POST /auth/register-dev-user`
- `POST /auth/login`
- `POST /auth/logout`
- `GET /auth/me`

Rules:

- Do not log plaintext passwords.
- Do not return password hashes.
- Store only password hash.
- Use Argon2id preferred; bcrypt acceptable.
- Use secure random session tokens or signed cookies.
- Bind default server to `127.0.0.1`.
- Provide `.env.example`; do not create real `.env` with secrets.

For first demo, it is acceptable to use local session token auth for browser/extension testing and a separate dev API key for Custom GPT Action-over-tunnel testing. Make clear in README that production must use OAuth/OIDC.

## Connection/session requirements

Implement:

- `POST /v1/connect/start`
- `GET /v1/connect/status`

`connect/start` creates or returns a short-lived `connection_ref` for the authenticated user/workspace. The response may include:

```json
{
  "connection_ref": "conn_...",
  "workspace_ref": "ws_...",
  "mount_status": "READY_READ_ONLY",
  "state_root_hash": "sha256:...",
  "allowed_modes": ["READ_ONLY", "DRY_RUN"],
  "forbidden_modes": ["BROAD_SHELL", "PRODUCTION_DEPLOY", "PUSH_MAIN"],
  "next_recommended_action": "list_tools"
}
```

`connection_ref` is not a secret and must not authorize by itself. Server must verify user/session/dev action key and workspace access.

## Workspace requirements

Implement:

- local SQLite DB;
- default workspace creation on first user registration;
- `GET /v1/workspaces`;
- per-workspace root path inside a safe configured base directory such as `./workspace_data/`.

Do not allow arbitrary root paths from API input in MVP.

## Tools/status requirements

Implement:

- `GET /v1/tools`

Return a small tool list:

```text
workspace_status
create_codex_work_packet
export_context_preview
read_receipt
```

Mark tools with mode:

```text
READ_ONLY
DRY_RUN
APPROVAL_REQUIRED
BLOCKED
```

## Action proposal requirements

Implement:

- `POST /v1/actions/propose`

Accept an intent such as:

```text
create_codex_work_packet
write_file_draft
export_context_preview
```

Rules:

- require `connection_ref`;
- require `workspace_ref`;
- require `idempotency_key`;
- reject duplicate idempotency key with prior result;
- never execute broad shell;
- write an `action_proposal` record;
- return `APPROVAL_REQUIRED` for mutating actions unless local approval flag is present;
- always create a receipt draft or proposal receipt.

## Codex work-packet requirements

Implement:

- `POST /v1/codex/workpack`

This endpoint should create a bounded Markdown work packet in:

```text
workspace_data/<workspace_ref>/codex_work_packets/
```

Packet content must include:

```text
packet_id
objective
allowed_roots
forbidden_paths
files_to_create_or_modify
commands_allowed
commands_forbidden
proof_required
return_contract
receipt_required
```

Forbidden by default:

```text
delete outside workspace
read browser cookies
read SSH keys
read credential stores
write production config
git push
production deploy
broad shell
```

Return:

```json
{
  "result_class": "DRY_RUN",
  "receipt_id": "rcpt_...",
  "packet_path": "...",
  "warnings": []
}
```

## Receipt requirements

Every endpoint that changes gateway state must create a receipt with:

```text
receipt_id
created_at
user_id
workspace_ref
action_id or connection_ref
status
files_touched
validation
warnings
redactions
```

Implement:

- `GET /v1/receipts/{receipt_id}`

## OpenAPI requirements

Generate or write:

```text
openapi/ion_local_gateway_actions.openapi.yaml
```

It should expose only `/health` and `/v1/*` endpoints intended for Custom GPT Actions. Do not expose `/auth/login` as a GPT action for password submission.

For local tunnel testing, support an API key header:

```text
X-ION-Gateway-Key
```

Mark this as dev-only. Production route must be OAuth/OIDC.

## Tests

Minimum pytest coverage:

1. health returns ok;
2. dev user registration stores hash, not password;
3. login works and does not leak password/hash;
4. connect/start returns connection_ref and allowed/forbidden modes;
5. connection_ref alone cannot access a workspace without valid server-side auth;
6. duplicate idempotency key returns prior result or conflict;
7. codex workpack is written inside workspace only;
8. secret-like strings are redacted from receipts;
9. broad shell / production deploy / push_main are rejected;
10. OpenAPI YAML parses.

## README requirements

README must include:

- local install commands;
- `.env.example` setup;
- start command;
- local-only extension route;
- tunnel route warning;
- Custom GPT Actions schema location;
- security non-claims;
- how to run tests;
- how to inspect receipts;
- how to manually feed generated packets to Codex CLI.

## Validation commands

Use commands equivalent to:

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell equivalent is acceptable
pip install -e ".[dev]"
pytest
uvicorn ion_local_gateway.app:app --host 127.0.0.1 --port 8765
```

Adjust Windows commands in README for the operator PC.

## Return contract

Return a Complete Change Package with:

- files created/modified;
- how to run locally;
- how to test;
- OpenAPI schema path;
- sample action call;
- sample extension YAML;
- receipts produced during tests;
- security non-claims;
- blockers;
- next packet.

## Non-claims

Do not claim production OAuth, hosted VM, hosted MCP, GitHub mutation, external deployment, or live Codex execution unless actually implemented and tested.
