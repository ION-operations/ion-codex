# ION FILE RECORD SCHEMA PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Purpose:** Define the machine-readable schema by which ION describes its own files as graph objects and context candidates.

---

## 1. Schema

```yaml
ion_file_record:
  path:
  title_or_identity:
  file_type:
  template_id:
  graph_node_type:
  graph_region:
  system_family:
  subsystem:
  purpose:
  governing_intent:
  authority_status:
  operational_status:
  epistemic_status:
  role_class:
  owner_agent_family:
  reviewer_agent_family:
  lineage_role:
  context_lineage_tags: []
  load_bearing_anchor:
  source_basis:
  excerpt_or_heading:
  direct_relation_count:
  upstream_dependencies: []
  downstream_dependencies: []
  supersedes: []
  superseded_by: []
  evolved_from: []
  contradiction_links: []
  approved_context_status:
  approved_context_scope: []
  default_retrieval_zone:
  last_indexed_at:
  last_verified_at:
```

---

## 2. Required fields

Minimum complete record:

```text
path
file_type
purpose
governing_intent
authority_status
operational_status
epistemic_status
role_class
lineage_role
approved_context_status
default_retrieval_zone
source_basis
```

Load-bearing records additionally require:

```text
owner_agent_family
reviewer_agent_family
upstream_dependencies
downstream_dependencies
last_verified_at
```

---

## 3. Authority statuses

```text
A1_CROWN_LAW
A2_PRODUCTION_GOVERNANCE
A3_OPERATIONAL_PROPOSAL
RUNTIME_PROOF_SURFACE
WITNESS
HISTORICAL_LINEAGE
EXPLANATORY_SYNTHESIS
UNKNOWN
```

---

## 4. Operational statuses

```text
ACTIVE
PROVISIONAL
DRAFT
SUPERSEDED
HISTORICAL_ONLY
QUARANTINED
STALE
UNKNOWN
```

---

## 5. Epistemic statuses

```text
PROVEN
TESTED
EVIDENCE_BACKED
INFERRED
SPECULATIVE
CONTRADICTED
UNKNOWN
```

---

## 6. Builder invariant

```text
A context package must not treat a file as trusted ION context unless an
ion_file_record or equivalent approved-context entry declares what the file is.
```
