# Archive variant relations

This note captures first-pass duplicate/variant relations between the archive artifacts available in the current recovery environment.

## Production estate variants
- `ION - Production(1).zip`
- `ION - Production(2).zip`

Current read:
- same production-estate family
- same child-root structure
- treat as duplicate production witnesses unless later file-level diff proves otherwise

## Current branch line variants
Main line witnesses:
- `ION_Working_Branch_M16.zip`
- `ION_Working_Branch_M16_bootstrap_activation_landed_2026-04-10(1).zip`
- `ION.zip`
- `ION(1).zip`
- `ION_current_with_pyproject*.zip`
- `ION_current_documented_and_prepared*.zip`
- `ION_current_composer2_prepared.zip`
- `ION_current_orchestration_managed.zip`
- `ION_truename_template_aligned_C2*.zip`
- `ION_steward_*`
- `ION_corpus_recovery_*`

Current read:
- these are not independent system families
- they are branch-state witnesses and progressively patched variants of the current extracted ION line
- the M16 pair preserve the earliest visible extracted kernel line in this chat
- the later `ION_current_*`, `ION_steward_*`, and `ION_corpus_recovery_*` archives preserve successive documentation and governance mutations of that same current-branch family

## Workbench / canonical bundle line
- `ION_Consolidation_Workbench_*`
- `ION_Canonical_Consolidation_*`
- `ION_MASTER_RECOVERY_RECORD_2026-04-13.zip`
- `ION_master_recovery_patched_branch.zip`

Current read:
- these are not primary system lines
- they are consolidation artifacts, atlases, and patched-branch witnesses created during recovery
- they should be used as audit lineage and evidence aids, not mistaken for the original historical production lines

## Duplicate/near-duplicate handling rule
If two archives belong to the same variant group and preserve the same root family with only packaging or documentation mutations, prefer:
1. the latest packaged branch witness for current startup truth
2. the earliest clean witness for lineage baseline
3. the production estate for historical breadth

## Still missing
- stronger file-level duplicate/delta proof between production `(1)` and `(2)`
- stronger file-level duplicate/delta proof across the later current-branch variants
- explicit child-root diff summaries for large production sibling roots
