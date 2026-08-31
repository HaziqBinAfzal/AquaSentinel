from __future__ import annotations

import time
from rich.console import Console
from rich.live import Live

from .analytics import analyze
from .audit import record
from .dashboard import build_dashboard
from .ml import QualityMLModel
from .optimizer import optimize
from .scenarios import SCENARIOS
from .security import correlate, events_for
from .telemetry import sample

console = Console()


def run_live(scenario: str = "normal", samples: int = 30, refresh_rate: float = 4.0, seed: int = 133) -> None:
    if scenario not in SCENARIOS:
        raise SystemExit(f"Unknown scenario: {scenario}")
    if samples < 1:
        raise SystemExit("--samples must be at least 1")
    refresh_rate = max(1.0, min(refresh_rate, 10.0))

    model = QualityMLModel.train_default()
    delay = 1.0 / refresh_rate

    with Live(console=console, refresh_per_second=refresh_rate, screen=False, transient=False) as live:
        for i in range(samples):
            t = sample(scenario, i, seed=seed)
            result = analyze(t)
            ml_result = model.score(t)
            security_events = events_for(t.cyber_event)
            correlation = correlate(security_events, result["quality_flags"])

            result["priority"] = max(
                result["priority"],
                ml_result["ml_priority"],
                correlation["correlation_score"],
            )
            if ml_result["ml_state"] == "ANOMALOUS" or correlation["correlation_score"] >= 70:
                result["human_review_required"] = True

            decision = optimize(t, result).dict()
            live.update(build_dashboard(t, result, scenario, ml_result, correlation, decision), refresh=True)

            record(
                "live_telemetry_analysis",
                {
                    "scenario": scenario,
                    "sample": i,
                    "telemetry": t.dict(),
                    "analysis": result,
                    "ml": ml_result,
                    "security_events": [event.dict() for event in security_events],
                    "correlation": correlation,
                    "optimization": decision,
                },
            )
            time.sleep(delay)
