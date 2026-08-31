from __future__ import annotations

from collections import deque
import time

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .analytics import analyze
from .audit import record
from .ml import QualityMLModel
from .optimizer import optimize
from .scenarios import SCENARIOS
from .security import correlate, events_for
from .telemetry import sample

console = Console()


def _meter(value: float, width: int = 18) -> str:
    value = max(0.0, min(100.0, float(value)))
    filled = round(width * value / 100)
    return "█" * filled + "░" * (width - filled)


def _severity(priority: float) -> tuple[str, str]:
    if priority >= 85:
        return "CRITICAL", "bold red"
    if priority >= 60:
        return "HIGH", "bold yellow"
    if priority >= 35:
        return "ELEVATED", "yellow"
    return "NORMAL", "bold green"


def _header(scenario: str, sample_index: int, samples: int, priority: float) -> Panel:
    level, style = _severity(priority)
    grid = Table.grid(expand=True)
    grid.add_column(ratio=3)
    grid.add_column(justify="center", ratio=2)
    grid.add_column(justify="right", ratio=2)
    grid.add_row(
        "[bold cyan]AQUASENTINEL AI[/bold cyan]  [dim]Water / Desalination Defense Console[/dim]",
        f"Scenario: [bold]{scenario}[/bold]",
        f"Frame {sample_index + 1}/{samples}  |  [{style}]{level}[/{style}]",
    )
    return Panel(grid, box=box.HEAVY, padding=(0, 1))


def _plant_panel(t, result: dict) -> Panel:
    stages = Table.grid(expand=True)
    stages.add_column(justify="center")
    stages.add_column(justify="center")
    stages.add_column(justify="center")
    stages.add_column(justify="center")
    stages.add_column(justify="center")
    stages.add_column(justify="center")
    stages.add_row(
        "[cyan]SEA / RAW[/cyan]",
        "[cyan]PRETREAT[/cyan]",
        "[cyan]HP PUMP[/cyan]",
        "[cyan]RO[/cyan]",
        "[cyan]POST-TREAT[/cyan]",
        "[cyan]STORAGE[/cyan]",
    )
    stages.add_row("→", "→", "→", "→", "→", "→")
    stages.add_row(
        f"Sal {t.salinity}",
        f"Turb {t.turbidity}",
        f"{t.feed_pressure} bar",
        f"{t.ro_pressure} bar\nMem {t.membrane_health:.0f}%",
        f"Cl {t.residual_chlorine}",
        f"Tank {t.tank_level:.0f}%",
    )
    return Panel(
        stages,
        title="[bold]SYNTHETIC DESALINATION PROCESS[/bold]",
        subtitle=f"Flow {t.flow_rate:.1f} | Fouling risk {result['fouling_risk']}%",
        box=box.ROUNDED,
    )


def _quality_panel(t, result: dict, ml_result: dict) -> Panel:
    table = Table.grid(padding=(0, 1), expand=True)
    table.add_column()
    table.add_column(justify="right")
    table.add_row("pH", str(t.ph))
    table.add_row("Conductivity", str(t.conductivity))
    table.add_row("Turbidity", str(t.turbidity))
    table.add_row("Residual chlorine", str(t.residual_chlorine))
    table.add_row("Rule priority", f"{result['quality_score']}%")
    table.add_row("ML state", f"{ml_result['ml_state']} ({ml_result['ml_priority']}%)")
    return Panel(table, title="WATER QUALITY + AI", subtitle=result["quality_state"], box=box.ROUNDED)


def _security_panel(t, correlation: dict, events: list) -> Panel:
    table = Table.grid(padding=(0, 1), expand=True)
    table.add_column()
    table.add_column(justify="right")
    table.add_row("SCADA evidence", t.cyber_event)
    table.add_row("Correlation", f"{correlation['correlation_score']}%")
    table.add_row("Cyber-physical", "YES" if correlation["cyber_physical"] else "NO")
    table.add_row("Sensors", ", ".join(correlation["sources"]))
    table.add_row("Events", str(len(events)))
    return Panel(table, title="OT / SCADA SECURITY", subtitle=correlation["disposition"], box=box.ROUNDED)


def _risk_panel(result: dict, ml_result: dict, correlation: dict) -> Panel:
    priority = result["priority"]
    level, style = _severity(priority)
    body = Text()
    body.append(f"{_meter(priority)}  {priority:.0f}%\n", style=style)
    body.append(f"Overall: {level}\n", style=style)
    body.append(f"Rules {result['quality_score']:>3}%  |  ML {ml_result['ml_priority']:>3}%\n")
    body.append(f"OT correlation {correlation['correlation_score']:>3}%\n")
    body.append("Decision: HUMAN REVIEW" if result["human_review_required"] else "Decision: MONITOR")
    return Panel(body, title="RISK & DECISION", box=box.ROUNDED)


def _optimization_panel(t, decision: dict, result: dict) -> Panel:
    table = Table.grid(padding=(0, 1), expand=True)
    table.add_column()
    table.add_column(justify="right")
    table.add_row("Mode", decision["mode"])
    table.add_row("Energy", f"{t.energy_kwh:.1f} kWh")
    table.add_row("Energy target", f"{decision['energy_target_pct']}%")
    table.add_row("Production target", f"{decision['production_target_pct']}%")
    table.add_row("Maintenance", result["maintenance"])
    return Panel(table, title="RESOURCE OPTIMIZER", subtitle=decision["quality_guardrail"], box=box.ROUNDED)


def _event_panel(event_feed: deque[str]) -> Panel:
    lines = list(event_feed) or ["[dim]No notable events yet.[/dim]"]
    return Panel("\n".join(lines), title="ACTIVE EVENT FEED", box=box.ROUNDED)


def _footer() -> Panel:
    return Panel(
        "[bold]BOUNDARY:[/bold] SYNTHETIC / DEFENSIVE / READ-ONLY DEMO   "
        "[dim]AI is advisory. No PLC, SCADA, dosing or utility control capability.[/dim]",
        box=box.HEAVY,
        padding=(0, 1),
    )


def build_soc_layout(t, result: dict, scenario: str, ml_result: dict, correlation: dict, decision: dict, events: list, event_feed: deque[str], sample_index: int, samples: int) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="plant", size=7),
        Layout(name="body", ratio=1, minimum_size=12),
        Layout(name="events", size=7),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(Layout(name="left"), Layout(name="middle"), Layout(name="right"))
    layout["left"].split_column(Layout(name="quality"), Layout(name="security"))
    layout["middle"].split_column(Layout(name="risk"), Layout(name="optimizer"))

    evidence = Table(title="LIVE EVIDENCE", expand=True, box=box.SIMPLE)
    evidence.add_column("Signal")
    evidence.add_column("Value", justify="right")
    evidence.add_row("Pump", t.pump_state)
    evidence.add_row("Flow", f"{t.flow_rate:.1f}")
    evidence.add_row("RO pressure", f"{t.ro_pressure:.1f} bar")
    evidence.add_row("Membrane", f"{t.membrane_health:.1f}%")
    evidence.add_row("Tank", f"{t.tank_level:.1f}%")
    evidence.add_row("Quality flags", str(len(result["quality_flags"])))
    evidence.add_row("Audit", "ENABLED")
    evidence.add_row("Control writes", "DISABLED")

    layout["header"].update(_header(scenario, sample_index, samples, result["priority"]))
    layout["plant"].update(_plant_panel(t, result))
    layout["quality"].update(_quality_panel(t, result, ml_result))
    layout["security"].update(_security_panel(t, correlation, events))
    layout["risk"].update(_risk_panel(result, ml_result, correlation))
    layout["optimizer"].update(_optimization_panel(t, decision, result))
    layout["right"].update(Panel(evidence, box=box.ROUNDED))
    layout["events"].update(_event_panel(event_feed))
    layout["footer"].update(_footer())
    return layout


def run_live(scenario: str = "normal", samples: int = 30, refresh_rate: float = 4.0, seed: int = 133, fullscreen: bool = False) -> None:
    if scenario not in SCENARIOS:
        raise SystemExit(f"Unknown scenario: {scenario}")
    if samples < 1:
        raise SystemExit("--samples must be at least 1")
    refresh_rate = max(1.0, min(refresh_rate, 10.0))

    model = QualityMLModel.train_default()
    delay = 1.0 / refresh_rate
    event_feed: deque[str] = deque(maxlen=5)

    with Live(
        console=console,
        refresh_per_second=refresh_rate,
        screen=fullscreen,
        transient=False,
        vertical_overflow="crop",
    ) as live:
        for i in range(samples):
            t = sample(scenario, i, seed=seed)
            result = analyze(t)
            ml_result = model.score(t)
            security_events = events_for(t.cyber_event)
            correlation = correlate(security_events, result["quality_flags"])

            result["priority"] = max(result["priority"], ml_result["ml_priority"], correlation["correlation_score"])
            if ml_result["ml_state"] == "ANOMALOUS" or correlation["correlation_score"] >= 70:
                result["human_review_required"] = True

            decision = optimize(t, result).dict()
            if result["quality_flags"]:
                event_feed.appendleft(f"[yellow]QUALITY[/yellow] {', '.join(result['quality_flags'])}")
            if t.cyber_event != "none":
                event_feed.appendleft(f"[red]OT[/red] {t.cyber_event} | correlation {correlation['correlation_score']}%")
            if ml_result["ml_state"] == "ANOMALOUS":
                event_feed.appendleft(f"[magenta]AI[/magenta] process anomaly priority {ml_result['ml_priority']}%")
            if not event_feed:
                event_feed.appendleft("[green]SYSTEM[/green] baseline telemetry within illustrative classroom bands")

            dashboard = build_soc_layout(
                t, result, scenario, ml_result, correlation, decision, security_events,
                event_feed, i, samples,
            )
            live.update(dashboard, refresh=True)

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
