# Lane C runtime/session surface-design outlines

These outlines are **proposal-space only**.
They are candidate shapes for future current-line protocol drafting after review.

## 1. `RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`

### Proposed purpose
State what a runtime session is, how it persists, what lifecycle postures it may occupy, and how it relates to kernel truth, continuation, and carrier-specific service shells.

### Proposed sections
1. Purpose
2. Session law
3. Canonical objects
4. Session identity and scope
5. Persistence boundary
6. Session posture classes
7. Relation to route-state and automation-state witnesses
8. Relation to continuation / takeover / handoff
9. Carrier and service-shell bindings
10. Non-goals

### Candidate posture classes
- `DECLARED`
- `READY`
- `ACTIVE`
- `BLOCKED`
- `SUSPENDED`
- `SETTLING`
- `CLOSED`

### Candidate core law
- A runtime session is a bounded executable context, not a claim of unattended autonomy.
- Session identity must remain distinct from carrier-specific process identity.
- Session truth belongs to the kernel substrate; service shells may witness or request it, not redefine it.
- Continuation and handoff may resume or rebind a session only through lawful entry surfaces.

## 2. `SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`

### Proposed purpose
State how session-local work enters queue state, becomes runnable, is dispatched, returns, retries, blocks, settles, or is cancelled.

### Proposed sections
1. Purpose
2. Queue law
3. Canonical objects
4. Queue admission classes
5. Runnable / blocked classification
6. Dispatch attempt lifecycle
7. Return and settlement semantics
8. Retry, stale, and cancellation rules
9. Relation to scheduler and execution receipts
10. Non-goals

### Candidate queue states
- `QUEUED`
- `RUNNABLE`
- `BLOCKED`
- `DISPATCHED`
- `RETURNED`
- `SETTLED`
- `CANCELLED`

### Candidate core law
- Session queues are local to a runtime session, not a replacement for project-wide schedule law.
- Scheduler selection may propose dispatch pressure, but queue settlement must remain session-aware.
- Every dispatch attempt must produce a receipt or explicit block state.
- Queue transitions must not silently mutate session identity or kernel truth.

## 3. `API_RUNTIME_ENTRY_PROTOCOL.md`

### Proposed purpose
State how external/API clients lawfully request runtime-session creation, inspection, enqueue, drive, or cancellation without collapsing the kernel into a transport facade.

### Proposed sections
1. Purpose
2. Entry law
3. Canonical request / response objects
4. Request classes
5. Validation and control gates
6. Service-shell translation rules
7. Receipt and visibility requirements
8. Failure / denial classes
9. Relation to supervised daemon and external execution bridges
10. Non-goals

### Candidate request classes
- `CREATE_SESSION`
- `INSPECT_SESSION`
- `ENQUEUE_WORK`
- `DRIVE_QUEUE`
- `CANCEL_WORK`
- `CLOSE_SESSION`

### Candidate denial classes
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`
- `INVALID_BINDING`
- `SESSION_NOT_FOUND`
- `APPROVAL_REQUIRED`

### Candidate core law
- API entry is a request surface, not a source of kernel truth.
- Every approved request must resolve to a bounded session action or an explicit denial receipt.
- Transport-level convenience must not bypass operator control, automation policy, or capability boundaries.
- External clients may inspect runtime posture, but they may not infer autonomy from supervised service availability.

## Integration note

The three candidate protocol surfaces should be drafted only as a bundle.
Drafting one without the others would risk reloading the same ambiguity Lane C already separated.
