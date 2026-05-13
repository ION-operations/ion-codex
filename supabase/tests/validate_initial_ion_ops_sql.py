#!/usr/bin/env python3
"""Static validation for ION Supabase migrations.

This intentionally does not connect to Supabase and does not read local .env
files. It validates that the repo-managed SQL keeps the required authority,
RLS, view, policy split, and RPC surfaces present before an operator applies
migrations with Supabase CLI or SQL Editor.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MIGRATION_001 = REPO_ROOT / "supabase" / "migrations" / "001_initial_ion_ops.sql"
MIGRATION_002 = REPO_ROOT / "supabase" / "migrations" / "002_dev_private_cockpit_read_policies.sql"
MIGRATION_003 = REPO_ROOT / "supabase" / "migrations" / "003_ion_ops_authority_and_rpc.sql"
SEED = REPO_ROOT / "supabase" / "seed" / "001_ion_ops_bootstrap_seed.sql"
DOCS = [
    REPO_ROOT / "ION" / "docs" / "setup" / "ION_SUPABASE_OPERATING_RUNTIME_SETUP.md",
    REPO_ROOT / "ION" / "02_architecture" / "ION_SUPABASE_OPERATING_RUNTIME_PROTOCOL_V0_1.md",
]

REQUIRED_001_SNIPPETS = [
    "create schema if not exists ion_ops",
    "create table if not exists ion_ops.automation_events",
    "create table if not exists ion_ops.carrier_mount_receipts",
    "create table if not exists ion_ops.service_health_snapshots",
    "alter table ion_ops.automation_events enable row level security",
    "alter table ion_ops.carrier_mount_receipts enable row level security",
    "alter table ion_ops.service_health_snapshots enable row level security",
    "create policy automation_events_service_write",
    "create policy carrier_mount_receipts_service_write",
    "create policy service_health_snapshots_service_write",
    "create or replace view ion_ops.v_current_carrier_mounts",
    "create or replace view ion_ops.v_latest_service_health",
    "create or replace view ion_ops.v_recent_automation_events",
    "create or replace view ion_ops.v_cockpit_overview",
    "create trigger automation_events_set_updated_at",
    "create trigger carrier_mount_receipts_set_updated_at",
    "create trigger service_health_snapshots_set_updated_at",
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
    "create or replace function ion_ops.ion_ops_record_service_health_snapshot",
    "create or replace function ion_ops.ion_ops_record_carrier_mount_receipt",
    "accepted_state_claim_default', false",
    "direct_table_write_for_authenticated', false",
    "rejected accepted_state_claim=true",
    "rejected accepted_state_authority=true",
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


def main() -> int:
    for path in [MIGRATION_001, MIGRATION_002, MIGRATION_003, SEED, *DOCS]:
        if not path.exists():
            print(f"missing required file: {path.relative_to(REPO_ROOT)}")
            return 1

    sql_001 = _read_lower(MIGRATION_001)
    sql_002 = _read_lower(MIGRATION_002)
    sql_003 = _read_lower(MIGRATION_003)

    missing_001 = _missing(sql_001, REQUIRED_001_SNIPPETS)
    missing_002 = _missing(sql_002, REQUIRED_002_SNIPPETS)
    missing_003 = _missing(sql_003, REQUIRED_003_SNIPPETS)
    if missing_001 or missing_002 or missing_003:
        print("missing required migration snippets:")
        for label, missing in [("001", missing_001), ("002", missing_002), ("003", missing_003)]:
            for snippet in missing:
                print(f"- {label}: {snippet}")
        return 1

    if "to authenticated" in sql_001 or "grant select on all tables in schema ion_ops to authenticated" in sql_001:
        print("001 contains broad authenticated read posture; it must stay split into 002")
        return 1

    if "create policy automation_events_authenticated_read" not in sql_002:
        print("002 does not contain the private cockpit authenticated read policy split")
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

    for path in _iter_scanned_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_KEY_PATTERNS:
            if pattern.search(text):
                print(f"possible Supabase service_role key found in {path.relative_to(REPO_ROOT)}")
                return 1

    print("ion_ops Supabase migrations static validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
