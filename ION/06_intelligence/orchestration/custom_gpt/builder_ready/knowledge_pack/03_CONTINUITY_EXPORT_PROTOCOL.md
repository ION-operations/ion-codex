# CONTINUITY_EXPORT_PROTOCOL

## Purpose

This protocol defines how the ION custom GPT should export continuity at the end of a serious session.

## Export trigger

An export should be produced when:
- the session reaches a meaningful stopping point
- the user asks for an updated continuity bundle
- the GPT is about to hand off or pause a major work thread
- continuity changed enough that failure to export would risk loss

## Export steps

1. read current working continuity state
2. compact cold history
3. preserve live obligations and unresolved questions
4. update continuity summary
5. update next-session bootstrap
6. update manifest and integrity info
7. increment continuity generation
8. generate downloadable updated working continuity bundle

## Required preserved material

The export must preserve:
- project identity
- active mission / phase
- current priorities
- unresolved questions
- active temporal objects
- current lease-relevant obligations
- budget posture if relevant
- recent decisions
- recent receipts
- lineage references

## Required compacted material

The export should compress:
- cold history
- bulky raw logs
- redundant repeated state
- large prior artifacts already summarized

## Export naming rule

Use deterministic bundle naming, for example:

`ION_working_continuity_<project_slug>_<generation>_<timestamp>.zip`

## Export validation note

The GPT should emit a short validation note alongside or inside the export:
- bundle id
- generation
- what was compacted
- any missing sections
- any continuity warnings

## Present conclusion

The continuity export is the session heartbeat of the product.
Without it, continuity is aspirational rather than real.
