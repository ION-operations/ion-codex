# Lovable Prompt: Helixion ION GPT Actions Privacy Policy Page

Build and publish a simple public HTTPS privacy policy page for Helixion ION GPT Actions.

The page will be used as the Privacy Policy URL for two Custom GPT Actions:

- Action 1: ION Action Gateway at `https://ion-actions.helixion.net`
- Action 2: ION MCP JSON-RPC Action at `https://ion.helixion.net`

The output must be a real public web page, not a placeholder. It must load over HTTPS and be accessible without login.

## Page Requirements

- Page title: `Helixion ION Privacy Policy`
- Clean, professional, text-first layout.
- No marketing hero required.
- No login, forms, popups, analytics, tracking banners, or gated content.
- Include clear sections for:
  - What the Actions can access
  - Information sent by GPTs
  - Logs and receipts
  - Data control
  - Data sharing
  - Retention
  - Contact
- The page must explicitly mention:
  - `ion-actions.helixion.net`
  - `ion.helixion.net`
  - GPT prompts/conversation context/action payloads may be sent to those endpoints
  - ION may store logs, action receipts, validation receipts, idempotency records, queue records, tool-call summaries, timestamps, endpoint status, refusal outcomes, and approval outcomes
  - Helixion/operator controls the endpoints and project data
  - Users should not send secrets or sensitive personal information unless explicitly approved

## Exact Page Copy

Use this text as the page content.

```text
Helixion ION Privacy Policy

Last updated: May 7, 2026

This policy covers the Helixion ION Custom GPT Actions and MCP JSON-RPC Action endpoints used by operator-configured GPTs: ion-actions.helixion.net and ion.helixion.net.

What the Actions can access

The Action Gateway at ion-actions.helixion.net can receive bounded action requests, validation requests, approval evidence, idempotency keys, and context references that a GPT sends through the configured Action.

The MCP JSON-RPC Action at ion.helixion.net can receive JSON-RPC requests for ION status, tool discovery, file/read visibility tools, queue/status tools, and bounded tool calls exposed by the ION MCP preview.

Information sent by GPTs

When you use a GPT configured with these Actions, OpenAI may send user prompts, conversation context, action payloads, tool arguments, approval evidence, and request metadata to the Helixion ION endpoints so the requested operation can be validated or answered.

Logs and receipts

ION may store operational logs, action receipts, validation receipts, idempotency records, queue records, tool-call summaries, timestamps, endpoint status, and refusal or approval outcomes. These records are used for operator review, debugging, auditability, and abuse prevention. The endpoints are designed not to store API bearer tokens in receipts or public documentation.

Data control

The Helixion operator controls the ION endpoints and the local/project data reachable through them. Do not send secrets, credentials, private keys, financial account data, medical data, or other sensitive personal information through these Actions unless you have explicitly approved that use.

Data sharing

Helixion does not sell Action data. Data may be processed by infrastructure providers used to operate the endpoints, such as hosting, tunnel, DNS, logging, and security providers. Data may also be disclosed if required to comply with applicable law or to protect the security and integrity of the services.

Retention

Operational logs and receipts may be retained for as long as needed for ION continuity, audit, security, debugging, or operator review, unless deletion is requested and deletion is technically and legally feasible.

Contact

For privacy questions or deletion requests, contact the Helixion operator through the channel where you received access to the GPT or ION endpoint.
```

## Acceptance Criteria

- The published page has a public HTTPS URL.
- The page loads without authentication.
- The page is not a homepage placeholder.
- The page includes the exact two endpoint hostnames:
  - `ion-actions.helixion.net`
  - `ion.helixion.net`
- The URL can be pasted into both Custom GPT Action Privacy Policy URL fields.

