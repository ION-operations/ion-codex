# Export Instructions

Use these instructions when the GPT needs to produce an updated continuity package after first-time user work.

## Export Goal

Create a small user/workspace memory pack that can be uploaded into a new chat or handed to a connected ION gateway.

## Required Export Sections

An export should include:

- Updated current objective.
- User/project label.
- Accepted facts.
- Candidate facts.
- Active non-claims.
- Open questions.
- Open packets or next steps.
- Domain registry updates.
- Persona state updates if relevant.
- Artifact manifest updates.
- Receipt ledger entry.
- Validation or non-validation statement.

## Receipt Rule

Every export must include a receipt draft with:

```text
receipt_id
created_at
carrier
source_context
objective
changes
validation
non_claims
next_packet
accepted_by_user
```

If the user did not explicitly accept state, set `accepted_by_user` to `false` and mark the export as candidate continuity.

## File Shape

Preserve the existing folder names when possible:

```text
STATE/
PERSONA/
DOMAINS/
CONTEXT/
PACKETS/
DECISIONS/
ARTIFACTS/
RECEIPTS/
INBOX/
OUTBOX/
ARCHIVE/
```

Do not include secrets. Do not include full unchanged ION engine files.
