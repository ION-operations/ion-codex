# Local Browser Capture Adapter Stub Protocol

The local browser capture adapter is a stub interface between the Visual Agent and future local browser/screenshot/DOM capture tooling. In V47 it only composes receipts around explicitly supplied local artifacts and requested capture modes.

Forbidden in V47: unrestricted browser control, network side effects, credential-sensitive action, account operation, destructive action, form submission, purchase/submission action, persistent DOM mutation, production visual automation.
