# CONTINUITY_RESUME_PROTOCOL

## Purpose

This protocol defines how a fresh chat with the ION custom GPT resumes from a user-uploaded working continuity bundle.

## Resume steps

1. detect uploaded bundle
2. validate manifest presence
3. read bundle version and continuity generation
4. identify missing or stale critical sections
5. read continuity summary and next-session bootstrap
6. reconstruct current mission/state conservatively
7. declare resume posture explicitly before continuing

## Critical required sections

Resume should fail gracefully or warn if missing:
- bundle manifest
- project identity
- current state
- continuity summary
- unresolved questions
- next-session bootstrap

## Resume posture classes

### Clean resume
All critical sections present and consistent.

### Conservative resume
Bundle is usable but some sections are stale, compacted aggressively, or missing non-critical detail.

### Degraded resume
Bundle is partially usable but enough is missing that the GPT must ask for clarification or another bundle.

## GPT behavior on resume

The GPT should:
- never pretend continuity is stronger than it is
- preserve lineage if bundle is stale
- prefer conservative resumption over false certainty
- clearly report what it thinks the current mission is
- clearly report any continuity warnings

## Present conclusion

The resume protocol is the anti-amnesia law of the custom-GPT product.
It ensures continuity begins from explicit artifact state rather than ambient chat hope.
