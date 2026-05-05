"""Classify operator messages for the ION carrier-control loop.

V88 makes the operator message a durable runtime primitive instead of a fragile
chat-memory event. This classifier is intentionally conservative and deterministic:
it does not call an LLM, does not infer hidden intent, and does not execute work.

The parent Cursor chat should use this layer to distinguish:
- continuation signals such as "continue" or "proceed";
- new work directives;
- human-gate answers;
- status requests;
- design-only discussion.
"""

from __future__ import annotations

import argparse
import json
import re
from typing import Any, Mapping, Sequence


CONTINUATION_SIGNALS = {
    "",
    "continue",
    "continue.",
    "proceed",
    "proceed.",
    "resume",
    "resume.",
    "keep going",
    "carry on",
    "next",
    "next step",
    "run next",
    "advance",
    "advance the plan",
    "go ahead",
}

STATUS_PATTERNS = (
    "status",
    "state",
    "where are we",
    "what remains",
    "what is left",
    "what's left",
    "why did it stop",
    "current packet",
    "current queue",
    "show queue",
    "show gates",
)

DESIGN_DISCUSSION_PATTERNS = (
    "let's discuss",
    "lets discuss",
    "think through",
    "consider",
    "explain",
    "walk through",
    "go through",
    "architecture",
    "workflow process",
)

IMPLEMENTATION_VERBS = (
    "add",
    "build",
    "create",
    "implement",
    "patch",
    "fix",
    "wire",
    "update",
    "write",
    "generate",
    "package",
    "zip",
    "test",
    "audit",
    "run",
    "land",
    "integrate",
    "remove",
    "delete",
)

HUMAN_GATE_ANSWERS = {
    "yes",
    "y",
    "approve",
    "approved",
    "allow",
    "allowed",
    "no",
    "n",
    "deny",
    "denied",
    "reject",
    "rejected",
    "block",
    "blocked",
    "stop",
    "cancel",
}


def normalize_operator_message(message: str | None) -> str:
    text = " ".join((message or "").strip().lower().split())
    text = text.strip()
    return text


def _contains_any(text: str, patterns: Sequence[str]) -> bool:
    return any(pattern in text for pattern in patterns)


def _starts_with_implementation_verb(text: str) -> bool:
    first = re.split(r"[^a-z0-9_-]+", text.strip(), maxsplit=1)[0] if text.strip() else ""
    return first in IMPLEMENTATION_VERBS


def _looks_like_human_gate_answer(text: str) -> bool:
    if text in HUMAN_GATE_ANSWERS:
        return True
    if re.fullmatch(r"(use|choose|select)\s+(option\s+)?[a-d]", text):
        return True
    if text.startswith(("use option ", "choose option ", "select option ")):
        return True
    if text.startswith(("yes,", "no,", "approved:", "rejected:", "allow:", "deny:")):
        return True
    return False


def classify_operator_message(
    message: str | None,
    *,
    active_human_gates: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a deterministic classification record for an operator message."""

    normalized = normalize_operator_message(message)
    gates = list(active_human_gates or [])
    has_open_gate = bool(gates)

    if has_open_gate and _looks_like_human_gate_answer(normalized):
        classification = "human_gate_answer"
        action = "resolve_human_gate_then_continue"
        confidence = 0.94
    elif normalized in CONTINUATION_SIGNALS:
        classification = "continuation_signal"
        action = "run_carrier_continue"
        confidence = 0.98
    elif _contains_any(normalized, STATUS_PATTERNS) and not _starts_with_implementation_verb(normalized):
        classification = "status_request"
        action = "run_ion_status_without_mutation"
        confidence = 0.86
    elif _contains_any(normalized, DESIGN_DISCUSSION_PATTERNS) and not _starts_with_implementation_verb(normalized):
        classification = "design_discussion"
        action = "discuss_or_document_without_runtime_mutation"
        confidence = 0.74
    else:
        classification = "new_work_directive"
        action = "record_operator_work_item_and_refresh_carrier"
        confidence = 0.82

    return {
        "schema_id": "ion.operator_message_classification.v1",
        "message": message or "",
        "normalized_message": normalized,
        "classification": classification,
        "action": action,
        "confidence": confidence,
        "active_human_gate_count": len(gates),
        "requires_human_gate_resolution": classification == "human_gate_answer",
        "mutates_runtime": classification in {"continuation_signal", "new_work_directive", "human_gate_answer"},
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Classify an ION operator message.")
    parser.add_argument("message", nargs="*", help="Operator message text.")
    parser.add_argument("--active-human-gate", action="append", default=[], help="Optional active gate id/name.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    gates = [{"id": gate} for gate in args.active_human_gate]
    result = classify_operator_message(" ".join(args.message), active_human_gates=gates)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["classification"])
        print(result["action"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
