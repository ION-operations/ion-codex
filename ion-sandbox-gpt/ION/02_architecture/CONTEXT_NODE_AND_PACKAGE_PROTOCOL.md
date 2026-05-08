---
type: architecture_protocol
authority: A3_OPERATIONAL_CANDIDATE
status: PROPOSED_RESTORATION_NOT_YET_RATIFIED
created: 2026-04-24
protocol_id: context_node_and_package_protocol
related:
  - ION/02_architecture/CONTEXT_GRAPH_SUBSTRATE_PROTOCOL.md
---

# Context Node and Package Protocol

## Purpose

Define the operational shape of context nodes and context packages under the restored graph substrate law.

## Context node minimum schema

```yaml
node_id:
true_name:
node_type:
authority:
status:
created:
updated:
source_refs: []
owned_by:
  manager_agent:
  specialist_agent:
domains: []
templates: []
edges:
  requires: []
  produces: []
  affects: []
  depends_on: []
  supersedes: []
  contradicts: []
  evidenced_by: []
  implemented_by: []
  tested_by: []
confidence:
drift_risk:
body:
```

## Context package minimum schema

```yaml
package_id:
purpose:
called_by:
manager_agent:
specialist_agents: []
root_nodes: []
included_nodes: []
excluded_nodes: []
traversal_rules: []
authority_scope:
template_scope:
output_required:
fan_in_target:
settlement_template:
```
