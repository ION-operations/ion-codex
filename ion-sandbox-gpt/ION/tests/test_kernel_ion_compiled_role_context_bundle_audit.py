from contextlib import contextmanager
from pathlib import Path

from kernel.ion_compiled_role_context_bundle_audit import audit_compiled_role_context_bundles
from kernel.ion_cycle_runner import build_cycle_plan, write_cycle_plan

ACTIVE_SPAWN_PLAN = Path(__file__).resolve().parents[2] / "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json"


@contextmanager
def preserve_active_spawn_plan():
    original = ACTIVE_SPAWN_PLAN.read_bytes() if ACTIVE_SPAWN_PLAN.exists() else None
    try:
        yield
    finally:
        if original is None:
            ACTIVE_SPAWN_PLAN.unlink(missing_ok=True)
        else:
            ACTIVE_SPAWN_PLAN.parent.mkdir(parents=True, exist_ok=True)
            ACTIVE_SPAWN_PLAN.write_bytes(original)


def test_compiled_context_bundle_exists_for_every_spawned_role(tmp_path):
    with preserve_active_spawn_plan():
        plan = build_cycle_plan(None, workstream='implementation', objective='v95 compiled bundle audit test', spawn_policy='full', execution_root=tmp_path / 'cycle')
        write_cycle_plan(plan, None)
        result = audit_compiled_role_context_bundles(None)
    assert result.accepted, result.findings
    assert 'steward' in result.checked_roles
    assert 'mason' in result.checked_roles
    assert 'nemesis' in result.checked_roles
