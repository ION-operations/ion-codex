# Activation/lifecycle carrier-crossing worked examples

## Purpose
Show the activation/lifecycle candidate operating through concrete carrier variation without losing the boundary between:
- enactment permission,
- executor transition law,
- runtime/service shell behavior,
- and continuation-safe re-entry.

## Common invariant sequence
Across all worked examples, the lawful sequence remains:

1. bounded work candidate exists
2. activation request is presented
3. activation decision is emitted
4. lifecycle claim/readiness/entry follows only if crossing is allowed
5. carrier shell operationalizes invocation and witnesses receipts
6. settlement/return/release records outcome without rewriting prior lawfulness

If a carrier compresses or hides any of these stages, the carrier has not changed the law; it has only obscured it.

---

## Example 1 — Manual operator enactment

### Situation
A human operator asks for immediate execution of a packetized continuity repair task.
The packet exists, continuity context is available, and the task appears urgent.

### Lawful reading
- Operator request is a strong input.
- The request does **not** itself grant enactment permission.
- Activation authority evaluates packet readiness, continuity integrity, side-effect posture, capability fit, and settlement pressure.

### Example flow
1. `ActivationIntent` is formed from the operator request.
2. `ActivationRequest` names the packet, manual carrier, capability needs, and side-effect boundary.
3. Activation authority returns `ALLOW` with a receipt reference.
4. Lifecycle emits `CLAIM` for the manual executor identity.
5. Lifecycle emits `READY` once required packet/context checks are satisfied.
6. Lifecycle emits `ENTER`, and the manual enactment begins.
7. The work later emits `RETURN` rather than disappearing if a pause is required.

### Boundary proved
- operator request is not activation authority
- manual action still owes lifecycle state transitions
- pause/return is not a hidden denial or silent release

---

## Example 2 — Daemon/service enactment

### Situation
A supervised daemon shell is online, a prepared task is queued, and the daemon appears technically ready to run.

### Lawful reading
- Daemon readiness is not enactment permission.
- Queue presence is not enactment permission.
- Activation still decides whether this prepared work may cross now.

### Example flow
1. Scheduler nominates a bounded task for daemon execution.
2. Service shell reports that the daemon carrier is healthy.
3. `ActivationRequest` is created for daemon enactment with the chosen capability posture.
4. Activation authority returns `DEFER` because a side-effect prerequisite is unresolved.
5. No lifecycle `CLAIM` or `ENTER` occurs.
6. After the prerequisite is resolved, a fresh activation request is presented.
7. Activation authority returns `ALLOW`.
8. Lifecycle emits `CLAIM`, `READY`, and `ENTER` for the daemon executor.
9. Service shell witnesses the run; it does not substitute for activation or lifecycle law.

### Boundary proved
- daemon health is not activation authority
- service shell readiness is not lifecycle entry
- deferred activation blocks enactment without requiring fake executor history

---

## Example 3 — External/API enactment

### Situation
A bounded work packet is transport-compatible with an external/API carrier and the endpoint is available.

### Lawful reading
- Transport compatibility is not enactment permission.
- Endpoint availability is not enactment permission.
- The API shell is an invocation carrier and witness surface.

### Example flow
1. A bounded task is prepared for an external/API executor class.
2. `ActivationRequest` names the external carrier, capability requirements, and scope boundary.
3. Activation authority returns `ESCALATE` because carrier equivalence is ambiguous for a sensitive side-effect class.
4. No lifecycle claim occurs yet.
5. Higher review clarifies the eligible carrier class and records the boundary.
6. A revised activation request is submitted.
7. Activation authority returns `ALLOW`.
8. Lifecycle emits `CLAIM`, `READY`, and `ENTER` for the external/API executor identity.
9. API transport emits runtime receipts and final settlement witnesses.

### Boundary proved
- external transport availability is not enactment permission
- carrier ambiguity is resolved in activation, not hidden in lifecycle
- API transport witnesses enactment but does not own activation law

---

## Example 4 — Continuation across carrier change

### Situation
A previously lawful enactment path began in a manual carrier, was `SUSPENDED` or `RETURNED`, and later resumes through a daemon carrier.

### Lawful reading
- Continuation may preserve bounded authority and work identity.
- Carrier change does not itself mint a new activation center.
- Resume is lawful only if preserved authority and continuity integrity remain valid.

### Example flow
1. Manual enactment was previously activated lawfully and entered lifecycle `ACTIVE`.
2. The work is later `SUSPENDED` with continuity-safe state preserved.
3. A daemon carrier becomes available for resumed execution.
4. Continuity/takeover surfaces present preserved work identity and prior activation receipt.
5. Lifecycle checks readiness and continuity integrity for daemon re-entry.
6. If preserved authority remains valid, lifecycle may emit `RESUME` or `ENTER` under the cited prior activation receipt.
7. If preserved authority is stale or prerequisites drifted materially, the repo requests fresh activation instead.
8. The daemon carrier then proceeds only under the lawful path that actually applies.

### Boundary proved
- continuation is not a hidden second activation center
- carrier change does not erase receipt lineage
- fresh activation is required when preserved authority no longer holds

---

## Compressed findings

### 1. Carrier neutrality now has first-form evidence
The review set can now show, not only assert, that the same enactment boundary survives across carrier changes.

### 2. The most failure-prone points are still defer, escalate, and resume paths
Simple `ALLOW -> CLAIM -> READY -> ENTER` flows are relatively stable.
Boundary drift becomes likelier when:
- activation is deferred,
- carrier eligibility is escalated,
- or continuation is used to justify re-entry.

### 3. Runtime/service shells remain witnesses, not the center
The examples strengthen the claim that shells may expose receipts and operational entry points, but they do not own enactment permission or executor transition law.

## Resulting judgment
The activation/lifecycle set is stronger after carrier-crossing demonstration.
The next remaining blockers are:
- explicit receipt/settlement example set
- install-path mapping into active architecture
- thaw-readiness reassessment after those are added
