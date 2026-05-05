---
type: reasoning_journal
authority: A3_OPERATIONAL
created: 2026-04-09T23:20:00-04:00
status: ACTIVE
purpose: Record the M1 allocator embodiment, the corrections required to make it lawful, and the next path into M2
---

# M1 bounded multi-agent allocator reasoning journal

## What landed

M1 is now embodied in kernel code rather than only named in settlement doctrine.

The allocator can now:
- discover child work units by explicit parent relation,
- assess scheduler dispatchability,
- bind executors through the capability registry,
- enforce effective concurrency,
- refuse overlapping writes,
- persist branch-claim receipts,
- and expose snapshot/claim flows through the operator CLI.

## Corrections required during landing

Three concrete law mismatches had to be corrected:

1. child discovery was using the parent work-unit record bucket instead of an explicit parent→child relation,
2. allocator executor hints were too broad and collapsed named child roles into the first matching capability,
3. claim receipts were being persisted against the parent file scope instead of the parent work-unit scope.

Those corrections matter because they preserve M0 settlement law rather than merely satisfying tests.

## What M1 now proves

The kernel can create a lawful bounded fan-out surface without inventing merge or execution theater.

## What M1 still does not solve

M1 still does not handle:
- fan-in settlement,
- merge proposal contracts,
- review settlement,
- conflicting returns,
- stale-branch controls,
- or branch-aware horizon synchronization.

Those now become M2 and later work.
