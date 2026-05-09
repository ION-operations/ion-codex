# Package Authority And Limits

## Authority Class

This package is a candidate Custom GPT carrier package. It can guide a GPT
carrier, provide retrieval material, define starter state, and describe Action
surfaces. It is not production authority.

## What It Can Do

- Help a Custom GPT mount ION consistently.
- Provide hot boot files for source priority, auth, Actions/MCP, dynamic
  domains, Persona output, receipts, and export.
- Provide starter project memory when no user memory pack exists.
- Provide runtime body/reference material under `ION/`.
- Provide OpenAPI schemas and bridge docs for configured Actions.

## What It Cannot Do

- Accept its own candidate outputs as canon.
- Grant production or live execution authority.
- Grant secrets authority.
- Replace live connector proof.
- Mutate local files outside the ChatGPT sandbox.
- Prove that local ION/Codex services are online without Action/MCP/tool proof.

## Source Rank

Source rank is lane-scoped.

Sandbox/package lane, the default:

1. GPT instruction field and `001_GPT_INSTRUCTIONS_PASTE.md`.
2. This mount order and package authority file.
3. Mounted user memory pack state and receipts.
4. Hot boot files in `010_HOT_BOOT/`.
5. Active package manifests, validation reports, and starter state.
6. Runtime body under `ION/`.
7. Product explainers and journals.
8. Historical/donor/witness material.

Connector/local hub lane, explicit-use only:

1. Live Action/MCP/local hub returns with receipt/status proof.
2. Connector policy and refusal class.
3. Mounted package law and authority limits.

Connector/local hub returns outrank sandbox files only inside an explicit
connector-lane request. They do not mount this package, sign in a user, create
guest state, accept continuity, or replace package instructions.

## Secret Boundary

Never request secrets in chat. Secrets belong in OAuth, local gateway, extension
UI, or platform Action auth UI.
