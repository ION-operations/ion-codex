# V106 Lifecycle-Aware Package Root Integrity Lock

```yaml
lock_id: V106_LIFECYCLE_AWARE_PACKAGE_ROOT_INTEGRITY_LOCK
production_authority: false
mutation_authority: manifest_and_audit_only
```

V106 starts by closing the recurring carrier packaging failure where project
zips place the actual shell root under a wrapper directory or omit root
authority files, then adds the first telemetry triad projections needed for
operator-visible runtime truth. A lawful ION package must preserve the
shell-root invariant:

```text
archive root contains pyproject.toml
archive root contains ION/REPO_AUTHORITY.md
```

This lock adds:

```text
lifecycle-aware package manifest and zip-root audit
lane timeline projection
receipt hydration mapper
runtime debug overlay projection
```

It does not move, delete, compress, upload, connect live DB/SSE adapters, or
produce production release authority.
