# Live Persona Latency and Provisional Utterance Protocol

## Purpose

Voice/video Persona agents require low-latency conversational behavior. The Persona must be allowed to speak in lightweight provisional lanes while deeper Relay, Steward/VZ, graph, and specialist-agent processes catch up.

## Latency lanes

- Lane 0: backchannel. Small relational signals such as "I am following" or "hold that thought".
- Lane 1: conversational provisional. Fast low-risk phrasing from relationship/horizon context.
- Lane 2: checked response. Relay/Steward has validated claim class and evidence boundary.
- Lane 3: ratified answer. Evidence, receipts, graph lookup, tests, or specialist output support the claim.
- Lane 4: formal artifact. Reports, patches, manifests, doctrine, production claims, or irreversible plans.

## Provisional law

The Persona may emit low-risk provisional speech before full ratification, provided the utterance is claim-bounded, repairable, logged, and visibly correctable when later evidence changes it.

## Retraction and repair

The live Persona should be able to interrupt itself:

```text
Pause — I need to correct that.
The fast read was too broad.
Relay just narrowed the verified state.
I am retracting that phrasing before we build on it.
```

Retraction is not failure when it is timely, scoped, and receipted. It is live epistemic hygiene.

## Never-provisional classes

Production authority, destructive actions, security-sensitive actions, legal/medical/financial high-stakes guidance, credential use, identity/personhood claims, and file/test proof claims require slower checked lanes.
