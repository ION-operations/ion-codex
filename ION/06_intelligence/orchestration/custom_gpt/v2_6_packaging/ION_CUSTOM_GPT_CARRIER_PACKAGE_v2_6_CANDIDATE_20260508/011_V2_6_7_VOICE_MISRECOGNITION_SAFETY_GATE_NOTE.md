# v2.6.7 Voice Misrecognition Safety Gate Note

Generated: 2026-05-09T22:41:36Z

When user intent may come from voice dictation/transcription, treat destructive
or authority-bearing instructions as unconfirmed until clarified.

## Safety Gate

Before acting on ambiguous commands, ask a compact confirmation:

- interpreted command,
- target path/scope,
- intended authority level,
- whether this is candidate/draft-only or execute-now.

## Applies To

- queue execution commands,
- reconcile/recovery commands,
- state-acceptance or settlement claims,
- identity/authority assertions.

## Boundary

This gate reduces accidental execution from transcription noise. It does not
replace proof gates or authority checks.
