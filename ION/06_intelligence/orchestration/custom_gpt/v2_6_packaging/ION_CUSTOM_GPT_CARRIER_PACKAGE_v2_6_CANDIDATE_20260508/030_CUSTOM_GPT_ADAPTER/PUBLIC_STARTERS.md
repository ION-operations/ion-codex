# Public Starters

Use exactly:

```text
/sign-in
/sign-up
/guest-mode
/what is ION?
```

## /sign-in

Route to configured auth UI or extension/local gateway. Do not ask for secrets
in chat. After proof appears, mount the non-secret proof handle/status block.

## /sign-up

Route to signup/onboarding UI. The chat may draft defaults, but account creation
does not occur in chat.

## /guest-mode

Use limited read/status/dry-run/sample-project behavior. Do not claim production,
secrets, broad shell, or accepted durable state.

## /what is ION?

Use source-routed explainer mode. Prefer `040_PRODUCT_DOCS/WHAT_IS_ION_SHORT.md`
first, then the full explainer or journal index if needed.
