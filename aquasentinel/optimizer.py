from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class OptimizationDecision:
    mode: str
    energy_target_pct: int
    production_target_pct: int
    reason: str
    quality_guardrail: str
    operator_action: str

    def dict(self) -> dict:
        return asdict(self)


def optimize(t, analysis: dict) -> OptimizationDecision:
    """Return a safe, advisory-only operating recommendation.

    This function never writes to PLC/SCADA equipment. It only explains how
    resource optimization can be constrained by quality and equipment health.
    """
    quality_bad = analysis.get("quality_state") != "BASELINE"
    cyber_high = analysis.get("cyber_score", 0) >= 70
    fouling = analysis.get("fouling_risk", 0)

    if quality_bad or cyber_high:
        return OptimizationDecision(
            mode="HOLD-SAFE",
            energy_target_pct=100,
            production_target_pct=100,
            reason="Quality or OT-security evidence requires verification before optimization.",
            quality_guardrail="ACTIVE — quality/security overrides efficiency",
            operator_action="Maintain conservative simulated operation and request human review.",
        )

    if fouling >= 60:
        return OptimizationDecision(
            mode="MAINTENANCE-AWARE",
            energy_target_pct=95,
            production_target_pct=90,
            reason="Membrane condition indicates rising fouling risk and inefficient pressure demand.",
            quality_guardrail="ACTIVE — no aggressive production increase",
            operator_action="Plan membrane inspection/cleaning before increasing simulated throughput.",
        )

    if t.tank_level < 35:
        return OptimizationDecision(
            mode="SUPPLY-RECOVERY",
            energy_target_pct=105,
            production_target_pct=110,
            reason="Storage reserve is low, so resilience is prioritized over short-term energy savings.",
            quality_guardrail="ACTIVE — increase only while quality remains baseline",
            operator_action="Increase simulated production gradually and monitor quality/pressure.",
        )

    if t.tank_level > 75 and t.energy_kwh > 520:
        return OptimizationDecision(
            mode="ENERGY-SAVER",
            energy_target_pct=88,
            production_target_pct=90,
            reason="Storage reserve is healthy while energy consumption is elevated.",
            quality_guardrail="ACTIVE — do not reduce below water-quality/process constraints",
            operator_action="Reduce simulated loading gradually; retain reserve margin.",
        )

    return OptimizationDecision(
        mode="BALANCED",
        energy_target_pct=95,
        production_target_pct=100,
        reason="Quality, storage and membrane condition support modest efficiency optimization.",
        quality_guardrail="ACTIVE — advisory only",
        operator_action="Maintain production and seek small simulated energy savings.",
    )
