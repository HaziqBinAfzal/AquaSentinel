from aquasentinel.analytics import analyze
from aquasentinel.incidents import incident_severity, response_plan
from aquasentinel.security import correlate, events_for
from aquasentinel.telemetry import sample


def test_dosing_incident_builds_eight_stage_plan():
    telemetry = sample("dosing_event", 8)
    result = analyze(telemetry)
    correlation = correlate(events_for(telemetry.cyber_event), result["quality_flags"])
    plan = response_plan(result, correlation)
    assert len(plan) == 8
    assert plan[0].stage.startswith("1 DETECT")
    assert plan[-1].stage.startswith("8 EVIDENCE")


def test_baseline_incident_severity_is_not_high():
    telemetry = sample("normal", 8)
    result = analyze(telemetry)
    correlation = correlate(events_for(telemetry.cyber_event), result["quality_flags"])
    assert incident_severity(result, correlation) in {"BASELINE", "ELEVATED"}
