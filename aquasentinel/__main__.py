from __future__ import annotations

import argparse
import time
from rich.console import Console

from .analytics import analyze
from .audit import record
from .compliance import report
from .dashboard import architecture, render
from .scenarios import SCENARIOS
from .telemetry import sample

console = Console()


def run_scenario(name: str, samples: int, delay: float = 0.0) -> None:
    if name not in SCENARIOS:
        raise SystemExit(f"Unknown scenario: {name}")
    console.rule(f"AquaSentinel | {name}")
    console.print(SCENARIOS[name])
    for i in range(samples):
        t = sample(name, i)
        result = analyze(t)
        render(t, result, name)
        record("telemetry_analysis", {"scenario": name, "telemetry": t.dict(), "analysis": result})
        if delay:
            time.sleep(delay)


def demo() -> None:
    console.print("[bold]AquaSentinel AI — Topic 133 Safe Exam Demonstration[/bold]")
    console.print("Synthetic defensive lab only; no real plant or SCADA connection.\n")
    architecture()
    for name in ["normal", "sensor_anomaly", "quality_anomaly", "dosing_event", "fouling", "optimization"]:
        run_scenario(name, 7)
    console.print("\n[bold]Incident reasoning:[/bold] detect → validate → correlate → assess consequence → contain safely → verify quality → recover → preserve evidence")
    console.print("\n" + report())


def main() -> None:
    p = argparse.ArgumentParser(description="AquaSentinel AI safe water/desalination security simulation")
    sub = p.add_subparsers(dest="cmd")
    run = sub.add_parser("run")
    run.add_argument("--scenario", choices=SCENARIOS, default="normal")
    run.add_argument("--samples", type=int, default=10)
    run.add_argument("--delay", type=float, default=0.0)
    sub.add_parser("demo")
    sub.add_parser("architecture")
    sub.add_parser("compliance")
    args = p.parse_args()
    if args.cmd == "run":
        run_scenario(args.scenario, args.samples, args.delay)
    elif args.cmd == "architecture":
        architecture()
    elif args.cmd == "compliance":
        console.print(report())
    else:
        demo()


if __name__ == "__main__":
    main()
