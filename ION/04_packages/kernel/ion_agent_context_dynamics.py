"""ION Agent Context Dynamics and Front-Door Team Planning.

V91 adds the missing planning layer between static Agent Context System cards and
runtime Cursor task packages. V81/V82 made per-agent context systems visible to
spawn packages; this module makes the next question explicit: which context
layers should be alive for this turn, how deep should each role load, what is the
rough context budget, and which front-door roles should participate before the
user sees output.

The module is intentionally dependency-light and file-backed. It emits JSON that
Cursor, the JOC cockpit, or the SDK carrier can inspect without relying on chat
memory.
"""

from __future__ import annotations

import argparse
import json
import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ACTIVE_CONTEXT_WINDOW_PLAN = Path("ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json")
ACTIVE_FRONT_DOOR_TEAM_PLAN = Path("ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json")
REGISTRY_PATH = Path("ION/03_registry/agent_context_dynamics_registry.yaml")
AGENT_CONTEXT_SYSTEM_REGISTRY = Path("ION/03_registry/agent_context_system_registry.yaml")
AGENT_CONTEXT_SYSTEM_INDEX = Path("ION/05_context/current/agent_context_systems/AGENT_CONTEXT_SYSTEMS_INDEX.md")

CONTEXT_SYSTEM_CARD_DIR = Path("ION/05_context/current/agent_context_systems")
CURRENT_DIR = Path("ION/05_context/current")

CHAR_PER_TOKEN_ESTIMATE = 4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _shell_root(root: str | Path) -> Path:
    candidate = Path(root).expanduser().resolve()
    if candidate.name == "ION":
        return candidate.parent
    return candidate


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_text(path: Path, limit: int = 12000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    return text[:limit]


def _sha256(path: Path) -> str | None:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _exists_summary(root: Path, rel: str | Path) -> dict[str, Any]:
    rel_path = Path(rel)
    path = root / rel_path
    result: dict[str, Any] = {
        "path": str(rel_path).replace("\\", "/"),
        "exists": path.exists(),
        "kind": "missing",
    }
    if path.is_file():
        text = _read_text(path)
        result.update(
            {
                "kind": "file",
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "line_count": text.count("\n") + (0 if text.endswith("\n") or text == "" else 1),
                "first_line": next((ln.strip() for ln in text.splitlines() if ln.strip()), ""),
            }
        )
    elif path.is_dir():
        try:
            sample = sorted(p.name for p in path.iterdir())[:25]
        except Exception:
            sample = []
        result.update({"kind": "directory", "entry_count_sampled": len(sample), "entries_sample": sample})
    return result


@dataclass(frozen=True)
class RoleContextProfile:
    role: str
    display_name: str
    lane: str
    primary_function: str
    default_budget_class: str
    min_chars: int
    normal_chars: int
    deep_chars: int
    active_when: tuple[str, ...]
    route_deeper_surfaces: tuple[str, ...]
    forbidden_conflations: tuple[str, ...]
    timeline_lane: str

    def budget_for_depth(self, depth: str) -> dict[str, int | str]:
        depth = depth if depth in {"minimum", "normal", "deep"} else "normal"
        chars = {"minimum": self.min_chars, "normal": self.normal_chars, "deep": self.deep_chars}[depth]
        return {
            "depth": depth,
            "max_chars": chars,
            "estimated_tokens": max(1, chars // CHAR_PER_TOKEN_ESTIMATE),
        }


ROLE_PROFILES: dict[str, RoleContextProfile] = {
    "persona_interface": RoleContextProfile(
        role="persona_interface",
        display_name="PERSONA_INTERFACE",
        lane="user-facing expression",
        primary_function="Render accepted Relay/Steward state into user-facing discourse without pretending to be the whole system.",
        default_budget_class="compact_user_facing",
        min_chars=8000,
        normal_chars=18000,
        deep_chars=36000,
        active_when=("final_user_output", "relationship_continuity_needed", "operator_confusion", "tone_or_delivery_needed"),
        route_deeper_surfaces=(
            "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md",
            "ION/02_architecture/PERSONA_CONTEXT_BUDGET_AND_HORIZON_PROTOCOL.md",
            "ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md",
        ),
        forbidden_conflations=("STEWARD", "RELAY", "carrier_control", "global_authority"),
        timeline_lane="front_door_output",
    ),
    "relay": RoleContextProfile(
        role="relay",
        display_name="RELAY",
        lane="packetization and semantic relay",
        primary_function="Transform user/persona exchange into system-ready intent and accepted system output into persona-ready packets.",
        default_budget_class="packet_digest",
        min_chars=10000,
        normal_chars=22000,
        deep_chars=52000,
        active_when=("new_operator_message", "handoff_needed", "digest_needed", "user_output_preparation"),
        route_deeper_surfaces=(
            "ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md",
            "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md",
            "ION/07_templates/bindings/RELAY__HANDOFF.md",
        ),
        forbidden_conflations=("STEWARD", "PERSONA_INTERFACE", "doctrine_authority", "raw_worker_acceptance"),
        timeline_lane="relay_packets",
    ),
    "steward": RoleContextProfile(
        role="steward",
        display_name="STEWARD",
        lane="orchestration and integration authority",
        primary_function="Route work, manage gates, accept/reject specialist returns, and integrate accepted state.",
        default_budget_class="orchestration_authority",
        min_chars=16000,
        normal_chars=42000,
        deep_chars=96000,
        active_when=("continuation", "new_work_directive", "accepted_task_return", "gate_resolution", "integration_needed"),
        route_deeper_surfaces=(
            "ION/02_architecture/STEWARD_CURRENT_PHASE_ORCHESTRATION_PROTOCOL.md",
            "ION/02_architecture/HORIZON_ORCHESTRATION_PROTOCOL.md",
            "ION/02_architecture/BRANCH_BUDGET_RECURSION_AND_DRIFT_CONTROL_PROTOCOL.md",
            "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        ),
        forbidden_conflations=("carrier_control_surface", "raw_cursor_parent_chat", "persona_expression"),
        timeline_lane="steward_integration",
    ),
    "context_cartographer": RoleContextProfile(
        role="context_cartographer",
        display_name="CONTEXT_CARTOGRAPHER",
        lane="context graph and package compiler",
        primary_function="Compile role-specific active context windows, route-deeper maps, and context-load receipts.",
        default_budget_class="context_compiler",
        min_chars=14000,
        normal_chars=36000,
        deep_chars=110000,
        active_when=("context_drift", "new_agent_package", "large_objective", "route_deeper_needed"),
        route_deeper_surfaces=(
            "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md",
            "ION/03_registry/agent_context_system_registry.yaml",
            "ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md",
            "ION/07_templates/context/AGENT_CONTEXT_PACKAGE_INDEX.md",
        ),
        forbidden_conflations=("global_orchestration_authority", "user_facing_persona"),
        timeline_lane="context_compilation",
    ),
    "runtime_cartographer": RoleContextProfile(
        role="runtime_cartographer",
        display_name="RUNTIME_CARTOGRAPHER",
        lane="runtime map and carrier workflow",
        primary_function="Map how ION actually runs across kernel, carrier, hooks, commands, SDK, queues, and audits.",
        default_budget_class="runtime_compiler",
        min_chars=14000,
        normal_chars=36000,
        deep_chars=90000,
        active_when=("carrier_confusion", "workflow_audit", "cursor_hook", "sdk_runner", "extension_work"),
        route_deeper_surfaces=(
            "ION/02_architecture/ION_CURSOR_CARRIER_CONTINUATION_WORKFLOW_PROTOCOL.md",
            "ION/02_architecture/ION_CURSOR_MAIN_AGENT_TOPOLOGY_PROTOCOL.md",
            "ION/02_architecture/ION_CURSOR_SDK_HOOK_BRIDGE_PROTOCOL.md",
            "ION/04_packages/kernel/ion_carrier_continue.py",
        ),
        forbidden_conflations=("steward_integration_authority", "persona_output"),
        timeline_lane="runtime_mapping",
    ),
    "ionologist": RoleContextProfile(
        role="ionologist",
        display_name="IONOLOGIST",
        lane="living ION definition",
        primary_function="Maintain what ION is, how it should be described, and whether new work changes the ontology of ION.",
        default_budget_class="definition_context",
        min_chars=16000,
        normal_chars=42000,
        deep_chars=120000,
        active_when=("definition_change", "ontology_drift", "encyclopedia_update", "semantic_conflict"),
        route_deeper_surfaces=(
            "ION/02_architecture/ION_CONTEXT_AUTHORITY_TEAM_PROTOCOL.md",
            "ION/01_doctrine/SOVEREIGN_CONSTITUTION.md",
            "ION/01_doctrine/SOVEREIGN_KERNEL.md",
            "ION/02_architecture/META_TEMPLATE_CONSTITUTION_PROTOCOL.md",
        ),
        forbidden_conflations=("implementation_worker", "visual_dashboard_only"),
        timeline_lane="ion_definition",
    ),
    "canon_librarian": RoleContextProfile(
        role="canon_librarian",
        display_name="CANON_LIBRARIAN",
        lane="authority lineage and stale-surface classification",
        primary_function="Classify live, donor, stale, archive, receipt, projection, and false-primary surfaces.",
        default_budget_class="authority_lineage",
        min_chars=12000,
        normal_chars=30000,
        deep_chars=90000,
        active_when=("branch_consolidation", "archive_boundary", "stale_context_risk", "release_package"),
        route_deeper_surfaces=(
            "ION/02_architecture/ACTIVE_SURFACE_RETIREMENT_PROTOCOL.md",
            "ION/02_architecture/CANON_PROMOTION_AND_RATIFICATION_PROTOCOL.md",
            "ION/02_architecture/ION_PRODUCTIZED_RUNTIME_BOUNDARY_PROTOCOL.md",
        ),
        forbidden_conflations=("live_runtime_executor", "persona_output"),
        timeline_lane="canon_lineage",
    ),
    "template_curator": RoleContextProfile(
        role="template_curator",
        display_name="TEMPLATE_CURATOR",
        lane="template and receipt-shape governance",
        primary_function="Select, evolve, and audit the templates used by agents for bounded steps and context evolution.",
        default_budget_class="template_surface",
        min_chars=10000,
        normal_chars=26000,
        deep_chars=76000,
        active_when=("template_change", "receipt_shape_change", "context_template_needed"),
        route_deeper_surfaces=(
            "ION/07_templates/context/AGENT_CONTEXT_SYSTEM_CARD.md",
            "ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md",
            "ION/07_templates/context/ION_CONTEXT_DELTA_RECEIPT.md",
        ),
        forbidden_conflations=("doctrine_owner", "implementation_worker_without_route"),
        timeline_lane="template_evolution",
    ),
    "mason": RoleContextProfile(
        role="mason",
        display_name="MASON",
        lane="bounded implementation",
        primary_function="Implement exact scoped file changes and tests under an allowed mutation surface.",
        default_budget_class="implementation_context",
        min_chars=12000,
        normal_chars=32000,
        deep_chars=70000,
        active_when=("code_patch", "test_patch", "extension_scaffold", "kernel_module"),
        route_deeper_surfaces=("ION/07_templates/bindings/MASON__CODE.md", "ION/07_templates/actions/CODE.md"),
        forbidden_conflations=("architecture_authority", "doctrine_authority", "steward_integration"),
        timeline_lane="implementation",
    ),
    "nemesis": RoleContextProfile(
        role="nemesis",
        display_name="NEMESIS",
        lane="audit and adversarial review",
        primary_function="Pressure claims, validation, authority, safety, and release readiness independently.",
        default_budget_class="audit_context",
        min_chars=12000,
        normal_chars=30000,
        deep_chars=82000,
        active_when=("audit_needed", "release_candidate", "false_claim_risk", "proof_gap"),
        route_deeper_surfaces=("ION/07_templates/bindings/NEMESIS__AUDIT.md", "ION/07_templates/reports/AUDIT.md"),
        forbidden_conflations=("authoring_authority", "steward_integration"),
        timeline_lane="audit",
    ),
    "vizier": RoleContextProfile(
        role="vizier",
        display_name="VIZIER",
        lane="architecture and scope strategy",
        primary_function="Analyze architecture implications, dependency surfaces, and strategic sequence without silently patching code.",
        default_budget_class="architecture_context",
        min_chars=12000,
        normal_chars=34000,
        deep_chars=90000,
        active_when=("architecture_decision", "scope_risk", "system_design", "sequence_planning"),
        route_deeper_surfaces=("ION/02_architecture/", "ION/07_templates/bindings/STEWARD__PROPOSAL.md"),
        forbidden_conflations=("implementation_worker", "final_user_persona"),
        timeline_lane="architecture",
    ),
    "vestige": RoleContextProfile(
        role="vestige",
        display_name="VESTIGE",
        lane="provenance and recovery",
        primary_function="Recover lineage, classify donor/history material, and prevent stale authority promotion.",
        default_budget_class="recovery_context",
        min_chars=12000,
        normal_chars=30000,
        deep_chars=100000,
        active_when=("recovery", "donor_branch", "lost_context", "archive_review"),
        route_deeper_surfaces=("ION/06_intelligence/archaeology/vestige/", "ION/02_architecture/ACTIVE_SURFACE_RETIREMENT_PROTOCOL.md"),
        forbidden_conflations=("canon_promotion_without_review", "current_runtime_authority"),
        timeline_lane="provenance",
    ),
    "thoth": RoleContextProfile(
        role="thoth",
        display_name="THOTH",
        lane="research and reasoning synthesis",
        primary_function="Perform non-mutating reasoning, analysis, evidence synthesis, and conceptual decomposition.",
        default_budget_class="reasoning_context",
        min_chars=12000,
        normal_chars=32000,
        deep_chars=90000,
        active_when=("research_question", "deep_reasoning", "conceptual_analysis"),
        route_deeper_surfaces=("ION/07_templates/reports/", "ION/02_architecture/AGENT_REASONING_PROTOCOL.md"),
        forbidden_conflations=("mutation_authority", "steward_acceptance"),
        timeline_lane="reasoning",
    ),
    "scribe": RoleContextProfile(
        role="scribe",
        display_name="SCRIBE",
        lane="documentation and receipt projection",
        primary_function="Write reports, receipts, manifests, and docs from accepted state without inventing validation.",
        default_budget_class="documentation_context",
        min_chars=10000,
        normal_chars=26000,
        deep_chars=64000,
        active_when=("report_needed", "receipt_needed", "artifact_manifest", "release_notes"),
        route_deeper_surfaces=("ION/docs/consolidation/", "ION/05_context/signals/", "ION/07_templates/reports/"),
        forbidden_conflations=("validation_runner", "steward_authority"),
        timeline_lane="documentation",
    ),
    "vice": RoleContextProfile(
        role="vice",
        display_name="VICE",
        lane="contradiction pressure and future answerability",
        primary_function="Track unresolved dissent, contradictions, future risk, and brittle assumptions.",
        default_budget_class="contradiction_context",
        min_chars=10000,
        normal_chars=26000,
        deep_chars=70000,
        active_when=("dissent_needed", "risk_review", "future_answerability", "contradiction"),
        route_deeper_surfaces=("ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md",),
        forbidden_conflations=("final_decision_authority", "implementation_worker"),
        timeline_lane="dissent",
    ),
    "atlas": RoleContextProfile(
        role="atlas",
        display_name="ATLAS",
        lane="external systems reference",
        primary_function="Map external models, APIs, providers, and reference systems by evidence tier without becoming ION continuity authority.",
        default_budget_class="external_reference",
        min_chars=10000,
        normal_chars=26000,
        deep_chars=72000,
        active_when=("external_provider", "api_model_route", "integration_reference"),
        route_deeper_surfaces=("ION/02_architecture/MODEL_ROUTING_AND_PROVIDER_ECONOMICS_PROTOCOL.md", "ION/03_registry/model_*"),
        forbidden_conflations=("internal_continuity_authority", "steward_integration"),
        timeline_lane="external_reference",
    ),
}


KEYWORD_ROLE_TRIGGERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("ui", ("vizier", "mason", "runtime_cartographer", "scribe")),
    ("cockpit", ("vizier", "mason", "runtime_cartographer", "scribe")),
    ("extension", ("runtime_cartographer", "mason", "nemesis")),
    ("cursor", ("runtime_cartographer", "steward", "nemesis")),
    ("context", ("context_cartographer", "steward", "ionologist")),
    ("agent", ("context_cartographer", "steward", "runtime_cartographer")),
    ("workflow", ("runtime_cartographer", "steward", "relay")),
    ("audit", ("nemesis", "scribe")),
    ("test", ("mason", "nemesis")),
    ("zip", ("scribe", "canon_librarian", "nemesis")),
    ("archive", ("canon_librarian", "vestige")),
    ("persona", ("persona_interface", "relay", "steward")),
    ("relay", ("relay", "steward")),
    ("steward", ("steward", "relay")),
    ("gate", ("steward", "relay", "nemesis")),
    ("continue", ("steward", "runtime_cartographer")),
    ("proceed", ("steward", "runtime_cartographer")),
)


def classify_message(text: str, open_gate_count: int = 0) -> str:
    lowered = (text or "").strip().lower()
    if not lowered:
        return "status_request"
    if open_gate_count and lowered in {"yes", "no", "approve", "approved", "allow", "deny", "option a", "option b", "continue"}:
        return "human_gate_answer"
    if lowered in {"continue", "proceed", "resume", "keep going", "next"}:
        return "continuation_signal"
    if any(token in lowered for token in ("what is", "status", "where are we", "explain", "how does")):
        return "status_or_design_request"
    return "new_work_directive"


def _selected_depth(role: str, classification: str, text: str, open_gate_count: int) -> str:
    lowered = (text or "").lower()
    if role in {"steward", "context_cartographer", "runtime_cartographer", "ionologist"} and any(
        w in lowered for w in ("truly", "full", "maximum", "deep", "long horizon", "context system", "workflow")
    ):
        return "deep"
    if open_gate_count and role in {"steward", "relay", "persona_interface"}:
        return "normal"
    if classification == "continuation_signal" and role in {"steward", "runtime_cartographer"}:
        return "normal"
    if classification == "status_or_design_request" and role in {"persona_interface", "relay"}:
        return "minimum"
    return "normal"


def _activation_reason(role: str, classification: str, text: str, queues: dict[str, Any]) -> tuple[str, ...]:
    reasons: list[str] = []
    if role in {"steward", "relay", "persona_interface"}:
        reasons.append("front_door_triad")
    if classification == "continuation_signal" and role in {"steward", "runtime_cartographer"}:
        reasons.append("continuation_signal")
    if classification == "human_gate_answer" and role in {"steward", "relay", "persona_interface"}:
        reasons.append("human_gate_resolution")
    lowered = (text or "").lower()
    for keyword, roles in KEYWORD_ROLE_TRIGGERS:
        if keyword in lowered and role in roles:
            reasons.append(f"keyword:{keyword}")
    if queues.get("steward_pending", 0) and role == "steward":
        reasons.append("accepted_returns_waiting_for_integration")
    if queues.get("operator_pending", 0) and role in {"steward", "relay"}:
        reasons.append("operator_queue_pending")
    if queues.get("human_gates_open", 0) and role in {"steward", "relay", "persona_interface"}:
        reasons.append("human_gate_open")
    return tuple(dict.fromkeys(reasons))


def _queue_counts(root: Path) -> dict[str, int]:
    opq = _read_json(root / CURRENT_DIR / "ACTIVE_OPERATOR_MESSAGE_QUEUE.json") or {}
    gates = _read_json(root / CURRENT_DIR / "ACTIVE_HUMAN_GATE_QUEUE.json") or {}
    steward = _read_json(root / CURRENT_DIR / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json") or {}
    ledger = _read_json(root / CURRENT_DIR / "ACTIVE_CARRIER_TASK_RETURN_LEDGER.json") or {}

    def _items(obj: Any, keys: Iterable[str]) -> list[Any]:
        if isinstance(obj, list):
            return obj
        if isinstance(obj, dict):
            for k in keys:
                v = obj.get(k)
                if isinstance(v, list):
                    return v
        return []

    operator_items = _items(opq, ("items", "operator_messages", "queue"))
    gate_items = _items(gates, ("gates", "items", "human_gates"))
    steward_items = _items(steward, ("accepted_returns", "items", "queue"))
    returns = _items(ledger, ("returns", "items", "records"))
    open_gates = [g for g in gate_items if str(g.get("status", "open")).lower() not in {"resolved", "closed"}] if gate_items and isinstance(gate_items[0], dict) else gate_items
    pending_op = [i for i in operator_items if not isinstance(i, dict) or str(i.get("status", "pending")).lower() in {"pending", "queued"}]
    accepted_returns = [r for r in returns if isinstance(r, dict) and str(r.get("decision", r.get("status", ""))).lower() == "accepted"]
    rejected_returns = [r for r in returns if isinstance(r, dict) and "reject" in str(r.get("decision", r.get("status", ""))).lower()]
    return {
        "operator_pending": len(pending_op),
        "human_gates_open": len(open_gates),
        "steward_pending": len(steward_items),
        "returns_accepted": len(accepted_returns),
        "returns_rejected": len(rejected_returns),
        "returns_total": len(returns),
    }


def build_front_door_team_plan(root: str | Path, *, operator_message: str = "") -> dict[str, Any]:
    root_path = _shell_root(root)
    queues = _queue_counts(root_path)
    classification = classify_message(operator_message, queues["human_gates_open"])
    return {
        "schema_id": "ion.front_door_team_plan.v1",
        "created_at": _now(),
        "operator_message_classification": classification,
        "main_cursor_identity": {
            "name": "CURSOR_CARRIER_CONTROL_SURFACE",
            "is_ion_role": False,
            "must_not_claim_roles": ["STEWARD", "RELAY", "PERSONA_INTERFACE"],
            "duty": "Run kernel commands, execute generated carrier turn packets, capture returns, and report accepted state.",
        },
        "front_door_triad": [
            {
                "role": "relay",
                "display_name": "RELAY",
                "activation": "logical_resident_spawn_when_intent_or_output_packet_needed",
                "duty": "compile operator intent and package accepted internal state",
                "does_not": "orchestrate globally or integrate raw worker returns",
            },
            {
                "role": "steward",
                "display_name": "STEWARD",
                "activation": "spawn_when_routing_integration_gate_or_long_horizon_direction_needed",
                "duty": "route work, direct team, manage gates, integrate accepted returns",
                "does_not": "speak as persona or accept unproofed returns",
            },
            {
                "role": "persona_interface",
                "display_name": "PERSONA_INTERFACE",
                "activation": "spawn_or_compile_when_final_user_facing_answer_needed",
                "duty": "render accepted state honestly for the operator",
                "does_not": "own orchestration, implementation, audit, or doctrine",
            },
        ],
        "no_user_upkeep_law": {
            "statement": "The user must not be asked to manage ION upkeep, choose routine agents, refresh packets, or organize context. The carrier-control surface and STEWARD do that unless a human gate is explicit.",
            "allowed_user_requests": ["human_gate_resolution", "preference_or_direction", "credential_or_external_permission", "scope_authorization"],
            "forbidden_user_requests": ["which_agent_should_i_spawn", "please_refresh_context_manually", "please_update_ION_upkeep_files", "please_choose_sequence_when_packet_exists"],
        },
        "sequence": [
            "carrier_control_classifies_message",
            "carrier_control_runs_ion_carrier_continue",
            "RELAY packages intent when new user meaning must be transformed",
            "STEWARD routes objective and spawns specialist roles via generated context packages",
            "carrier slots return through proof-gated intake",
            "STEWARD integrates accepted returns only",
            "RELAY packages accepted state",
            "PERSONA_INTERFACE renders final user-facing output",
        ],
        "blocking_rule": "If ACTIVE_HUMAN_GATE_QUEUE has an open blocking gate, do not spawn ordinary work rows until the gate is resolved.",
        "queue_counts": queues,
        "active_files": {
            "operator_queue": str(CURRENT_DIR / "ACTIVE_OPERATOR_MESSAGE_QUEUE.json"),
            "human_gate_queue": str(CURRENT_DIR / "ACTIVE_HUMAN_GATE_QUEUE.json"),
            "carrier_turn_packet": str(CURRENT_DIR / "ACTIVE_CARRIER_TURN_PACKET.json"),
            "steward_queue": str(CURRENT_DIR / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json"),
        },
    }


def build_agent_context_window_plan(
    root: str | Path,
    *,
    operator_message: str = "",
    roles: Iterable[str] | None = None,
    write: bool = False,
) -> dict[str, Any]:
    root_path = _shell_root(root)
    queues = _queue_counts(root_path)
    classification = classify_message(operator_message, queues["human_gates_open"])
    role_list = [r.lower().strip() for r in (roles or ROLE_PROFILES.keys()) if r and r.lower().strip() in ROLE_PROFILES]
    selected: list[dict[str, Any]] = []
    dormant: list[str] = []

    for role in role_list:
        profile = ROLE_PROFILES[role]
        reasons = _activation_reason(role, classification, operator_message, queues)
        depth = _selected_depth(role, classification, operator_message, queues["human_gates_open"])
        lease = "active" if reasons else "warm" if role in {"persona_interface", "relay", "steward"} else "dormant"
        if lease == "dormant":
            dormant.append(role)
        card_rel = CONTEXT_SYSTEM_CARD_DIR / f"{profile.display_name}.context_system.md"
        card_summary = _exists_summary(root_path, card_rel)
        selected.append(
            {
                "role": role,
                "display_name": profile.display_name,
                "lane": profile.lane,
                "primary_function": profile.primary_function,
                "attention_lease": lease,
                "activation_reasons": list(reasons),
                "budget": profile.budget_for_depth(depth),
                "timeline_lane": profile.timeline_lane,
                "context_layers": [
                    {"layer": "semantic_identity", "status": "required", "purpose": "true name, role class, authority ceiling"},
                    {"layer": "agent_context_system_card", "status": "required", "path": str(card_rel), "surface": card_summary},
                    {"layer": "active_runtime_state", "status": "required", "paths": [str(CURRENT_DIR / "ACTIVE_WORK_PACKET.json"), str(CURRENT_DIR / "ACTIVE_CARRIER_TURN_PACKET.json")]},
                    {"layer": "mission_active_context", "status": "compiled_per_spawn_row", "purpose": "loaded context for current bounded objective"},
                    {"layer": "route_deeper_map", "status": "available", "paths": list(profile.route_deeper_surfaces)},
                    {"layer": "receipt_and_return_contract", "status": "required", "purpose": "CONTEXT PROOF, task-return intake, Steward queue"},
                    {"layer": "timeline_delta", "status": "planned", "purpose": "record what changed since prior active package"},
                ],
                "route_deeper_surfaces": list(profile.route_deeper_surfaces),
                "forbidden_conflations": list(profile.forbidden_conflations),
                "dynamic_rule": "Load the smallest package that can satisfy the immediate objective; deepen only when the active package exposes contradiction, missing evidence, or route-deeper trigger.",
                "drift_controls": [
                    "context_system_surfaces_before_MINI_CAPSULE",
                    "context_proof_gate",
                    "task_return_intake",
                    "steward_integration_queue_only",
                    "human_gate_queue_blocks_when_open",
                ],
            }
        )

    front_door = build_front_door_team_plan(root_path, operator_message=operator_message)
    plan = {
        "schema_id": "ion.agent_context_window_plan.v1",
        "created_at": _now(),
        "operator_message": operator_message,
        "operator_message_classification": classification,
        "summary": {
            "current_state": "V91_DYNAMIC_CONTEXT_PLANNING_READY",
            "current_implementation_level": "static agent context systems plus dynamic planning projection",
            "not_yet_full_vision": [
                "no persisted per-agent evolving context timeline yet",
                "no automatic semantic graph traversal/reranking yet",
                "no real token counter from carrier/model provider yet; estimates use chars/4",
                "no autonomous SDK autorun loop wired to this planner yet",
            ],
            "roles_planned": len(selected),
            "dormant_roles": dormant,
        },
        "source_surfaces": {
            "context_dynamics_registry": _exists_summary(root_path, REGISTRY_PATH),
            "agent_context_system_registry": _exists_summary(root_path, AGENT_CONTEXT_SYSTEM_REGISTRY),
            "agent_context_system_index": _exists_summary(root_path, AGENT_CONTEXT_SYSTEM_INDEX),
        },
        "queue_counts": queues,
        "front_door_team_plan": front_door,
        "roles": selected,
        "timeline_model": {
            "planned_file": str(CURRENT_DIR / "ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json"),
            "event_classes": [
                "context_window_planned",
                "context_package_compiled",
                "route_deeper_triggered",
                "context_delta_emitted",
                "task_return_accepted_or_rejected",
                "steward_integrated",
            ],
        },
    }
    if write:
        (root_path / ACTIVE_CONTEXT_WINDOW_PLAN).parent.mkdir(parents=True, exist_ok=True)
        (root_path / ACTIVE_CONTEXT_WINDOW_PLAN).write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (root_path / ACTIVE_FRONT_DOOR_TEAM_PLAN).write_text(json.dumps(front_door, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION dynamic agent context-window and front-door team plans.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--operator-message", default="")
    parser.add_argument("--roles", default="", help="Comma-separated role keys; default all known roles.")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    roles = [r.strip() for r in args.roles.split(",") if r.strip()] or None
    plan = build_agent_context_window_plan(args.ion_root, operator_message=args.operator_message, roles=roles, write=args.write)
    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
    else:
        print("ION_AGENT_CONTEXT_WINDOW_PLAN_READY")
        print(f"classification: {plan['operator_message_classification']}")
        print(f"roles_planned: {plan['summary']['roles_planned']}")
        if args.write:
            print(f"wrote: {ACTIVE_CONTEXT_WINDOW_PLAN}")
            print(f"wrote: {ACTIVE_FRONT_DOOR_TEAM_PLAN}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
