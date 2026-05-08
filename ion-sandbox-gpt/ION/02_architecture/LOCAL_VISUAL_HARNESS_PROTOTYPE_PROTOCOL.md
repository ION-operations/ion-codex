# Local Visual Harness Prototype Protocol

## Purpose

The Local Visual Harness Prototype gives ION a bounded way to ingest visual evidence from authorized local/dev environments without granting the Visual Agent broad autonomous computer-control authority.

The harness is a prototype bridge between V44 visual observation packets and V45 visual diagnosis receipts. It allows a local screenshot, DOM snapshot, viewport metadata, accessibility-tree export, or console-log summary to be hashed, referenced, packetized, and routed into diagnosis receipts.

## Authority boundary

V46 authority is limited to:

`LOCAL_DEV_CAPTURE_ONLY`

The harness may:

- read explicitly supplied local files under the workspace root;
- hash and reference those files;
- emit a local visual harness capture receipt;
- build an associated visual observation packet;
- build an associated visual diagnosis receipt;
- recommend that implementation agents inspect or patch visual issues only through Steward/VZ review.

The harness may not:

- control arbitrary browsers;
- use credentials;
- submit forms;
- make purchases;
- delete or mutate user data;
- perform persistent DOM mutation;
- bypass Steward/VZ review;
- claim production readiness or production visual automation authority.

## Steward gate

Every local harness capture must include a steward gate status:

- `APPROVED_LOCAL_DEV_ONLY`
- `STEWARD_REVIEW_REQUIRED`
- `BLOCKED`

When blocked, the harness may record that the request was blocked, but it must not produce a valid capture artifact set for operational use.

## Rendered truth

V46 formalizes the principle that rendered behavior is part of truth. Source correctness is not product correctness. Visual evidence must become receipted continuity state before implementation decisions depend on it.

## Future work

V46 is not a browser automation runtime. Future versions may introduce a local browser/screenshot harness with explicit permission boundaries. That later harness must inherit V46's restrictions and add additional Steward/VZ gates before any interactive automation is allowed.
