# ION No Silent Loss and Containment Preservation Protocol

## Purpose

ION cannot accept full-project zips or trunk mutations that silently lose
files. This protocol makes preservation proof a first-class runtime artifact.

The governing law is:

```text
NO PROJECT FILE MAY BE SILENTLY LOST.
```

This is not a no-deletion-ever doctrine. ION is an evolving project. Files may
leave hot/runtime paths when they are moved to a containment, quarantine,
archive, or forensic surface with manifest/hash proof. The forbidden event is
silent loss, not lawful lifecycle movement.

## Lifecycle Correction

V102 already established that context and evidence must metabolize through
hot, warm, cold, archive, and quarantine postures. V118 applies that law to the
trunk preservation gate.

The preservation gate must distinguish:

```text
generated/cache removal
lawful containment movement
protected uncontained removal
unexpected uncontained removal
```

Only the last two are blocking loss events.

## Required Workflow

```text
1. Confirm shell root.
2. Generate a baseline manifest of project file paths, sizes, and SHA-256 hashes.
3. Apply the bounded patch or package action.
4. Generate a post-action manifest.
5. Compare manifests.
6. Resolve removed paths as generated/cache removal, containment move, protected uncontained removal, or unexpected uncontained removal.
7. Block if protected_removed_files > 0.
8. Block if unexpected_removed_files > 0.
9. Emit TRUNK_PRESERVATION_REPORT_V118.json.
10. Create or accept a full-project package only when packaging_verdict = PASS.
```

## Protected Movement Rule

Protected project organs include bootstrap, doctrine, architecture, registry,
kernel, current context, templates, UI, integrations, tests, and root authority
files. The registry policy is authoritative for the current protected path
list.

Protected files may leave their original path only when the post-action
manifest contains a matching SHA-256 copy under an approved containment prefix.
The report must emit:

```text
contained_removed_files
contained_removed_paths
containment_moves
```

Each containment move must name:

```text
from_path
to_path
sha256
movement_class: CONTAINMENT_MOVE
```

Cache and explicit temporary generated surfaces may disappear only when they
match the allowlist in:

```text
ION/03_registry/ion_trunk_preservation_policy.yaml
```

## Full Project Package Rule

The safe full-project packager must create a canonical archive root:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

at archive root. Wrapper-directory archives are invalid for carrier mounting.
The packager excludes generated cache/package byproducts from the archive and
records the exclusion as evidence instead of deleting source files.

## Authority Boundary

This protocol is a preservation and packaging gate. It does not accept worker
returns, does not make production claims, and does not delete or move files by
itself.
