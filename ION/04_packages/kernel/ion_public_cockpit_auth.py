"""Public cockpit login/session helpers.

This module is deliberately small and dependency-free. It supports:

- signed HttpOnly cockpit sessions;
- permission-token login using the existing public token or invite tokens; and
- Google OpenID Connect login when operator-provided OAuth env vars exist.

It does not grant production authority, live execution authority, provider API
dispatch authority, or any ION state acceptance authority.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import hmac
import json
import os
import secrets
import time
from http.cookies import SimpleCookie
from typing import Any, Callable, Mapping
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PUBLIC_COCKPIT_TOKEN_ENV = "ION_COCKPIT_PUBLIC_TOKEN"
SESSION_SECRET_ENV = "ION_COCKPIT_SESSION_SECRET"
INVITE_TOKENS_ENV = "ION_COCKPIT_INVITE_TOKENS"
ALLOWED_EMAILS_ENV = "ION_COCKPIT_ALLOWED_GOOGLE_EMAILS"
GOOGLE_CLIENT_ID_ENV = "ION_GOOGLE_OAUTH_CLIENT_ID"
GOOGLE_CLIENT_SECRET_ENV = "ION_GOOGLE_OAUTH_CLIENT_SECRET"
GOOGLE_REDIRECT_URI_ENV = "ION_GOOGLE_OAUTH_REDIRECT_URI"

SESSION_COOKIE = "ion_cockpit_session"
OAUTH_STATE_COOKIE = "ion_cockpit_oauth_state"
SESSION_TTL_SECONDS = 12 * 60 * 60
OAUTH_STATE_TTL_SECONDS = 10 * 60

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_SCOPES = "openid email profile"


@dataclass(frozen=True)
class AuthResult:
    ok: bool
    finding: str | None = None
    principal: dict[str, Any] | None = None
    token_label: str | None = None


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _json_b64(payload: Mapping[str, Any]) -> str:
    return _b64url_encode(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _sign(value: str, secret: str) -> str:
    return _b64url_encode(hmac.new(secret.encode("utf-8"), value.encode("utf-8"), hashlib.sha256).digest())


def _token_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.replace(";", ",").split(",") if item.strip()]


def cockpit_session_secret(env: Mapping[str, str] | None = None) -> str:
    values = env or os.environ
    return (values.get(SESSION_SECRET_ENV) or values.get(PUBLIC_COCKPIT_TOKEN_ENV) or "").strip()


def google_oauth_configured(env: Mapping[str, str] | None = None) -> bool:
    values = env or os.environ
    return bool((values.get(GOOGLE_CLIENT_ID_ENV) or "").strip() and (values.get(GOOGLE_CLIENT_SECRET_ENV) or "").strip())


def allowed_google_emails(env: Mapping[str, str] | None = None) -> set[str]:
    values = env or os.environ
    return {item.lower() for item in _split_csv(values.get(ALLOWED_EMAILS_ENV) or "")}


def invite_token_rows(env: Mapping[str, str] | None = None) -> list[dict[str, str]]:
    values = env or os.environ
    rows: list[dict[str, str]] = []
    public_token = (values.get(PUBLIC_COCKPIT_TOKEN_ENV) or "").strip()
    if public_token:
        rows.append({"label": "public-token", "token": public_token, "sha256": _token_hash(public_token)})
    for index, item in enumerate(_split_csv(values.get(INVITE_TOKENS_ENV) or ""), start=1):
        if "=" in item:
            label, token = item.split("=", 1)
            label = label.strip() or f"invite-{index}"
            token = token.strip()
        else:
            label = f"invite-{index}"
            token = item
        if token:
            rows.append({"label": label, "token": token, "sha256": _token_hash(token)})
    return rows


def validate_permission_token(token: str, env: Mapping[str, str] | None = None) -> AuthResult:
    supplied = (token or "").strip()
    if not supplied:
        return AuthResult(False, "permission_token_required")
    for row in invite_token_rows(env):
        if hmac.compare_digest(row["token"], supplied):
            return AuthResult(
                True,
                principal={
                    "auth_method": "permission_token",
                    "subject": row["label"],
                    "email": None,
                    "token_label": row["label"],
                },
                token_label=row["label"],
            )
    return AuthResult(False, "permission_token_invalid")


def invite_token_hash_allowed(token_hash: str | None, env: Mapping[str, str] | None = None) -> bool:
    if not token_hash:
        return False
    return any(hmac.compare_digest(row["sha256"], token_hash) for row in invite_token_rows(env))


def signed_value(payload: Mapping[str, Any], secret: str) -> str:
    body = _json_b64(payload)
    return f"{body}.{_sign(body, secret)}"


def verify_signed_value(value: str, secret: str) -> dict[str, Any] | None:
    if not value or "." not in value or not secret:
        return None
    body, sig = value.rsplit(".", 1)
    if not hmac.compare_digest(_sign(body, secret), sig):
        return None
    try:
        payload = json.loads(_b64url_decode(body).decode("utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    expires_at = payload.get("expires_at")
    if expires_at is not None and int(expires_at) < int(time.time()):
        return None
    return payload


def parse_cookie_header(cookie_header: str | None) -> dict[str, str]:
    cookie = SimpleCookie()
    cookie.load(cookie_header or "")
    return {key: morsel.value for key, morsel in cookie.items()}


def make_session_cookie(
    principal: Mapping[str, Any],
    *,
    secret: str,
    secure: bool,
    now: int | None = None,
) -> str:
    ts = int(now if now is not None else time.time())
    payload = {
        "kind": "ion_cockpit_session",
        "session_id": secrets.token_urlsafe(18),
        "auth_method": principal.get("auth_method") or "unknown",
        "subject": principal.get("subject") or principal.get("email") or "operator",
        "email": principal.get("email"),
        "token_label": principal.get("token_label"),
        "issued_at": ts,
        "expires_at": ts + SESSION_TTL_SECONDS,
        "production_authority": False,
        "live_execution_authority": False,
    }
    return build_cookie_header(SESSION_COOKIE, signed_value(payload, secret), max_age=SESSION_TTL_SECONDS, secure=secure)


def validate_session_cookie(cookie_header: str | None, *, secret: str) -> AuthResult:
    cookies = parse_cookie_header(cookie_header)
    payload = verify_signed_value(cookies.get(SESSION_COOKIE, ""), secret)
    if not payload:
        return AuthResult(False, "cockpit_session_missing_or_invalid")
    return AuthResult(True, principal=payload)


def build_cookie_header(name: str, value: str, *, max_age: int, secure: bool, http_only: bool = True) -> str:
    parts = [f"{name}={value}", "Path=/cockpit", "SameSite=Lax", f"Max-Age={max_age}"]
    if http_only:
        parts.append("HttpOnly")
    if secure:
        parts.append("Secure")
    return "; ".join(parts)


def clear_cookie_header(name: str, *, secure: bool) -> str:
    return build_cookie_header(name, "deleted", max_age=0, secure=secure)


def make_oauth_state_cookie(
    *,
    secret: str,
    next_path: str,
    invite_token: str | None,
    secure: bool,
    now: int | None = None,
) -> tuple[str, str]:
    ts = int(now if now is not None else time.time())
    nonce = secrets.token_urlsafe(24)
    payload = {
        "kind": "ion_cockpit_google_oauth_state",
        "nonce": nonce,
        "next": safe_next_path(next_path),
        "invite_token_sha256": _token_hash(invite_token.strip()) if invite_token and invite_token.strip() else None,
        "issued_at": ts,
        "expires_at": ts + OAUTH_STATE_TTL_SECONDS,
    }
    return nonce, build_cookie_header(
        OAUTH_STATE_COOKIE,
        signed_value(payload, secret),
        max_age=OAUTH_STATE_TTL_SECONDS,
        secure=secure,
    )


def validate_oauth_state_cookie(cookie_header: str | None, *, secret: str, state: str) -> AuthResult:
    cookies = parse_cookie_header(cookie_header)
    payload = verify_signed_value(cookies.get(OAUTH_STATE_COOKIE, ""), secret)
    if not payload:
        return AuthResult(False, "google_oauth_state_missing_or_invalid")
    if not hmac.compare_digest(str(payload.get("nonce") or ""), str(state or "")):
        return AuthResult(False, "google_oauth_state_mismatch")
    return AuthResult(True, principal=payload)


def safe_next_path(value: str | None) -> str:
    text = (value or "/cockpit/chat").strip() or "/cockpit/chat"
    if not text.startswith("/cockpit") or text.startswith("//") or "\n" in text or "\r" in text:
        return "/cockpit/chat"
    return text


def google_redirect_uri(base_url: str, env: Mapping[str, str] | None = None) -> str:
    values = env or os.environ
    configured = (values.get(GOOGLE_REDIRECT_URI_ENV) or "").strip()
    if configured:
        return configured
    return base_url.rstrip("/") + "/cockpit/auth/google/callback"


def build_google_authorization_url(
    *,
    base_url: str,
    state: str,
    env: Mapping[str, str] | None = None,
) -> str:
    values = env or os.environ
    params = {
        "client_id": (values.get(GOOGLE_CLIENT_ID_ENV) or "").strip(),
        "redirect_uri": google_redirect_uri(base_url, values),
        "response_type": "code",
        "scope": GOOGLE_SCOPES,
        "state": state,
        "access_type": "online",
        "include_granted_scopes": "true",
        "prompt": "select_account",
    }
    return GOOGLE_AUTH_ENDPOINT + "?" + urlencode(params)


def exchange_google_code_for_userinfo(
    *,
    code: str,
    base_url: str,
    env: Mapping[str, str] | None = None,
    fetcher: Callable[[Request, int], bytes] | None = None,
) -> dict[str, Any]:
    values = env or os.environ
    fetch = fetcher or (lambda request, timeout: urlopen(request, timeout=timeout).read())  # noqa: S310 - fixed Google endpoints.
    token_body = urlencode(
        {
            "code": code,
            "client_id": (values.get(GOOGLE_CLIENT_ID_ENV) or "").strip(),
            "client_secret": (values.get(GOOGLE_CLIENT_SECRET_ENV) or "").strip(),
            "redirect_uri": google_redirect_uri(base_url, values),
            "grant_type": "authorization_code",
        }
    ).encode("utf-8")
    token_raw = fetch(
        Request(
            GOOGLE_TOKEN_ENDPOINT,
            data=token_body,
            headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
            method="POST",
        ),
        10,
    )
    token_data = json.loads(token_raw.decode("utf-8"))
    access_token = str(token_data.get("access_token") or "")
    if not access_token:
        raise ValueError("google_access_token_missing")
    userinfo_raw = fetch(
        Request(
            GOOGLE_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
            method="GET",
        ),
        10,
    )
    userinfo = json.loads(userinfo_raw.decode("utf-8"))
    if not isinstance(userinfo, dict):
        raise ValueError("google_userinfo_invalid")
    return userinfo


def authorize_google_user(userinfo: Mapping[str, Any], *, oauth_state: Mapping[str, Any], env: Mapping[str, str] | None = None) -> AuthResult:
    email = str(userinfo.get("email") or "").strip().lower()
    subject = str(userinfo.get("sub") or "").strip()
    verified = userinfo.get("email_verified")
    if not email:
        return AuthResult(False, "google_email_missing")
    if verified is False or str(verified).lower() == "false":
        return AuthResult(False, "google_email_not_verified")
    allowed = allowed_google_emails(env)
    invite_hash = str(oauth_state.get("invite_token_sha256") or "").strip()
    if email not in allowed and not invite_token_hash_allowed(invite_hash, env):
        return AuthResult(False, "google_email_not_allowed")
    return AuthResult(
        True,
        principal={
            "auth_method": "google",
            "subject": subject or email,
            "email": email,
            "name": userinfo.get("name"),
            "picture": userinfo.get("picture"),
            "token_label": "google_allowlist" if email in allowed else "google_invite_token",
        },
    )


def auth_status(env: Mapping[str, str] | None = None) -> dict[str, Any]:
    values = env or os.environ
    return {
        "schema_id": "ion.public_cockpit_auth_status.v1",
        "session_secret_configured": bool(cockpit_session_secret(values)),
        "permission_token_configured": bool(invite_token_rows(values)),
        "google_oauth_configured": google_oauth_configured(values),
        "google_allowed_email_count": len(allowed_google_emails(values)),
        "invite_token_count": len(invite_token_rows(values)),
        "production_authority": False,
        "live_execution_authority": False,
    }
