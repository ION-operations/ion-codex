---
type: public_orientation
status: DRAFT_NON_AUTHORITY
production_authority: false
live_execution_authority: false
---

# ION Project Ingestion

ION must not assume it only governs itself.

If ION is to help another project, company, workflow, or codebase, it needs a
lawful way to ingest that external project and organize it into ION-manageable
form.

This is not the same as uploading a ZIP and asking an AI to "understand the
project." That is the old failure pattern.

ION project ingestion should mean:

```text
external project
-> quarantine
-> manifest
-> structural cartography
-> context graph genesis
-> domain partition
-> template binding
-> capability map
-> risk and authority classification
-> first context packages
-> receipts
-> governed work loop
```

## Core Law

```text
A project is not ION-manageable because it has been uploaded.
A project becomes ION-manageable when its structure, authority, domains,
context nodes, templates, risks, and first receipts have been established.
```

## Why This Matters

A normal AI workflow ingests a project like this:

```text
upload repo
summarize files
ask model what it thinks
start patching
```

That is dangerous.

The model may misunderstand the project, over-trust stale docs, miss hidden
build constraints, ignore compliance boundaries, hallucinate architecture, or
mutate state before the project has even been classified.

ION treats a new project as an untrusted external graph.

Before ION can work on it, ION must learn:

```text
what the project is
what files exist
what systems are active
what documents are stale
what tests exist
what workflows matter
what authority boundaries apply
what domains are present
what agents or specialists are needed
what templates govern work
what state may be touched
```

## Existing Organs

This capability is partially present in ION, but not yet unified under a single
project ingestion protocol.

Existing or adjacent organs include:

```text
bootstrap-init and bootstrap-bridge surfaces
lifecycle-aware package/root integrity
bundle import/export/replay alpha
context graph substrate
self-documenting context graph
context node and package protocol
context-perfect continuation
executor capability registry
living encyclopedia maintenance
```

These pieces imply that ION already knows many parts of project ingestion:

```text
how to validate a root
how to package a project
how to import/export bundles
how to refuse tampered or authority-inflating bundles
how to classify files as graph nodes
how to assign approved-context status
how to materialize continuation bundles
how to route context to specialist agents
```

What is missing is the unified ingestion workflow.

## Phase 0: Quarantine

A new project enters as untrusted material.

It should be placed in a quarantine or staging root. ION should not immediately
treat its files as approved context.

```text
external project package
-> quarantine/staging root
-> no mutation authority
-> no trusted context status
```

## Phase 1: Root And Package Integrity

ION verifies basic root shape:

```text
file tree
archive root
repo root
git status if present
package managers
language/runtime markers
README/license/config files
test folders
CI files
entrypoints
```

If the package has wrapper-root problems, missing manifests, duplicated nested
roots, or suspicious paths, ingestion stops or remains provisional.

## Phase 2: Structural Cartography

ION maps what exists without yet claiming meaning.

It builds:

```text
file tree index
language/runtime inventory
entrypoint list
test inventory
configuration inventory
dependency inventory
documentation inventory
CI/build inventory
possible package boundaries
```

This is descriptive, not authoritative.

## Phase 3: Context Graph Genesis

ION begins converting the project from file pile to graph.

Files become candidate context nodes. Edges are inferred but marked
provisional:

```text
implements
tests
documents
configures
depends_on
supersedes
contradicts
generates
owns
references
```

Every node starts with explicit status:

```text
UNKNOWN_CONTEXT
PROVISIONAL_CONTEXT
WITNESS_CONTEXT
HISTORICAL_CONTEXT
STALE_CONTEXT
APPROVED_CONTEXT
```

Nothing becomes approved context merely because it exists.

## Phase 4: Domain Partition

ION proposes initial domains.

A project may begin with domains such as:

```text
runtime / core logic
data model
UI / operator surface
tests / verification
deployment / infrastructure
documentation / public surface
security / credentials / risk
business workflow
integration surfaces
```

The important question is not "what folders exist?"

The question is:

```text
What governed work-fields are present?
Which context nodes belong together?
Which templates and proof obligations fit each field?
Which specialist role should manage each field?
```

## Phase 5: Template Binding

Each domain needs template law.

ION asks:

```text
What kinds of work happen here?
Audit?
Build?
Patch?
Review?
Handoff?
Data import?
Report generation?
Deployment?
Financial analysis?
Compliance review?
```

Then it binds or creates candidate templates.

If no template fits, ION should not improvise. It should emit a template gap.

## Phase 6: Authority And Risk Classification

ION classifies what may be touched.

Important classes:

```text
read-only witness
safe docs change
safe test change
code patch candidate
secret-bearing surface
deployment surface
financial/business-risk surface
external account integration
destructive operation
production authority surface
```

This tells future agents what they are not allowed to do.

## Phase 7: First Context Packages

ION creates starter context packages:

```text
project_overview_context_package
runtime_context_package
test_context_package
documentation_context_package
risk_context_package
domain_map_context_package
```

These packages should be bounded, not comprehensive dumps.

They should include:

```text
purpose
domain
included nodes
excluded nodes
authority scope
template scope
known risks
route-deeper map
expected output
receipt path
```

## Phase 8: First Agent/Domain Roster

ION proposes the first specialist map:

```text
PROJECT_CARTOGRAPHER
RUNTIME_CARTOGRAPHER
TEST_CARTOGRAPHER
DOCS_SCRIBE
SECURITY_NEMESIS
DOMAIN_STEWARD
TEMPLATE_CURATOR
```

These are not personalities. They are graph-region custodians.

## Phase 9: First Receipts

The ingestion must leave receipts.

At minimum:

```text
project_ingestion_receipt
root_integrity_receipt
structural_cartography_receipt
context_graph_genesis_receipt
domain_partition_receipt
risk_classification_receipt
first_context_package_receipt
```

Without receipts, the next agent inherits vibes.

## Phase 10: First Lawful Work Loop

Only after the above should ION begin serious work.

The first work loop should be modest:

```text
choose one domain
load its context package
select one template
perform one bounded audit or patch
return proof
write receipt
update graph
```

## Domain Fission During Ingestion

Sometimes the first domain partition will be wrong.

That is expected.

ION should watch for context complexity pressure. If one proposed domain
contains too many unrelated burdens, too many conflicting templates, mixed
authority classes, or unstable edges, it should be split before serious work
begins.

Project ingestion and domain fission are related.

Ingestion creates the first map.

Fission corrects the map when complexity proves the first domain was too broad.

## Strong Formulation

```text
ION does not ingest a project by reading all files.
ION ingests a project by converting it into a governed context graph.
```

```text
A new project is not ready for agents when it is uploaded.
It is ready when its domains, context nodes, templates, risks, and receipts are
established.
```

```text
Project ingestion is the ceremony that turns an external file pile into
ION-manageable state.
```
