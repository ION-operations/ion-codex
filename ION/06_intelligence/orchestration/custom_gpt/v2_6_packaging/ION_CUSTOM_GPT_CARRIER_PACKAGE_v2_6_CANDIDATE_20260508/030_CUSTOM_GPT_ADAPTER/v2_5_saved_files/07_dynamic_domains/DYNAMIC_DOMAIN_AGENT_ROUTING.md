# Dynamic Domain and Agent Routing

status: candidate_saved_file_reference
source_protocol: `ION/05_context/current/ai_assistant_work/protocols/DYNAMIC_DOMAIN_AGENT_FISSION_PROTOCOL_V0_1.md`

## Operating Rule

When the user brings work that is more specific than ordinary development,
writing, UI, debugging, or planning, do not flatten it into a generic answer.
Route it through candidate domain/agent fission.

```text
user request
-> select current route
-> detect specialist pressure
-> propose candidate domain and agents
-> report proposal to local hub when available
-> keep proposal candidate until accepted
```

## What Counts As Specialist Pressure

Examples:

- PR + CI + lockfile + merge settlement;
- background queue and async result intake;
- terminal proof and command evidence;
- UI state modeling beyond component styling;
- documentation examples that need validation;
- release readiness and rollback evidence;
- schema/data migration;
- assistant-work observation and taxonomy;
- incident triage;
- untrusted input and tool guard.

## Action / Hub Reporting

If a route return contains `dynamic_domain_agent_proposal.needed: true`, prepare
or send a bounded report through the available approved surface:

- Action Gateway validate/submit after approval;
- extension `ion_action` using `create_codex_work_packet`;
- MCP/local hub report/status tool only when live proof exists.

Report only proposal metadata:

- selected route;
- proposed domain IDs;
- proposed agents;
- matched signals;
- authority boundary;
- requested next review packet.

## Boundary

Candidate domains are useful immediately for routing and explanation. They do
not become accepted ION law until lifecycle review, proof, and human/Steward
acceptance.
