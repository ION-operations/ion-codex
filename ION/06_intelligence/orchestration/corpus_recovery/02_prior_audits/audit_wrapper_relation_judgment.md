# Audit wrapper relation judgment

This note clarifies how `composeraudit` and `geminiaudit` relate to `00_CONSOLIDATED_ATLAS`.

## Main judgment

- `00_CONSOLIDATED_ATLAS` remains the primary prior atlas/consolidation center.
- `composeraudit` and `geminiaudit` are best read as **wrapper/regeneration roots** around that atlas work, not as independent primary organism centers.
- The wrappers preserve substantial **relative-path overlap** with the atlas, but the overlapping files are generally **regenerated rather than byte-identical copies**.

## Evidence summary

### 00_CONSOLIDATED_ATLAS vs composeraudit
- atlas files: 151
- composeraudit nested atlas files: 326
- common relative paths: 40
- exact same bytes on common paths: 0

Interpretation:
composeraudit appears to be a larger regenerated audit-wrapper root that incorporates and re-emits atlas material, not a clean frozen copy of the atlas.

### 00_CONSOLIDATED_ATLAS vs geminiaudit
- atlas files: 151
- geminiaudit nested atlas files: 41
- common relative paths: 23
- exact same bytes on common paths: 0

Interpretation:
geminiaudit is a smaller regenerated audit-wrapper root around part of the atlas material, again not a clean frozen copy.

### composeraudit vs geminiaudit
- common relative paths: 20
- exact same bytes on common paths: 0

Interpretation:
the two wrappers are related to the same prior atlas family, but neither should be promoted over `00_CONSOLIDATED_ATLAS` as the primary center.

## Recovery consequence

The corpus atlas should treat:
- `00_CONSOLIDATED_ATLAS` as the strongest prior atlas/consolidation line
- `composeraudit` as an expanded audit-wrapper witness
- `geminiaudit` as a smaller audit-wrapper witness

They are historically valuable, but they are **not** separate primary organism centers.
