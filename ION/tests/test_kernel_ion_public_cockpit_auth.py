import json
import time

from kernel.ion_public_cockpit_auth import (
    GOOGLE_AUTH_ENDPOINT,
    build_google_authorization_url,
    clear_cookie_header,
    cockpit_session_secret,
    exchange_google_code_for_userinfo,
    make_oauth_state_cookie,
    make_session_cookie,
    validate_oauth_state_cookie,
    validate_permission_token,
    validate_session_cookie,
    authorize_google_user,
)


def test_permission_token_accepts_public_and_invite_tokens():
    env = {
        "ION_COCKPIT_PUBLIC_TOKEN": "owner-token",
        "ION_COCKPIT_INVITE_TOKENS": "friend=friend-token,raw-token",
    }

    owner = validate_permission_token("owner-token", env)
    friend = validate_permission_token("friend-token", env)
    raw = validate_permission_token("raw-token", env)
    denied = validate_permission_token("wrong", env)

    assert owner.ok is True
    assert owner.token_label == "public-token"
    assert friend.ok is True
    assert friend.token_label == "friend"
    assert raw.ok is True
    assert raw.token_label == "invite-2"
    assert denied.ok is False


def test_session_cookie_is_signed_and_expires():
    secret = "session-secret"
    now = int(time.time())
    cookie = make_session_cookie(
        {"auth_method": "permission_token", "subject": "public-token"},
        secret=secret,
        secure=True,
        now=now,
    )

    accepted = validate_session_cookie(cookie, secret=secret)
    denied = validate_session_cookie(cookie.replace("ion_cockpit_session=", "ion_cockpit_session=X", 1), secret=secret)

    assert "HttpOnly" in cookie
    assert "Secure" in cookie
    assert accepted.ok is True
    assert accepted.principal["subject"] == "public-token"
    assert denied.ok is False
    assert "Max-Age=0" in clear_cookie_header("ion_cockpit_session", secure=False)


def test_google_authorization_url_and_state_cookie_are_bounded():
    env = {"ION_GOOGLE_OAUTH_CLIENT_ID": "client-id", "ION_GOOGLE_OAUTH_CLIENT_SECRET": "secret"}
    now = int(time.time())
    nonce, cookie = make_oauth_state_cookie(
        secret="session-secret",
        next_path="https://evil.test/",
        invite_token="invite-token",
        secure=True,
        now=now,
    )
    url = build_google_authorization_url(base_url="https://ion.helixion.net", state=nonce, env=env)
    state = validate_oauth_state_cookie(cookie, secret="session-secret", state=nonce)

    assert url.startswith(GOOGLE_AUTH_ENDPOINT)
    assert "client_id=client-id" in url
    assert "redirect_uri=https%3A%2F%2Fion.helixion.net%2Fcockpit%2Fauth%2Fgoogle%2Fcallback" in url
    assert state.ok is True
    assert state.principal["next"] == "/cockpit/chat"
    assert state.principal["invite_token_sha256"]


def test_google_user_authorization_requires_allowlist_or_invite_token():
    allow_env = {"ION_COCKPIT_ALLOWED_GOOGLE_EMAILS": "sev@example.com"}
    invite_env = {"ION_COCKPIT_INVITE_TOKENS": "guest=guest-token"}
    now = int(time.time())
    _nonce, state_cookie = make_oauth_state_cookie(
        secret="session-secret",
        next_path="/cockpit/chat",
        invite_token="guest-token",
        secure=False,
        now=now,
    )
    oauth_state = validate_oauth_state_cookie(state_cookie, secret="session-secret", state=_nonce).principal

    allowed = authorize_google_user({"email": "sev@example.com", "email_verified": True, "sub": "1"}, oauth_state={}, env=allow_env)
    invited = authorize_google_user({"email": "guest@example.com", "email_verified": True, "sub": "2"}, oauth_state=oauth_state, env=invite_env)
    denied = authorize_google_user({"email": "guest@example.com", "email_verified": True, "sub": "2"}, oauth_state={}, env=allow_env)

    assert allowed.ok is True
    assert invited.ok is True
    assert denied.ok is False
    assert denied.finding == "google_email_not_allowed"


def test_google_code_exchange_uses_token_and_userinfo_endpoints():
    calls = []

    def fake_fetch(request, timeout):
        calls.append((request.full_url, request.get_method(), timeout, dict(request.header_items())))
        if request.full_url.endswith("/token"):
            return json.dumps({"access_token": "access"}).encode("utf-8")
        return json.dumps({"email": "sev@example.com", "email_verified": True, "sub": "sub"}).encode("utf-8")

    userinfo = exchange_google_code_for_userinfo(
        code="code",
        base_url="https://ion.helixion.net",
        env={
            "ION_GOOGLE_OAUTH_CLIENT_ID": "client",
            "ION_GOOGLE_OAUTH_CLIENT_SECRET": "secret",
        },
        fetcher=fake_fetch,
    )

    assert userinfo["email"] == "sev@example.com"
    assert calls[0][1] == "POST"
    assert calls[1][1] == "GET"
    assert calls[1][3]["Authorization"] == "Bearer access"
    assert cockpit_session_secret({"ION_COCKPIT_SESSION_SECRET": "a"}) == "a"
