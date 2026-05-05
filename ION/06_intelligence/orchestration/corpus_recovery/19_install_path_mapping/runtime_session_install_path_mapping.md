# Runtime/session install-path mapping

## Why this exists

The Lane C trio no longer fails because it lacks plausible landing paths.
In this branch, the install paths already exist.

The real risk is now the opposite:

- forgetting that the trio already has bounded active-law presence
- or overstating that bounded slice as if it were the full historical
  runtime/session/API organism

This mapping therefore answers:

- where the trio already lives
- what it is adjacent to
- what it must not overwrite
- and what remains after install-path ambiguity is removed

## Active insertion points already present

### 1. `ION/02_architecture/RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`

Role:
- defines what a runtime session is
- governs session identity, persistence, carrier binding, and queue existence
- refuses scheduler, reporting, and shell inflation

Immediate adjacency:
- scheduler protocol
- runtime-state binding/query/reporting protocols
- continuation protocol

Must not replace:
- scheduler queue/ranking law
- reporting/witness law
- continuation or settlement law

### 2. `ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`

Role:
- governs session-local queue ownership and dispatch movement inside one lawful
  runtime session
- binds session queue items to kernel dispatch without collapsing boundaries

Immediate adjacency:
- runtime session authority
- scheduler protocol
- activation authority

Must not replace:
- session identity/persistence
- top-level scheduler law
- activation authority

### 3. `ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md`

Role:
- governs external/API attachment into a runtime/session center
- permits bounded session creation only when explicitly allowed
- names refusal conditions and carrier-boundary witnesses

Immediate adjacency:
- runtime session authority
- session queue/dispatch
- supervised daemon and external execution bridge surfaces

Must not replace:
- session identity center
- queue ownership
- activation authority

## Bounded kernel embodiment already present

The trio is not only prose in this branch. It already has bounded kernel
embodiment at:

- `ION/04_packages/kernel/runtime_session_store.py`
- `ION/04_packages/kernel/runtime_session_dispatch_binding.py`
- `ION/04_packages/kernel/api_runtime_entry.py`

These slices prove:
- durable session authority storage exists
- queue/dispatch binding to kernel dispatch exists
- bounded API carrier entry exists

They do **not** imply:
- a full runtime daemon shell
- a broad transport stack
- or a complete restored historical runtime organism

## Explicit non-installs

This mapping rejects the following false interpretations:

- “the trio still needs hypothetical install paths before it can be reviewed”
- “because active files exist, Lane C is already thaw-ready”
- “the daemon/service shell is therefore the runtime center”
- “API entry presence means the whole historical runtime shell is restored”
- “queue readiness or API entry can now silently answer activation law”

## Root-map implication

The install-path question is now answered strongly enough that the root maps
should speak in the present tense:

- the trio already exists as bounded active architecture
- the next work is not path discovery
- the next work is receipt linkage and negative-case review

## Present conclusion

Install-path ambiguity is resolved for Lane C in this branch.
The trio already has active-law and bounded-kernel landing paths.

The remaining question is not where it would live.
The remaining question is whether its receipts, failure handling, and bounded
coexistence are strong enough for thaw review.
