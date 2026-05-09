# PCKT-GATEWAY-EXTENSION-COSIGN-004 — Two-Channel Extension-Co-Signed Gateway

**Status:** CANDIDATE CODEX WORK PACKET  
**Date:** 2026-05-08  
**Authority:** local demo only; no production authority  
**Objective:** Build the two-channel request/approval protocol so one ION Custom GPT Action surface can serve multiple users while private data is released only when the signed-in browser extension co-approves the exact gateway request.

---

## 0. Executive target

Create a local PC-as-VM ION Gateway demo where this works:

```text
User asks ION GPT: "Load my current project state."

GPT Action:
  creates request_id at gateway

Extension:
  sees pending request for the signed-in user/session
  shows approval panel
  signs challenge for that exact request

Gateway:
  verifies GPT channel + extension channel + ACL + scope
  releases sanitized project state
  writes receipt
```

And this fails:

```text
Attacker opens same public GPT
types same user handle or stolen connection_ref
asks for private data
does not have the signed-in extension/device/chat pairing
gateway releases nothing
```

---

## 1. Required reads

Read first if present:

```text
ION_Two_Channel_Extension_Cosigned_Gateway_Architecture_v0_1_CANDIDATE.md
ION_User_Routing_Auth_Model_v0_1_CANDIDATE.md
ION_Extension_Mediated_Auth_Flow_v0_1_CANDIDATE.md
ION_Local_PC_VM_Gateway_Demo_Architecture_v0_1_CANDIDATE.md
PCKT-LOCAL-PC-VM-GATEWAY-003_USER_ROUTING_AUTH_CODEX_WORKPACK.md
ION_Custom_GPT_Instructions_v2_5_USER_ROUTING_AUTH_PASTE_CANDIDATE.md
```

If the repo contains ION authority/mount files, mount them before edits:

```text
README.md
START_HERE.md
ION/REPO_AUTHORITY.md
ION/02_architecture/ION_MOUNT_CONTRACT.md
ION/02_architecture/ION_GPT_SANDBOX_ENVIRONMENT_CONTRACT.md
ION/03_registry/gpt_sandbox_carrier_profile.yaml
ION/05_context/current/ACTIVE_GPT_SANDBOX_PREFLIGHT.json
VALIDATION_REPORT.json
```

---

## 2. Build target

Prefer the existing repo stack if present. If no gateway exists, create a minimal prototype:

```text
local_gateway/
  app.py or main.py
  db.py
  models.py
  auth.py
  crypto.py
  pairings.py
  requests.py
  receipts.py
  codex_packets.py
  tests/

extension/
  manifest.json
  background.js
  content_script.js
  popup.html
  popup.js
  approval_panel.html
  approval_panel.js
  crypto.js
```

Recommended prototype stack:

```text
Python 3.11+
FastAPI
SQLite
Pydantic
pytest
argon2-cffi or passlib[argon2] if available
cryptography for server-side signature verification if needed
```

For browser device signatures, prefer WebCrypto ECDSA P-256. If WebCrypto persistence is delayed, stub device signing behind a clear `DEV_INSECURE_DEVICE_KEY` flag and mark it non-production.

---

## 3. Hard boundaries

Do not ask for or store passwords in GPT chat.

Do not expose these through GPT Actions:

```text
password
OAuth token
refresh token
session cookie
API key
device private key
extension private key
SSH key
```

Do not create arbitrary shell execution.

Do not auto-run Codex CLI in this packet.

Do not write outside the configured workspace root.

Do not treat `connection_ref`, `workspace_ref`, `user_handle`, or `request_id` as authority.

Do not release private data unless the request is approved by the extension channel or explicitly classified guest/public.

---

## 4. Database schema

Create migrations or initialization for these tables.

### users

```sql
id TEXT PRIMARY KEY,
handle TEXT UNIQUE NOT NULL,
password_hash TEXT,
status TEXT NOT NULL,
created_at TEXT NOT NULL
```

### devices

```sql
id TEXT PRIMARY KEY,
user_id TEXT NOT NULL,
public_jwk TEXT NOT NULL,
label TEXT,
status TEXT NOT NULL,
created_at TEXT NOT NULL
```

### workspaces

```sql
id TEXT PRIMARY KEY,
user_id TEXT NOT NULL,
label TEXT NOT NULL,
root_path TEXT,
root_kind TEXT NOT NULL,
state_root_hash TEXT,
status TEXT NOT NULL,
created_at TEXT NOT NULL
```

### connections

```sql
id TEXT PRIMARY KEY,
user_id TEXT NOT NULL,
workspace_id TEXT NOT NULL,
device_id TEXT,
chat_pairing_ref TEXT NOT NULL,
scopes_json TEXT NOT NULL,
status TEXT NOT NULL,
expires_at TEXT NOT NULL,
created_at TEXT NOT NULL
```

### requests

```sql
id TEXT PRIMARY KEY,
connection_id TEXT NOT NULL,
requested_scope TEXT NOT NULL,
resource TEXT NOT NULL,
reason TEXT,
canonical_request_hash TEXT NOT NULL,
challenge_nonce TEXT NOT NULL,
status TEXT NOT NULL,
expires_at TEXT NOT NULL,
created_at TEXT NOT NULL,
released_at TEXT
```

### approvals

```sql
id TEXT PRIMARY KEY,
request_id TEXT NOT NULL,
user_id TEXT NOT NULL,
device_id TEXT NOT NULL,
decision TEXT NOT NULL,
signature TEXT,
signature_alg TEXT,
approved_scopes_json TEXT,
created_at TEXT NOT NULL
```

### receipts

```sql
id TEXT PRIMARY KEY,
request_id TEXT,
connection_id TEXT,
workspace_id TEXT,
receipt_type TEXT NOT NULL,
result TEXT NOT NULL,
proof_json TEXT NOT NULL,
created_at TEXT NOT NULL
```

---

## 5. API contract

Implement two route groups.

## 5.1 GPT Action API

These are safe to expose in the Custom GPT OpenAPI schema.

### GET /health

Return service health.

### POST /v1/pairings/start

Input:

```json
{
  "intent": "sign_in|sign_up|guest_mode",
  "conversation_hint": "optional",
  "requested_scopes": ["workspace.read", "action.propose"]
}
```

Return:

```json
{
  "pairing_ref": "pair_...",
  "status": "PENDING_EXTENSION",
  "expires_at": "...",
  "instructions": "Open the ION extension to complete sign-in."
}
```

### GET /v1/connections/{connection_ref}/status

Return mount status, scopes, expiry, workspace label, and no secrets.

### POST /v1/requests

Input:

```json
{
  "connection_ref": "conn_...",
  "requested_scope": "workspace.state.read",
  "resource": "state/current",
  "reason": "Load current project state for resume.",
  "action_id": "act_..."
}
```

Return pending request:

```json
{
  "request_id": "req_...",
  "status": "PENDING_EXTENSION_APPROVAL",
  "expires_at": "...",
  "approval_required": true
}
```

### GET /v1/requests/{request_id}/status

Return pending/approved/released/denied/expired.

### GET /v1/requests/{request_id}/result

Return result only if gateway verification passed and the request is released. Otherwise return a structured pending/denied response.

### GET /v1/receipts/{receipt_id}

Return sanitized receipt.

## 5.2 Extension/Gateway API

These are not GPT Actions.

### POST /v1/auth/signup

User enters handle/password outside chat. Hash password server-side.

### POST /v1/auth/signin

User signs in outside chat.

### POST /v1/devices/register

Register extension public key.

### GET /v1/extension/pending?connection_ref=...

Return pending requests available to this signed-in user/session.

### POST /v1/extension/requests/{request_id}/approve

Input:

```json
{
  "device_id": "dev_...",
  "decision": "APPROVED",
  "signature_alg": "ES256",
  "signature": "base64url...",
  "signed_payload": {
    "request_id": "req_...",
    "connection_ref": "conn_...",
    "challenge_nonce": "nonce_...",
    "canonical_request_hash": "sha256:...",
    "decision": "APPROVED",
    "approved_scopes": ["workspace.state.read"],
    "iat": "..."
  }
}
```

### POST /v1/extension/requests/{request_id}/deny

Deny request and write receipt.

---

## 6. Canonical signature payload

Create a stable canonical JSON payload for approvals.

Minimum fields:

```json
{
  "schema": "ion.extension.approval.v1",
  "request_id": "req_...",
  "connection_ref": "conn_...",
  "chat_pairing_ref": "chat_...",
  "challenge_nonce": "nonce_...",
  "canonical_request_hash": "sha256:...",
  "decision": "APPROVED",
  "approved_scopes": ["workspace.state.read"],
  "iat": "2026-05-08T00:00:00Z",
  "exp": "2026-05-08T00:05:00Z"
}
```

Rules:

```text
sort keys before hashing/signing
reject missing fields
reject expired payload
reject unknown connection_ref/request_id pair
reject mismatched chat_pairing_ref
reject replayed signature/request
reject approved scopes that exceed requested scope
```

---

## 7. Extension behavior

Implement minimal extension behavior:

```text
1. Popup has /sign-in, /sign-up, /guest-mode controls.
2. Extension authenticates with local gateway.
3. Extension registers device public key.
4. Extension can receive or poll pending requests.
5. Extension displays exact request details.
6. User approves or denies.
7. Extension signs approval challenge.
8. Extension injects ion_reentry proof into ChatGPT after sign-in.
```

`ion_reentry` proof shape:

```yaml
ion_reentry:
  schema: ion.reentry.proof.v1
  user_handle: braden
  connection_ref: conn_...
  workspace_ref: wrk_...
  state_root_hash: sha256:...
  scopes:
    - workspace.state.read
    - action.propose
    - codex.workpacket.write
  expires_at: "..."
  receipt_id: rcp_...
  verified_by: ion_extension_local_gateway
```

For MVP, the extension may inject into the chat input and let the user press send. Avoid silent auto-send unless the user explicitly enables it.

---

## 8. Gateway behavior

### Request creation

When GPT calls `/v1/requests`:

```text
authenticate GPT Action/dev key
lookup connection_ref
check connection status and expiry
check requested_scope is within connection scopes
create request_id + nonce
compute canonical_request_hash
set status=PENDING_EXTENSION_APPROVAL
return request_id
```

### Extension approval

When extension approves:

```text
authenticate extension user/session
lookup request
lookup connection
check user_id matches
check device is active and belongs to user
verify signature over canonical payload
check nonce/expiry/one-time status
check scope
set request status=APPROVED
```

### Release

When GPT fetches result:

```text
if request APPROVED:
  perform data fetch/proposal/write
  sanitize output
  set RELEASED
  write receipt
  return result + receipt_id
else:
  return pending/denied/expired status
```

---

## 9. Workspace data for demo

Create two demo users and workspaces in test fixtures:

```text
user_a / workspace_a
user_b / workspace_b
```

Each workspace should have a different fake current state:

```json
{
  "project": "A private project",
  "owner": "user_a",
  "state_root_hash": "sha256:..."
}
```

Use this for isolation tests.

---

## 10. Codex packet writer

Implement a dry-run/approved packet writer.

Input scope:

```text
codex.workpacket.write
```

Allowed path:

```text
<workspace_root>/ION/05_context/inbox/codex_work_packets/
```

Rules:

```text
normalize path
reject ../ traversal
write markdown only
write receipt with file hash
do not execute codex
```

---

## 11. Tests required

### Unit tests

```text
test_user_handle_not_authority
test_connection_ref_without_extension_approval_no_release
test_wrong_user_cannot_approve_request
test_wrong_device_cannot_approve_request
test_revoked_device_cannot_approve_request
test_expired_request_cannot_release
test_replayed_signature_rejected
test_scope_escalation_rejected
test_path_traversal_rejected
test_guest_cannot_read_private_workspace
```

### Integration tests

```text
test_user_a_happy_path_state_read
test_user_b_cannot_read_user_a_state
test_stolen_connection_ref_pending_but_never_released
test_extension_denial_writes_receipt
test_codex_workpacket_write_after_approval
test_codex_workpacket_no_auto_execute
```

### Manual E2E test

```text
1. Start local gateway.
2. Load extension unpacked.
3. Use /sign-up in GPT.
4. Extension signs up and injects ion_reentry.
5. Ask GPT to load current project state.
6. Gateway returns PENDING_EXTENSION_APPROVAL.
7. Extension approval panel appears.
8. Approve.
9. GPT polls/fetches result.
10. Receipt appears.
```

---

## 12. Deliverables

Return a Complete Change Package containing:

```text
files changed/created
setup commands
run commands
test commands/results
API endpoints added
database schema
extension files changed
security downgrades, if any
known limitations
receipt draft
next packet
```

If implementation cannot be completed, return the strongest partial package and blocker.

---

## 13. Validation commands

Suggested:

```bash
python -m pytest local_gateway/tests -q
python -m compileall local_gateway
python local_gateway/main.py --check-config
```

If using Node for extension tests:

```bash
npm test
npm run lint
```

---

## 14. Expected receipt draft

```json
{
  "receipt_id": "rcp_gateway_extension_cosign_004",
  "packet_id": "PCKT-GATEWAY-EXTENSION-COSIGN-004",
  "result": "IMPLEMENTED|PARTIAL|BLOCKED",
  "proof": {
    "tests": [],
    "manual_e2e": "not_run|passed|failed",
    "security_boundaries": {
      "passwords_in_chat": "blocked",
      "private_data_without_extension": "blocked",
      "cross_user_read": "blocked"
    }
  },
  "non_claims": [
    "No production hardening claimed.",
    "No hosted VM isolation claimed unless implemented separately.",
    "No Codex auto-execution claimed."
  ]
}
```

---

## 15. Next packet after success

```text
PCKT-GATEWAY-EXTENSION-COSIGN-005

Objective:
Add hosted/VM routing and local-edge outbound relay so the same co-signed request protocol can target per-user hosted containers or user-local PCs without exposing local ports publicly.
```
