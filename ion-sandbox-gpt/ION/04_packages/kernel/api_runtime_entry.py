"""Narrow API runtime-entry adapter for the runtime/session center.

Target 1 / Slice 3:

- allow an external/API carrier to attach to an existing runtime session authority center,
  or create a new session when explicitly allowed;
- emit explicit API entry receipts without importing any server stack;
- preserve the boundary that API entry is not scheduler law, queue/dispatch law,
  or enactment/activation authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid

from .model import KernelRecord, StrEnum
from .runtime_session_store import (
    RuntimeCarrierKind,
    RuntimeSessionLifecycleState,
    RuntimeSessionCarrierBinding,
    RuntimeSessionContextBinding,
    RuntimeSessionIdentity,
    RuntimeSessionAuthority,
    RuntimeSessionStore,
    RuntimeSessionStoreError,
)


_CARRIER_REF_RE = re.compile(r"^[A-Za-z0-9:/?&=_.#@+-]{1,256}$")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ApiRuntimeEntryError(Exception):
    """Raised when API runtime entry setup itself is malformed."""


class ApiRuntimeEntryStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"


class RuntimeEntryFailureDisposition(StrEnum):
    MISSING_SESSION = "MISSING_SESSION"
    MISSING_ROOT_AUTHORITY_REF = "MISSING_ROOT_AUTHORITY_REF"
    INVALID_CARRIER_REF = "INVALID_CARRIER_REF"
    CARRIER_CONFLICT = "CARRIER_CONFLICT"
    CONTEXT_CONFLICT = "CONTEXT_CONFLICT"
    SESSION_PAUSED = "SESSION_PAUSED"
    SESSION_CLOSED = "SESSION_CLOSED"


@dataclass(frozen=True)
class ApiRuntimeEntryIntent(KernelRecord):
    intent_id: str
    requested_at: str
    carrier_ref: str
    session_id: str | None = None
    create_session_if_missing: bool = False
    root_authority_ref: str | None = None
    label: str | None = None
    purpose: str | None = None
    context_version: str | None = None
    context_ref: str | None = None


@dataclass(frozen=True)
class ApiCarrierBoundary(KernelRecord):
    boundary_id: str
    session_id: str
    created_at: str
    carrier_ref: str
    boundary_note: str


@dataclass(frozen=True)
class ApiRuntimeEntryReceipt(KernelRecord):
    receipt_id: str
    intent_id: str
    status: ApiRuntimeEntryStatus
    created_at: str
    detail: str
    session_id: str | None = None
    failure_disposition: RuntimeEntryFailureDisposition | None = None
    witness_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class ApiRuntimeEntryResult(KernelRecord):
    intent: ApiRuntimeEntryIntent
    receipt: ApiRuntimeEntryReceipt
    carrier_boundary: ApiCarrierBoundary | None = None
    session_identity: RuntimeSessionIdentity | None = None
    session_authority: RuntimeSessionAuthority | None = None
    carrier_binding: RuntimeSessionCarrierBinding | None = None
    context_binding: RuntimeSessionContextBinding | None = None


class ApiRuntimeEntryGateway:
    """Attach an API carrier to a lawful runtime/session center.

    This class deliberately does not expose an HTTP server or transport loop.
    It only materializes the lawful session-side consequences of an API carrier entry.
    """

    def __init__(self) -> None:
        pass

    def _receipt_dir(self, session_store: RuntimeSessionStore) -> Path:
        path = session_store.base / "api_entry_receipts"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _boundary_dir(self, session_store: RuntimeSessionStore) -> Path:
        path = session_store.base / "api_carrier_boundaries"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _write_json(self, path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def _validate_carrier_ref(self, carrier_ref: str) -> str:
        candidate = carrier_ref.strip()
        if not candidate or not _CARRIER_REF_RE.match(candidate):
            raise ApiRuntimeEntryError(f"Invalid API carrier_ref: {carrier_ref!r}")
        return candidate

    def _build_intent(
        self,
        *,
        carrier_ref: str,
        session_id: str | None,
        create_session_if_missing: bool,
        root_authority_ref: str | None,
        label: str | None,
        purpose: str | None,
        context_version: str | None,
        context_ref: str | None,
        requested_at: str | None,
    ) -> ApiRuntimeEntryIntent:
        return ApiRuntimeEntryIntent(
            intent_id=f"arei-{uuid.uuid4().hex[:12]}",
            requested_at=requested_at or _utc_now(),
            carrier_ref=self._validate_carrier_ref(carrier_ref),
            session_id=session_id,
            create_session_if_missing=create_session_if_missing,
            root_authority_ref=root_authority_ref,
            label=label,
            purpose=purpose,
            context_version=context_version,
            context_ref=context_ref,
        )

    def _refusal(
        self,
        *,
        session_store: RuntimeSessionStore,
        intent: ApiRuntimeEntryIntent,
        detail: str,
        failure: RuntimeEntryFailureDisposition,
    ) -> ApiRuntimeEntryResult:
        receipt_id = f"arer-{uuid.uuid4().hex[:12]}"
        receipt_path = self._receipt_dir(session_store) / f"{receipt_id}.json"
        receipt = ApiRuntimeEntryReceipt(
            receipt_id=receipt_id,
            intent_id=intent.intent_id,
            status=ApiRuntimeEntryStatus.REFUSED,
            created_at=_utc_now(),
            detail=detail,
            session_id=intent.session_id,
            failure_disposition=failure,
            witness_paths=(str(receipt_path),),
        )
        self._write_json(receipt_path, receipt.to_dict())
        return ApiRuntimeEntryResult(intent=intent, receipt=receipt)

    def enter_runtime_session(
        self,
        *,
        session_store: RuntimeSessionStore,
        carrier_ref: str,
        session_id: str | None = None,
        create_session_if_missing: bool = False,
        allow_reentry_if_paused: bool = False,
        root_authority_ref: str | None = None,
        label: str | None = None,
        purpose: str | None = None,
        context_version: str | None = None,
        context_ref: str | None = None,
        requested_at: str | None = None,
    ) -> ApiRuntimeEntryResult:
        intent = self._build_intent(
            carrier_ref=carrier_ref,
            session_id=session_id,
            create_session_if_missing=create_session_if_missing,
            root_authority_ref=root_authority_ref,
            label=label,
            purpose=purpose,
            context_version=context_version,
            context_ref=context_ref,
            requested_at=requested_at,
        )

        resolved_session_id = session_id
        identity = None
        authority = None
        carrier_binding = None
        context_binding = None
        witness_paths: list[str] = []

        if resolved_session_id is None:
            if not create_session_if_missing:
                return self._refusal(
                    session_store=session_store,
                    intent=intent,
                    detail="API runtime entry requires an existing session unless create_session_if_missing is true",
                    failure=RuntimeEntryFailureDisposition.MISSING_SESSION,
                )
            resolved_session_id = f"sess-api-{uuid.uuid4().hex[:10]}"

        was_paused = False

        if not session_store.exists(resolved_session_id):
            if not create_session_if_missing:
                return self._refusal(
                    session_store=session_store,
                    intent=intent,
                    detail=f"missing runtime session: {resolved_session_id}",
                    failure=RuntimeEntryFailureDisposition.MISSING_SESSION,
                )
            if not root_authority_ref:
                return self._refusal(
                    session_store=session_store,
                    intent=intent,
                    detail="root_authority_ref is required when API entry creates a runtime session",
                    failure=RuntimeEntryFailureDisposition.MISSING_ROOT_AUTHORITY_REF,
                )
            identity, authority, create_receipt = session_store.create_session(
                resolved_session_id,
                root_authority_ref=root_authority_ref,
                label=label,
                purpose=purpose,
                created_at=intent.requested_at,
            )
            witness_paths.extend(create_receipt.witness_paths)
        else:
            identity = session_store.read_identity(resolved_session_id)
            authority = session_store.read_authority(resolved_session_id)
            if authority.lifecycle_state == RuntimeSessionLifecycleState.CLOSED:
                return self._refusal(
                    session_store=session_store,
                    intent=intent,
                    detail=f"runtime session is closed: {resolved_session_id}",
                    failure=RuntimeEntryFailureDisposition.SESSION_CLOSED,
                )
            if authority.lifecycle_state == RuntimeSessionLifecycleState.PAUSED:
                if not allow_reentry_if_paused:
                    return self._refusal(
                        session_store=session_store,
                        intent=intent,
                        detail=(
                            f"runtime session is paused and requires explicit re-entry: "
                            f"{resolved_session_id}"
                        ),
                        failure=RuntimeEntryFailureDisposition.SESSION_PAUSED,
                    )
                was_paused = True

        existing_binding = session_store.read_carrier_binding(resolved_session_id)
        if existing_binding is not None:
            if not (
                existing_binding.carrier_kind == RuntimeCarrierKind.EXTERNAL_API
                and existing_binding.carrier_ref == intent.carrier_ref
            ):
                return self._refusal(
                    session_store=session_store,
                    intent=intent,
                    detail=(
                        f"runtime session already bound to carrier {existing_binding.carrier_kind}: "
                        f"{existing_binding.carrier_ref}"
                    ),
                    failure=RuntimeEntryFailureDisposition.CARRIER_CONFLICT,
                )
            carrier_binding = existing_binding
            witness_paths.append(str(session_store._carrier_path(resolved_session_id)))
        else:
            carrier_binding, carrier_receipt = session_store.bind_carrier(
                resolved_session_id,
                carrier_kind=RuntimeCarrierKind.EXTERNAL_API,
                carrier_ref=intent.carrier_ref,
                bound_at=intent.requested_at,
            )
            witness_paths.extend(carrier_receipt.witness_paths)

        if intent.context_version is not None or intent.context_ref is not None:
            if not intent.context_version or not intent.context_ref:
                return self._refusal(
                    session_store=session_store,
                    intent=intent,
                    detail="context_version and context_ref must be provided together",
                    failure=RuntimeEntryFailureDisposition.CONTEXT_CONFLICT,
                )
            existing_context = session_store.read_context_binding(resolved_session_id)
            if existing_context is not None:
                if not (
                    existing_context.context_version == intent.context_version
                    and existing_context.context_ref == intent.context_ref
                ):
                    return self._refusal(
                        session_store=session_store,
                        intent=intent,
                        detail=(
                            f"runtime session already bound to context {existing_context.context_version}: "
                            f"{existing_context.context_ref}"
                        ),
                        failure=RuntimeEntryFailureDisposition.CONTEXT_CONFLICT,
                    )
                context_binding = existing_context
                witness_paths.append(str(session_store._context_path(resolved_session_id)))
            else:
                context_binding, context_receipt = session_store.bind_context(
                    resolved_session_id,
                    context_version=intent.context_version,
                    context_ref=intent.context_ref,
                    bound_at=intent.requested_at,
                )
                witness_paths.extend(context_receipt.witness_paths)

        if was_paused:
            authority, reentry_receipt = session_store.reenter_session(
                resolved_session_id,
                detail=f"runtime session re-entered through API carrier {intent.carrier_ref}",
                reentered_at=intent.requested_at,
                expected_carrier_ref=intent.carrier_ref,
                expected_context_version=intent.context_version,
                expected_context_ref=intent.context_ref,
            )
            witness_paths.extend(reentry_receipt.witness_paths)

        boundary = ApiCarrierBoundary(
            boundary_id=f"acb-{uuid.uuid4().hex[:12]}",
            session_id=resolved_session_id,
            created_at=_utc_now(),
            carrier_ref=intent.carrier_ref,
            boundary_note=(
                "API runtime entry binds an external carrier into an existing runtime/session center "
                "without implying scheduler sovereignty, queue sovereignty, or activation authority."
            ),
        )
        boundary_path = self._boundary_dir(session_store) / f"{boundary.boundary_id}.json"
        self._write_json(boundary_path, boundary.to_dict())
        witness_paths.append(str(boundary_path))

        receipt_id = f"arer-{uuid.uuid4().hex[:12]}"
        receipt_path = self._receipt_dir(session_store) / f"{receipt_id}.json"
        receipt = ApiRuntimeEntryReceipt(
            receipt_id=receipt_id,
            intent_id=intent.intent_id,
            status=ApiRuntimeEntryStatus.ACCEPTED,
            created_at=_utc_now(),
            detail=f"API carrier {intent.carrier_ref} entered runtime session {resolved_session_id}",
            session_id=resolved_session_id,
            failure_disposition=None,
            witness_paths=tuple([*witness_paths, str(receipt_path)]),
        )
        self._write_json(receipt_path, receipt.to_dict())

        if identity is None or authority is None or carrier_binding is None:
            raise ApiRuntimeEntryError("accepted API runtime entry is missing required session artifacts")

        return ApiRuntimeEntryResult(
            intent=intent,
            receipt=receipt,
            carrier_boundary=boundary,
            session_identity=identity,
            session_authority=authority,
            carrier_binding=carrier_binding,
            context_binding=context_binding,
        )


IonApiRuntimeEntryGateway = ApiRuntimeEntryGateway
