# CUSTOM GPT PREP INDEX

## Purpose

This subtree is the first custom-GPT preparation layer for the current canonical ION branch.

It exists to answer one practical question:

**How do we mount current ION into a ChatGPT custom GPT product shape without pretending that the chat shell itself is the continuity substrate?**

The answer used here is:

- stable **ION core law** stays in GPT instructions + GPT knowledge,
- mutable **user/project continuity** lives in a working continuity bundle,
- long-horizon encrypted persistence remains outside ChatGPT in a local vault.

## What is in this subtree

1. `01_CUSTOM_GPT_READINESS_ASSESSMENT.md`
   - grounded judgment of how ready the current ION tree is for custom-GPT productization

2. `02_ION_CUSTOM_GPT_BUILD_SPEC.md`
   - exact product/build posture for ION as a custom GPT

3. `03_ION_CUSTOM_GPT_CONTINUITY_BUNDLE_SPEC.md`
   - layer split, bundle classes, manifest model, export/resume loop

4. `04_WORKING_CONTINUITY_BUNDLE_SCHEMA.md`
   - canonical uploadable, GPT-readable working bundle schema

5. `05_VAULT_CONTINUITY_BUNDLE_SCHEMA.md`
   - encrypted local archive bundle schema

6. `06_CONTINUITY_EXPORT_PROTOCOL.md`
   - what the GPT must emit at session end

7. `07_CONTINUITY_RESUME_PROTOCOL.md`
   - how a new chat resumes from a continuity bundle

8. `08_ACTIONS_DECISION_TREE_FOR_ION.md`
   - when ION should remain file-only and when Actions become justified

9. `09_ION_CUSTOM_GPT_INSTRUCTION_TEMPLATE.md`
   - compact instruction skeleton for the first GPT shell

10. `10_ION_CUSTOM_GPT_KNOWLEDGE_PACK_LAYOUT.md`
    - curation plan for the initial Knowledge pack

## Related existing ION material

The current branch already contains temporal doctrine and starter kernel surfaces that strongly support this custom-GPT layer:

- `ION/02_architecture/ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL.md`
- `ION/02_architecture/TEMPORAL_CONTEXT_LEASE_PROTOCOL.md`
- `ION/02_architecture/TRIPLE_TIME_RECONCILIATION_PROTOCOL.md`
- `ION/02_architecture/TEMPORAL_OBJECT_SCHEMA.md`
- `ION/06_intelligence/orchestration/temporal_stack/`

These should be treated as the continuity/temporal substrate that the custom-GPT product layer mounts onto, not replaces.

## Suggested reading order

1. readiness assessment
2. build spec
3. continuity bundle spec
4. working bundle schema
5. resume/export protocols
6. instruction template
7. knowledge-pack layout
8. actions decision tree

## Target product split

### GPT-side
- compact instruction law
- compact stable doctrine knowledge pack
- working-bundle interpreter
- updated continuity export

### Local-side
- encrypted archive storage
- continuity lineage
- decryption before upload
- re-encryption after export
- optional auto-download / auto-save

## Present conclusion

Current ION is ready enough to begin custom-GPT development now.

The missing work is not “invent ION.”
The missing work is “package and mount ION into a ChatGPT-native shell.”
