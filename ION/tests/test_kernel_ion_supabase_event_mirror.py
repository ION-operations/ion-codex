from __future__ import annotations

import json
from pathlib import Path

import pytest

from kernel import ion_supabase_event_mirror as mirror


def test_dry_run_automation_event_writes_receipt(tmp_path: Path) -> None:
    result = mirror.mirror_event(
        {
            "kind": "automation_event",
            "event_type": "unit_test",
            "title": "Unit test event",
            "payload": {"accepted_state_claim": False},
        },
        ion_root=tmp_path,
        receipt_dir=tmp_path / "receipts",
        dry_run=True,
    )

    assert result["ok"] is True
    assert result["status"] == "MIRROR_DRY_RUN"
    assert result["rpc"] == "record_automation_event"
    receipt = json.loads(Path(result["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt["direct_table_write"] is False
    assert receipt["mirror_request"]["args"]["p_event_type"] == "unit_test"


def test_rejects_nested_accepted_state_claim() -> None:
    with pytest.raises(mirror.SupabaseMirrorError, match="accepted_state_claim=true"):
        mirror.build_request(
            {
                "kind": "automation_event",
                "event_type": "bad",
                "payload": {"nested": {"accepted_state_claim": True}},
            }
        )


def test_rejects_service_production_and_live_authority() -> None:
    with pytest.raises(mirror.SupabaseMirrorError, match="production_authority=true"):
        mirror.build_request(
            {
                "kind": "service_health_snapshot",
                "service_name": "ION MCP",
                "status": "healthy",
                "production_authority": True,
            }
        )
    with pytest.raises(mirror.SupabaseMirrorError, match="live_execution_authority=true"):
        mirror.build_request(
            {
                "kind": "service_health_snapshot",
                "service_name": "ION MCP",
                "status": "healthy",
                "live_execution_authority": True,
            }
        )


def test_rejects_carrier_accepted_state_authority() -> None:
    with pytest.raises(mirror.SupabaseMirrorError, match="accepted_state_authority=true"):
        mirror.build_request(
            {
                "kind": "carrier_mount_receipt",
                "agent_tag": "codex_local_ion_mason",
                "carrier_type": "local_codex_cli",
                "context_instance_id": "ctx_test",
                "authority": {"accepted_state_authority": True},
            }
        )


def test_non_dry_run_uses_rpc_without_live_supabase(tmp_path: Path) -> None:
    calls: list[tuple[str, dict[str, object], dict[str, str], float]] = []

    def fake_post(url: str, payload: dict[str, object], headers: dict[str, str], timeout: float) -> dict[str, object]:
        calls.append((url, payload, headers, timeout))
        return {"mirrored": True}

    result = mirror.mirror_event(
        {
            "kind": "service_health_snapshot",
            "service_name": "ION MCP preview",
            "status": "healthy",
            "host": "127.0.0.1",
            "port": 8765,
            "health": {"ok": True},
        },
        ion_root=tmp_path,
        receipt_dir=tmp_path / "receipts",
        dry_run=False,
        environ={"SUPABASE_URL": "https://example.supabase.co", "SUPABASE_KEY": "public-test-key"},
        http_post=fake_post,
    )

    assert result["ok"] is True
    assert result["rpc"] == "record_service_health_snapshot"
    assert calls
    url, payload, headers, _timeout = calls[0]
    assert url == "https://example.supabase.co/rest/v1/rpc/record_service_health_snapshot"
    assert payload["p_service_name"] == "ION MCP preview"
    assert headers["apikey"] == "public-test-key"
    assert headers["Content-Profile"] == "ion_ops"
    assert headers["Accept-Profile"] == "ion_ops"
    assert json.loads(Path(result["receipt_path"]).read_text(encoding="utf-8"))["status"] == "MIRROR_RECORDED"


def test_default_schema_is_ion_ops_and_public_is_not_assumed() -> None:
    config = mirror.SupabaseConfig.from_env(
        {"SUPABASE_URL": "https://example.supabase.co", "SUPABASE_KEY": "public-test-key"}
    )

    assert config.schema == "ion_ops"
    assert config.schema != "public"


def test_backend_key_is_preferred_for_write_rpc() -> None:
    config = mirror.SupabaseConfig.from_env(
        {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE_KEY": "service-role-test-key",
            "SUPABASE_SECRET_KEY": "secret-test-key",
            "SUPABASE_KEY": "publishable-test-key",
        }
    )

    assert config.key == "service-role-test-key"
    assert config.key_source == "SUPABASE_SERVICE_ROLE_KEY"


def test_secret_key_is_preferred_over_publishable_fallback() -> None:
    config = mirror.SupabaseConfig.from_env(
        {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SECRET_KEY": "secret-test-key",
            "SUPABASE_KEY": "publishable-test-key",
        }
    )

    assert config.key == "secret-test-key"
    assert config.key_source == "SUPABASE_SECRET_KEY"


def test_supabase_schema_env_override_is_forwarded() -> None:
    calls: list[tuple[str, dict[str, object], dict[str, str], float]] = []

    def fake_post(url: str, payload: dict[str, object], headers: dict[str, str], timeout: float) -> dict[str, object]:
        calls.append((url, payload, headers, timeout))
        return {"mirrored": True}

    config = mirror.SupabaseConfig.from_env(
        {
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_KEY": "public-test-key",
            "SUPABASE_SCHEMA": "ion_ops_dev",
        }
    )
    mirror.call_rpc(config, "record_automation_event", {"p_event_type": "unit_test"}, http_post=fake_post)

    assert calls[0][2]["Content-Profile"] == "ion_ops_dev"
    assert calls[0][2]["Accept-Profile"] == "ion_ops_dev"


def test_builds_carrier_mount_rpc_args() -> None:
    request = mirror.build_request(
        {
            "agent_tag": "codex_local_ion_mason",
            "carrier_type": "local_codex_cli",
            "context_instance_id": "ctx_test",
            "current_packet": "PCKT-TEST",
            "authority": {"accepted_state_authority": False},
        }
    )

    assert request["kind"] == "carrier_mount_receipt"
    assert request["rpc"] == "record_carrier_mount_receipt"
    assert request["args"]["p_agent_tag"] == "codex_local_ion_mason"
    assert request["args"]["p_current_packet"] == "PCKT-TEST"


def test_supabase_local_env_is_ignored() -> None:
    gitignore = Path(".gitignore").read_text(encoding="utf-8")
    assert ".env.*" in gitignore
