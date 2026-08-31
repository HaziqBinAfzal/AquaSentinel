from __future__ import annotations

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .analytics import analyze
from .compliance import report as compliance_report
from .dashboard import build_dashboard
from .ml import QualityMLModel
from .optimizer import optimize
from .presenter import incident_brief
from .security import correlate, events_for
from .telemetry import sample

console = Console()


def _pause(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


def _scene(title: str, explanation: str) -> None:
    console.rule(f"[bold cyan]{title}[/bold cyan]")
    console.print(Panel(explanation, border_style="cyan"))


def _snapshot(scenario: str, step: int, model: QualityMLModel):
    t = sample(scenario, step)
    result = analyze(t)
    ml_result = model.score(t)
    security_events = events_for(t.cyber_event)
    correlation = correlate(security_events, result["quality_flags"])
    result["priority"] = max(result["priority"], ml_result["ml_priority"], correlation["correlation_score"])
    if ml_result["ml_state"] == "ANOMALOUS" or correlation["correlation_score"] >= 70:
        result["human_review_required"] = True
    optimization = optimize(t, result).dict()
    console.print(build_dashboard(t, result, scenario, ml_result, correlation, optimization))
    return t, result, ml_result, correlation, optimization


def run_exam_demo(pause: float = 1.2) -> None:
    """Guided, read-only Topic 133 demonstration for an oral exam."""
    console.clear()
    console.print(Panel.fit(
        "[bold]AQUASENTINEL AI[/bold]\n"
        "Smart Water & Desalination Infrastructure Security Platform\n"
        "EduQual Level 6 — Topic 133\n\n"
        "[yellow]SYNTHETIC • DEFENSIVE • READ-ONLY[/yellow]\n"
        "No connection to real PLC, SCADA, dosing or public-water infrastructure.",
        title="ORAL EXAM DEMONSTRATION",
        border_style="bright_blue",
    ))
    _pause(pause)

    model = QualityMLModel.train_default()

    _scene(
        "1/7 — Normal desalination operation",
        "Start with the baseline. Explain the process from raw/sea water through pretreatment, high-pressure pumping, reverse osmosis, post-treatment, storage and distribution. The platform combines process telemetry, water-quality evidence, OT visibility and AI analysis.",
    )
    _snapshot("normal", 3, model)
    _pause(pause)

    _scene(
        "2/7 — Water-quality anomaly",
        "Multiple synthetic sensors move outside the classroom baseline together. Explain cross-sensor validation: one unusual value may be a sensor problem, while several related measurements provide stronger evidence that operators should investigate the process and protect public health.",
    )
    _snapshot("quality_anomaly", 8, model)
    _pause(pause)

    _scene(
        "3/7 — AI anomaly detection",
        "IsolationForest evaluates a synthetic multi-feature process baseline. The model is advisory: it helps prioritize unusual operating states but never makes a real treatment or safety decision by itself.",
    )
    _snapshot("sensor_anomaly", 8, model)
    _pause(pause)

    _scene(
        "4/7 — OT/SCADA cyber-physical correlation",
        "A simulated unexpected dosing-related event creates Zeek-style, Suricata-style and SCADA-audit evidence. AquaSentinel correlates that security evidence with independent water-quality observations. This is detection and reasoning only — there are no control commands.",
    )
    _snapshot("dosing_event", 8, model)
    _pause(pause)

    _scene(
        "5/7 — Incident response",
        "Explain the safe response lifecycle: detect, validate, correlate, assess consequence, contain safely, verify water quality, recover and preserve evidence. Human and public-health authority remain above AI recommendations.",
    )
    incident_brief("dosing_event", 8, 133)
    _pause(pause)

    _scene(
        "6/7 — Predictive maintenance & resource optimization",
        "Membrane fouling changes pressure, flow, membrane health and energy use. The optimizer can suggest efficiency modes, but quality/security guardrails force a safe hold whenever evidence requires human review.",
    )
    _snapshot("fouling", 10, model)
    _snapshot("optimization", 10, model)
    _pause(pause)

    _scene(
        "7/7 — DevSecOps, compliance context & evidence",
        "Close by explaining that the project preserves audit evidence, generates an exam report, uses automated tests/static/security checks, and maps its educational controls to NIST SP 800-82 plus EPA/WHO water-safety context. The mapping is educational, not regulatory certification.",
    )
    console.print(Panel(compliance_report(), title="Assurance Context", border_style="green"))

    summary = Table(title="What AquaSentinel Demonstrated")
    summary.add_column("Exam area")
    summary.add_column("Evidence shown")
    summary.add_row("Architecture", "Segmented Enterprise / DMZ / OT / Safety & Quality model")
    summary.add_row("OT protection", "Passive synthetic security telemetry and correlation")
    summary.add_row("Water quality", "Cross-sensor checks and anomaly prioritization")
    summary.add_row("AI", "IsolationForest advisory anomaly detection")
    summary.add_row("Maintenance", "Synthetic membrane fouling risk")
    summary.add_row("Optimization", "Energy/resource recommendations with safety guardrails")
    summary.add_row("Response", "Eight-stage human-led incident workflow")
    summary.add_row("DevSecOps", "Tests, static analysis, security scan and evidence reporting")
    console.print(summary)
    console.print(Panel.fit(
        "[bold green]DEMO COMPLETE[/bold green]\n"
        "Key message: AquaSentinel connects cyber evidence, process context, water-quality verification and AI-assisted prioritization while keeping humans and public-health safety in control.",
        border_style="green",
    ))
