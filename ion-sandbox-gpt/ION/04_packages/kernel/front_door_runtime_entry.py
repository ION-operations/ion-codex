"""Front-door runtime entry adapter.

This module materializes the current front-door split in executable kernel state:

    Persona Interface -> Relay -> Steward

It deliberately does not implement an HTTP server, LLM call, or autonomous chat loop.
Its job is to persist the lawful boundary artifacts that a browser/API/chat surface
can call before the deeper orchestration path runs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from .id_compaction import compact_identifier
from .model import KernelRecord, StrEnum


FRONT_DOOR_HISTORY_RELATIVE = Path("ION/05_context/history/front_door_runtime")
PERSONA_INTERFACE_ROLE = "role.persona_interface"
RELAY_ROLE = "role.relay"
STEWARD_ROLE = "role.steward"
DEFAULT_ROLE_CHAIN = (PERSONA_INTERFACE_ROLE, RELAY_ROLE, STEWARD_ROLE)
DEFAULT_FORBIDDEN_COLLAPSES = (
    "persona_interface_may_not_route_or_orchestrate",
    "relay_may_not_own_persona_or_orchestrate",
    "steward_may_not_claim_user_bonded_persona_context",
    "raw_user_text_may_not_be_treated_as_system_truth_without_relay_boundary_packet",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_short(prefix: str, *parts: str) -> str:
    base = "::".join(part for part in parts if part)
    if not base:
        return f"{prefix}-{uuid.uuid4().hex[:12]}"
    return f"{prefix}-{compact_identifier(base, empty='front-door', max_length=56)}"


class FrontDoorRuntimeEntryError(Exception):
    """Raised when a front-door runtime entry would violate role boundaries."""


class FrontDoorBoundaryStage(StrEnum):
    USER_TO_PERSONA = "USER_TO_PERSONA"
    PERSONA_TO_RELAY = "PERSONA_TO_RELAY"
    RELAY_TO_STEWARD = "RELAY_TO_STEWARD"
    STEWARD_TO_RELAY = "STEWARD_TO_RELAY"
    RELAY_TO_PERSONA = "RELAY_TO_PERSONA"
    PERSONA_TO_USER = "PERSONA_TO_USER"


class FrontDoorReceiptStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class PersonaInterfaceIngress(KernelRecord):
    message_id: str
    created_at: str
    session_id: str
    user_ref: str
    persona_role_ref: str
    visible_persona_name: str | None
    raw_user_text: str
    relation_context_refs: tuple[str, ...]
    boundary_stage: FrontDoorBoundaryStage = FrontDoorBoundaryStage.USER_TO_PERSONA


@dataclass(frozen=True)
class RelaySemanticBoundaryPacket(KernelRecord):
    packet_id: str
    created_at: str
    session_id: str
    source_message_id: str
    relay_role_ref: str
    persona_role_ref: str
    steward_role_ref: str
    raw_user_text_ref: str
    normalized_intent: str
    semantic_packet: dict[str, object]
    template_ref: str
    forbidden_role_collapses: tuple[str, ...]
    boundary_stage: FrontDoorBoundaryStage = FrontDoorBoundaryStage.PERSONA_TO_RELAY


@dataclass(frozen=True)
class StewardRoutingEnvelope(KernelRecord):
    envelope_id: str
    created_at: str
    session_id: str
    relay_packet_id: str
    target_role_ref: str
    route_purpose: str
    payload_class: str
    allowed_consumers: tuple[str, ...]
    prohibited_actions: tuple[str, ...]
    boundary_stage: FrontDoorBoundaryStage = FrontDoorBoundaryStage.RELAY_TO_STEWARD


@dataclass(frozen=True)
class RelayReturnPackage(KernelRecord):
    return_id: str
    created_at: str
    session_id: str
    source_system_ref: str
    relay_role_ref: str
    persona_role_ref: str
    steward_role_ref: str
    controlled_reexpression: str
    persona_rendering_instructions: tuple[str, ...]
    template_ref: str
    boundary_stage: FrontDoorBoundaryStage = FrontDoorBoundaryStage.STEWARD_TO_RELAY


@dataclass(frozen=True)
class PersonaResponsePackage(KernelRecord):
    response_id: str
    created_at: str
    session_id: str
    relay_return_id: str
    persona_role_ref: str
    visible_persona_name: str | None
    user_ref: str
    user_facing_text: str
    style_notes: tuple[str, ...]
    template_ref: str
    boundary_stage: FrontDoorBoundaryStage = FrontDoorBoundaryStage.PERSONA_TO_USER


@dataclass(frozen=True)
class FrontDoorRuntimeReceipt(KernelRecord):
    receipt_id: str
    created_at: str
    status: FrontDoorReceiptStatus
    stage: FrontDoorBoundaryStage
    detail: str
    session_id: str
    witness_paths: tuple[str, ...]


@dataclass(frozen=True)
class FrontDoorIngressResult(KernelRecord):
    persona_ingress: PersonaInterfaceIngress
    relay_packet: RelaySemanticBoundaryPacket
    steward_envelope: StewardRoutingEnvelope
    receipt: FrontDoorRuntimeReceipt


@dataclass(frozen=True)
class FrontDoorReturnResult(KernelRecord):
    relay_return: RelayReturnPackage
    persona_response: PersonaResponsePackage
    receipt: FrontDoorRuntimeReceipt


class FrontDoorRuntimeGateway:
    """Persist executable front-door boundary artifacts.

    This gateway is intentionally narrow. It does not decide the user's final answer,
    invoke an LLM, or choose downstream work. It records the lawful boundary state
    so browser/API/chat adapters can keep Persona Interface, Relay, and Steward
    separated in runtime artifacts.
    """

    def __init__(self, *, base_relative: Path = FRONT_DOOR_HISTORY_RELATIVE) -> None:
        self.base_relative = base_relative

    def _base(self, workspace_root: Path) -> Path:
        path = workspace_root / self.base_relative
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _dir(self, workspace_root: Path, name: str) -> Path:
        path = self._base(workspace_root) / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _write_json(self, path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def _rel(self, workspace_root: Path, path: Path) -> str:
        try:
            return str(path.relative_to(workspace_root))
        except ValueError:
            return str(path)

    def _validate_text(self, text: str) -> str:
        value = text.strip()
        if not value:
            raise FrontDoorRuntimeEntryError("front-door user text cannot be blank")
        return value

    def _validate_role_split(self, *, persona_role_ref: str, relay_role_ref: str, steward_role_ref: str) -> None:
        roles = (persona_role_ref, relay_role_ref, steward_role_ref)
        if len(set(roles)) != 3:
            raise FrontDoorRuntimeEntryError(
                "front-door roles must remain separate: persona, relay, and steward may not share one role ref"
            )
        if persona_role_ref == RELAY_ROLE:
            raise FrontDoorRuntimeEntryError("Relay may not be used as the Persona Interface role")
        if relay_role_ref == STEWARD_ROLE:
            raise FrontDoorRuntimeEntryError("Steward may not be used as the Relay role")

    def _semantic_packet(
        self,
        *,
        raw_user_text: str,
        session_id: str,
        user_ref: str,
        persona_role_ref: str,
        visible_persona_name: str | None,
        relation_context_refs: tuple[str, ...],
        created_at: str,
    ) -> dict[str, object]:
        return {
            "semantic_packet": {
                "intake": raw_user_text,
                "resolved_objects": [
                    persona_role_ref,
                    RELAY_ROLE,
                    STEWARD_ROLE,
                    "context.packet.semantic_payload",
                    "identity.semantic.true_name",
                ],
                "provisional_objects": [
                    "user_intent.true_name_resolution_pending",
                    "persona_visible_name.pending" if visible_persona_name else "persona_visible_name.absent",
                ],
                "context_bindings": {
                    "branch_scope": "current_runtime_front_door",
                    "temporal_scope": created_at,
                    "authority_scope": "user_intent_projection__not_governed_write",
                    "role_scope": "Persona Interface -> Relay -> Steward",
                    "horizon_scope": "front_door_intake_to_orchestration",
                    "session_id": session_id,
                    "user_ref": user_ref,
                    "relation_context_refs": list(relation_context_refs),
                },
                "donor_line_notes": [
                    "Aletheion translation discipline governs meaning-before-wording and true-name preservation.",
                    "Relay is a semantic-boundary/courier role, not final persona owner or orchestrator.",
                ],
                "ambiguity_notes": [
                    "Raw user language remains user intent until Relay boundary translation and Steward routing.",
                    "Visible persona names and style signals are persona-surface data, not system truth by themselves.",
                ],
                "contradiction_notes": [],
                "loss_notes": [
                    "This runtime adapter emits a first-pass semantic packet; deeper true-name resolution may refine it.",
                ],
                "recommended_followups": [
                    "Steward should route only from the Relay semantic-boundary packet, not from raw user text alone.",
                ],
            }
        }

    def ingest_user_message(
        self,
        *,
        workspace_root: str | Path,
        raw_user_text: str,
        user_ref: str = "user.sovereign",
        session_id: str = "front-door-session",
        persona_role_ref: str = PERSONA_INTERFACE_ROLE,
        relay_role_ref: str = RELAY_ROLE,
        steward_role_ref: str = STEWARD_ROLE,
        visible_persona_name: str | None = None,
        relation_context_refs: tuple[str, ...] = (),
        created_at: str | None = None,
    ) -> FrontDoorIngressResult:
        root = Path(workspace_root).resolve()
        created = created_at or _utc_now()
        text = self._validate_text(raw_user_text)
        self._validate_role_split(
            persona_role_ref=persona_role_ref,
            relay_role_ref=relay_role_ref,
            steward_role_ref=steward_role_ref,
        )

        message_id = _stable_short("fdmsg", session_id, user_ref, text, created)
        packet_id = _stable_short("fdrelay", message_id, relay_role_ref, created)
        envelope_id = _stable_short("fdsteward", packet_id, steward_role_ref, created)
        receipt_id = _stable_short("fdreceipt", envelope_id, "ingress", created)

        persona_ingress = PersonaInterfaceIngress(
            message_id=message_id,
            created_at=created,
            session_id=session_id,
            user_ref=user_ref,
            persona_role_ref=persona_role_ref,
            visible_persona_name=visible_persona_name,
            raw_user_text=text,
            relation_context_refs=relation_context_refs,
        )
        persona_path = self._dir(root, "persona_ingress") / f"{message_id}.json"
        self._write_json(persona_path, persona_ingress.to_dict())

        semantic_packet = self._semantic_packet(
            raw_user_text=text,
            session_id=session_id,
            user_ref=user_ref,
            persona_role_ref=persona_role_ref,
            visible_persona_name=visible_persona_name,
            relation_context_refs=relation_context_refs,
            created_at=created,
        )

        relay_packet = RelaySemanticBoundaryPacket(
            packet_id=packet_id,
            created_at=created,
            session_id=session_id,
            source_message_id=message_id,
            relay_role_ref=relay_role_ref,
            persona_role_ref=persona_role_ref,
            steward_role_ref=steward_role_ref,
            raw_user_text_ref=self._rel(root, persona_path),
            normalized_intent=text,
            semantic_packet=semantic_packet,
            template_ref="ION/07_templates/bindings/RELAY__SEMANTIC_BOUNDARY.md",
            forbidden_role_collapses=DEFAULT_FORBIDDEN_COLLAPSES,
        )
        relay_path = self._dir(root, "relay_semantic_boundary_packets") / f"{packet_id}.json"
        self._write_json(relay_path, relay_packet.to_dict())

        steward_envelope = StewardRoutingEnvelope(
            envelope_id=envelope_id,
            created_at=created,
            session_id=session_id,
            relay_packet_id=packet_id,
            target_role_ref=steward_role_ref,
            route_purpose="front_door_user_intake",
            payload_class="RELAY_SEMANTIC_BOUNDARY_PACKET",
            allowed_consumers=(steward_role_ref,),
            prohibited_actions=(
                "do_not_treat_raw_user_text_as_governed_write",
                "do_not_route_persona_style_as_system_truth",
                "do_not_bypass_relay_boundary_packet",
            ),
        )
        envelope_path = self._dir(root, "steward_routing_envelopes") / f"{envelope_id}.json"
        self._write_json(envelope_path, steward_envelope.to_dict())

        witness_paths = (
            self._rel(root, persona_path),
            self._rel(root, relay_path),
            self._rel(root, envelope_path),
        )
        receipt = FrontDoorRuntimeReceipt(
            receipt_id=receipt_id,
            created_at=created,
            status=FrontDoorReceiptStatus.ACCEPTED,
            stage=FrontDoorBoundaryStage.RELAY_TO_STEWARD,
            detail="front-door user message accepted through Persona Interface -> Relay -> Steward boundary",
            session_id=session_id,
            witness_paths=witness_paths,
        )
        receipt_path = self._dir(root, "receipts") / f"{receipt_id}.json"
        receipt = FrontDoorRuntimeReceipt(
            receipt_id=receipt.receipt_id,
            created_at=receipt.created_at,
            status=receipt.status,
            stage=receipt.stage,
            detail=receipt.detail,
            session_id=receipt.session_id,
            witness_paths=(*witness_paths, self._rel(root, receipt_path)),
        )
        self._write_json(receipt_path, receipt.to_dict())

        return FrontDoorIngressResult(
            persona_ingress=persona_ingress,
            relay_packet=relay_packet,
            steward_envelope=steward_envelope,
            receipt=receipt,
        )

    def prepare_persona_response(
        self,
        *,
        workspace_root: str | Path,
        controlled_system_output: str,
        user_ref: str = "user.sovereign",
        session_id: str = "front-door-session",
        source_system_ref: str = "steward.output",
        persona_role_ref: str = PERSONA_INTERFACE_ROLE,
        relay_role_ref: str = RELAY_ROLE,
        steward_role_ref: str = STEWARD_ROLE,
        visible_persona_name: str | None = None,
        style_notes: tuple[str, ...] = (),
        created_at: str | None = None,
    ) -> FrontDoorReturnResult:
        root = Path(workspace_root).resolve()
        created = created_at or _utc_now()
        text = self._validate_text(controlled_system_output)
        self._validate_role_split(
            persona_role_ref=persona_role_ref,
            relay_role_ref=relay_role_ref,
            steward_role_ref=steward_role_ref,
        )

        return_id = _stable_short("fdreturn", session_id, source_system_ref, text, created)
        response_id = _stable_short("fdresponse", return_id, persona_role_ref, created)
        receipt_id = _stable_short("fdreceipt", response_id, "return", created)

        relay_return = RelayReturnPackage(
            return_id=return_id,
            created_at=created,
            session_id=session_id,
            source_system_ref=source_system_ref,
            relay_role_ref=relay_role_ref,
            persona_role_ref=persona_role_ref,
            steward_role_ref=steward_role_ref,
            controlled_reexpression=text,
            persona_rendering_instructions=(
                "render for user through Persona Interface",
                "preserve system authority limits",
                "do not let persona styling change factual or authority content",
            ),
            template_ref="ION/07_templates/bindings/RELAY__SEMANTIC_BOUNDARY.md",
        )
        return_path = self._dir(root, "relay_return_packages") / f"{return_id}.json"
        self._write_json(return_path, relay_return.to_dict())

        persona_response = PersonaResponsePackage(
            response_id=response_id,
            created_at=created,
            session_id=session_id,
            relay_return_id=return_id,
            persona_role_ref=persona_role_ref,
            visible_persona_name=visible_persona_name,
            user_ref=user_ref,
            user_facing_text=text,
            style_notes=style_notes,
            template_ref="ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md",
        )
        response_path = self._dir(root, "persona_response_packages") / f"{response_id}.json"
        self._write_json(response_path, persona_response.to_dict())

        witness_paths = (self._rel(root, return_path), self._rel(root, response_path))
        receipt = FrontDoorRuntimeReceipt(
            receipt_id=receipt_id,
            created_at=created,
            status=FrontDoorReceiptStatus.ACCEPTED,
            stage=FrontDoorBoundaryStage.PERSONA_TO_USER,
            detail="system output prepared through Relay -> Persona Interface return boundary",
            session_id=session_id,
            witness_paths=(*witness_paths, str((self._dir(root, "receipts") / f"{receipt_id}.json").relative_to(root))),
        )
        receipt_path = self._dir(root, "receipts") / f"{receipt_id}.json"
        self._write_json(receipt_path, receipt.to_dict())

        return FrontDoorReturnResult(
            relay_return=relay_return,
            persona_response=persona_response,
            receipt=receipt,
        )


IonFrontDoorRuntimeGateway = FrontDoorRuntimeGateway
