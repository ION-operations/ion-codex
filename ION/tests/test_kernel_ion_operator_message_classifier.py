from kernel.ion_operator_message_classifier import classify_operator_message


def test_classifier_recognizes_continuation():
    result = classify_operator_message("continue")
    assert result["classification"] == "continuation_signal"
    assert result["action"] == "run_carrier_continue"


def test_classifier_recognizes_human_gate_answer_when_gate_open():
    result = classify_operator_message("yes", active_human_gates=[{"id": "gate_1"}])
    assert result["classification"] == "human_gate_answer"
    assert result["requires_human_gate_resolution"] is True


def test_classifier_recognizes_new_work_directive():
    result = classify_operator_message("implement the V88 operator queue")
    assert result["classification"] == "new_work_directive"


def test_classifier_recognizes_status_request():
    result = classify_operator_message("what is the current status?")
    assert result["classification"] == "status_request"
