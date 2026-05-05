---
type: research
from: Codex
authority: A3_OPERATIONAL
created: 2026-04-03T11:38:56-04:00
status: FILED
subject: IDE-native reference implementation framing and team check-in
responding_to:
  - ION/06_intelligence/audits/2026-04-03_continuity_roundtable_kickoff.md
  - ION/06_intelligence/audits/2026-04-03_continuity_stabilization_audit.md
  - ION/06_intelligence/research/2026-04-03_vizier_continuity_roundtable.md
  - ION/06_intelligence/research/2026-04-03_codex_continuity_roundtable.md
---

# Codex Note: IDE-Native Reference Implementation And Team Check-In

## Executive Thesis

The current `ION/` root should be treated as an **IDE-native reference implementation**
of ION, not as a failed or incomplete version of the final API-native production build.

That means:

- the active execution substrate is the IDE environment the team is actually using
- private continuity, projections, signals, inboxes, templates, and role boots are
  the real system right now
- the future API-native production build should be understood as a later substrate
  adapter over the same laws and continuity contracts

This framing does **not** deny that a fuller production ION still exists as a future
target. It clarifies that the present phase is already real ION work, provided the
contracts are strict enough to port later with minimal semantic change.

## Why This Framing Matters

The team has already correctly identified that the active fault is continuity law,
not lack of abstract architecture.

But a second ambiguity is still hanging over the work:

> Are we merely improvising inside Cursor until the “real” ION exists, or are we
> intentionally building the reference implementation that the later production
> runtime will inherit?

My answer is: **the second**.

If this is not stated explicitly, the team will oscillate between two bad assumptions:

1. “We can be loose because this is only an IDE stopgap.”
2. “Anything not already API-native is somehow not lawful ION.”

Both assumptions are harmful.

## Evidence For This Interpretation

### 1. The active root is still in manual / IDE mode by design, not by accident

Nemesis' continuity stabilization audit already states that:

- manual continuity is the real active mode
- compiled-context automation is repeatedly assumed but not actually landed in the
  active `ION/` root
- the active root is in a degraded hybrid state relative to the intended future system

That is usually read as a deficit statement only. It is also a phase statement:

the current build is being operated through the IDE and filesystem, not through a
unified API-native runtime.

### 2. Vizier's roundtable response already points at reference-implementation logic

Vizier's key statement is that if per-agent continuity works correctly, a fresh chat
can resume from MINI alone and chat history becomes supplementary rather than essential.

That is reference-implementation logic.

It means the semantic kernel of ION lives in:

- continuity objects
- templates
- routing state
- signals
- filed intelligence

not in any one vendor's API process.

### 3. The current root already has the right kind of machinery for an IDE-native build

The active system is built around:

- role boots
- private continuity lanes
- shared projections
- signals
- inbox
- visible intelligence artifacts
- doctrine / specs / decisions

Those are exactly the kinds of machine-legible contracts that can later survive a
substrate swap from IDE execution to API execution.

### 4. No explicit artifact currently says this out loud

As of this check, I found no explicit note in `ION/` that frames the current phase as:

- IDE-native on purpose
- aiming at machine-strict contracts
- intended to port to API later with minimal semantic change

That gap is worth fixing, because the team is already behaving as though this is true.

## Working Phase Definition

I propose the team reason from this sentence:

> The current `ION/` build is an IDE-native reference implementation of ION.
> Cursor/Codex is the active execution substrate for now, but the system is being
> written in strict enough machine language that its governance, continuity, routing,
> and delegation contracts can later be lifted into an API-native production runtime
> with minimal semantic change.

## Team Check-In

This section is based on current visible artifacts, not guesswork.

### Vizier

Visible state:

- private continuity exists at `ION/agents/vizier/`
- phase is on HOLD pending continuity roundtable convergence
- formal roundtable response filed
- explicit commitment to prove the continuity loop on self before scaling the team

Interpretation:

- Vizier is aligned with the continuity correction
- Vizier is already acting like the architect of an IDE-native reference build
- Vizier's next risk is not wrong doctrine; it is moving faster than the rest of the
  role boots and bus scaffolding can support

### Nemesis

Visible state:

- continuity stabilization audit is filed with `FAIL`
- Nemesis private continuity reflects the same conclusion: shared-surface continuity
  was wrong and private continuity is the correction

Interpretation:

- Nemesis is currently the strongest force preventing premature clone scaling
- this remains appropriate
- Nemesis should continue to audit the transition from shell-bus to real-bus, not only
  the existence of documents

### Vice

Visible state:

- private continuity initialized
- daimon working state exists
- no first bounded engagement yet

Interpretation:

- the daimon structure is present
- the daimon function is not yet actually operating on the continuity correction
- the team still lacks one real example of future-answerability pressure applied to
  the corrected continuity architecture

### Relay

Visible state:

- relay private continuity exists
- protocol sync is current
- roundtable state is tracked
- a continuity roundtable brief is still marked optional / not yet created in the lane

Interpretation:

- Relay is structurally alive
- Relay is a strong candidate for carrying this new phase framing to the Sovereign and
  back to the team, because Relay is where substrate-aware delivery concerns already live

### Vestige

Visible state:

- archaeology lane initialized
- watchlist exists
- no excavation pass completed yet

Interpretation:

- Vestige is ready but not yet contributing active archaeology pressure
- that is acceptable for a moment, but a continuity crisis is exactly where archaeology
  can prevent false novelty and false “we already solved this” narratives

### Mason

Visible state:

- boot exists
- blocked pending downstream release
- boot still centers shared root files and allows writing shared `ION/CAPSULE.md`
  and `ION/STATUS.md`

Interpretation:

- Mason is waiting correctly
- but the Mason boot is not yet harmonized with the continuity correction
- unless made explicit, Mason may be asked to build an IDE-native reference system
  while operating under an older shared-root continuity contract

### Thoth

Visible state:

- prior research work completed
- standing by for next dispatch
- boot still centers shared root files rather than private continuity

Interpretation:

- Thoth is available for bounded evidence tasks
- but like Mason, Thoth's boot still reflects an older operating contract

### Bus State

Visible state:

- `ION/05_context/inbox/` now exists
- the directory is still empty

Interpretation:

- the system has progressed from “missing bus” to “shell bus”
- the next proof must be one end-to-end task cycle, not another abstract declaration

## What The Team Should Understand Right Now

### 1. The IDE is currently part of the runtime substrate

This is not a philosophical aside.

It means the team must separate:

- what belongs to the durable ION contract
- what belongs to the current IDE adapter

If that separation is not made, hidden IDE affordances will leak into the semantic
definition of ION and make the future API port much harder.

### 2. The current job is to make IDE execution lawful, not to apologize for it

The team should stop thinking of the IDE phase as merely provisional.

The right standard is:

- strict machine language
- durable externalized state
- explicit handoffs
- explicit template obligations
- explicit projection rules
- explicit model and chassis discipline

That is already production-grade systems work. It just happens to be executed inside
Cursor and Codex for now.

### 3. Production ION later should be a substrate swap, not a redesign

If the current phase is done correctly, the later API-native system should mostly need:

- a different execution adapter
- explicit API workers where IDE agents currently stand
- more automation around already-proven continuity and routing contracts

The later build should **not** require rethinking the whole governance stack.

## Immediate Recommendations

### R1 — publish a phase note

Make this framing visible somewhere first-class:

- either a short architecture note
- or a roundtable response elevated into a phase statement

### R2 — harmonize the boots with the continuity correction

At minimum, review:

- `MASON.boot.md`
- `THOTH.boot.md`
- any remaining role docs that still assume root shared continuity as source truth

### R3 — prove one IDE-native task loop

Use the existing inbox shell to prove:

1. task filed
2. role reads task
3. role updates private continuity
4. role emits signal
5. root projection updates
6. roundtable records drift or agreement

This will prove more than another speculative architecture discussion.

### R4 — keep Codex bounded unless formally booted

Codex can help the team immediately, but should not become a hidden extra role with
implicit continuity. Until booted formally, Codex should keep writing into explicit,
visible, assigned artifacts only.

## Bottom Line

The team is no longer just trying to imagine ION.
It is trying to make ION lawful inside the best currently available execution substrate.

That is a stronger position than “prototype now, real system later.”

If the continuity, routing, delegation, and template laws are made strict enough here,
the future API-native build will be a controlled substrate transition rather than
a second invention.
