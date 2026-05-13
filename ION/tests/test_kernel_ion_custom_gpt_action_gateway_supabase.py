from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest
import yaml

from kernel.ion_custom_gpt_action_gateway import (
    build_supabase_readmodel_response,
    submit_supabase_record_event,
)


OPENAPI_PATH = Path("ION/07_templates/actions/ION_SUPABASE_ACTIONS_OPENAPI_V0_1.yaml")


def _seed_root(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-supabase-gateway-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def _env() -> dict[str, str]:
    return {
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SECRET_KEY": "local-secret-test-key",
        "SUPABASE_SCHEMA": "ion_ops",
    }


def test_overview_route_returns_mocked_supabase_result(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    calls: list[tuple[str, dict[str, str], float]] = []

    def fake_get(url: str, headers: dict[str, str], timeout: float) -> list[dict[str, object]]:
        calls.append((url, headers, timeout))
        return [{"generated_at": "2026-05-13T00:00:00Z", "recent_events": []}]

    result = build_supabase_readmodel_response(
        tmp_path,
        "/supabase/cockpit/overview",
        environ=_env(),
        http_get=fake_get,
    )

    assert result["ok"] is True
    assert result["data"][0]["recent_events"] == []
    assert calls[0][0] == "https://example.supabase.co/rest/v1/v_cockpit_overview?select=%2A&limit=1"
    assert calls[0][1]["Accept-Profile"] == "ion_ops"
    assert "local-secret-test-key" not in json.dumps(result)


def test_recent_events_route_clamps_limit_to_100(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    seen_url = ""

    def fake_get(url: str, headers: dict[str, str], timeout: float) -> list[dict[str, object]]:
        nonlocal seen_url
        seen_url = url
        return []

    result = build_supabase_readmodel_response(
        tmp_path,
        "/supabase/events/recent",
        "limit=500",
        environ=_env(),
        http_get=fake_get,
    )

    query = parse_qs(urlparse(seen_url).query)
    assert result["ok"] is True
    assert query["limit"] == ["100"]
    assert query["order"] == ["created_at.desc"]


def test_env_missing_returns_safe_error(tmp_path: Path) -> None:
    _seed_root(tmp_path)

    result = build_supabase_readmodel_response(tmp_path, "/supabase/events/recent", environ={})

    assert result["ok"] is False
    assert result["refusal_class"] == "SUPABASE_ENV_MISSING"
    assert "Traceback" not in json.dumps(result)


def test_record_automation_event_rejects_accepted_state_claim(tmp_path: Path) -> None:
    _seed_root(tmp_path)

    result = submit_supabase_record_event(
        tmp_path,
        "/supabase/events/record",
        {"event_type": "bad", "accepted_state_claim": True},
        environ=_env(),
    )

    assert result["ok"] is False
    assert result["refusal_class"] == "SCHEMA_INVALID"


def test_record_automation_event_calls_adapter_with_safe_payload(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    calls: list[tuple[str, dict[str, object], dict[str, str], float]] = []

    def fake_post(url: str, payload: dict[str, object], headers: dict[str, str], timeout: float) -> dict[str, object]:
        calls.append((url, payload, headers, timeout))
        return {"event_id": "evt_gateway_smoke", "accepted_state_claim": False, "settlement_required": True}

    result = submit_supabase_record_event(
        tmp_path,
        "/supabase/events/record",
        {
            "event_type": "gateway_unit_test",
            "client_request_id": "client-001",
            "accepted_state_claim": False,
            "settlement_required": True,
        },
        environ=_env(),
        http_post=fake_post,
    )

    assert result["ok"] is True
    assert result["remote_row_id"] == "evt_gateway_smoke"
    assert Path(result["receipt_path"]).exists()
    assert calls[0][1]["p_idempotency_key"] == "client-001"
    assert calls[0][2]["Content-Profile"] == "ion_ops"
    assert "local-secret-test-key" not in json.dumps(result)


def test_record_service_health_rejects_production_authority(tmp_path: Path) -> None:
    _seed_root(tmp_path)

    result = submit_supabase_record_event(
        tmp_path,
        "/supabase/service-health/record",
        {"service_name": "gateway", "status": "healthy", "production_authority": True},
        environ=_env(),
    )

    assert result["ok"] is False
    assert result["refusal_class"] == "SCHEMA_INVALID"


def test_record_carrier_mount_rejects_accepted_state_authority(tmp_path: Path) -> None:
    _seed_root(tmp_path)

    result = submit_supabase_record_event(
        tmp_path,
        "/supabase/carrier-mounts/record",
        {
            "agent_tag": "codex_local_ion_mason",
            "carrier_type": "codex_cli",
            "context_instance_id": "ctx_test",
            "authority": {"accepted_state_authority": True},
        },
        environ=_env(),
    )

    assert result["ok"] is False
    assert result["refusal_class"] == "SCHEMA_INVALID"


def test_openapi_schema_contains_supabase_operation_ids_and_no_supabase_secret_text() -> None:
    text = OPENAPI_PATH.read_text(encoding="utf-8")
    doc = yaml.safe_load(text)
    operation_ids = {
        operation.get("operationId")
        for path_item in doc["paths"].values()
        for operation in path_item.values()
    }

    assert {
        "ionSupabaseCockpitOverview",
        "ionSupabaseRecentEvents",
        "ionSupabaseLatestServiceHealth",
        "ionSupabaseCurrentCarrierMounts",
        "ionSupabaseRecordAutomationEvent",
        "ionSupabaseRecordServiceHealth",
        "ionSupabaseRecordCarrierMount",
    }.issubset(operation_ids)
    lowered = text.lower()
    assert "service_role_key" not in lowered
    assert "supabase_secret_key" not in lowered
    assert "supabase_service_role_key" not in lowered
    assert "supabase.co" not in lowered


def test_read_route_response_does_not_return_secrets(tmp_path: Path) -> None:
    _seed_root(tmp_path)

    result = build_supabase_readmodel_response(
        tmp_path,
        "/supabase/service-health/latest",
        environ=_env(),
        http_get=lambda url, headers, timeout: [{"service_name": "gateway", "status": "healthy"}],
    )

    assert result["ok"] is True
    assert "local-secret-test-key" not in json.dumps(result)
