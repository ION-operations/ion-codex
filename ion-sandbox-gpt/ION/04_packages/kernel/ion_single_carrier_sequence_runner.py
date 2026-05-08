"""ION single-carrier sequential runtime runner.

This module restores the baseline runtime shape for package lanes that cannot or
should not spawn external agents:

    Persona ingress -> Relay -> Steward -> Vizier -> Mason
    -> Nemesis/Vice review if required -> Scribe -> Steward final
    -> Persona response -> receipt candidate

It materializes one executable packet for a single capable LLM carrier and
validates completed carrier output when provided. It does not call external
models, spawn carrier slots, use MCP, push Git, or grant production authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import ACTIVE_PACKET_RELATIVE_PATH, resolve_shell_root_from_ion_root
from .ion_template_action_gate import evaluate_template_action_proof

try:  # Optional in older package lines.
    from .ion_sandbox_preflight import build_gpt_sandbox_preflight
except Exception:  # pragma: no cover - defensive compatibility
    build_gpt_sandbox_preflight = None  # type: ignore[assignment]


SCHEMA_ID = "ion.single_carrier_sequence_runner.v1"
PACKET_TEMPLATE_ID = "ion.template.single_carrier_sequential_runtime.v1"
RECEIPT_TEMPLATE_ID = "ion.template.single_carrier_sequence_receipt.v1"

PROTOCOL_RELATIVE_PATH = Path("ION/02_architecture/SINGLE_CARRIER_SEQUENTIAL_RUNTIME_PROTOCOL.md")
PACKET_TEMPLATE_RELATIVE_PATH = Path("ION/07_templates/carriers/SINGLE_CARRIER_SEQUENTIAL_PACKET.md")
RECEIPT_TEMPLATE_RELATIVE_PATH = Path("ION/07_templates/receipts/SINGLE_CARRIER_SEQUENCE_RECEIPT.md")
ACTIVE_PACKET_OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_PACKET.md")
ACTIVE_RECEIPT_OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_RECEIPT.json")
HISTORY_DIR_RELATIVE_PATH = Path("ION/05_context/current/single_carrier_sequences")

CONTEXT_PROOF_HEADING = "### CONTEXT PROOF"
TEMPLATE_ACTION_PROOF_HEADING = "### TEMPLATE ACTION PROOF"

DEFAULT_PHASES: tuple[dict[str, str], ...] = (
    {
        "phase_id": "PERSONA_INTERFACE_INGRESS",
        "role": "PERSONA_INTERFACE",
        "required": "true",
        "purpose": "Receive human language, preserve intent, and render it into ION-admissible intent without overexposing machinery.",
    },
    {
        "phase_id": "RELAY",
        "role": "RELAY",
        "required": "true",
        "purpose": "Preserve signal integrity and package the intent for Steward/internal routing.",
    },
    {
        "phase_id": "STEWARD",
        "role": "STEWARD",
        "required": "true",
        "purpose": "Classify authority, decide route, and prevent output from becoming state without review.",
    },
    {
        "phase_id": "VIZIER",
        "role": "VIZIER",
        "required": "true",
        "purpose": "Strategic route analysis and context-aware sequencing.",
    },
    {
        "phase_id": "MASON",
        "role": "MASON",
        "required": "true",
        "purpose": "Implementation or concrete construction phase within sandbox limits.",
    },
    {
        "phase_id": "NEMESIS_OR_VICE_REVIEW",
        "role": "NEMESIS_OR_VICE",
        "required": "true",
        "purpose": "Risk/adversarial review; explicitly mark not required only with reason.",
    },
    {
        "phase_id": "SCRIBE",
        "role": "SCRIBE",
        "required": "true",
        "purpose": "Documentation and receipt synthesis.",
    },
    {
        "phase_id": "STEWARD_FINAL",
        "role": "STEWARD",
        "required": "true",
        "purpose": "Final integration recommendation; still proposal-only unless separately accepted.",
    },
    {
        "phase_id": "PERSONA_INTERFACE_RESPONSE",
        "role": "PERSONA_INTERFACE",
        "required": "true",
        "purpose": "Render the internal result back to the user clearly, hiding machinery unless useful/requested.",
    },
)


ROLE_SURFACES: dict[str, tuple[str, ...]] = {
    "PERSONA_INTERFACE": (
        "ION/03_registry/boots/PERSONA_INTERFACE.boot.md",
        "ION/03_registry/semantic_identities/PERSONA_INTERFACE.semantic.yaml",
        "ION/05_context/current/agent_context_systems/PERSONA_INTERFACE.context_system.md",
        "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md",
        "ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md",
    ),
    "RELAY": (
        "ION/03_registry/boots/RELAY.boot.md",
        "ION/03_registry/semantic_identities/RELAY.semantic.yaml",
        "ION/05_context/current/agent_context_systems/RELAY.context_system.md",
        "ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md",
    ),
    "STEWARD": (
        "ION/03_registry/boots/STEWARD.boot.md",
        "ION/03_registry/semantic_identities/STEWARD.semantic.yaml",
        "ION/05_context/current/agent_context_systems/STEWARD.context_system.md",
    ),
    "VIZIER": (
        "ION/03_registry/boots/VIZIER.boot.md",
        "ION/03_registry/semantic_identities/VIZIER.semantic.yaml",
        "ION/05_context/current/agent_context_systems/VIZIER.context_system.md",
    ),
    "MASON": (
        "ION/03_registry/boots/MASON.boot.md",
        "ION/05_context/current/agent_context_systems/MASON.context_system.md",
    ),
    "NEMESIS_OR_VICE": (
        "ION/03_registry/boots/NEMESIS.boot.md",
        "ION/03_registry/semantic_identities/NEMESIS.semantic.yaml",
        "ION/05_context/current/agent_context_systems/NEMESIS.context_system.md",
        "ION/03_registry/boots/VICE.boot.md",
        "ION/03_registry/semantic_identities/VICE.semantic.yaml",
        "ION/05_context/current/agent_context_systems/VICE.context_system.md",
    ),
    "SCRIBE": (
        "ION/03_registry/boots/SCRIBE.boot.md",
        "ION/05_context/current/agent_context_systems/SCRIBE.context_system.md",
    ),
}


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "sequence"


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("::".join(str(part) for part in parts if part).encode("utf-8")).hexdigest()[:18]
    return f"{prefix}-{digest}"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _role_surface_status(shell_root: Path, role: str) -> list[dict[str, Any]]:
    surfaces: list[dict[str, Any]] = []
    for rel in ROLE_SURFACES.get(role, ()):
        path = shell_root / rel
        surfaces.append({"path": rel, "exists": path.exists(), "required": True})
    return surfaces


def _required_surface_missing(role_surfaces: Mapping[str, list[Mapping[str, Any]]]) -> list[str]:
    missing: list[str] = []
    for role, surfaces in role_surfaces.items():
        for item in surfaces:
            if item.get("required") is True and item.get("exists") is not True:
                missing.append(f"{role}:{item.get('path')}")
    return missing


def _active_objective(active_packet: Mapping[str, Any] | None, objective: str | None) -> str:
    if objective and objective.strip():
        return objective.strip()
    if isinstance(active_packet, Mapping):
        existing = active_packet.get("objective") or active_packet.get("active_objective")
        if isinstance(existing, str) and existing.strip():
            return existing.strip()
    return "single-carrier sequential ION run"


def default_phase_order() -> list[dict[str, str]]:
    return [dict(item) for item in DEFAULT_PHASES]


def build_single_carrier_sequence_packet(
    root: str | Path | None = None,
    *,
    carrier: str = "GPT_SANDBOX_CARRIER",
    objective: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build a single-carrier sequential packet without writing files."""

    shell_root = resolve_shell_root_from_ion_root(root)
    emitted_at = created_at or _iso_now()
    active_packet = _read_json(shell_root / ACTIVE_PACKET_RELATIVE_PATH)
    resolved_objective = _active_objective(active_packet, objective)
    sequence_id = _stable_id("scseq", carrier, emitted_at, resolved_objective)
    phase_order = default_phase_order()

    role_names = sorted({phase["role"] for phase in phase_order})
    role_surfaces = {role: _role_surface_status(shell_root, role) for role in role_names}
    missing_surfaces = _required_surface_missing(role_surfaces)

    preflight: dict[str, Any] | None = None
    if build_gpt_sandbox_preflight is not None and carrier.upper() == "GPT_SANDBOX_CARRIER":
        preflight = build_gpt_sandbox_preflight(shell_root, carrier="GPT_SANDBOX_CARRIER")

    packet_rel = HISTORY_DIR_RELATIVE_PATH / sequence_id / "SINGLE_CARRIER_SEQUENTIAL_PACKET.md"
    receipt_rel = HISTORY_DIR_RELATIVE_PATH / sequence_id / "SINGLE_CARRIER_SEQUENCE_RECEIPT.json"

    phase_headings = [f"### ROLE PHASE: {phase['phase_id']}" for phase in phase_order]
    context_read_paths = [
        "ION/REPO_AUTHORITY.md",
        "ION/02_architecture/ION_MOUNT_CONTRACT.md",
        str(PROTOCOL_RELATIVE_PATH),
        str(PACKET_TEMPLATE_RELATIVE_PATH),
        str(RECEIPT_TEMPLATE_RELATIVE_PATH),
        "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "ION/02_architecture/ION_GPT_SANDBOX_ENVIRONMENT_CONTRACT.md",
        "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md",
        "ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md",
        "ION/03_registry/boots/PERSONA_INTERFACE.boot.md",
        "ION/03_registry/boots/RELAY.boot.md",
        "ION/03_registry/boots/STEWARD.boot.md",
        "ION/03_registry/boots/VIZIER.boot.md",
        "ION/03_registry/boots/MASON.boot.md",
        "ION/03_registry/boots/SCRIBE.boot.md",
    ]

    packet_md = _render_packet_markdown(
        sequence_id=sequence_id,
        emitted_at=emitted_at,
        carrier=carrier,
        objective=resolved_objective,
        active_packet_path=str(ACTIVE_PACKET_RELATIVE_PATH),
        phase_order=phase_order,
        role_surfaces=role_surfaces,
        missing_surfaces=missing_surfaces,
        context_read_paths=context_read_paths,
        packet_rel=packet_rel.as_posix(),
        receipt_rel=receipt_rel.as_posix(),
        preflight_verdict=preflight.get("preflight_verdict") if preflight else None,
    )

    packet_ready = not missing_surfaces and (
        preflight is None or preflight.get("preflight_verdict") == "ION_GPT_SANDBOX_PREFLIGHT_READY"
    )

    return {
        "schema_id": SCHEMA_ID,
        "sequence_id": sequence_id,
        "created_at": emitted_at,
        "carrier": carrier,
        "objective": resolved_objective,
        "phase_order": phase_order,
        "phase_headings": phase_headings,
        "role_surfaces": role_surfaces,
        "missing_required_surfaces": missing_surfaces,
        "context_read_paths": context_read_paths,
        "preflight": preflight,
        "packet_markdown": packet_md,
        "packet_path": packet_rel.as_posix(),
        "receipt_path": receipt_rel.as_posix(),
        "active_packet_path": str(ACTIVE_PACKET_OUTPUT_RELATIVE_PATH),
        "active_receipt_path": str(ACTIVE_RECEIPT_OUTPUT_RELATIVE_PATH),
        "context_proof_required": True,
        "template_action_proof_required": True,
        "steward_review_required": True,
        "external_dependencies": {
            "codex": False,
            "mcp": False,
            "github": False,
            "daemon": False,
            "browser_extension": False,
            "external_agent_spawn": False,
        },
        "verdict": "ION_SINGLE_CARRIER_SEQUENCE_PACKET_READY" if packet_ready else "ION_SINGLE_CARRIER_SEQUENCE_PACKET_BLOCKED",
        "production_authority": False,
        "live_execution_authority": False,
    }


def _render_packet_markdown(
    *,
    sequence_id: str,
    emitted_at: str,
    carrier: str,
    objective: str,
    active_packet_path: str,
    phase_order: list[dict[str, str]],
    role_surfaces: Mapping[str, list[Mapping[str, Any]]],
    missing_surfaces: list[str],
    context_read_paths: list[str],
    packet_rel: str,
    receipt_rel: str,
    preflight_verdict: str | None,
) -> str:
    phase_lines = "\n".join(
        f"{index + 1}. `{phase['phase_id']}` — role `{phase['role']}` — {phase['purpose']}"
        for index, phase in enumerate(phase_order)
    )
    surface_lines: list[str] = []
    for role in sorted(role_surfaces):
        surface_lines.append(f"### {role} surfaces")
        for item in role_surfaces[role]:
            marker = "present" if item.get("exists") else "MISSING"
            surface_lines.append(f"- `{item['path']}` — {marker}")
    required_output = "\n\n".join(
        f"### ROLE PHASE: {phase['phase_id']}\n\n- role: `{phase['role']}`\n- required: `{phase['required']}`\n- return:\n"
        for phase in phase_order
    )
    reads = "\n".join(f"- `{path}`" for path in context_read_paths)

    return f"""# ION Single-Carrier Sequential Packet

schema_id: ion.single_carrier_sequence_packet.v1
template_id: {PACKET_TEMPLATE_ID}
sequence_id: {sequence_id}
created_at: {emitted_at}
carrier: {carrier}
objective: {objective}
production_authority: false
live_execution_authority: false

## Runtime law

One capable LLM carrier executes the ION role chain sequentially. This packet
does not spawn external agents and does not grant production authority.

Required baseline sequence:

```text
PERSONA_INTERFACE ingress
→ RELAY
→ STEWARD
→ VIZIER
→ MASON
→ NEMESIS / VICE when required
→ SCRIBE
→ STEWARD FINAL
→ PERSONA_INTERFACE response
→ RECEIPT / NEXT STATE
```

## Active packet

- active work packet: `{active_packet_path}`
- sequence receipt candidate: `{receipt_rel}`
- packet path: `{packet_rel}`
- GPT sandbox preflight verdict: `{preflight_verdict or "NOT_RUN"}`

## Required context reads

The carrier must include evidence for these paths in `### CONTEXT PROOF`:

{reads}

## Phase order

{phase_lines}

## Role surface status

{chr(10).join(surface_lines)}

## Missing required surfaces

```json
{json.dumps(missing_surfaces, indent=2)}
```

## Required carrier output shape

Copy the following headings into the carrier return and fill each section. The
return is a candidate until Steward/human review accepts it.

### CONTEXT PROOF

- Mention every required context path read.
- Include line/heading/excerpt/hash evidence, not a generic acknowledgement.

### TEMPLATE ACTION PROOF

template_id: {PACKET_TEMPLATE_ID}
action_id: {sequence_id}
result: <candidate_result>
touched_paths:
  - ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_RECEIPT.json

{required_output}

## Final response rule

Only the `PERSONA_INTERFACE_RESPONSE` phase is user-facing. Internal machinery
may be summarized only when useful or requested.
"""


def _section_present(text: str, heading: str) -> bool:
    return heading in text


def evaluate_single_carrier_sequence_output(
    *,
    packet: Mapping[str, Any],
    carrier_output: str,
) -> dict[str, Any]:
    """Validate a completed single-carrier return against the generated packet."""

    findings: list[str] = []
    if not carrier_output.lstrip().startswith(CONTEXT_PROOF_HEADING):
        findings.append("missing_initial_context_proof_heading")
    if TEMPLATE_ACTION_PROOF_HEADING not in carrier_output:
        findings.append("missing_template_action_proof_heading")

    context_section = carrier_output.split(TEMPLATE_ACTION_PROOF_HEADING, 1)[0]
    for path in packet.get("context_read_paths", []):
        if isinstance(path, str) and path not in context_section:
            findings.append(f"missing_context_read_path:{path}")

    allowed_templates = {
        PACKET_TEMPLATE_ID,
        RECEIPT_TEMPLATE_ID,
        "ion.template.patch_proposal.v1",
        "ion.template.audit_observation.v1",
    }
    template_eval = evaluate_template_action_proof(
        worker_output=carrier_output,
        allowed_template_ids=allowed_templates,
    )
    if not template_eval.get("accepted"):
        findings.extend(f"template_action_gate:{item}" for item in template_eval.get("findings", []))

    missing_phases: list[str] = []
    for heading in packet.get("phase_headings", []):
        if isinstance(heading, str) and not _section_present(carrier_output, heading):
            missing_phases.append(heading)
            findings.append(f"missing_role_phase_heading:{heading}")

    accepted = not findings
    return {
        "schema_id": "ion.single_carrier_sequence_output_evaluation.v1",
        "accepted": accepted,
        "findings": findings,
        "missing_phase_headings": missing_phases,
        "template_action_gate": template_eval,
        "integration_decision": "ALLOW_STEWARD_REVIEW" if accepted else "REJECT_SEQUENCE_RETURN_AND_RERUN",
        "production_authority": False,
        "live_execution_authority": False,
    }


def _build_receipt(
    *,
    packet: Mapping[str, Any],
    packet_written_path: str,
    active_packet_written_path: str,
    completed_output_path: str | None = None,
    output_evaluation: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    phase_validation = "ready"
    if output_evaluation is not None:
        phase_validation = "accepted" if output_evaluation.get("accepted") else "blocked"

    return {
        "schema_id": "ion.single_carrier_sequence_receipt.v1",
        "receipt_id": _stable_id("screceipt", str(packet.get("sequence_id")), packet_written_path),
        "created_at": _iso_now(),
        "sequence_id": packet.get("sequence_id"),
        "carrier": packet.get("carrier"),
        "objective": packet.get("objective"),
        "template_id": RECEIPT_TEMPLATE_ID,
        "phase_order": packet.get("phase_order"),
        "packet_path": packet_written_path,
        "active_packet_path": active_packet_written_path,
        "completed_output_path": completed_output_path,
        "context_proof_required": True,
        "template_action_proof_required": True,
        "phase_section_validation": phase_validation,
        "output_evaluation": output_evaluation,
        "steward_review_required": True,
        "receipt_status": (
            "SEQUENCE_OUTPUT_ACCEPTED_FOR_STEWARD_REVIEW"
            if output_evaluation and output_evaluation.get("accepted")
            else "SEQUENCE_PACKET_READY_AWAITING_CARRIER_OUTPUT"
            if output_evaluation is None
            else "SEQUENCE_OUTPUT_BLOCKED"
        ),
        "next_state_projection": "none_written_without_steward_or_human_acceptance",
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_single_carrier_sequence_packet(
    root: str | Path | None = None,
    *,
    carrier: str = "GPT_SANDBOX_CARRIER",
    objective: str | None = None,
    completed_output_path: str | Path | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Write active/history packet and receipt candidate."""

    shell_root = resolve_shell_root_from_ion_root(root)
    packet = build_single_carrier_sequence_packet(
        shell_root,
        carrier=carrier,
        objective=objective,
        created_at=created_at,
    )

    packet_history_path = shell_root / packet["packet_path"]
    packet_history_path.parent.mkdir(parents=True, exist_ok=True)
    packet_history_path.write_text(str(packet["packet_markdown"]), encoding="utf-8")

    active_packet_path = shell_root / ACTIVE_PACKET_OUTPUT_RELATIVE_PATH
    active_packet_path.parent.mkdir(parents=True, exist_ok=True)
    active_packet_path.write_text(str(packet["packet_markdown"]), encoding="utf-8")

    output_evaluation: dict[str, Any] | None = None
    output_rel: str | None = None
    if completed_output_path is not None:
        candidate = Path(completed_output_path)
        if not candidate.is_absolute():
            candidate = shell_root / candidate
        carrier_output = candidate.read_text(encoding="utf-8")
        output_evaluation = evaluate_single_carrier_sequence_output(packet=packet, carrier_output=carrier_output)
        output_rel = _rel(shell_root, candidate)

    receipt = _build_receipt(
        packet=packet,
        packet_written_path=packet["packet_path"],
        active_packet_written_path=str(ACTIVE_PACKET_OUTPUT_RELATIVE_PATH),
        completed_output_path=output_rel,
        output_evaluation=output_evaluation,
    )

    receipt_history_path = shell_root / str(packet["receipt_path"])
    _write_json(receipt_history_path, receipt)
    active_receipt_path = shell_root / ACTIVE_RECEIPT_OUTPUT_RELATIVE_PATH
    _write_json(active_receipt_path, receipt)

    return {
        **packet,
        "packet_written_path": packet["packet_path"],
        "active_packet_written_path": str(ACTIVE_PACKET_OUTPUT_RELATIVE_PATH),
        "receipt": receipt,
        "receipt_written_path": packet["receipt_path"],
        "active_receipt_written_path": str(ACTIVE_RECEIPT_OUTPUT_RELATIVE_PATH),
        "output_evaluation": output_evaluation,
        "verdict": (
            "ION_SINGLE_CARRIER_SEQUENCE_OUTPUT_ACCEPTED_FOR_STEWARD_REVIEW"
            if output_evaluation and output_evaluation.get("accepted")
            else packet["verdict"]
            if output_evaluation is None
            else "ION_SINGLE_CARRIER_SEQUENCE_OUTPUT_BLOCKED"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Materialize an ION single-carrier sequential packet.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--carrier", default="GPT_SANDBOX_CARRIER")
    parser.add_argument("--objective", default=None)
    parser.add_argument("--completed-output-path", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)

    result = (
        build_single_carrier_sequence_packet(
            args.ion_root,
            carrier=args.carrier,
            objective=args.objective,
        )
        if args.no_write
        else write_single_carrier_sequence_packet(
            args.ion_root,
            carrier=args.carrier,
            objective=args.objective,
            completed_output_path=args.completed_output_path,
        )
    )

    if args.json:
        printable = {key: value for key, value in result.items() if key != "packet_markdown"}
        print(json.dumps(printable, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        if not args.no_write:
            print(f"packet: {result['active_packet_written_path']}")
            print(f"receipt: {result['active_receipt_written_path']}")

    return 0 if str(result["verdict"]).endswith(("READY", "REVIEW")) else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
