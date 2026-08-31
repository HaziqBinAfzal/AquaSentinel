from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .analytics import analyze
from .incidents import incident_severity, response_plan
from .ml import QualityMLModel
from .optimizer import optimize
from .security import correlate, events_for
from .telemetry import sample

console = Console()


def incident_brief(scenario: str, step: int = 8, seed: int = 133) -> None:
    t = sample(scenario, step, seed=seed)
    result = analyze(t)
    model = QualityMLModel.train_default()
    ml_result = model.score(t)
    security_events = events_for(t.cyber_event)
    correlation = correlate(security_events, result["quality_flags"])
    result["priority"] = max(
        result["priority"],
        ml_result["ml_priority"],
        correlation["correlation_score"],
    )
    optimization = optimize(t, result).dict()

    console.print(
        Panel.fit(
            f"Scenario: {scenario}\n"
            f"Severity: {incident_severity(result, correlation)}\n"
            f"Overall priority: {result['priority']}%\n"
            f"Decision: {'HUMAN REVIEW' if result['human_review_required'] or result['priority'] >= 70 else 'MONITOR'}",
            title="AquaSentinel Incident Brief",
            subtitle="Synthetic defensive evidence only",
        )
    )

    evidence = Table(title="Correlated Evidence", show_lines=True)
    evidence.add_column("Layer")
    evidence.add_column("Evidence")
    evidence.add_row("Quality", ", ".join(result["quality_flags"]) or "No rule-band flags")
    evidence.add_row("ML", f"{ml_result['ml_state']} | priority {ml_result['ml_priority']}%")
    evidence.add_row("OT security", ", ".join(event.source for event in security_events))
    evidence.add_row("Correlation", f"{correlation['correlation_score']}% | {correlation['disposition']}")
    evidence.add_row("Optimization", f"{optimization['mode']} | {optimization['quality_guardrail']}")
    console.print(evidence)

    timeline = Table(title="Safe Incident Response Timeline", show_lines=True)
    timeline.add_column("Stage", no_wrap=True)
    timeline.add_column("Action")
    timeline.add_column("Why it matters")
    for item in response_plan(result, correlation):
        timeline.add_row(item.stage, item.action, item.purpose)
    console.print(timeline)

    console.print(
        Panel(
            "Exam point: detection does not equal contamination. AquaSentinel correlates cyber, process and quality evidence, keeps optimization advisory, and requires human/public-health authority before any real operational action.",
            title="What to explain to the examiner",
        )
    )
