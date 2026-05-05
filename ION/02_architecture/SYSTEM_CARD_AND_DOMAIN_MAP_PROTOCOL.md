# SYSTEM CARD AND DOMAIN MAP PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Purpose:** Define self-documenting cards and maps for ION systems, domains, and graph regions.

---

## 1. System card purpose

A system card is a compact approved-context surface for a subsystem.

It answers:

```text
What is this system?
What graph region does it own or operate?
What files implement it?
What protocols govern it?
What templates does it use?
What tests guard it?
What receipts prove operation?
What current risks or gaps remain?
```

---

## 2. Required system card fields

```yaml
system_card:
  system_id:
  title:
  graph_region:
  owner_agent_family:
  reviewer_agent_family:
  purpose:
  governing_protocols: []
  implementation_files: []
  templates: []
  registries: []
  tests: []
  receipts: []
  dependencies: []
  downstream_dependents: []
  approved_context_status:
  retrieval_zone:
  current_gaps: []
```

---

## 3. Domain map purpose

A domain map describes a larger graph region and its internal systems.

```yaml
domain_map:
  domain_id:
  graph_region:
  owner_agent_family:
  systems: []
  child_regions: []
  upstream_domains: []
  downstream_domains: []
  active_protocols: []
  approved_context_entries: []
  risk_notes: []
```

System cards and domain maps are projection surfaces. They are not source truth.
