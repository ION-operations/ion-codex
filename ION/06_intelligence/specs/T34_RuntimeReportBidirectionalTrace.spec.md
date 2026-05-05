# T34 — Runtime Report Bidirectional Trace

## Intent

Add a bounded read-only packet that shows the lawful forward profile→digest path and reverse digest→profile path together as one downstream witness view.

## Requirements

1. Accept exactly one lawful starting side:
   - forward selection: `profile_name`, `profile_path`, or `browser_entry_index`
   - reverse selection: `digest_json_path` or `digest_markdown_path`
2. Compose the existing I1 and I2 layers instead of bypassing them.
3. Surface explicit consistency markers:
   - profile name match
   - digest json path match
   - digest markdown path match
4. Surface explicit asymmetry rows when any forward/reverse mismatch exists.
5. Preserve read-only downstream witness semantics.

## Governed output root

`ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/`

## Non-goals

- No new digest authority
- No new profile authority
- No daemon or scheduler
- No mutation of kernel truth
