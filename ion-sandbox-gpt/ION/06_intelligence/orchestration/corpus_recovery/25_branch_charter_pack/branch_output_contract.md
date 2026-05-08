# Branch output contract

Every branch chat must end each work cycle by returning one bounded packet and one concise judgment.

## Required fields

- **Branch name**
- **Selected objective**
- **Current horizon**
- **Allowed files**
- **Forbidden files**
- **Output class**
- **What changed**
- **What remains blocked**
- **Recommended next move**
- **Whether conductor action is required**

## Valid output classes

- delta packet
- surface-design packet
- quarantined review draft
- counterexample review
- worked-example packet
- install-path mapping packet
- promotion-candidate packet
- thaw-readiness packet

## Invalid output classes

- broad summary with no bounded artifact
- direct canon rewrite
- unbounded repo cleanup
- root-surface mutation by non-conductor branch
- active-law emission by a branch chat

## Merge rule

The conductor may do exactly one of three things with a branch output:

1. accept into repo review-space
2. request one more bounded pass
3. reject as out-of-horizon or structurally unsound
