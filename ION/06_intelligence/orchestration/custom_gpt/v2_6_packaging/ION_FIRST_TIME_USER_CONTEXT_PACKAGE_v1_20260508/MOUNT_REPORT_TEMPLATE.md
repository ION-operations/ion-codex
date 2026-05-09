# Mount Report Template

Use this only when the user asks for proof, diagnostics, or a visible ION report. Do not show this by default in ordinary conversation.

```yaml
ion_mount_report:
  package_id: ion-first-time-user-context-v1
  mount_status: CLEAN | CONSERVATIVE | DEGRADED | BLOCKED
  mounted_files:
    - ION_DATA_MANIFEST.json
    - STATE/current_state.json
    - PERSONA/persona_state.json
    - DOMAINS/domain_registry.json
    - CONTEXT/context_graph.json
    - PACKETS/open_packets.json
    - DECISIONS/decision_ledger.json
    - ARTIFACTS/artifact_manifest.json
    - RECEIPTS/bootstrap_receipt.json
  authority:
    production_authority: false
    live_execution_authority: false
    accepted_state_source: receipt_ledger_or_user_acceptance
  current_objective: ""
  active_domains: []
  candidate_domains: []
  active_packets: []
  open_questions: []
  next_safe_step: ""
  non_claims:
    - "AI output is not accepted state by itself."
    - "Connector access is not claimed without proof."
```
