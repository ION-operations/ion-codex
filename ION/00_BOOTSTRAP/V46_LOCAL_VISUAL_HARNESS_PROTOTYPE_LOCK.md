# V46 Local Visual Harness Prototype Lock

Status: **A3 prototype surface**  
Branch: `V46_LOCAL_VISUAL_HARNESS_PROTOTYPE`  
Authority: `LOCAL_DEV_CAPTURE_ONLY`  
Production authority: **false**

V46 introduces a local/dev-only visual harness prototype for the Visual Agent line.

This lock permits bounded capture of local visual evidence references such as screenshots, read-only DOM snapshots, viewport metadata, accessibility-tree files, and console-log summaries when they are supplied from an authorized local workspace path.

This lock does **not** authorize unrestricted browser control, credential-sensitive action, destructive action, form submission, purchases, account operations, persistent DOM mutation, network side effects, or production visual automation.

The purpose of this branch is to let ION begin closing the visual truth loop safely:

`local render evidence -> visual observation packet -> visual diagnosis receipt -> implementation recommendation -> future verification`
