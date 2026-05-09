from kernel.ion_persona_response_envelope import (
    READY_VERDICT,
    build_persona_response_envelope,
    format_persona_response_envelope_yaml,
    validate_persona_response_envelope,
)


def test_persona_response_envelope_renders_visible_yaml_without_authority_claims():
    envelope = build_persona_response_envelope(
        visible_persona_name="ION",
        user_response="I can route this through the active assistant-work lane and keep it proof-bound.",
        route={
            "route_id": "route.ide_agent_work_map",
            "selection_basis": "fallback",
            "candidate_domains": ["ide_work_domain"],
            "candidate_agents": ["IDE_CARTOGRAPHER"],
            "dynamic_domain_agent_proposal": {
                "needed": False,
                "candidate_domains": [],
                "candidate_agents": [],
            },
        },
    )

    assert envelope["ok"] is True
    assert envelope["verdict"] == READY_VERDICT
    assert envelope["confidence"]["semantic"]
    assert envelope["gesture"]["semantic"]
    assert envelope["inner_monologue"]["type"] == "operator_visible_persona_signal_not_hidden_reasoning"
    assert envelope["boundaries"]["hidden_chain_of_thought_exposed"] is False
    assert envelope["boundaries"]["production_authority"] is False
    assert envelope["persona"]["persona_is_total_ion"] is False
    assert validate_persona_response_envelope(envelope) == []

    rendered = format_persona_response_envelope_yaml(envelope)

    assert rendered.startswith("```yaml\nion_persona:")
    assert "confidence:" in rendered
    assert "gesture:" in rendered
    assert "inner_monologue:" in rendered
    assert "operator_visible_persona_signal_not_hidden_reasoning" in rendered
    assert "production_authority: false" in rendered
    assert "I can route this through the active assistant-work lane" in rendered


def test_persona_response_envelope_surfaces_dynamic_domain_signal():
    envelope = build_persona_response_envelope(
        user_response="This should become a governed PR specialist route proposal before it lands.",
        certainty="MEDIUM",
        route={
            "route_id": "route.ide_agent_work_map",
            "selection_basis": "trigger_match",
            "candidate_domains": ["ide_work_domain"],
            "candidate_agents": ["PATCH_MASON"],
            "dynamic_domain_agent_proposal": {
                "needed": True,
                "trigger": "fission_candidate_match",
                "lifecycle_state": "operational_candidate",
                "recommended_local_hub_report": True,
                "candidate_domains": [{"domain_id": "pr_agent_work_domain"}],
                "candidate_agents": [{"agent_id": "PR_REVIEW_STEWARD"}, {"agent_id": "CI_EVIDENCE_TRIAGER"}],
            },
        },
    )

    signal = envelope["dynamic_domain_signal"]
    assert signal["needed"] is True
    assert signal["trigger"] == "fission_candidate_match"
    assert signal["candidate_domains"] == ["pr_agent_work_domain"]
    assert "PR_REVIEW_STEWARD" in signal["candidate_agents"]
    assert envelope["confidence"]["level"] == "scoped_expansion"
    assert envelope["dynamic_domain_signal"]["local_hub_report_recommended"] is True
