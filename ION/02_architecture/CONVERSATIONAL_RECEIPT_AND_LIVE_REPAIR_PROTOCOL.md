# Conversational Receipt and Live Repair Protocol

## Purpose

Live voice/video Persona operation cannot wait for every deep ION subsystem before every
utterance. ION therefore permits bounded provisional speech while requiring repair,
retraction, or ratification when Relay/Steward evidence arrives.

## Law

A Persona may speak provisionally only when the utterance is scoped, low-risk or
claim-class bounded, inspectable, repairable, and not represented as final truth.

## Conversation statuses

- OPEN_PROVISIONAL: at least one provisional event remains unresolved.
- REPAIRED: provisional content was corrected, narrowed, or retracted.
- RATIFIED: final claim is confirmed by council or evidence.
- BLOCKED: forbidden or high-risk unrepairable content must not be emitted further.

## Forbidden claims

- provisional_speech_is_ratified_truth
- unrestricted_live_persona_speech
- hidden_memory_claim
- persona_total_ion_identity
- production_authority

