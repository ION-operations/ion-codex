from pathlib import Path

from kernel import ion_chatgpt_browser_cloudflare_tunnel as tunnel
from kernel.ion_chatgpt_browser_cloudflare_tunnel import (
    DEFAULT_ENDPOINT_PATH,
    READY_VERDICT,
    SETUP_REQUIRED_VERDICT,
    TRANSPORT_INSTALLED_NOT_RUNNING,
    TRANSPORT_LOCAL_HTTP_RUNNING_ONLY,
    TRANSPORT_NOT_INSTALLED,
    TRANSPORT_TUNNEL_RUNNING_VERIFIED,
    audit_cloudflare_tunnel,
    build_cloudflared_command,
    build_cloudflared_route_dns_command,
    connector_url_from_tunnel_url,
    extract_tunnel_url,
    find_cloudflared,
    write_tunnel_status,
)


def test_extract_trycloudflare_url():
    line = "INF +--------------------------------------------------------------------------------------------+ https://abc-def.trycloudflare.com"

    assert extract_tunnel_url(line) == "https://abc-def.trycloudflare.com"


def test_extract_tunnel_url_ignores_cloudflare_docs_and_terms_urls():
    terms_line = (
        "without a Cloudflare account, these account-less Tunnels are subject to "
        "the Cloudflare Online Services Terms of Use (https://www.cloudflare.com/website-terms/)"
    )
    docs_line = (
        "If you intend to use Tunnels in production follow: "
        "https://developers.cloudflare.com/cloudflare-one/connections/connect-apps"
    )

    assert extract_tunnel_url(terms_line) is None
    assert extract_tunnel_url(docs_line) is None


def test_connector_url_uses_mcp_endpoint_not_sse():
    connector_url = connector_url_from_tunnel_url("https://abc-def.trycloudflare.com")

    assert connector_url == "https://abc-def.trycloudflare.com/mcp"
    assert not connector_url.endswith("/sse")


def test_build_cloudflared_command_targets_local_preview_root():
    command = build_cloudflared_command(local_url="http://127.0.0.1:8765", cloudflared_binary="/usr/bin/cloudflared")

    assert command == ["/usr/bin/cloudflared", "tunnel", "--url", "http://127.0.0.1:8765"]


def test_build_named_cloudflared_command_targets_local_preview_root():
    command = build_cloudflared_command(
        local_url="http://127.0.0.1:8765",
        cloudflared_binary="/usr/bin/cloudflared",
        tunnel_name="ion-browser",
        credentials_file="/home/sev/.cloudflared/ion-browser.json",
    )

    assert command == [
        "/usr/bin/cloudflared",
        "tunnel",
        "run",
        "--credentials-file",
        "/home/sev/.cloudflared/ion-browser.json",
        "--url",
        "http://127.0.0.1:8765",
        "ion-browser",
    ]


def test_build_named_tunnel_route_dns_command():
    command = build_cloudflared_route_dns_command(
        cloudflared_binary="/usr/bin/cloudflared",
        tunnel_name="ion-browser",
        hostname="ion.helixion.net",
    )

    assert command == ["/usr/bin/cloudflared", "tunnel", "route", "dns", "ion-browser", "ion.helixion.net"]


def test_audit_reports_setup_required_when_cloudflared_missing():
    result = audit_cloudflare_tunnel(Path.cwd(), cloudflared_binary="definitely-not-cloudflared")

    assert result["accepted"] is True
    assert result["verdict"] == SETUP_REQUIRED_VERDICT
    assert result["connector_state"] == TRANSPORT_NOT_INSTALLED
    assert result["transport_state"] == TRANSPORT_NOT_INSTALLED
    assert result["endpoint_path"] == DEFAULT_ENDPOINT_PATH
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False
    assert result["deployment_authority"] is False
    assert "cloudflared_not_found_on_path" in result["findings"]


def test_audit_reports_ready_when_status_running_and_cloudflared_present(tmp_path, monkeypatch):
    fake_cloudflared = tmp_path / "cloudflared"
    fake_cloudflared.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cloudflared.chmod(0o755)
    status_path = tmp_path / "ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json"
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (tmp_path / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    monkeypatch.setattr(tunnel, "audit_http_mcp_preview", lambda _root: {"verdict": tunnel.HTTP_PREVIEW_READY_VERDICT})
    monkeypatch.setattr(tunnel, "_pid_running", lambda _pid: True)
    monkeypatch.setattr(
        tunnel,
        "check_connector_health",
        lambda *, local_url, connector_url=None, timeout=3.0: {
            "local_http_preview": {"ok": True, "status_code": 200, "error": None},
            "local_mcp_tools_list": {"ok": True},
            "public_mcp_tools_list": {"ok": True},
            "public_write_confirmation_required": {"ok": True},
        },
    )
    write_tunnel_status(
        tmp_path,
        tunnel_url="https://abc-def.trycloudflare.com",
        running=True,
        local_url="http://127.0.0.1:8765",
    )

    result = audit_cloudflare_tunnel(tmp_path, cloudflared_binary=str(fake_cloudflared))

    assert status_path.exists()
    assert result["verdict"] == READY_VERDICT
    assert result["connector_state"] == TRANSPORT_TUNNEL_RUNNING_VERIFIED
    assert result["transport_state"] == TRANSPORT_TUNNEL_RUNNING_VERIFIED
    assert result["active_connector_url"] == "https://abc-def.trycloudflare.com/mcp"
    assert result["local_http_running"] is True
    assert result["public_tunnel_verified"] is True
    assert result["write_tools_require_confirmation"] is True


def test_audit_classifies_stale_status_url_when_tunnel_process_not_running(tmp_path, monkeypatch):
    fake_cloudflared = tmp_path / "cloudflared"
    fake_cloudflared.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cloudflared.chmod(0o755)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (tmp_path / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    monkeypatch.setattr(tunnel, "audit_http_mcp_preview", lambda _root: {"verdict": tunnel.HTTP_PREVIEW_READY_VERDICT})
    monkeypatch.setattr(tunnel, "_pid_running", lambda _pid: False)
    monkeypatch.setattr(
        tunnel,
        "check_connector_health",
        lambda *, local_url, connector_url=None, timeout=3.0: {
            "local_http_preview": {"ok": False, "status_code": None, "error": "not_running"},
            "local_mcp_tools_list": {"ok": False},
            "public_mcp_tools_list": {"ok": False},
            "public_write_confirmation_required": {"ok": False},
        },
    )
    write_tunnel_status(
        tmp_path,
        tunnel_url="https://abc-def.trycloudflare.com",
        running=True,
        local_url="http://127.0.0.1:8765",
        process_id=999999,
    )

    result = audit_cloudflare_tunnel(tmp_path, cloudflared_binary=str(fake_cloudflared))

    assert result["verdict"] == SETUP_REQUIRED_VERDICT
    assert result["connector_state"] == TRANSPORT_INSTALLED_NOT_RUNNING
    assert result["transport_state"] == TRANSPORT_INSTALLED_NOT_RUNNING
    assert result["active_connector_url"] is None
    assert result["stale_connector_url"] == "https://abc-def.trycloudflare.com/mcp"
    assert "stale_active_connector_url_not_currently_running" in result["findings"]
    assert "local_http_mcp_preview_runtime_not_running" in result["findings"]
    assert result["local_http_running"] is False
    assert result["public_tunnel_verified"] is False
    assert result["write_tools_require_confirmation"] is False


def test_audit_reports_local_http_only_when_preview_runs_without_tunnel(tmp_path, monkeypatch):
    fake_cloudflared = tmp_path / "cloudflared"
    fake_cloudflared.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cloudflared.chmod(0o755)
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (tmp_path / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    monkeypatch.setattr(tunnel, "audit_http_mcp_preview", lambda _root: {"verdict": tunnel.HTTP_PREVIEW_READY_VERDICT})
    monkeypatch.setattr(
        tunnel,
        "check_connector_health",
        lambda *, local_url, connector_url=None, timeout=3.0: {
            "local_http_preview": {"ok": True, "status_code": 200, "error": None},
            "local_mcp_tools_list": {"ok": True},
            "public_mcp_tools_list": {"ok": False},
            "public_write_confirmation_required": {"ok": False},
        },
    )

    result = audit_cloudflare_tunnel(tmp_path, cloudflared_binary=str(fake_cloudflared))

    assert result["verdict"] == SETUP_REQUIRED_VERDICT
    assert result["connector_state"] == TRANSPORT_LOCAL_HTTP_RUNNING_ONLY
    assert result["transport_state"] == TRANSPORT_LOCAL_HTTP_RUNNING_ONLY
    assert result["active_connector_url"] is None
    assert result["local_http_running"] is True
    assert result["public_tunnel_verified"] is False
    assert result["write_tools_require_confirmation"] is False


def test_find_cloudflared_falls_back_to_user_local_bin(tmp_path, monkeypatch):
    fake_home = tmp_path / "home"
    fake_cloudflared = fake_home / ".local/bin/cloudflared"
    fake_cloudflared.parent.mkdir(parents=True)
    fake_cloudflared.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cloudflared.chmod(0o755)
    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv("PATH", "")

    assert find_cloudflared("cloudflared") == fake_cloudflared.as_posix()


def test_write_tunnel_status_records_non_authority_fields(tmp_path):
    status = write_tunnel_status(
        tmp_path,
        tunnel_url="https://abc-def.trycloudflare.com",
        running=True,
        local_url="http://127.0.0.1:8765",
        process_id=123,
    )

    assert status["connector_url"] == "https://abc-def.trycloudflare.com/mcp"
    assert status["process_id"] == 123
    assert status["production_authority"] is False
    assert status["live_execution_authority"] is False
    assert status["deployment_authority"] is False


def test_audit_reports_stable_hostname_plan_without_treating_it_as_active(tmp_path, monkeypatch):
    fake_cloudflared = tmp_path / "cloudflared"
    fake_cloudflared.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cloudflared.chmod(0o755)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (tmp_path / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    monkeypatch.setattr(tunnel, "audit_http_mcp_preview", lambda _root: {"verdict": tunnel.HTTP_PREVIEW_READY_VERDICT})
    monkeypatch.setattr(
        tunnel,
        "check_connector_health",
        lambda *, local_url, connector_url=None, timeout=3.0: {
            "local_http_preview": {"ok": True, "status_code": 200, "error": None},
            "local_mcp_tools_list": {"ok": True},
            "public_mcp_tools_list": {"ok": False},
            "public_write_confirmation_required": {"ok": False},
        },
    )

    result = audit_cloudflare_tunnel(
        tmp_path,
        cloudflared_binary=str(fake_cloudflared),
        tunnel_name="ion-browser",
        stable_hostname="https://ion.helixion.net/mcp",
    )

    assert result["stable_hostname"] == "ion.helixion.net"
    assert result["stable_connector_url"] == "https://ion.helixion.net/mcp"
    assert result["stable_connector_active"] is False
    assert result["active_connector_url"] is None
    assert result["verdict"] == SETUP_REQUIRED_VERDICT
    assert result["connector_state"] == "STABLE_HOSTNAME_NOT_ACTIVE"
    assert result["named_tunnel_route_dns_command"] == [
        str(fake_cloudflared),
        "tunnel",
        "route",
        "dns",
        "ion-browser",
        "ion.helixion.net",
    ]
    assert "named_tunnel_credentials_or_config_not_found_locally" in result["findings"]
    assert "stable_connector_url_not_active" in result["findings"]
