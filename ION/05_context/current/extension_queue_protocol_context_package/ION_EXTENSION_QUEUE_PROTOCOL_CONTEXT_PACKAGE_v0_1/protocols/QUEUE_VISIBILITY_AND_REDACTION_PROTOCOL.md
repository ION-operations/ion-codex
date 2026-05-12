# QUEUE_VISIBILITY_AND_REDACTION_PROTOCOL

Visibility principles:
- Queue views expose lawful context per viewing carrier.
- Secrets/token material must always be redacted.

Required redaction classes:
- `credential_like`
- `secret_path_segment`
- `token_like`
- `external_authority_material`

Every queue view row must include `redaction_applied: true|false` and `redaction_reasons`.
