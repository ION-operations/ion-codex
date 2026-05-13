"""ION -> Supabase operating event mirror adapter.

This module mirrors selected local ION runtime evidence into the Supabase
`ion_ops` operational mirror through typed RPCs only. Supabase remains a mirror,
not source truth.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib import request
from urllib.error import HTTPError, URLError


RPC_BY_KIND = {
    "automation_event": "record_automation_event",
    "service_health_snapshot": "record_service_health_snapshot",
    "carrier_mount_receipt": "record_carrier_mount_receipt",
}

DEFAULT_SUPABASE_SCHEMA = "ion_ops"

FIELD_MAPS = {
    "automation_event": {
        "event_type",
        "title",
        "summary",
        "event_id",
        "occurred_at",
        "observed_at",
        "source_system",
        "severity",
        "carrier_id",
        "carrier_type",
        "agent_tag",
        "branch_id",
        "context_instance_id",
        "packet_id",
        "correlation_id",
        "idempotency_key",
        "payload",
        "evidence_refs",
        "source_posture",
        "settlement_required",
    },
    "service_health_snapshot": {
        "service_name",
        "status",
        "snapshot_id",
        "observed_at",
        "service_role",
        "carrier_id",
        "endpoint",
        "host",
        "port",
        "pid",
        "verdict",
        "version_line",
        "production_authority",
        "live_execution_authority",
        "health",
        "findings",
        "source_posture",
    },
    "carrier_mount_receipt": {
        "agent_tag",
        "carrier_type",
        "context_instance_id",
        "mount_receipt_id",
        "mounted_at",
        "carrier_id",
        "carrier_instance_id",
        "conversation_tag",
        "branch_id",
        "parent_context_id",
        "current_packet",
        "model_lane",
        "loaded_refs",
        "authority",
        "write_scope",
        "source_posture",
        "return_target",
        "persona_presentation",
        "drift_findings",
        "raw_receipt",
        "settlement_required",
        "valid",
    },
}

REQUIRED_FIELDS = {
    "automation_event": {"event_type"},
    "service_health_snapshot": {"service_name", "status"},
    "carrier_mount_receipt": {"agent_tag", "carrier_type", "context_instance_id"},
}

FORBIDDEN_TRUE_KEYS = {
    "accepted_state_claim",
    "accepted_state_authority",
    "production_authority",
    "live_execution_authority",
}


class SupabaseMirrorError(ValueError):
    """Raised when a mirror payload violates ION authority rules."""


@dataclass(frozen=True)
class SupabaseConfig:
    url: str
    key: str
    schema: str = DEFAULT_SUPABASE_SCHEMA
    key_source: str = "SUPABASE_KEY"

    @classmethod
    def from_env(cls, environ: dict[str, str] | None = None) -> "SupabaseConfig":
        env = environ if environ is not None else os.environ
        url = env.get("SUPABASE_URL", "").strip().rstrip("/")
        key_source = ""
        key = ""
        for candidate in [
            "SUPABASE_SERVICE_ROLE_KEY",
            "SUPABASE_SECRET_KEY",
            "SUPABASE_KEY",
            "SUPABASE_ANON_KEY",
            "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY",
            "VITE_SUPABASE_PUBLISHABLE_KEY",
        ]:
            value = (env.get(candidate) or "").strip()
            if value:
                key = value
                key_source = candidate
                break
        schema = (env.get("SUPABASE_SCHEMA") or DEFAULT_SUPABASE_SCHEMA).strip() or DEFAULT_SUPABASE_SCHEMA
        if not url:
            raise SupabaseMirrorError("SUPABASE_URL is required for non-dry-run mirror calls")
        if not key:
            raise SupabaseMirrorError(
                "SUPABASE_SERVICE_ROLE_KEY, SUPABASE_SECRET_KEY, SUPABASE_KEY, or a publishable Supabase key is required for non-dry-run mirror calls"
            )
        return cls(url=url, key=key, schema=schema, key_source=key_source)


def _now_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def load_event_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SupabaseMirrorError("event JSON must be an object")
    return data


def detect_kind(data: dict[str, Any], explicit_kind: str | None = None) -> str:
    kind = explicit_kind or data.get("kind") or data.get("record_type") or data.get("type")
    if kind:
        normalized = str(kind).strip()
        aliases = {
            "event": "automation_event",
            "automation": "automation_event",
            "service_health": "service_health_snapshot",
            "service": "service_health_snapshot",
            "carrier_mount": "carrier_mount_receipt",
            "mount_receipt": "carrier_mount_receipt",
        }
        normalized = aliases.get(normalized, normalized)
        if normalized in RPC_BY_KIND:
            return normalized
        raise SupabaseMirrorError(f"unsupported Supabase mirror kind: {normalized}")

    if "event_type" in data:
        return "automation_event"
    if "service_name" in data:
        return "service_health_snapshot"
    if {"agent_tag", "carrier_type", "context_instance_id"}.issubset(data):
        return "carrier_mount_receipt"
    raise SupabaseMirrorError("could not infer mirror kind from JSON input")


def _reject_forbidden_true(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_TRUE_KEYS and child is True:
                raise SupabaseMirrorError(f"rejected {key}=true at {child_path}")
            _reject_forbidden_true(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_forbidden_true(child, f"{path}[{index}]")


def validate_authority(data: dict[str, Any]) -> None:
    _reject_forbidden_true(data)


def _payload_source(data: dict[str, Any]) -> dict[str, Any]:
    args = data.get("args")
    if args is not None:
        if not isinstance(args, dict):
            raise SupabaseMirrorError("args must be an object when present")
        return args
    return data


def build_rpc_args(data: dict[str, Any], kind: str) -> dict[str, Any]:
    source = _payload_source(data)
    validate_authority(source)
    allowed = FIELD_MAPS[kind]
    required = REQUIRED_FIELDS[kind]
    missing = sorted(field for field in required if source.get(field) in (None, ""))
    if missing:
        raise SupabaseMirrorError(f"missing required fields for {kind}: {', '.join(missing)}")

    rpc_args: dict[str, Any] = {}
    for field in allowed:
        if field in source:
            rpc_args[f"p_{field}"] = source[field]
    return rpc_args


def build_request(data: dict[str, Any], explicit_kind: str | None = None) -> dict[str, Any]:
    kind = detect_kind(data, explicit_kind)
    args = build_rpc_args(data, kind)
    return {
        "kind": kind,
        "rpc": RPC_BY_KIND[kind],
        "args": args,
    }


def _http_post_json(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float) -> Any:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return None
            return json.loads(raw)
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise SupabaseMirrorError(f"Supabase RPC HTTP {exc.code}: {raw}") from exc
    except URLError as exc:
        raise SupabaseMirrorError(f"Supabase RPC connection failed: {exc}") from exc


def call_rpc(
    config: SupabaseConfig,
    rpc_name: str,
    rpc_args: dict[str, Any],
    *,
    timeout: float = 20.0,
    http_post: Callable[[str, dict[str, Any], dict[str, str], float], Any] | None = None,
) -> Any:
    url = f"{config.url}/rest/v1/rpc/{rpc_name}"
    headers = {
        "apikey": config.key,
        "Authorization": f"Bearer {config.key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Profile": config.schema,
        "Accept-Profile": config.schema,
        "Prefer": "return=representation",
    }
    post = http_post or _http_post_json
    return post(url, rpc_args, headers, timeout)


def default_receipt_dir(ion_root: Path) -> Path:
    return ion_root / "ION" / "05_context" / "current" / "supabase_event_mirror" / "receipts"


def write_mirror_receipt(
    *,
    receipt_dir: Path,
    mirror_request: dict[str, Any],
    dry_run: bool,
    remote_result: Any = None,
    status: str = "MIRROR_DRY_RUN",
    error: str | None = None,
) -> Path:
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_id = f"{_now_id()}_{uuid.uuid4().hex[:12]}_{mirror_request['rpc']}.json"
    receipt_path = receipt_dir / receipt_id
    receipt = {
        "schema_id": "ion.supabase_event_mirror.receipt.v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "dry_run": dry_run,
        "production_authority": False,
        "live_execution_authority": False,
        "accepted_state_claim": False,
        "direct_table_write": False,
        "mirror_request": mirror_request,
        "remote_result": remote_result,
        "error": error,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt_path


def mirror_event(
    data: dict[str, Any],
    *,
    ion_root: Path,
    dry_run: bool,
    kind: str | None = None,
    receipt_dir: Path | None = None,
    environ: dict[str, str] | None = None,
    http_post: Callable[[str, dict[str, Any], dict[str, str], float], Any] | None = None,
) -> dict[str, Any]:
    mirror_request = build_request(data, kind)
    receipts = receipt_dir or default_receipt_dir(ion_root)

    if dry_run:
        receipt_path = write_mirror_receipt(
            receipt_dir=receipts,
            mirror_request=mirror_request,
            dry_run=True,
            status="MIRROR_DRY_RUN",
        )
        return {
            "ok": True,
            "status": "MIRROR_DRY_RUN",
            "dry_run": True,
            "rpc": mirror_request["rpc"],
            "receipt_path": str(receipt_path),
            "would_call_remote": False,
        }

    receipt_path = write_mirror_receipt(
        receipt_dir=receipts,
        mirror_request=mirror_request,
        dry_run=False,
        status="MIRROR_ATTEMPT_RECORDED",
    )
    config = SupabaseConfig.from_env(environ)
    try:
        remote_result = call_rpc(config, mirror_request["rpc"], mirror_request["args"], http_post=http_post)
    except Exception as exc:
        error_path = write_mirror_receipt(
            receipt_dir=receipts,
            mirror_request=mirror_request,
            dry_run=False,
            status="MIRROR_FAILED",
            error=str(exc),
        )
        return {
            "ok": False,
            "status": "MIRROR_FAILED",
            "dry_run": False,
            "rpc": mirror_request["rpc"],
            "receipt_path": str(error_path),
            "attempt_receipt_path": str(receipt_path),
            "error": str(exc),
        }

    success_path = write_mirror_receipt(
        receipt_dir=receipts,
        mirror_request=mirror_request,
        dry_run=False,
        status="MIRROR_RECORDED",
        remote_result=remote_result,
    )
    return {
        "ok": True,
        "status": "MIRROR_RECORDED",
        "dry_run": False,
        "rpc": mirror_request["rpc"],
        "receipt_path": str(success_path),
        "attempt_receipt_path": str(receipt_path),
        "remote_result": remote_result,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mirror an ION runtime event to Supabase ion_ops RPCs.")
    parser.add_argument("--event-json", required=True, help="Path to JSON event payload.")
    parser.add_argument("--kind", choices=sorted(RPC_BY_KIND), help="Explicit mirror payload kind.")
    parser.add_argument("--ion-root", default=".", help="ION repo root. Default: current directory.")
    parser.add_argument("--receipt-dir", help="Override local mirror receipt directory.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and write local receipt without remote RPC call.")
    parser.add_argument("--json", action="store_true", help="Print JSON result.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    event_path = Path(args.event_json)
    ion_root = Path(args.ion_root)
    receipt_dir = Path(args.receipt_dir) if args.receipt_dir else None
    try:
        data = load_event_json(event_path)
        result = mirror_event(
            data,
            ion_root=ion_root,
            dry_run=args.dry_run,
            kind=args.kind,
            receipt_dir=receipt_dir,
        )
    except Exception as exc:
        result = {"ok": False, "status": "MIRROR_INPUT_REJECTED", "error": str(exc)}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result.get("status", "UNKNOWN"))
        if "receipt_path" in result:
            print(result["receipt_path"])
        if "error" in result:
            print(result["error"], file=sys.stderr)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
