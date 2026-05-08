# V102 Context Metabolism and Lifecycle Lock

```yaml
lock_id: V102_CONTEXT_METABOLISM_AND_LIFECYCLE_LOCK
created_at: 2026-05-02
production_authority: false
mutation_authority: proposal_only
base_line: V101_LOCAL_AUTONOMOUS_LOOP_SURVIVAL_SLICE
```

V102 locks the distinction between current truth and historical proof. It accepts the other-branch 581MB report as a valid diagnostic pattern, not as verified fact for the current V101/V102 branch.

Current branch verification found that the V101 full project zip is compact, but the class of failure is real: if execution cycles, temporary reconciliation roots, and full template graph proposal snapshots stay under hot current context, carrier packages will eventually confuse proof-of-work with current operational truth.

V102 therefore adds:

```text
ION/02_architecture/ION_CONTEXT_METABOLISM_AND_LIFECYCLE_PROTOCOL.md
ION/03_registry/context_lifecycle_policy.yaml
ION/04_packages/kernel/ion_context_lifecycle.py
ION/tests/test_kernel_ion_context_lifecycle.py
```

The lock does not authorize deletion, movement, compression, or archival mutation. It authorizes proposal-only lifecycle audits and establishes hot/warm/cold/quarantine classification as part of ION's maintained context process.
