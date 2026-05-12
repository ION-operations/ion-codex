# ION Multi-Agent Context and Workpacket Settlement Protocol v0.1

Status: active provisional protocol
Created: 2026-05-11
Authority: governance and settlement workflow only
Production authority: false
Live execution authority: false

## Purpose

This protocol prevents parallel Codex/ION agents from corrupting shared context while preserving parallel work.

The triggering incident was a checkpoint collision: one agent wrote a UI recovery `C-088` entry while another active lane already had `C-088` for bounded queue timeout policy. The failure was not the number itself. The failure was that multiple agents could write settled context directly.

## Core law

Parallel agents may produce candidate receipts, workpackets, diffs, claims, and task returns.

Only the context settler may mutate shared settled context surfaces:

```text
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/STATUS.json
ION/05_context/current/codex_solo/ROUTE.json
checkpoint indexes / C-number assignment
```

## Source law integrated

This protocol inherits the workpacket and diff ingestion doctrine from:

```text
ION_CODEX FULL/workpackets/ion_workpackets_diffs_ingestion_002_20260510T234208.zip
```

Important inherited definitions:

```text
workpacket = intent / bounded work proposal / role route
diff = proposed state delta / patch or context-package evidence
receipt = what actually landed, was rejected, or remains deferred
```

Candidate material is not current law until settlement explicitly promotes it.

## Directory model

```text
ION/05_context/current/context_settlement/
  README.md
  CONTEXT_SETTLEMENT_REGISTRY_V0_1.json
  claims/
  inbox/
  accepted/
  conflicts/
```

Use `inbox/` for candidate settlement packets.
Use `accepted/` only for settler-approved outputs.
Use `conflicts/` for checkpoint collisions, file-scope collisions, route collisions, and authority conflicts.
Use `claims/` for active write-scope declarations.

## Roles

### Worker agent

May:

```text
read context
edit explicitly scoped implementation files
write candidate receipts
write task returns
write settlement inbox packets
write claims
```

Must not:

```text
assign C-numbers
edit Capsule/Mini/HOT_CONTEXT directly
claim accepted state
promote workpackets or diffs
apply candidate diffs without settlement
hide non-claims
```

### Context settler

May:

```text
read candidate receipts/workpackets/diffs
detect conflicts
assign C-numbers
update Capsule/Mini/HOT_CONTEXT/STATUS/ROUTE
move inbox packets to accepted or conflicts
write settlement receipts
```

Must preserve:

```text
source evidence
conflict record
non-claims
authority boundaries
human/steward gates
```

### Human/steward gate

Required when a candidate touches:

```text
production or live connector surfaces
secret or auth surfaces
code or state patches
connector schema or config
instruction/router law
governance protocols
shared context indexes
JOC/UI accepted state
```

## Claim protocol

Before material writes, an agent should write a claim packet:

```json
{
  "schema_id": "ion.context_settlement.claim.v1",
  "claim_id": "claim_YYYYMMDDTHHMMSSZ_short_scope",
  "agent_id": "agent_or_lane_name",
  "purpose": "short purpose",
  "write_scope": ["repo/relative/path"],
  "shared_context_write": false,
  "requested_settlement": true,
  "ttl_minutes": 45,
  "authority": {
    "production_authority": false,
    "live_execution_authority": false,
    "secrets_authority": false
  }
}
```

Claims do not grant authority. They expose collision risk.

## Settlement packet minimum shape

```json
{
  "schema_id": "ion.context_settlement.inbox_packet.v1",
  "packet_id": "SETTLE_...",
  "status": "CANDIDATE_PENDING_SETTLEMENT",
  "source_type": "receipt|workpacket|diff|context_package|conflict",
  "source_refs": [],
  "domain": "ui_joc_opus",
  "risk_class": "context_package_bundle_candidate",
  "requested_outcome": "DEFERRED|MERGE_PROPOSAL_REQUIRED|ACCEPTED_AS_WITNESS|ACCEPTED_AS_CURRENT",
  "checkpoint_request": {
    "assign_c_number": true,
    "agent_assigned_c_number": null
  },
  "non_claims": [],
  "authority": {
    "production_authority": false,
    "live_execution_authority": false,
    "secrets_authority": false
  }
}
```

## Checkpoint assignment law

Agents must not assign `C-###`.

Receipts and workpackets use stable timestamped IDs. The context settler later assigns a display checkpoint.

Correct flow:

```text
candidate receipt
-> settlement inbox
-> conflict scan
-> settler assigns C-number
-> Capsule/Mini/HOT_CONTEXT generated or patched by settler only
```

If an agent accidentally writes a C-number directly, the settler must:

```text
record conflict
preserve evidence
decide whether to renumber, merge, or abandon
avoid overwriting another agent's settled entry
```

## Workpacket/diff ingestion integration

The workpacket ingestion packet defines read-only content proof before settlement.

Accepted batch map:

```text
B00 root and folder proof
B01 indexes and front doors
B02 patch/diff affected-path review
B03 Custom GPT and instruction surfaces
B04 Action gateway / MCP / connector surfaces
B05 Extension / DOM / cockpit surfaces
B06 UI / JOC / OPUS context packages
B07 self-knowledge and doctrine witnesses
B08 Codex CLI / IDE / local worker surfaces
B09 lineage, dAimon, and unclassified candidates
```

This protocol adds:

```text
C00 active-agent claim and write-scope conflict review
C01 checkpoint assignment and shared-context settlement
C02 generated Capsule/Mini/HOT_CONTEXT update
```

## UI/JOC special gate

JOC, Helixion, dAimon, Codex Chat, extension UI, drawer, rail, inspector, bottom timeline, and monolith recovery work must route through:

```text
ui-frontend-excellence
JOC_UI_CANON_STEWARD
FRONTEND_WORK_SURFACE_ARCHITECT
INTERACTION_STATE_WEAVER
CONTEXT_VISUALIZATION_CARTOGRAPHER when context/proof UI is involved
COMPONENT_BUILDER
VISUAL_PROOF_AUDITOR
```

UI receipts remain candidate until visual proof is run or explicitly marked unrun. Failed prototype inventory remains candidate evidence, not accepted product UI.

## Conflict classes

```text
checkpoint_collision
shared_context_direct_write
implementation_file_overlap
route_or_registry_overlap
authority_boundary_conflict
candidate_currentness_conflict
diff_apply_risk
visual_proof_missing
receipt_missing
```

## Settlement outcomes

```text
ACCEPTED_AS_CURRENT
ACCEPTED_AS_WITNESS
MERGE_PROPOSAL_REQUIRED
ESCALATE_REVIEW
DEFERRED
ABANDONED
CONFLICT_RECORDED
```

## Hard non-claims

This protocol does not:

```text
accept any current candidate receipt
apply any diff
run the local content-proof scanner
restart services
claim visual proof
grant production authority
grant live browser authority
grant secrets authority
```

## Immediate recovery rule

The `C-088` UI recovery collision must be settled by conflict receipt, not by silently overwriting context.

The UI recovery evidence should enter `context_settlement/inbox/` with `agent_assigned_c_number` recorded as the collision source. The existing queue-timeout `C-088` must not be overwritten.
