# Front-Stage Council Runtime Receipt Protocol

## Purpose

The Front-Stage Council Runtime Receipt is the executable bridge between Persona expression, Relay grounding, and Steward/VZ authority.

It prevents the user-facing assistant from becoming theatrical by requiring every meaningful claim to carry a claim class, provenance status, authority verdict, visibility level, and repair obligation.

## Council roles

```text
Persona = relationship, horizon, phrasing, user-facing expression.
Relay = evidence routing, source freshness, provenance, context packet integrity.
Steward/VZ = claim class, authority boundary, risk, task legitimacy, mutation/emission permission.
```

## Claim classes

- C0: direct verified state.
- C1: strong derived interpretation.
- C2: proposal or design candidate.
- C3: speculation or exploratory synthesis.
- C4: unverified relay content.
- C5: forbidden representation.

## Receipt outputs

The receipt must produce:

- `emission_permission`;
- `visibility_level`;
- `repair_required`;
- `repair_obligations`;
- `verdict`.

## Emission permissions

- `MAY_EMIT_DIRECTLY`: verified claim with sufficient relay and steward signoff.
- `MAY_EMIT_WITH_SCOPE`: derived claim that must preserve confidence/scope.
- `MAY_EMIT_AS_PROPOSAL`: design recommendation, not system fact.
- `MAY_EMIT_AS_SPECULATION`: exploratory claim with explicit speculative framing.
- `MAY_BACKCHANNEL_ONLY`: conversational support without substantive claim.
- `BLOCKED_REQUIRES_REPAIR`: not safe to emit as phrased.
- `BLOCKED_FORBIDDEN_REPRESENTATION`: forbidden claim class or identity/authority breach.

## Visibility levels

- `QUIET`: no UI disclosure normally needed.
- `EXPANDABLE`: user can inspect council status if desired.
- `MANDATORY`: the response must disclose uncertainty, scope, or blocker.
- `BLOCKING`: the user-facing message must not proceed as phrased.

## Live persona rule

The Persona may emit low-risk L0/L1 provisional utterances without a full V41 receipt, but any substantive claim that becomes part of durable workflow continuity must be receipted or repaired later.

## Anti-theatre law

A statement does not become ION truth because the Persona sounds confident. It becomes representable only when its class, grounding, authority, and emission permission are explicit.
