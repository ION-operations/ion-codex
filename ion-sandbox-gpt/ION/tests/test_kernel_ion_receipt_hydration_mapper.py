import json

from kernel.ion_receipt_hydration_mapper import build_receipt_hydration_view_model, hydrate_receipts, write_receipt_hydration_view_model


ASSISTANT_BUBBLES = [
    {"bubble_id": "bubble-a", "utterance_id": "u1", "atom_ids": ["a1", "a2"]},
    {"bubble_id": "bubble-b", "utterance_id": "u2", "atom_ids": ["b1"]},
]


def test_receipt_hydration_resolves_utterance_only_atom_only_and_agree_cases():
    records = hydrate_receipts(
        [
            {"receipt_id": "r-u", "utterance_id": "u1"},
            {"receipt_id": "r-a", "atom_id": "b1"},
            {"receipt_id": "r-both", "utterance_id": "u1", "atom_id": "a2"},
        ],
        ASSISTANT_BUBBLES,
    )

    by_id = {record["receipt_id"]: record for record in records}
    assert by_id["r-u"]["resolved_bubble_id"] == "bubble-a"
    assert by_id["r-u"]["resolution_method"] == "utterance_id"
    assert by_id["r-a"]["resolved_bubble_id"] == "bubble-b"
    assert by_id["r-a"]["resolution_method"] == "atom_id"
    assert by_id["r-both"]["resolved_bubble_id"] == "bubble-a"
    assert by_id["r-both"]["resolution_method"] == "utterance_atom_agree"


def test_receipt_hydration_blocks_conflicting_utterance_and_atom():
    records = hydrate_receipts(
        [{"receipt_id": "r-conflict", "utterance_id": "u1", "atom_id": "b1"}],
        ASSISTANT_BUBBLES,
    )

    record = records[0]
    assert record["resolved_bubble_id"] is None
    assert record["resolution_method"] == "conflict"
    assert record["confidence"] == "blocked"
    assert record["latest_effective"] is False
    assert "HYDRATION_CONFLICT" in record["warning"]


def test_receipt_hydration_supersession_marks_latest_effective_without_recency_attachment():
    records = hydrate_receipts(
        [
            {"receipt_id": "old", "utterance_id": "u1", "timestamp": "2026-05-02T00:00:03+00:00"},
            {"receipt_id": "repair", "utterance_id": "u1", "supersedes": ["old"], "timestamp": "2026-05-02T00:00:01+00:00"},
            {"receipt_id": "newer-other-bubble", "utterance_id": "u2", "timestamp": "2026-05-02T00:00:04+00:00"},
        ],
        ASSISTANT_BUBBLES,
    )

    by_id = {record["receipt_id"]: record for record in records}
    assert by_id["old"]["latest_effective"] is False
    assert by_id["old"]["superseded_by"] == "repair"
    assert by_id["repair"]["latest_effective"] is True
    assert by_id["repair"]["resolution_method"] == "supersession"
    assert by_id["repair"]["resolved_bubble_id"] == "bubble-a"
    assert by_id["newer-other-bubble"]["resolved_bubble_id"] == "bubble-b"


def test_receipt_hydration_missing_ids_stay_unresolved():
    records = hydrate_receipts([{"receipt_id": "r-missing"}], ASSISTANT_BUBBLES)

    assert records[0]["resolution_method"] == "unresolved"
    assert records[0]["resolved_bubble_id"] is None
    assert records[0]["latest_effective"] is False
    assert "recency attachment is forbidden" in records[0]["warning"]


def test_receipt_hydration_view_model_and_write(tmp_path):
    model = build_receipt_hydration_view_model(
        tmp_path,
        receipt_rows=[{"receipt_id": "r1", "utterance_id": "u1"}],
        assistant_bubbles=ASSISTANT_BUBBLES,
    )
    assert model["schema_id"] == "ion.receipt_hydration_view_model.v1"
    assert model["receipt_count"] == 1
    assert model["recency_attachment_allowed"] is False

    (tmp_path / "ION/05_context/current").mkdir(parents=True)
    (tmp_path / "ION/05_context/current/ACTIVE_ASSISTANT_BUBBLES.json").write_text(
        json.dumps({"assistant_bubbles": ASSISTANT_BUBBLES}),
        encoding="utf-8",
    )
    (tmp_path / "ION/05_context/current/ACTIVE_RECEIPT_SOURCE_ROWS.json").write_text(
        json.dumps({"receipt_rows": [{"receipt_id": "r2", "atom_id": "b1"}]}),
        encoding="utf-8",
    )
    written = write_receipt_hydration_view_model(tmp_path)
    assert written["records"][0]["resolved_bubble_id"] == "bubble-b"
    assert (tmp_path / "ION/05_context/current/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json").exists()
