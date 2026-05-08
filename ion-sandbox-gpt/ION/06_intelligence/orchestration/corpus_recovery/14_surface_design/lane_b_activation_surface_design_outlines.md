# Lane B activation surface-design outlines

These outlines are **proposal-space only**.
They are candidate shapes for future current-line protocol drafting after review.

## 1. `ACTIVATION_AUTHORITY_PROTOCOL.md`

### Proposed purpose
State what activation authority is, when candidate work may become executable enactment, and how activation relates to scheduler, allocator, operator entry, capability truth, and continuation/handoff law.

### Proposed sections
1. Purpose
2. Activation law
3. Canonical objects
4. Activation jurisdiction
5. Activation request classes
6. Approval, denial, and escalation rules
7. Relation to scheduler and allocator
8. Relation to operator entry and capability registry
9. Relation to continuation / takeover / handoff
10. Non-goals

### Candidate request classes
- `NEW_ENTRY`
- `CONTINUATION_ENTRY`
- `REBIND_ENTRY`
- `PARALLEL_BRANCH_ENTRY`
- `RESUME_ENTRY`
- `REVIEW_BLOCKED`

### Candidate denial classes
- `CAPABILITY_MISMATCH`
- `BOUNDARY_BLOCKED`
- `REVIEW_REQUIRED`
- `ALLOCATOR_BLOCKED`
- `CONTINUATION_INVALID`

### Candidate core law
- Activation authority is the lawful function that converts approved work into bounded enactment.
- Scheduler pressure may nominate work, but it may not by itself constitute activation.
- Activation authority must remain capability-aware, allocator-aware, and continuation-aware.
- Activation authority must not imply hidden unattended fleet autonomy.

## 2. `EXECUTOR_LIFECYCLE_PROTOCOL.md`

### Proposed purpose
State how an executor is claimed, prepared, entered, suspended, resumed, released, or retired under one-workflow law, with explicit receipts and bounded settlement semantics.

### Proposed sections
1. Purpose
2. Lifecycle law
3. Canonical objects
4. Executor identity and binding
5. Claim and readiness rules
6. Entry and active enactment
7. Suspension and resume semantics
8. Release, retirement, and failure classes
9. Relation to handoff capsules and takeover validation
10. Non-goals

### Candidate lifecycle states
- `UNBOUND`
- `CLAIMED`
- `READY`
- `ACTIVE`
- `SUSPENDED`
- `RETURNED`
- `RELEASED`
- `RETIRED`

### Candidate core law
- Executor identity must remain distinct from transient carrier/session/process identifiers.
- Every lifecycle transition must be receipted or explicitly blocked.
- Release and retirement must preserve settlement truth rather than orphaning enactment.
- Manual and automated carriers must share lifecycle classes even when their shells differ.

## Integration note

The two candidate protocol surfaces should be drafted only as a bundle.
Drafting one without the other would risk reloading the same ambiguity Lane B already separated.
