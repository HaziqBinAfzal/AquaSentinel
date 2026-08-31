from aquasentinel.analytics import analyze
from aquasentinel.telemetry import sample


def test_normal_is_low_priority():
    result = analyze(sample("normal", 0))
    assert result["quality_state"] == "BASELINE"
    assert result["cyber_score"] == 0


def test_multi_sensor_quality_anomaly_escalates():
    result = analyze(sample("quality_anomaly", 6))
    assert len(result["quality_flags"]) >= 3
    assert result["human_review_required"] is True


def test_dosing_event_is_high_priority():
    result = analyze(sample("dosing_event", 6))
    assert result["cyber_score"] == 95
    assert result["human_review_required"] is True


def test_fouling_risk_increases():
    early = analyze(sample("fouling", 1))["fouling_risk"]
    late = analyze(sample("fouling", 12))["fouling_risk"]
    assert late > early
