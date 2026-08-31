from __future__ import annotations

import argparse
import time
from rich.console import Console
from rich.table import Table

from .analytics import analyze
from .audit import record
from .compliance import report
from .dashboard import architecture, render
from .doctor import healthy, run_checks
from .live import run_live
from .ml import QualityMLModel
from .optimizer import optimize
from .presenter import incident_brief
from .reporting import generate_exam_report
from .scenarios import SCENARIOS
from .security import correlate, events_for
from .telemetry import sample

console = Console()
_MODEL: QualityMLModel | None = None


def get_model() -> QualityMLModel:
    global _MODEL
    if _MODEL is None:
        console.print("[dim]Training synthetic baseline anomaly model...[/dim]")
        _MODEL = QualityMLModel.train_default()
    return _MODEL


def run_scenario(name: str, samples: int, delay: float = 0.0, use_ml: bool = True, seed: int = 133) -> None:
    if name not in SCENARIOS:
        raise SystemExit(f"Unknown scenario: {name}")
    console.rule(f"AquaSentinel | {name}")
    console.print(SCENARIOS[name])
    model = get_model() if use_ml else None
    for i in range(samples):
        t = sample(name, i, seed=seed)
        result = analyze(t)
        ml_result = model.score(t) if model else None
        security_events = events_for(t.cyber_event)
        correlation = correlate(security_events, result["quality_flags"])
        if ml_result:
            result["priority"] = max(result["priority"], ml_result["ml_priority"])
            if ml_result["ml_state"] == "ANOMALOUS":
                result["human_review_required"] = True
        result["priority"] = max(result["priority"], correlation["correlation_score"])
        if correlation["correlation_score"] >= 70:
            result["human_review_required"] = True
        optimization = optimize(t, result).dict()
        render(t, result, name, ml_result, correlation, optimization)
        record(
            "telemetry_analysis",
            {
                "scenario": name,
                "telemetry": t.dict(),
                "analysis": result,
                "ml": ml_result,
                "security_events": [event.dict() for event in security_events],
                "correlation": correlation,
                "optimization": optimization,
            },
        )
        if delay:
            time.sleep(delay)


def doctor() -> None:
    checks = run_checks()
    table = Table(title="AquaSentinel Environment Doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")
    for check in checks:
        table.add_row(check.name, "PASS" if check.ok else "FAIL", check.detail)
    console.print(table)
    if not healthy(checks):
        raise SystemExit(1)


def demo() -> None:
    console.print("[bold]AquaSentinel AI — Topic 133 Safe Exam Demonstration[/bold]")
    console.print("Synthetic defensive lab only; no real plant or SCADA connection.\n")
    architecture()
    for name in ["normal", "sensor_anomaly", "quality_anomaly", "dosing_event", "fouling", "optimization"]:
        run_scenario(name, 7)
    console.print("\n[bold]Incident reasoning:[/bold] detect → validate → correlate → assess consequence → contain safely → verify quality → recover → preserve evidence")
    console.print("\n[bold]AI guardrail:[/bold] ML and optimization are advisory; they never override quality, engineering, public-health or human authority.")
    console.print("\n" + report())


def main() -> None:
    p = argparse.ArgumentParser(description="AquaSentinel AI safe water/desalination security simulation")
    sub = p.add_subparsers(dest="cmd")

    run = sub.add_parser("run", help="Run a scenario as discrete terminal snapshots")
    run.add_argument("--scenario", choices=SCENARIOS, default="normal")
    run.add_argument("--samples", type=int, default=10)
    run.add_argument("--delay", type=float, default=0.0)
    run.add_argument("--seed", type=int, default=133)
    run.add_argument("--no-ml", action="store_true", help="Use only deterministic classroom checks")

    live = sub.add_parser("live", help="Run the industrial low-lag SOC terminal dashboard")
    live.add_argument("--scenario", choices=SCENARIOS, default="normal")
    live.add_argument("--samples", type=int, default=30)
    live.add_argument("--refresh-rate", type=float, default=4.0)
    live.add_argument("--seed", type=int, default=133)
    live.add_argument("--fullscreen", action="store_true", help="Use terminal alternate-screen mode for an app-like exam demo")

    incident = sub.add_parser("incident", help="Show an examiner-friendly correlated incident brief")
    incident.add_argument("--scenario", choices=SCENARIOS, default="dosing_event")
    incident.add_argument("--step", type=int, default=8)
    incident.add_argument("--seed", type=int, default=133)

    sub.add_parser("demo")
    sub.add_parser("architecture")
    sub.add_parser("compliance")
    sub.add_parser("ml-check")
    sub.add_parser("doctor")

    export = sub.add_parser("report")
    export.add_argument("--output", default="reports/aquasentinel_exam_report.json")

    args = p.parse_args()
    if args.cmd == "run":
        run_scenario(args.scenario, args.samples, args.delay, not args.no_ml, args.seed)
    elif args.cmd == "live":
        run_live(args.scenario, args.samples, args.refresh_rate, args.seed, args.fullscreen)
    elif args.cmd == "incident":
        incident_brief(args.scenario, args.step, args.seed)
    elif args.cmd == "architecture":
        architecture()
    elif args.cmd == "compliance":
        console.print(report())
    elif args.cmd == "ml-check":
        model = get_model()
        for scenario in SCENARIOS:
            t = sample(scenario, 8)
            console.print(f"{scenario:16} {model.score(t)}")
    elif args.cmd == "doctor":
        doctor()
    elif args.cmd == "report":
        path = generate_exam_report(args.output)
        console.print(f"[green]Exam evidence report written to {path}[/green]")
    else:
        demo()


if __name__ == "__main__":
    main()
