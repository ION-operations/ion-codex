# ION Context Metabolism and Lifecycle Protocol V102

```yaml
schema_id: ion.context_metabolism_and_lifecycle_protocol.v1
version_line: V102_CONTEXT_METABOLISM_AND_LIFECYCLE
status: active_protocol_candidate
production_authority: false
archive_mutation_authority: proposal_only_until_operator_or_steward_apply_gate
created_at: 2026-05-02
```

## 1. Why this protocol exists

ION was built to defeat stateless AI amnesia by externalizing memory into context packages, receipts, packets, projections, manifests, execution cycles, and review surfaces. That succeeded. The next failure mode is the inverse: externalized memory can grow faster than ION's ability to distinguish living operational truth from historical proof.

The correct repair is not a cleanup script. The correct repair is **context metabolism**: every work cycle must leave a compact living residue, while raw evidence is classified, indexed, and eventually retired to an archive tier without losing auditability.

## 2. First-principles distinction

ION must keep these categories separate:

```text
current truth      compact state needed for the next lawful run
hot state          active queues, locks, manifests, role packages, cockpit view, active work packet
warm evidence      recent receipts and execution cycles that may still be needed for repair or review
cold history       old receipts, old cycles, resolved proposals, lineage evidence, reconstructive archive
quarantine         temporary sessions, unpacked foreign roots, failed reconciliation scratch space
```

A large file or directory is not automatically waste. It is a problem only when its lifecycle class is unknown, or when cold/history material is sitting inside the hot runtime surface as if it were current truth.

## 3. Operating law

```text
ION shall not confuse proof-of-work with current truth.
ION shall not delete evidence merely because it is large.
ION shall not pack cold history into a hot carrier bundle unless explicitly requested.
ION shall produce a residue before retiring raw evidence.
ION shall prefer proposal-only lifecycle reports before moving, deleting, compressing, or rewriting artifacts.
```

## 4. Metabolic cycle

```text
cycle closes
→ return receipts and template/action proofs are validated
→ accepted delta is integrated into living state
→ compact residue is written to current truth surfaces
→ raw cycle evidence is marked warm
→ older warm evidence is eligible for cold archival
→ oversized proposals are eligible for diff/snapshot compaction review
→ temporary reconciliation roots are eligible for quarantine/closeout
→ carrier package excludes cold history unless forensic mode is requested
```

## 5. Lifecycle actions

### KEEP_HOT

Used for active state required by the next run: active work packet, active spawn plan, runtime manifest, cockpit view, current role context packages, current queue, current lock surfaces.

### DIGEST_TO_RESIDUE

Used when raw evidence must produce a compact summary, floor certificate, accepted delta, or context-card update before any archival action.

### ARCHIVE_COLD

Used for older cycles, old receipts, old proposals, and historical evidence after residue exists. This is not deletion.

### REVIEW_COMPRESS_TO_DIFF

Used for large graph or template proposals that appear to serialize complete snapshots repeatedly. The lawful repair is to preserve at least one base snapshot plus reviewed diffs, not to erase proposals.

### QUARANTINE_AFTER_RECONCILIATION

Used for temporary root copies, unpacked zip sessions, failed branch reconciliation directories, or foreign project roots that should not remain under `ION/05_context/current`.

## 6. Relationship to existing ION systems

This protocol does not replace ION's temporal, context graph, template graph, runtime report, or agent context systems. It binds them.

```text
temporal system      decides freshness, heat, lease, dormancy, wake/reconfirm conditions
context graph        decides semantic identity, region, edge, provenance, custody
agent context system decides what a role needs in its active package
template graph       decides valid action/return/writeback shape
context lifecycle    decides hot/warm/cold/quarantine storage posture and carrier packaging eligibility
```

## 7. Carrier packaging law

A carrier package must include enough current truth to resume lawfully. It must not automatically include full cold history.

Default carrier package class:

```yaml
package_class: HOT_RUNTIME_CARRIER_PACKAGE
include:
  - repo authority
  - bootstrap locks
  - runtime manifests
  - active work packet
  - active role/context package indexes
  - active queue/gates
  - current cockpit/status view
  - last relevant receipts or digest residues
exclude_by_default:
  - old execution cycles
  - template graph proposal snapshots older than the hot window
  - temporary reconciliation roots
  - full forensic archives
```

Forensic package class:

```yaml
package_class: FORENSIC_ARCHIVE_PACKAGE
include:
  - hot runtime package
  - warm and cold evidence requested by scope
  - old cycles
  - old proposals
  - reconciliation work material
  - reconstructive encyclopedia/history
```

## 8. Non-production boundary

V102 adds lifecycle detection and proposal-only reporting. It does not grant autonomous destructive cleanup authority. Any module implementing movement, compression, deletion, or archive mutation must pass a separate Steward/operator apply gate.
