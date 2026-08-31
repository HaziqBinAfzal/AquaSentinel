from aquasentinel.ml import QualityMLModel
from aquasentinel.security import correlate, events_for
from aquasentinel.telemetry import sample
from aquasentinel.analytics import analyze


def test_ml_model_scores_quality_anomaly_above_normal():
    model = QualityMLModel.train_default(samples=180)
    normal = model.score(sample("normal", 8))["ml_priority"]
    abnormal = model.score(sample("quality_anomaly", 8))["ml_priority"]
    assert abnormal > normal


def test_dosing_event_generates_multiple_security_sources():
    events = events_for("unexpected_dosing_command")
    assert len(events) >= 3
    assert {e.source for e in events} >= {"zeek-sim", "suricata-sim", "scada-audit"}


def test_cyber_physical_correlation_requires_process_evidence():
    events = events_for("unexpected_dosing_command")
    no_quality = correlate(events, [])
    with_quality = correlate(events, ["residual_chlorine"])
    assert no_quality["cyber_physical"] is False
    assert with_quality["cyber_physical"] is True
    assert with_quality["correlation_score"] >= no_quality["correlation_score"]


def test_quality_scenario_produces_multiple_flags():
    result = analyze(sample("quality_anomaly", 8))
    assert len(result["quality_flags"]) >= 3
