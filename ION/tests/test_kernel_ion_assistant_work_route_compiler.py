import json
from pathlib import Path

import pytest

from kernel import ion_assistant_work_route_compiler as compiler
from kernel.ion_assistant_work_route_compiler import (
    READY_VERDICT,
    SURFACE_SCHEMA_ID,
    UNAVAILABLE_VERDICT,
    build_assistant_work_route_surface,
    compile_assistant_work_route,
)


def _seed_route_compiler(root: Path) -> None:
    registry = root / "ION/05_context/current/ai_assistant_work/registries/AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        """
schema: ion.ai_assistant_work.route_registry.v0_1
status: candidate_current_state_not_accepted_canon
routes:
  - route_id: route.ui_specialist_work
    trigger_patterns:
      - build interface
      - frontend component
      - accessibility
      - ux flow
    required_domains:
      - ui_ux_domain
      - product_requirements_domain
      - implementation_domain
      - testing_quality_domain
    primary_agents:
      - UI_ARCHITECT
      - UX_FLOW_DESIGNER
      - COMPONENT_BUILDER
      - ACCESSIBILITY_AUDITOR
    output_contract:
      include:
        - user flow
        - screen states
        - component contract
        - a11y obligations
      forbid:
        - generic coder guesses UI
        - visual polish without state/a11y proof
  - route_id: route.ide_agent_work_map
    trigger_patterns:
      - codex ide
      - developer ai workflow
    required_domains:
      - ide_work_domain
      - codebase_understanding_domain
    primary_agents:
      - IDE_CARTOGRAPHER
      - PATCH_MASON
    output_contract:
      include:
        - workspace surfaces
        - validation loop
      forbid:
        - coding before workspace/context map
""".strip()
        + "\n",
        encoding="utf-8",
    )
    compiler_dir = root / "ION/05_context/current/ai_assistant_work/route_compiler"
    compiler_dir.mkdir(parents=True, exist_ok=True)
    (compiler_dir / "AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T175230Z.json").write_text(
        json.dumps(
            {
                "schema": "ion.ai_assistant_work.route_compiler_candidate_map.v0_1",
                "status": "candidate_current_context_not_accepted_canon",
                "route_mappings": [
                    {
                        "route_id": "route.ui_specialist_work",
                        "candidate_domains": ["ui_ux_domain"],
                        "candidate_agents": ["UI_ARCHITECT"],
                        "active_skill_candidates": ["codex-solo-work", "template-curation"],
                        "active_lens_candidates": ["vizier", "mason_codex", "nemesis", "persona"],
                        "template_spec_candidates": ["screen_state_matrix_packet"],
                        "active_behavior": "force UI tasks through state matrix and a11y proof",
                        "promotion_target": "new accepted UI specialist route after human review",
                    }
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _seed_lifecycle(root: Path, *, ui_state: str = "proof_gated_candidate", ui_enabled: bool = True) -> None:
    lifecycle = root / "ION/05_context/current/ai_assistant_work/candidate_lifecycle/CANDIDATE_DOMAIN_LIFECYCLE_REGISTRY_V0_1.yaml"
    lifecycle.parent.mkdir(parents=True, exist_ok=True)
    lifecycle.write_text(
        f"""
schema: ion.ai_assistant_work.candidate_lifecycle_registry.v0_1
status: candidate_current_state_not_accepted_canon
lifecycle_records:
  - candidate_id: route.ui_specialist_work
    candidate_type: route
    lifecycle_state: {ui_state}
    route_compiler_enabled: {str(ui_enabled).lower()}
  - candidate_id: route.ide_agent_work_map
    candidate_type: route
    lifecycle_state: operational_candidate
    route_compiler_enabled: true
""".strip()
        + "\n",
        encoding="utf-8",
    )


def test_route_compiler_selects_candidate_ui_route_without_promoting_law(tmp_path: Path):
    if compiler.yaml is None:
        pytest.skip("PyYAML unavailable")
    _seed_route_compiler(tmp_path)
    _seed_lifecycle(tmp_path)

    route = compile_assistant_work_route(
        tmp_path,
        lane_id="codex_general",
        message="Build a frontend UI with accessibility states and a clear drawer flow.",
        response_mode="queue_work",
        selected_skill_id="codex-solo-work",
        execution_mode="queue_for_codex",
    )

    assert route["ok"] is True
    assert route["verdict"] == READY_VERDICT
    assert route["candidate_only"] is True
    assert route["route_id"] == "route.ui_specialist_work"
    assert route["selection_basis"] == "trigger_match"
    assert route["candidate_lifecycle"]["lifecycle_state"] == "proof_gated_candidate"
    assert route["candidate_lifecycle"]["route_compiler_enabled"] is True
    assert "ui_ux_domain" in route["candidate_domains"]
    assert "UI_ARCHITECT" in route["candidate_agents"]
    assert "codex-solo-work" in route["active_skill_candidates"]
    assert "screen_state_matrix_packet" in route["template_spec_candidates"]
    assert "a11y obligations" in route["output_contract"]["include"]
    assert route["authority_boundary"]["mutates_ION_03_registry"] is False
    assert route["authority_boundary"]["mutates_product_front_door"] is False
    assert route["production_authority"] is False


def test_route_compiler_filters_disabled_lifecycle_route(tmp_path: Path):
    if compiler.yaml is None:
        pytest.skip("PyYAML unavailable")
    _seed_route_compiler(tmp_path)
    _seed_lifecycle(tmp_path, ui_state="archived", ui_enabled=False)

    surface = build_assistant_work_route_surface(tmp_path)

    assert surface["ok"] is True
    assert surface["total_route_count"] == 2
    assert surface["route_count"] == 1
    assert surface["inactive_route_ids"] == ["route.ui_specialist_work"]
    assert surface["lifecycle_record_count"] == 2

    route = compile_assistant_work_route(
        tmp_path,
        lane_id="codex_general",
        message="Build a frontend UI with accessibility states and a clear drawer flow.",
        response_mode="queue_work",
        selected_skill_id="codex-solo-work",
        execution_mode="queue_for_codex",
    )

    assert route["ok"] is True
    assert route["route_id"] == "route.ide_agent_work_map"
    assert route["route_id"] != "route.ui_specialist_work"
    assert route["surface"]["inactive_route_ids"] == ["route.ui_specialist_work"]


def test_route_surface_reports_candidate_map_and_missing_registry(tmp_path: Path):
    empty_surface = build_assistant_work_route_surface(tmp_path)

    assert empty_surface["schema_id"] == SURFACE_SCHEMA_ID
    assert empty_surface["ok"] is False
    assert empty_surface["verdict"] == UNAVAILABLE_VERDICT
    assert empty_surface["route_count"] == 0
    assert any("route_registry_missing_or_invalid" in finding for finding in empty_surface["findings"])

    if compiler.yaml is None:
        pytest.skip("PyYAML unavailable")
    _seed_route_compiler(tmp_path)
    _seed_lifecycle(tmp_path)
    ready_surface = build_assistant_work_route_surface(tmp_path)

    assert ready_surface["ok"] is True
    assert ready_surface["route_count"] == 2
    assert ready_surface["total_route_count"] == 2
    assert ready_surface["inactive_route_count"] == 0
    assert ready_surface["lifecycle_record_count"] == 2
    assert ready_surface["mapped_route_count"] == 1
    assert ready_surface["candidate_map_path"].endswith("AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T175230Z.json")
    assert ready_surface["policy"] == "candidate_route_metadata_only_no_registry_or_product_law_mutation"
