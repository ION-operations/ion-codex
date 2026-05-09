# PCKT-LOCAL-PC-VM-GATEWAY-003 — User Routing/Auth Demo

**Status:** CANDIDATE CODEX WORK PACKET  
**Date:** 2026-05-08  
**Authority:** local demo only; no production authority  
**Objective:** Build the next local ION Gateway demo layer: multi-user routing, extension-mediated sign-in/sign-up, guest mode, single Action router, workspace isolation, and Codex work-packet handoff.

---

## 1. Inputs to read first

Read these candidate surfaces if present:

```text
ION_Custom_GPT_Instructions_v2_5_USER_ROUTING_AUTH_PASTE_CANDIDATE.md
ION_User_Routing_Auth_Model_v0_1_CANDIDATE.md
ION_Extension_Mediated_Auth_Flow_v0_1_CANDIDATE.md
ION_Local_PC_VM_Gateway_Demo_Architecture_v0_1_CANDIDATE.md
ION_Local_PC_VM_Gateway_OpenAPI_v0_1_CANDIDATE.yaml
PCKT-LOCAL-PC-VM-GATEWAY-002_EXTENSION_AUTH_STARTERS_CODEX_WORKPACK.md
```

If repo package law exists, mount it before changing files.

---

## 2. Build target

Create or update a local demo stack:

```text
local_gateway/
  app server
  SQLite database
  auth/session module
  workspace router
  action router
  receipt writer
  Codex work-packet writer

extension/
  sign-in panel
  sign-up panel
  guest-mode panel
  workspace selector
  ion_reentry injector
```

Use the existing repo stack if one exists. If no stack exists, prefer a simple Python FastAPI + SQLite prototype for the gateway and minimal extension JS/HTML changes.

---

## 3. Required rules

Do not ask the GPT/user to paste passwords into chat.

Do not expose password login/register endpoints in the Custom GPT Action OpenAPI schema.

Passwords, if used in local demo, must be entered only through extension/local gateway UI and stored hashed.

Use non-secret handles in GPT-facing responses:

```text
connection_ref
workspace_ref
state_root_hash
action_id
receipt_id
allowed_modes
forbidden_modes
```

Every GPT-facing request must be routed through server-side connection/workspace checks.

---

## 4. Minimum gateway endpoints

### GPT/Action-safe endpoints

```text
GET  /health
POST /v1/connect/start
GET  /v1/connect/status
GET  /v1/workspaces
GET  /v1/tools
POST /v1/actions/route
POST /v1/codex/workpack
GET  /v1/receipts/{receipt_id}
```

### Extension/local-only endpoints

```text
POST /local/auth/signup
POST /local/auth/signin
POST /local/auth/signout
POST /local/auth/guest
POST /local/connect/bind
GET  /local/session/status
```

Bind local-only endpoints to localhost and do not include them in the GPT Action schema.

---

## 5. Database tables

Implement minimum tables:

```text
users(user_id, handle, password_hash, created_at)
devices(device_id, user_id, extension_install_ref, last_seen_at)
workspaces(workspace_id, user_id, display_name, root_path, state_root_hash, mode)
connections(connection_ref, user_id, workspace_id, device_id, scopes, status, expires_at)
action_requests(action_id, connection_ref, workspace_id, action_type, payload_hash, status, receipt_id)
receipts(receipt_id, user_id, workspace_id, action_id, result_json, proof_json, created_at)
```

Use opaque IDs. Do not use raw emails/names in filesystem paths.

---

## 6. Routing behavior

For `/v1/actions/route`:

```text
1. require connection_ref
2. load connection
3. reject if missing/expired/unbound
4. verify workspace_ref matches connection
5. verify action_type is allowed by scope/mode
6. create action_request
7. if requires approval, return approval_pending
8. if dry-run allowed, perform dry-run route
9. write receipt
10. return sanitized result
```

For `/v1/codex/workpack`:

```text
1. require signed-in workspace
2. write bounded packet into workspace inbox
3. do not execute Codex automatically unless an explicit demo flag/approval is enabled
4. write receipt
5. return packet path relative to workspace and receipt_id
```

---

## 7. Extension behavior

Add front-door UI:

```text
/sign-in  -> open sign-in panel
/sign-up  -> open sign-up panel
/guest-mode -> create/use guest workspace
```

After successful auth/bind, inject a proof block into chat or make it available for the GPT Action status call:

```yaml
ion_reentry:
  schema: ion.reentry.v1
  source: ion_extension
  mount_status: CLEAN
  connection_ref: conn_...
  workspace_ref: wsp_...
  state_root_hash: sha256:...
  allowed_modes:
    - READ_ONLY
    - DRY_RUN
    - CREATE_CODEX_WORK_PACKET_DRAFT
  forbidden_modes:
    - SECRET_REQUEST
    - BROAD_SHELL
    - PRODUCTION_DEPLOY
  receipt_id: rcp_...
```

No tokens or passwords in `ion_reentry`.

---

## 8. Package outputs

Create bounded demo packages, not full ION export:

```text
dist/ion-extension-demo.zip
dist/ion-edge-node-demo.zip
dist/ion-local-gateway-openapi.yaml
dist/ion-local-demo-context-package.zip
```

The ZIPs should contain only the scoped product/demo surfaces required to install/test the extension and local gateway.

---

## 9. Validation

Produce proof artifacts:

```text
validation/user_routing_auth_demo_report.md
validation/user_routing_auth_demo_results.json
receipts/LOCAL_PC_VM_GATEWAY_003_RECEIPT_DRAFT.md
```

Test cases:

```text
1. /guest-mode creates guest workspace without password.
2. /sign-up creates user through extension/local UI only.
3. Password never appears in GPT Action schema or GPT-facing logs.
4. GPT-facing route without connection_ref is rejected.
5. Expired/unbound connection_ref is rejected.
6. Valid connection_ref routes to correct workspace only.
7. User A cannot access User B workspace_ref.
8. Codex work packet is written but not auto-executed without approval.
9. Receipt is created for every state-changing action.
10. ion_reentry contains no secrets.
```

---

## 10. Return contract

Return a Complete Change Package including:

```text
files changed/created
how to run local gateway
how to load extension demo
OpenAPI schema path
validation results
receipts
known failures
next packet
```

Do not claim production readiness.
