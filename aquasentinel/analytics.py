from __future__ import annotations

from .telemetry import Telemetry


def analyze(t: Telemetry) -> dict:
    quality_flags = []
    # Illustrative classroom bands, deliberately not regulatory limits.
    checks = {
        "pH": 6.5 <= t.ph <= 8.5,
        "conductivity": t.conductivity <= 650,
        "turbidity": t.turbidity <= 1.0,
        "residual_chlorine": .25 <= t.residual_chlorine <= 1.5,
        "salinity": t.salinity <= .7,
    }
    quality_flags.extend(k for k, ok in checks.items() if not ok)
    quality_score = min(100, len(quality_flags) * 22)

    fouling_risk = min(100, max(0,
        (100 - t.membrane_health) * 2.2
        + max(0, t.ro_pressure - 60) * 5
        + max(0, 98 - t.flow_rate) * 2
    ))

    cyber_score = 0
    cyber_reason = "No synthetic cyber event"
    if t.cyber_event == "unexpected_dosing_command":
        cyber_score = 95
        cyber_reason = "Unexpected synthetic dosing command requires identity/SCADA/quality correlation"

    if quality_score >= 44:
        quality_state = "ESCALATE & VERIFY"
    elif quality_score:
        quality_state = "SENSOR/PROCESS REVIEW"
    else:
        quality_state = "BASELINE"

    if t.tank_level < 40:
        recommendation = "Prioritize storage recovery; keep quality/equipment guardrails authoritative"
    elif t.energy_kwh > 410 and t.tank_level > 60:
        recommendation = "Consider reducing non-essential pumping during high-energy period"
    else:
        recommendation = "Maintain current simulated operating plan"

    priority = max(quality_score, fouling_risk, cyber_score)
    return {
        "quality_flags": quality_flags,
        "quality_score": round(quality_score, 1),
        "quality_state": quality_state,
        "fouling_risk": round(fouling_risk, 1),
        "cyber_score": cyber_score,
        "cyber_reason": cyber_reason,
        "priority": round(priority, 1),
        "recommendation": recommendation,
        "maintenance": "Inspect membrane train" if fouling_risk >= 55 else "Routine monitoring",
        "human_review_required": priority >= 44,
    }
