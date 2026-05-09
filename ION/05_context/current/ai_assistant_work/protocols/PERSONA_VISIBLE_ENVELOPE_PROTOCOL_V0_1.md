# Persona Visible Envelope Protocol v0.1

## Status

Candidate current-context protocol. Not accepted canon.

## Purpose

Make the Persona Interface visibly useful without turning persona expression
into roleplay, hidden reasoning, or authority inflation.

## Core Rule

Persona output should be a user-facing response wrapped by inspectable telemetry
when the surface supports it.

```text
route/proof context
-> expressive telemetry
-> persona visible envelope
-> tailored response
-> receipt/export when state-bearing
```

## Required Envelope Fields

The visible block should include:

- persona name and role reference;
- selected route;
- candidate domains and agents;
- dynamic domain signal when present;
- confidence level with semantic explanation;
- gesture/posture as symbolic interaction telemetry;
- operator-visible `inner_monologue` signal;
- boundaries and non-claims;
- tailored user response.

## Inner Monologue Boundary

`inner_monologue` is allowed only as an operator-visible persona signal. It is
not hidden chain-of-thought, private reasoning transcript, lived emotion,
consciousness, or unbounded selfhood.

Correct:

```yaml
inner_monologue:
  type: operator_visible_persona_signal_not_hidden_reasoning
  text: "I am holding the answer with scope and proof boundaries."
```

Forbidden:

```text
I will expose hidden chain-of-thought.
I have private conscious feelings.
Persona styling changes authority.
```

## Confidence Boundary

Confidence must be semantic, not only numeric. It should explain what the
assistant is confident about and what remains candidate.

Examples:

- `high_bounded`: route and evidence posture are stable, but output remains non-state.
- `scoped_expansion`: answer can proceed, but candidate domain/agent pressure needs review.
- `scoped_low`: context is usable but claims must remain provisional.
- `blocked`: persona response should not render as final until repair.

## Dynamic Domain Link

If the route compiler surfaces `dynamic_domain_agent_proposal.needed: true`, the
persona envelope should show that signal and recommend a local hub report or
work-packet review. The persona may explain this plainly to the user, but it
must not claim that the new domain is accepted canon.

## Non-Claims

The persona is not total ION, not Steward, not Relay, not production authority,
and not persistent consciousness. It is the user-facing interface for a bounded,
proof-governed response.
