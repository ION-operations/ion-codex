# Runtime/session receipt-linkage worked examples

## Purpose
Show the Lane C trio operating through explicit receipt lineage without losing
the boundary between:

- runtime session authority,
- session queue/dispatch,
- API runtime entry,
- continuation as preserved thread identity,
- and settlement as closure/deferment classification rather than runtime
  authority.

## Common invariant sequence

Across all worked examples, the lawful sequence remains:

1. a runtime session center is created or referenced
2. runtime/session receipts witness center creation or binding
3. queue receipts witness bounded movement inside that center
4. API entry receipts, if present, witness external attachment or refusal
5. continuation or settlement may later cite that chain without replacing the
   center

The key boundary is this:

**receipts witness runtime/session history; continuation preserves thread
identity; settlement classifies closure posture; none of those surfaces replace
session authority or queue ownership.**

---

## Example 1 — Session creation and bounded queue admission

### Situation
A lawful runtime session is created, carrier and context are bound, and a
bounded queue item is admitted to the session.

### Lawful reading
- `RuntimeSessionReceipt(CREATED)` witnesses that the session identity,
  authority, and queue files were created.
- `RuntimeSessionReceipt(CARRIER_BOUND)` and
  `RuntimeSessionReceipt(CONTEXT_BOUND)` witness bounded session bindings.
- `RuntimeSessionReceipt(QUEUE_ITEM_ADDED)` witnesses queue admission.
- None of these receipts grant scheduler authority or activation permission.

### Example flow
1. `RuntimeSessionStore.create_session()` creates session identity, authority,
   queue, and one `CREATED` receipt.
2. `bind_carrier()` emits one `CARRIER_BOUND` receipt.
3. `bind_context()` emits one `CONTEXT_BOUND` receipt.
4. `add_queue_item()` emits one `QUEUE_ITEM_ADDED` receipt.
5. Each receipt points at the concrete witness path for the affected session
   artifact.

### Boundary proved
- session receipts establish and witness the center
- queue admission remains bounded movement inside that center
- receipts do not become a replacement for session authority itself

---

## Example 2 — Dispatch transition with kernel handoff witness

### Situation
A queue item becomes dispatch-ready and is sent through the existing kernel
dispatch path.

### Lawful reading
- `RuntimeSessionReceipt(QUEUE_ITEM_STATUS_UPDATED)` witnesses the local
  session-queue transition to `DISPATCH_READY`.
- `RuntimeSessionReceipt(DISPATCHED_WORK_UNIT)` witnesses that a session queue
  item nominated a kernel work unit and dispatched it.
- kernel dispatch emits its own downstream packet witness.
- the session-side receipt does not replace kernel dispatch truth, and the
  kernel packet does not replace session queue ownership.

### Example flow
1. `update_queue_item_status()` emits `QUEUE_ITEM_STATUS_UPDATED`.
2. `RuntimeSessionQueueDispatcher.dispatch_queue_item()` sends the nominated
   `work_unit_id` through kernel dispatch.
3. Kernel dispatch transitions the work unit and may emit a packet witness.
4. Session queue state is updated from `DISPATCH_READY` to `DISPATCHED`.
5. `RuntimeSessionReceipt(DISPATCHED_WORK_UNIT)` records the session-side
   dispatch witness and points at the kernel packet path when present.

### Boundary proved
- queue ownership stays local to the runtime session
- kernel dispatch remains downstream execution truth
- the receipt chain links the two without collapsing them

---

## Example 3 — API carrier attachment with accepted and refused entry

### Situation
An external/API carrier either attaches to a lawful runtime session or is
explicitly refused.

### Lawful reading
- `ApiRuntimeEntryReceipt(ACCEPTED)` or `ApiRuntimeEntryReceipt(REFUSED)`
  witnesses the API-entry outcome.
- accepted entry receipts point at the created or reused session-side witness
  artifacts, the carrier boundary witness, and the API receipt itself.
- refused entry receipts classify failure without pretending the runtime center
  exists under that carrier.

### Example flow
1. `ApiRuntimeEntryGateway.enter_runtime_session()` builds an explicit
   `ApiRuntimeEntryIntent`.
2. When session creation is explicitly allowed, the gateway may trigger session
   creation first and inherit the resulting `CREATED` receipt witnesses.
3. Carrier/context bindings are either created or reused and their witness
   paths are added to the receipt chain.
4. `ApiCarrierBoundary` is persisted as an explicit witness.
5. The final `ApiRuntimeEntryReceipt` cites the session-side witness paths plus
   the API boundary and receipt path.
6. In refusal cases, the receipt records a failure disposition such as
   `MISSING_SESSION` or `CARRIER_CONFLICT`.

### Boundary proved
- API entry receipts witness attachment or refusal
- API entry does not become session authority
- refusal does not erase the distinction between missing center and denied
  carrier attachment

---

## Example 4 — Continuation or settlement adjacency after runtime history exists

### Situation
A runtime session path later pauses, resumes, or closes while continuation and
settlement remain adjacent lawful surfaces.

### Lawful reading
- runtime/session receipts preserve what happened inside the center
- `CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md` may later materialize bounded
  continuation context without replacing session identity
- `BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md` may later classify closure,
  deferment, escalation, or future re-entry posture without becoming a second
  session center

### Example flow
1. A session has already emitted creation, binding, queue, dispatch, or API
   receipts.
2. If the work pauses, continuation law may preserve thread identity and
   required reads for lawful re-entry.
3. If the path closes or defers, settlement law may classify that posture by
   citing the existing receipt lineage.
4. Neither continuation nor settlement needs to recreate session authority or
   queue ownership to stay truthful.

### Boundary proved
- continuation remains thread-identity preservation, not session authority
- settlement remains closure/deferment classification, not runtime authority
- the runtime receipt chain is sufficient to be cited by adjacent law without
  being replaced by it

---

## Compressed findings

### 1. Receipt lineage now has first-form runtime evidence
The bounded current slice already emits a coherent receipt chain across session
creation, binding, queue movement, dispatch, and API entry.

### 2. API entry receipts are now better constrained
The API receipt is healthiest when treated as a carrier-boundary witness that
may include session-side witness paths, not as a replacement for the center.

### 3. Continuation and settlement remain adjacent, not central
The receipt chain is now strong enough to be cited by continuation or
settlement without requiring either surface to become a hidden runtime center.

### 4. The remaining gap is now negative-case breadth
The current slice is intelligible under receipt linkage, but it still needs a
dedicated negative-case review for invalid session, stale binding, blocked
queue, refusal, cancellation, and re-entry edge cases.

## Resulting judgment
The Lane C trio is stronger after receipt-linkage review.
The remaining major blocker before thaw-readiness reassessment is:
- negative-case coverage
