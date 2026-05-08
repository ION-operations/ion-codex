# V70 Release Candidate Preview and Preflight Verifier View Model Lock

Version: `V70_RELEASE_CANDIDATE_PREVIEW_AND_PREFLIGHT_VERIFIER_VIEW_MODEL`

V70 binds the V69 handoff package assembly plan to a release-candidate preview and preflight verifier checklist.

Boundary:

- preview only
- no release archive creation
- no file writes
- no zip creation
- no real checksum claim
- no external transfer
- no memory write
- no canonical graph write
- no source-summary rewrite
- no live dispatch
- no production authority

Law: a package assembly plan may become a release-candidate preview. A release-candidate preview may not become a release archive or production claim without separate authority.
