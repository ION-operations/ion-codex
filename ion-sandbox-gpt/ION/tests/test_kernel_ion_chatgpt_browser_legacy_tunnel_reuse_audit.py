from pathlib import Path

from kernel.ion_chatgpt_browser_legacy_tunnel_reuse_audit import (
    BLOCKED_VERDICT,
    READY_VERDICT,
    SETUP_REQUIRED_VERDICT,
    build_legacy_tunnel_reuse_audit,
    write_legacy_tunnel_reuse_audit,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    authority = root / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("# ION authority\n", encoding="utf-8")


def _seed_donor(root: Path) -> Path:
    donor = root / "donors/aimos/cloudflare_tunnel.py"
    donor.parent.mkdir(parents=True, exist_ok=True)
    donor.write_text(
        "AIMOS_NAME = 'AIM-OS'\n"
        "PORT = 8000\n"
        "SSE_PATH = '/sse'\n"
        "STATUS_PATH = 'data/mcp/active_tunnel.json'\n"
        "INSTALL_HINT = 'winget install cloudflared'\n"
        "command = ['cloudflared', 'tunnel', '--url', f'http://localhost:{PORT}']\n"
        "url_marker = 'https://example.trycloudflare.com'\n",
        encoding="utf-8",
    )
    return donor


def _seed_current_tunnel(root: Path, *, include_legacy_sse: bool = False) -> Path:
    current = root / "ION/04_packages/kernel/ion_chatgpt_browser_cloudflare_tunnel.py"
    current.parent.mkdir(parents=True, exist_ok=True)
    legacy_line = "LEGACY = '/sse'\n" if include_legacy_sse else ""
    current.write_text(
        "DEFAULT_ENDPOINT_PATH = '/mcp'\n"
        "STATUS_RELATIVE_PATH = 'ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json'\n"
        "def build_cloudflared_command():\n"
        "    return ['cloudflared', 'tunnel', '--url', 'http://127.0.0.1:8765']\n"
        "status = {'production_authority': False, 'live_execution_authority': False, 'deployment_authority': False}\n"
        f"{legacy_line}",
        encoding="utf-8",
    )
    return current


def test_legacy_tunnel_reuse_accepts_cloudflared_transport_and_classifies_aimos_sse_as_donor_only(tmp_path):
    _seed_root(tmp_path)
    donor = _seed_donor(tmp_path)
    _seed_current_tunnel(tmp_path)

    audit = build_legacy_tunnel_reuse_audit(
        tmp_path,
        donor_paths=(donor,),
        cloudflared_binary="definitely-not-cloudflared-v124",
        emitted_at="2026-05-03T00:00:00+00:00",
    )

    assert audit.accepted is True
    assert audit.verdict == SETUP_REQUIRED_VERDICT
    assert audit.connector_state == "DONOR_TRANSPORT_REUSE_BLOCKED_CLOUDFLARED_NOT_INSTALLED"
    assert audit.endpoint_path == "/mcp"
    assert audit.current_connector_url_shape == "https://<cloudflare-host>/mcp"
    assert audit.donor_reusable_pattern_count > 0
    assert audit.donor_forbidden_pattern_count > 0
    assert audit.current_forbidden_pattern_count == 0
    assert "legacy_aimos_sse_patterns_classified_donor_only" in audit.findings
    assert "current_tunnel_excludes_legacy_sse_and_aimos_authority" in audit.findings
    assert audit.production_authority is False
    assert audit.live_execution_authority is False
    assert audit.deployment_authority is False


def test_legacy_tunnel_reuse_blocks_current_sse_carry_forward(tmp_path):
    _seed_root(tmp_path)
    donor = _seed_donor(tmp_path)
    _seed_current_tunnel(tmp_path, include_legacy_sse=True)

    audit = build_legacy_tunnel_reuse_audit(
        tmp_path,
        donor_paths=(donor,),
        cloudflared_binary="definitely-not-cloudflared-v124",
        emitted_at="2026-05-03T00:00:00+00:00",
    )

    assert audit.accepted is False
    assert audit.verdict == BLOCKED_VERDICT
    assert audit.current_forbidden_pattern_count > 0
    assert "current_tunnel_contains_legacy_forbidden_patterns" in audit.findings


def test_legacy_tunnel_reuse_blocks_when_donor_script_missing(tmp_path):
    _seed_root(tmp_path)
    _seed_current_tunnel(tmp_path)

    audit = build_legacy_tunnel_reuse_audit(
        tmp_path,
        donor_paths=(tmp_path / "missing/cloudflare_tunnel.py",),
        cloudflared_binary="definitely-not-cloudflared-v124",
        emitted_at="2026-05-03T00:00:00+00:00",
    )

    assert audit.accepted is False
    assert audit.verdict == BLOCKED_VERDICT
    assert audit.donor_scripts_found == 0
    assert "legacy_cloudflare_tunnel_donor_scripts_missing" in audit.findings


def test_legacy_tunnel_reuse_ready_when_safe_contract_and_cloudflared_available(tmp_path):
    _seed_root(tmp_path)
    donor = _seed_donor(tmp_path)
    _seed_current_tunnel(tmp_path)
    fake_cloudflared = tmp_path / "bin/cloudflared"
    fake_cloudflared.parent.mkdir(parents=True)
    fake_cloudflared.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_cloudflared.chmod(0o755)

    audit = build_legacy_tunnel_reuse_audit(
        tmp_path,
        donor_paths=(donor,),
        cloudflared_binary=str(fake_cloudflared),
        emitted_at="2026-05-03T00:00:00+00:00",
    )

    assert audit.accepted is True
    assert audit.verdict == READY_VERDICT
    assert audit.connector_state == "DONOR_TRANSPORT_READY_TO_RUN"
    assert audit.cloudflared_found is True


def test_legacy_tunnel_reuse_audit_writes_current_report(tmp_path):
    _seed_root(tmp_path)
    donor = _seed_donor(tmp_path)
    _seed_current_tunnel(tmp_path)
    audit = build_legacy_tunnel_reuse_audit(
        tmp_path,
        donor_paths=(donor,),
        cloudflared_binary="definitely-not-cloudflared-v124",
        emitted_at="2026-05-03T00:00:00+00:00",
    )

    out = write_legacy_tunnel_reuse_audit(tmp_path, audit)

    assert out.exists()
    assert out.name == "CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json"
