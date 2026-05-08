"""Front-door chat orchestration adapter.

This module connects the executable front-door boundary artifacts to the first
kernel runtime/session and dispatch surfaces.

It is deliberately not an HTTP server, not an LLM caller, and not the full
Steward reasoning loop. It gives browser/API/chat adapters one lawful internal
path:

    user text -> Persona Interface ingress -> Relay semantic-boundary packet
    -> Steward routing envelope -> runtime session queue -> Steward work unit
    -> kernel dispatch packet

and a matching controlled return path:

    Steward/system output -> Relay return package -> Persona response package

The point is to make the Persona / Relay / Steward split operational without
collapsing user-facing style, semantic-boundary translation, and orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .api_runtime_entry import ApiRuntimeEntryGateway, ApiRuntimeEntryResult
from .dispatch import DispatchResult
from .front_door_runtime_entry import (
    FrontDoorIngressResult,
    FrontDoorReturnResult,
    FrontDoorRuntimeGateway,
    PERSONA_INTERFACE_ROLE,
    RELAY_ROLE,
    STEWARD_ROLE,
)
from .graph import KernelGraph
from .id_compaction import compact_identifier
from .index import KernelIndex
from .model import (
    AgentIdentity,
    ContextPackage,
    ContextTiers,
    InputRef,
    InputRefType,
    InputVisibility,
    ScopeType,
    SpawnPolicy,
    TargetFile,
    TierFourSemantic,
    TierOneDoctrine,
    TierThreeMission,
    TierTwoTarget,
    WorkPriority,
    WorkUnit,
    WorkUnitStatus,
)
from .runtime_session_dispatch_binding import (
    RuntimeSessionQueueDispatchResult,
    RuntimeSessionQueueDispatcher,
)
from .runtime_session_store import (
    RuntimeSessionStore,
    SessionQueueItem,
    SessionQueueItemStatus,
)
from .store import KernelStore


FRONT_DOOR_SESSION_STORE_RELATIVE = Path("ION/05_context/history/front_door_runtime_sessions")
KERNEL_STORE_RELATIVE = Path("ION/05_context/history/kernel_store")
FRONT_DOOR_DISPATCH_PACKETS_RELATIVE = Path("ION/05_context/history/front_door_runtime/dispatch_packets")
FRONT_DOOR_CHAT_PROTOCOL_REF = "ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md"
FRONT_DOOR_BOUNDARY_PROTOCOL_REF = "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _short(prefix: str, *parts: str) -> str:
    return f"{prefix}-{compact_identifier('::'.join(part for part in parts if part), empty='front-door-chat', max_length=56)}"


@dataclass(frozen=True)
class FrontDoorChatTurnResult:
    """Result of turning one user message into dispatched Steward work."""

    ingress: FrontDoorIngressResult
    api_entry: ApiRuntimeEntryResult
    steward_work_unit: WorkUnit
    context_package: ContextPackage
    queue_item: SessionQueueItem
    dispatch_result: RuntimeSessionQueueDispatchResult | None


@dataclass(frozen=True)
class FrontDoorChatReturnResult:
    """Result of preparing one system output for Persona Interface delivery."""

    return_result: FrontDoorReturnResult


class FrontDoorChatOrchestrationAdapter:
    """Bridge front-door boundary packets into kernel runtime/session dispatch."""

    def __init__(
        self,
        *,
        front_door_gateway: FrontDoorRuntimeGateway | None = None,
        api_gateway: ApiRuntimeEntryGateway | None = None,
        queue_dispatcher: RuntimeSessionQueueDispatcher | None = None,
    ) -> None:
        self._front_door = front_door_gateway or FrontDoorRuntimeGateway()
        self._api_gateway = api_gateway or ApiRuntimeEntryGateway()
        self._queue_dispatcher = queue_dispatcher or RuntimeSessionQueueDispatcher()

    def submit_user_turn(
        self,
        *,
        workspace_root: str | Path,
        raw_user_text: str,
        session_id: str = "front-door-chat-session",
        user_ref: str = "user.sovereign",
        visible_persona_name: str | None = None,
        relation_context_refs: tuple[str, ...] = (),
        carrier_ref: str = "api://front-door-chat",
        root_authority_ref: str = "ION/00_BOOTSTRAP/ROOT_AUTHORITY_BUNDLE.md",
        created_at: str | None = None,
        dispatch: bool = True,
    ) -> FrontDoorChatTurnResult:
        root = Path(workspace_root).resolve()
        created = created_at or _utc_now()

        ingress = self._front_door.ingest_user_message(
            workspace_root=root,
            raw_user_text=raw_user_text,
            user_ref=user_ref,
            session_id=session_id,
            persona_role_ref=PERSONA_INTERFACE_ROLE,
            relay_role_ref=RELAY_ROLE,
            steward_role_ref=STEWARD_ROLE,
            visible_persona_name=visible_persona_name,
            relation_context_refs=relation_context_refs,
            created_at=created,
        )

        session_store = RuntimeSessionStore(root / FRONT_DOOR_SESSION_STORE_RELATIVE)
        api_entry = self._api_gateway.enter_runtime_session(
            session_store=session_store,
            carrier_ref=carrier_ref,
            session_id=session_id,
            create_session_if_missing=True,
            allow_reentry_if_paused=True,
            root_authority_ref=root_authority_ref,
            label="Front-door chat runtime session",
            purpose="Persona Interface -> Relay -> Steward chat entry",
            context_version=_short("fdctxv", session_id, ingress.relay_packet.packet_id),
            context_ref=f"ION/05_context/history/front_door_runtime/relay_semantic_boundary_packets/{ingress.relay_packet.packet_id}.json",
            requested_at=created,
        )

        kernel_store = KernelStore(root / KERNEL_STORE_RELATIVE)
        index = KernelIndex()
        index.build_from_store(kernel_store)

        work_unit, context_package = self._build_steward_work(
            root=root,
            ingress=ingress,
            raw_user_text=raw_user_text,
            session_id=session_id,
            created_at=created,
        )

        if not kernel_store.exists("context_package", context_package.context_package_id):
            kernel_store.create(context_package)
            index.record_added(context_package)
        if not kernel_store.exists("work_unit", work_unit.work_unit_id):
            kernel_store.create(work_unit)
            index.record_added(work_unit)

        queue_item, _, _ = session_store.add_queue_item(
            session_id,
            work_unit_id=work_unit.work_unit_id,
            payload={
                "front_door_envelope_id": ingress.steward_envelope.envelope_id,
                "relay_packet_id": ingress.relay_packet.packet_id,
                "persona_ingress_id": ingress.persona_ingress.message_id,
                "payload_class": ingress.steward_envelope.payload_class,
                "route_purpose": ingress.steward_envelope.route_purpose,
            },
            status=SessionQueueItemStatus.DISPATCH_READY if dispatch else SessionQueueItemStatus.PENDING,
            item_id=_short("fdq", session_id, work_unit.work_unit_id),
            created_at=created,
        )

        dispatch_result = None
        if dispatch:
            graph = KernelGraph()
            graph.build_from_index(index)
            dispatch_result = self._queue_dispatcher.dispatch_queue_item(
                session_store=session_store,
                kernel_store=kernel_store,
                index=index,
                graph=graph,
                session_id=session_id,
                item_id=queue_item.item_id,
                dispatched_at=created,
                packet_output_path=(
                    root
                    / FRONT_DOOR_DISPATCH_PACKETS_RELATIVE
                    / f"{work_unit.work_unit_id}.dispatch_packet.json"
                ),
            )

        return FrontDoorChatTurnResult(
            ingress=ingress,
            api_entry=api_entry,
            steward_work_unit=work_unit,
            context_package=context_package,
            queue_item=queue_item,
            dispatch_result=dispatch_result,
        )

    def prepare_system_return(
        self,
        *,
        workspace_root: str | Path,
        controlled_system_output: str,
        session_id: str = "front-door-chat-session",
        user_ref: str = "user.sovereign",
        source_system_ref: str = "steward.output",
        visible_persona_name: str | None = None,
        style_notes: tuple[str, ...] = (),
        created_at: str | None = None,
    ) -> FrontDoorChatReturnResult:
        result = self._front_door.prepare_persona_response(
            workspace_root=workspace_root,
            controlled_system_output=controlled_system_output,
            user_ref=user_ref,
            session_id=session_id,
            source_system_ref=source_system_ref,
            persona_role_ref=PERSONA_INTERFACE_ROLE,
            relay_role_ref=RELAY_ROLE,
            steward_role_ref=STEWARD_ROLE,
            visible_persona_name=visible_persona_name,
            style_notes=style_notes,
            created_at=created_at,
        )
        return FrontDoorChatReturnResult(return_result=result)

    def _build_steward_work(
        self,
        *,
        root: Path,
        ingress: FrontDoorIngressResult,
        raw_user_text: str,
        session_id: str,
        created_at: str,
    ) -> tuple[WorkUnit, ContextPackage]:
        work_unit_id = _short("fdwu", session_id, ingress.steward_envelope.envelope_id)
        context_package_id = _short("fdctx", work_unit_id, ingress.relay_packet.packet_id)
        context_version = _short("fdctxv", session_id, ingress.relay_packet.packet_id)
        transition_id = "front_door_relay_to_steward"

        relay_packet_path = (
            f"ION/05_context/history/front_door_runtime/relay_semantic_boundary_packets/"
            f"{ingress.relay_packet.packet_id}.json"
        )
        steward_envelope_path = (
            f"ION/05_context/history/front_door_runtime/steward_routing_envelopes/"
            f"{ingress.steward_envelope.envelope_id}.json"
        )

        agent_identity = AgentIdentity(
            personal_name="Steward",
            role="current-phase orchestration",
            structural_identity=STEWARD_ROLE,
            tier=1,
            domain="orchestration",
            specialty="front-door semantic packet routing",
        )

        target_files = (
            TargetFile(
                path=relay_packet_path,
                content="Relay semantic-boundary packet; raw user wording is not direct system truth.",
                line_count=1,
                language="json",
            ),
            TargetFile(
                path=steward_envelope_path,
                content="Steward routing envelope derived from Relay boundary packet.",
                line_count=1,
                language="json",
            ),
        )

        allowed_writes = (
            "front_door_route_proposal",
            "open_question",
            "generated_state",
            "controlled_system_return",
        )
        allowed_next_actions = (
            "route_to_specialist_or_kernel_surface",
            "ask_clarifying_question",
            "prepare_persona_response",
            "defer_without_fake_completion",
        )
        must_not = (
            "do_not_treat_raw_user_text_as_governed_write",
            "do_not_route_persona_style_as_system_truth",
            "do_not_collapse_persona_relay_steward_roles",
        )

        context_package = ContextPackage(
            context_package_id=context_package_id,
            context_version=context_version,
            compiled_at=created_at,
            work_unit_id=work_unit_id,
            protocol_id=FRONT_DOOR_CHAT_PROTOCOL_REF,
            transition_id=transition_id,
            agent_identity=agent_identity,
            tiers=ContextTiers(
                tier_1_doctrine=TierOneDoctrine(
                    constitution_excerpt=(
                        "Front-door runtime entry preserves Persona Interface, Relay, "
                        "and Steward as separate role planes."
                    ),
                    template_spec=FRONT_DOOR_BOUNDARY_PROTOCOL_REF,
                    kernel_excerpt=(
                        "Relay emits a semantic-boundary packet; Steward routes from "
                        "that packet without treating raw user wording or persona style "
                        "as governed write authority."
                    ),
                ),
                tier_2_target=TierTwoTarget(target_files=target_files),
                tier_3_mission=TierThreeMission(
                    task_payload=raw_user_text,
                    objective=(
                        "Route the Relay semantic-boundary packet to the lawful next "
                        "system action while preserving role separation and authority limits."
                    ),
                    output_schema="front_door_steward_route_or_clarifying_question",
                ),
                tier_4_semantic=TierFourSemantic(
                    semantic_overlays=(),
                    prior_findings=(),
                    open_questions=(),
                ),
            ),
            token_budget=2400,
            actual_tokens=max(1, len(raw_user_text.split())),
            tiers_dropped=(),
            allowed_writes=allowed_writes,
            allowed_next_actions=allowed_next_actions,
            must_not=must_not,
        )

        work_unit = WorkUnit(
            work_unit_id=work_unit_id,
            created_at=created_at,
            protocol_id=FRONT_DOOR_CHAT_PROTOCOL_REF,
            transition_id=transition_id,
            context_version=context_version,
            agent_personal_name="Steward",
            agent_role="current-phase orchestration",
            agent_structural_id=STEWARD_ROLE,
            agent_tier=1,
            agent_domain="orchestration",
            chassis="front_door_chat_orchestration_adapter",
            scope_type=ScopeType.PROJECT,
            scope_ref=f"front-door-session:{session_id}",
            bound_template=FRONT_DOOR_BOUNDARY_PROTOCOL_REF,
            input_refs=(
                InputRef(
                    ref_id=ingress.relay_packet.packet_id,
                    ref_type=InputRefType.STATE_FILE,
                    ref_path=relay_packet_path,
                    visibility=InputVisibility.FULL,
                    required=True,
                ),
                InputRef(
                    ref_id=ingress.steward_envelope.envelope_id,
                    ref_type=InputRefType.STATE_FILE,
                    ref_path=steward_envelope_path,
                    visibility=InputVisibility.FULL,
                    required=True,
                ),
            ),
            context_package_id=context_package_id,
            allowed_writes=allowed_writes,
            allowed_next_actions=allowed_next_actions,
            priority=WorkPriority.P2_NORMAL,
            status=WorkUnitStatus.PENDING,
            must_not=must_not,
            open_questions_in_scope=(),
            dependencies=(),
            spawn_policy=SpawnPolicy(may_spawn=False),
            timeout_seconds=300,
            expected_output_schema="front_door_steward_route_or_clarifying_question",
            parent_work_unit_id=None,
        )
        return work_unit, context_package


IonFrontDoorChatOrchestrationAdapter = FrontDoorChatOrchestrationAdapter
