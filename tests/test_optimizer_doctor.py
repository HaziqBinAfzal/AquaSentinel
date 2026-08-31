from aquasentinel.analytics import analyze
from aquasentinel.doctor import healthy, run_checks
from aquasentinel.optimizer import optimize
from aquasentinel.telemetry import sample


def test_optimizer_holds_when_quality_is_abnormal():
    t = sample("quality_anomaly", 8)
    decision = optimize(t, analyze(t))
    assert decision.mode == "HOLD-SAFE"
    assert "overrides efficiency" in decision.quality_guardrail


def test_optimizer_is_advisory_for_normal_operation():
    t = sample("normal", 2)
    decision = optimize(t, analyze(t))
    assert decision.mode in {"BALANCED", "ENERGY-SAVER", "SUPPLY-RECOVERY", "MAINTENANCE-AWARE"}
    assert decision.operator_action


def test_environment_doctor_passes_in_supported_runtime():
    checks = run_checks()
    assert healthy(checks)
    assert any(c.name == "Safety mode" and c.ok for c in checks)
