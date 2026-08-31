from aquasentinel.webui import HTML, build_state


def test_web_dashboard_normal_state():
    state = build_state("normal", 0)
    assert state["version"] == "1.0.0"
    assert state["scenario"] == "normal"
    assert state["telemetry"]["cyber_event"] == "none"
    assert "Synthetic" in state["safety"]
    assert len(state["process"]) == 6
    assert len(state["incident"]["steps"]) == 8


def test_web_dashboard_dosing_event_holds_safe():
    state = build_state("dosing_event", 8)
    assert state["correlation"]["correlation_score"] >= 70
    assert state["analysis"]["human_review_required"] is True
    assert state["optimization"]["mode"] == "HOLD-SAFE"


def test_web_dashboard_is_examiner_facing_and_local_safe():
    assert "LOCALHOST / READ ONLY" in HTML
    assert "No connection or write path" in HTML
    assert "/api/state" in HTML
