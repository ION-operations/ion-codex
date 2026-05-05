# Activation/lifecycle install-path mapping

## Why this exists

The activation/lifecycle candidate no longer fails because it is undefined.
It risks failure if it enters active architecture unclearly.

This mapping therefore answers:

- where the candidate belongs
- what it is adjacent to
- what it must not overwrite
- what order of promotion preserves boundary clarity

## Proposed active insertion points

### 1. `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md`

Role:
- defines when a bounded work candidate may cross into enactment
- binds activation decision classes to executor capability truth and workflow law
- refuses scheduler, carrier, and continuation inflation

Immediate adjacency:
- scheduler protocol
- executor capability registry protocol
- packet/handoff standardization protocol

Must not replace:
- scheduler queue/selection logic
- lifecycle state transitions
- continuation/handoff legality

### 2. `ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md`

Role:
- governs what an already-authorized executor may do after enactment crossing
- defines claim, readiness, entry, active execution, suspension, release, and failure handling
- constrains enactment behavior without re-adjudicating authority

Immediate adjacency:
- continuation protocol
- takeover normalization protocol
- bounded parallelism and settlement protocol

Must not replace:
- activation permission
- settlement classification
- carrier-specific runtime mechanics

## Expected root-map consequences

If later promoted, the following root surfaces must change in the same packet:
- `README.md`
- `STATUS.md`
- `SYSTEM_MAP.md`
- `MASTER_ORCHESTRATION_INDEX.md`

Why:
because the repo startup story must acknowledge the new center the same day it becomes active law.

## Explicit non-installs

This mapping rejects these install patterns:

- embedding activation as a subsection of scheduler law
- embedding lifecycle as a subsection of continuation law
- landing either protocol first while leaving the pair split across review and active law
- treating carrier worked examples as active law text
- mutating settlement law to absorb activation lineage

## Bounded promotion recommendation

When promotion is eventually attempted, the right bounded packet shape is:

- two new `02_architecture/` protocol files
- one promotion note / ratification receipt
- synchronized root-map updates
- no registry expansion unless lifecycle object vocabulary is explicitly ratified

## Present conclusion

The install path is now clear enough that future thaw review can evaluate the candidate as a realistic active-law insertion, not a floating conceptual set.
