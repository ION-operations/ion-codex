# SELF-DOCUMENTING CONTEXT GRAPH PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-02 — Self-Documenting Approved Context System  
**Purpose:** Define how ION documents, tags, indexes, validates, and emits approved context for its own systems.

---

## 1. Root principle

```text
Before ION can use a file as trusted context, ION must know what that file is.
```

ION is a living context graph. Therefore its own files must be readable as graph objects, not as an opaque file pile.

A meaningful ION file should be classifiable by:

```text
identity
template/schema
graph node type
graph region
system family
authority status
operational status
epistemic status
owner/reviewer role
lineage posture
approved context status
retrieval zone
dependencies
downstream dependents
receipts
```

---

## 2. Relation to existing ION law

This protocol operationalizes existing commitments:

```text
Documentation is a governing organ of recoverability and continuity.
Context is a governed organ, not prompt stuffing.
The living context graph requires typed nodes, edges, regions, packages, and settlements.
A completed template file may become an event surface only under validation, authority, allowed reactions, and receipts.
```

Self-documentation is not optional prose. It is graph maintenance.

---

## 3. Approved context law

A file is not approved context merely because it exists, is recent, appears in a zip, or sounds authoritative.

Approved context requires:

```text
classification
metadata or index record
authority posture
operational status
retrieval zone
approved scope
lineage posture
review/receipt basis
```

A context package may load a file only if the file’s approved-context status is compatible with the task, role, graph region, and authority class.

---

## 4. Required file-record floor

Every load-bearing ION file must have or be given an `ion_file_record`.

Minimum fields:

```text
path
file_type
purpose
governing_intent
authority_status
operational_status
epistemic_status
role_class
owner_agent_family
reviewer_agent_family
lineage_role
context_lineage_tags
load_bearing_anchor
source_basis
approved_context_status
approved_context_scope
default_retrieval_zone
last_indexed_at
last_verified_at
```

Full schema is defined in:

```text
ION/02_architecture/ION_FILE_RECORD_SCHEMA_PROTOCOL.md
ION/03_registry/ion_file_record_schema.yaml
ION/07_templates/self_documentation/ION_FILE_RECORD.md
```

---

## 5. Approved context statuses

```text
APPROVED_CONTEXT
PROVISIONAL_CONTEXT
WITNESS_CONTEXT
HISTORICAL_CONTEXT
QUARANTINED_CONTEXT
STALE_CONTEXT
SUPERSEDED_CONTEXT
NEEDS_REVIEW
UNKNOWN_CONTEXT
```

### APPROVED_CONTEXT

May be loaded into context packages for declared scope.

### PROVISIONAL_CONTEXT

May be loaded only with provisional posture visible.

### WITNESS_CONTEXT

May support evidence or recovery but must not impersonate governing law.

### HISTORICAL_CONTEXT

May inform lineage and donor comparison but is not current authority.

### QUARANTINED_CONTEXT

Must not load by default.

### STALE_CONTEXT

Requires reconfirmation before current use.

### SUPERSEDED_CONTEXT

May load only for evolution/recovery lineage.

### NEEDS_REVIEW

Requires specialist or reviewer pass before approved use.

### UNKNOWN_CONTEXT

Must be classified before use.

---

## 6. Retrieval zones

```text
L1_ROOT_LAW
L2_BOOT_ROUTE_EMBODIMENT
L3_MISSION_CANON_IDENTITY
L4_CURRENT_STATE
L5_ACTIVE_PLAN_OBJECTIVE
L6_CONTRADICTIONS_RISKS
L7_DEPENDENCIES_DOMAIN_MAPS_SYSTEM_CARDS
L8_HISTORICAL_LINEAGE_ARCHIVE
L9_QUARANTINE_NEVER_DEFAULT
```

Retrieval zone controls default loading behavior.

---

## 7. Self-documentation event cycle

Self-documentation participates in the evented template file graph:

```text
file created or modified
→ template/schema detected
→ metadata/frontmatter parsed or inferred
→ ion_file_record candidate emitted
→ validator checks required fields and authority posture
→ approved context projection updated
→ missing metadata creates gap warning
→ load-bearing surfaces get deeper indexing
→ receipt emitted
```

No file becomes approved context merely by existing.

---

## 8. Agent responsibilities

```text
Steward = routing and current-phase approval posture
Scribe = documentation expression, encyclopedia, changelogs, approved-context surfaces
Atlas = topology, dependency maps, domain maps, graph-region cartography
Vestige = donor-line evidence, historical lineage, stale-surface detection
Nemesis = audit, contradiction review, index integrity, release-risk objections
Mason = implementation mapping, code/doc linkage, tests
Relay / Persona Interface = front-door approved-context projection without source-truth rewrite
```

---

## 9. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. raw files to become approved context without classification;
2. summaries to replace source truth;
3. stale documents to load as current law;
4. historical witnesses to impersonate authority;
5. indexes to become canon without receipts;
6. generated documentation to bypass contradiction review;
7. undocumented systems to remain hidden black boxes;
8. missing metadata to be ignored on load-bearing surfaces;
9. agent-private continuity to be merged into raw shared context;
10. ION to update its own doctrine without self-documenting the update.

---

## 10. Minimal test guards

```text
test_self_documenting_context_protocol_exists
test_file_record_schema_required_fields
test_approved_context_status_enum
test_retrieval_zone_registry_exists
test_unknown_file_not_approved_context
test_load_bearing_surface_requires_deep_record
test_approved_context_index_tracks_doctrine_evolution_surfaces
```
