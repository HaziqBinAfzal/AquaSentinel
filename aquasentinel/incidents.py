from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IncidentStep:
    stage: str
    action: str
    purpose: str


def response_plan(result: dict, correlation: dict) -> list[IncidentStep]:
    cyber_physical = bool(correlation.get("cyber_physical"))
    quality_flags = result.get("quality_flags", [])

    validate = (
        "Cross-check independent quality/process evidence before declaring impact."
        if quality_flags
        else "Confirm the signal against independent telemetry before escalation."
    )
    contain = (
        "Isolate the simulated access path and preserve safe-state boundaries; no automatic plant actuation."
        if cyber_physical
        else "Restrict the simulated suspect path while keeping the treatment process under human supervision."
    )

    return [
        IncidentStep("1 DETECT", "Register anomaly and timestamp evidence.", "Establish a traceable starting point."),
        IncidentStep("2 VALIDATE", validate, "Reduce false positives and single-sensor bias."),
        IncidentStep("3 CORRELATE", "Combine OT security, SCADA audit and process/quality context.", "Distinguish cyber evidence from physical consequence."),
        IncidentStep("4 ASSESS", "Prioritize public-health, quality and equipment consequence.", "Risk is based on consequence, not alert count alone."),
        IncidentStep("5 CONTAIN", contain, "Limit exposure without unsafe automated control."),
        IncidentStep("6 VERIFY", "Re-check independent quality indicators and process stability.", "Demonstrate that safe-water evidence is restored."),
        IncidentStep("7 RECOVER", "Return the synthetic environment to a validated baseline under human approval.", "Avoid blind or premature restoration."),
        IncidentStep("8 EVIDENCE", "Preserve audit, correlation and decision records for review/reporting.", "Support DevSecOps and compliance evidence."),
    ]


def incident_severity(result: dict, correlation: dict) -> str:
    score = max(int(result.get("priority", 0)), int(correlation.get("correlation_score", 0)))
    if score >= 85:
        return "CRITICAL REVIEW"
    if score >= 70:
        return "HIGH REVIEW"
    if score >= 40:
        return "ELEVATED"
    return "BASELINE"
