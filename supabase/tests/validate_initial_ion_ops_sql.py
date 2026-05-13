#!/usr/bin/env python3
"""Static validation for ION Supabase migrations.

This intentionally does not connect to Supabase and does not read local .env
files. It validates that repo-managed SQL matches the live ion_ops baseline,
keeps private cockpit policies split, and exposes only guarded typed RPC writes.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MIGRATION_001 = REPO_ROOT / "supabase" / "migrations" / "001_initial_ion_ops.sql"
MIGRATION_002 = REPO_ROOT / "supabase" / "migrations" / "002_dev_private_cockpit_read_policies.sql"
MIGRATION_003 = REPO_ROOT / "supabase" / "migrations" / "003_ion_ops_authority_and_rpc.sql"
SEED = REPO_ROOT / "supabase" / "seed" / "001_ion_ops_bootstrap_seed.sql"
LIVE_SNAPSHOT = REPO_ROOT / "supabase" / "live_schema_snapshots" / "ion_ops_live_schema_20260513.sql"
DOCS = [
    REPO_ROOT / "ION" / "docs" / "setup" / "ION_SUPABASE_OPERATING_RUNTIME_SETUP.md",
    REPO_ROOT / "ION" / "02_architecture" / "ION_SUPABASE_OPERATING_RUNTIME_PROTOCOL_V0_1.md",
]

REQUIRED_001_SNIPPETS = [
    "create schema if not exists ion_ops",
    "create table if not exists ion_ops.automation_events",
    "event_id uuid primary key default gen_random_uuid()",
    "accepted_state_claim boolean not null default false",
    "settlement_required boolean not null default true",
    "create table if not exists ion_ops.carrier_mount_receipts",
    "mount_receipt_id uuid primary key default gen_random_uuid()",
    "accepted_state_authority boolean not null default false",
    "write_scope jsonb not null default '[]'::jsonb",
    "create table if not exists ion_ops.service_health_snapshots",
    "snapshot_id uuid primary key default gen_random_uuid()",
    "service_role text",
    "endpoint text",
    "host text",
    "pid integer",
    "verdict text",
    "version_line text",
    "findings jsonb not null default '[]'::jsonb",
    "production_authority boolean not null default false",
    "live_execution_authority boolean not null default false",
    "check (status in ('ready', 'healthy', 'degraded', 'blocked', 'unknown', 'offline'))",
    "alter table ion_ops.automation_events enable row level security",
    "alter table ion_ops.carrier_mount_receipts enable row level security",
    "alter table ion_ops.service_health_snapshots enable row level security",
    "create or replace view ion_ops.v_current_carrier_mounts",
    "create or replace view ion_ops.v_latest_service_health",
    "create or replace view ion_ops.v_recent_automation_events",
    "create or replace view ion_ops.v_cockpit_overview",
    "create trigger automation_events_set_updated_at",
    "create trigger carrier_mount_receipts_set_updated_at",
    "create trigger service_health_snapshots_set_updated_at",
]

LIVE_BASELINE_SNIPPETS = [
    'create table if not exists "ion_ops"."automation_events"',
    '"event_id" "uuid" default "gen_random_uuid"() not null',
    '"accepted_state_claim" boolean default false not null',
    '"settlement_required" boolean default true not null',
    'create table if not exists "ion_ops"."carrier_mount_receipts"',
    '"mount_receipt_id" "uuid" default "gen_random_uuid"() not null',
    '"accepted_state_authority" boolean default false not null',
    '"write_scope" "jsonb" default \'[]\'::"jsonb" not null',
    'create table if not exists "ion_ops"."service_health_snapshots"',
    '"snapshot_id" "uuid" default "gen_random_uuid"() not null',
    '"service_role" "text"',
    '"endpoint" "text"',
    '"host" "text"',
    '"pid" integer',
    '"verdict" "text"',
    '"version_line" "text"',
    '"findings" "jsonb" default \'[]\'::"jsonb" not null',
]

REQUIRED_002_SNIPPETS = [
    "create policy automation_events_authenticated_read",
    "create policy carrier_mount_receipts_authenticated_read",
    "create policy service_health_snapshots_authenticated_read",
    "to authenticated",
    "for select",
]

REQUIRED_003_SNIPPETS = [
    "create or replace function ion_ops.assert_ion_authority",
    "create or replace function ion_ops.reject_accepted_state_claim",
    "create or replace function ion_ops.ion_ops_rpc_authority",
    "create or replace function ion_ops.ion_ops_record_automation_event",
    "returns ion_ops.automation_events",
    "p_event_id uuid default gen_random_uuid()",
    "payload = excluded.payload",
    "create or replace function ion_ops.ion_ops_record_service_health_snapshot",
    "returns ion_ops.service_health_snapshots",
    "p_snapshot_id uuid default gen_random_uuid()",
    "service_role = excluded.service_role",
    "endpoint = excluded.endpoint",
    "host = excluded.host",
    "pid = excluded.pid",
    "verdict = excluded.verdict",
    "version_line = excluded.version_line",
    "findings = excluded.findings",
    "create or replace function ion_ops.ion_ops_record_carrier_mount_receipt",
    "returns ion_ops.carrier_mount_receipts",
    "p_mount_receipt_id uuid default gen_random_uuid()",
    "mount_receipt_id",
    "write_scope = excluded.write_scope",
    "accepted_state_claim_default', false",
    "direct_table_write_for_authenticated', false",
    "rejected accepted_state_claim=true",
    "rejected accepted_state_authority=true",
    "rejected production_authority=true",
    "rejected live_execution_authority=true",
]

SECRET_KEY_PATTERNS = [
    re.compile(r"supabase[_-]?service[_-]?role[_-]?key\s*[:=]\s*['\"]?eyJ", re.IGNORECASE),
    re.compile(r"service_role\s*[:=]\s*['\"]?eyJ", re.IGNORECASE),
]

SCAN_TEXT_PATHS = [
    REPO_ROOT / "supabase",
    REPO_ROOT / "ION" / "docs" / "setup",
    REPO_ROOT / "ION" / "02_architecture",
]


def _read_lower(path: Path) -> str:
    return path.read_text(encoding="utf-8").lower()


def _missing(sql: str, snippets: list[str]) -> list[str]:
    return [snippet for snippet in snippets if snippet.lower() not in sql]


def _iter_scanned_files() -> list[Path]:
    files: list[Path] = []
    for root in SCAN_TEXT_PATHS:
        if root.is_file():
            files.append(root)
            continue
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.name.startswith(".env"):
                continue
            if path.suffix.lower() not in {".sql", ".py", ".md", ".json", ".yaml", ".yml", ".txt"}:
                continue
            files.append(path)
    return files


def _tracked_env_files() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [line for line in result.stdout.splitlines() if Path(line).name.startswith(".env")]


def main() -> int:
    for path in [MIGRATION_001, MIGRATION_002, MIGRATION_003, SEED, LIVE_SNAPSHOT, *DOCS]:
        if not path.exists():
            print(f"missing required file: {path.relative_to(REPO_ROOT)}")
            return 1

    sql_001 = _read_lower(MIGRATION_001)
    sql_002 = _read_lower(MIGRATION_002)
    sql_003 = _read_lower(MIGRATION_003)
    live_sql = _read_lower(LIVE_SNAPSHOT)

    missing_001 = _missing(sql_001, REQUIRED_001_SNIPPETS)
    missing_live = _missing(live_sql, LIVE_BASELINE_SNIPPETS)
    missing_002 = _missing(sql_002, REQUIRED_002_SNIPPETS)
    missing_003 = _missing(sql_003, REQUIRED_003_SNIPPETS)
    if missing_001 or missing_live or missing_002 or missing_003:
        print("missing required migration/live snippets:")
        for label, missing in [
            ("001", missing_001),
            ("live", missing_live),
            ("002", missing_002),
            ("003", missing_003),
        ]:
            for snippet in missing:
                print(f"- {label}: {snippet}")
        return 1

    if "to authenticated" in sql_001 or "grant select on all tables in schema ion_ops to authenticated" in sql_001:
        print("001 contains broad authenticated read posture; it must stay split into 002")
        return 1

    forbidden_defaults = [
        "accepted_state_claim', true",
        "accepted_state_claim\": true",
        "accepted_state_authority', true",
        "accepted_state_authority\": true",
        "production_authority', true",
        "live_execution_authority', true",
    ]
    combined = "\n".join([sql_001, sql_002, sql_003, _read_lower(SEED)])
    for forbidden in forbidden_defaults:
        if forbidden in combined:
            print(f"forbidden authority default found: {forbidden}")
            return 1

    seed_sql = _read_lower(SEED)
    if "development/bootstrap seed" not in seed_sql:
        print("seed file is missing bootstrap/development warning")
        return 1
    if "on conflict" not in seed_sql:
        print("seed file should be replay-safe with on conflict")
        return 1
    for required_seed in ["event_id", "mount_receipt_id", "snapshot_id", "accepted_state_claim", "production_authority", "live_execution_authority"]:
        if required_seed not in seed_sql:
            print(f"seed file missing live-schema field: {required_seed}")
            return 1

    tracked_env = _tracked_env_files()
    if tracked_env:
        print("tracked env files are not allowed:")
        for path in tracked_env:
            print(f"- {path}")
        return 1

    for path in _iter_scanned_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_KEY_PATTERNS:
            if pattern.search(text):
                print(f"possible Supabase service_role key found in {path.relative_to(REPO_ROOT)}")
                return 1

    print("ion_ops Supabase live-baseline migrations static validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
