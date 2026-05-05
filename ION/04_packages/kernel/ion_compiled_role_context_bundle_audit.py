"""Audit that every spawned ION role has a physical compiled context bundle."""
from __future__ import annotations
import argparse, json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable
from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_cycle_runner import ACTIVE_SPAWN_PLAN_RELATIVE_PATH

@dataclass
class CompiledRoleBundleAudit:
    audit_id: str
    accepted: bool
    status: str
    checked_roles: list[str]
    findings: list[str]
    active_spawn_plan_path: str
    production_authority: bool = False
    live_execution_authority: bool = False

def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))

def audit_compiled_role_context_bundles(root: str | Path | None = None) -> CompiledRoleBundleAudit:
    shell_root = resolve_shell_root_from_ion_root(root)
    plan_path = shell_root / ACTIVE_SPAWN_PLAN_RELATIVE_PATH
    findings: list[str] = []
    checked: list[str] = []
    if not plan_path.exists():
        findings.append(f'missing_active_spawn_plan:{ACTIVE_SPAWN_PLAN_RELATIVE_PATH}')
        return CompiledRoleBundleAudit('v95_compiled_role_context_bundle_audit', False, 'ION_COMPILED_ROLE_CONTEXT_BUNDLE_BLOCKED', [], findings, str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH))
    plan = _read_json(plan_path)
    rows = plan.get('role_spawn_plan')
    if not isinstance(rows, list) or not rows:
        findings.append('active_spawn_plan_missing_role_spawn_plan')
        rows = []
    for row in rows:
        if row.get('spawn') is not True: continue
        role = str(row.get('role') or 'unknown'); role_upper = role.upper(); checked.append(role)
        context_package = row.get('context_package_path')
        compiled_bundle = row.get('compiled_context_bundle_path')
        receipt = row.get('context_load_receipt_path')
        if not context_package: findings.append(f'{role}:missing_context_package_path')
        elif not (shell_root / str(context_package)).exists(): findings.append(f'{role}:context_package_missing_on_disk:{context_package}')
        if not compiled_bundle:
            findings.append(f'{role}:missing_compiled_context_bundle_path'); continue
        bundle_path = shell_root / str(compiled_bundle)
        if not bundle_path.exists():
            findings.append(f'{role}:compiled_context_bundle_missing_on_disk:{compiled_bundle}'); continue
        text = bundle_path.read_text(encoding='utf-8', errors='replace')
        if f'COMPILED {role_upper} CONTEXT BUNDLE' not in text: findings.append(f'{role}:compiled_context_bundle_missing_role_header')
        if '## Agent Context System authority' not in text: findings.append(f'{role}:compiled_context_bundle_missing_agent_context_system_authority')
        if '### CONTEXT PROOF' not in text: findings.append(f'{role}:compiled_context_bundle_missing_context_proof_contract')
        if context_package and str(context_package) not in text: findings.append(f'{role}:compiled_context_bundle_not_bound_to_context_package_path')
        if receipt and str(receipt) not in text: findings.append(f'{role}:compiled_context_bundle_not_bound_to_receipt_path')
    status = 'ION_COMPILED_ROLE_CONTEXT_BUNDLE_READY' if not findings else 'ION_COMPILED_ROLE_CONTEXT_BUNDLE_BLOCKED'
    return CompiledRoleBundleAudit('v95_compiled_role_context_bundle_audit', not findings, status, checked, findings, str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH))

def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument('--ion-root', default='.'); parser.add_argument('--json', action='store_true'); args = parser.parse_args(list(argv) if argv is not None else None)
    result = audit_compiled_role_context_bundles(args.ion_root)
    if args.json: print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        print(result.status)
        for finding in result.findings: print(f'finding: {finding}')
    return 0 if result.accepted else 1
if __name__ == '__main__': raise SystemExit(main())
