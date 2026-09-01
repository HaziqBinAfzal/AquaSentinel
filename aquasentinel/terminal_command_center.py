"""Rich terminal command center for schema-driven AquaSentinel evidence."""
from __future__ import annotations

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .evidence import EvidencePackage


def _risk_style(score: float) -> str:
    if score >= 70:
        return "bold red"
    if score >= 40:
        return "bold yellow"
    return "bold green"


def _meter(score: float, width: int = 28) -> str:
    filled = max(0, min(width, round(width * score / 100)))
    return "█" * filled + "░" * (width - filled)


def render_command_center(
    package: EvidencePackage,
    console: Console | None = None,
) -> None:
    console = console or Console()
    console.print(
        Panel(
            Group(
                Text(
                    "≈ A Q U A S E N T I N E L ≈",
                    style="bold cyan",
                    justify="center",
                ),
                Text(
                    "WATER SECURITY & RESILIENCE COMMAND CENTER",
                    style="bold white",
                    justify="center",
                ),
                Text(
                    "Evidence-driven • local • read-only • schema-adaptive • human-reviewed",
                    style="dim cyan",
                    justify="center",
                ),
            ),
            border_style="cyan",
            box=box.DOUBLE,
        )
    )

    total_cells = sum(dataset.total_cells for dataset in package.datasets)
    missing_cells = sum(dataset.missing_cells for dataset in package.datasets)
    quality = 100.0 - (100.0 * missing_cells / total_cells) if total_cells else 100.0

    stats = Table.grid(expand=True)
    for _ in range(5):
        stats.add_column(ratio=1)
    stats.add_row(
        Panel(
            f"[bold cyan]{len(package.datasets)}[/]\nEVIDENCE SOURCES",
            border_style="cyan",
        ),
        Panel(
            f"[bold blue]{package.total_rows:,}[/]\nRECORDS INDEXED",
            border_style="blue",
        ),
        Panel(
            f"[{_risk_style(package.risk_score)}]{package.risk_score:.1f}/100[/]"
            "\nADVISORY RISK",
            border_style="yellow",
        ),
        Panel(
            f"[bold magenta]{package.total_flags:,}[/]\nMODEL FLAGS",
            border_style="magenta",
        ),
        Panel(
            f"[bold green]{quality:.1f}%[/]\nDATA QUALITY",
            border_style="green",
        ),
    )
    console.print(stats)

    console.print(
        Panel(
            f"[{_risk_style(package.risk_score)}]"
            f"{_meter(package.risk_score)}  "
            f"{package.risk_score:.1f}/100  {package.risk_level}[/]",
            title="GLOBAL WATER / OT ANOMALY PRESSURE",
            border_style="cyan",
        )
    )

    status = Table.grid(expand=True)
    status.add_column()
    status.add_column()
    status.add_row(
        "[green]● ANALYSIS ENGINE ONLINE[/]",
        "[green]● SHA-256 PROVENANCE ACTIVE[/]",
    )
    status.add_row(
        "[cyan]● CONTROL WRITES DISABLED[/]",
        "[yellow]● HUMAN REVIEW REQUIRED[/]",
    )
    console.print(Panel(status, title="PLATFORM STATUS", border_style="blue"))

    cards = Table.grid(expand=True)
    cards.add_column(ratio=1)
    cards.add_column(ratio=1)
    panels: list[Panel] = []
    for item in package.datasets:
        body = (
            f"[bold]{item.name}[/]\n"
            f"Domain confidence   {item.confidence * 100:.0f}%\n"
            f"Records             {item.rows:,}\n"
            f"Discovered features {len(item.numeric_features)}\n"
            f"Analysis method     {item.analysis_method}\n"
            f"Missing evidence    {item.missing_pct:.1f}%\n"
            f"Anomaly pressure    [{_risk_style(item.anomaly_score)}]"
            f"{item.anomaly_score:.1f}/100[/]\n"
            f"Model flags         {item.anomaly_flags:,}\n"
            f"Time field          {item.timestamp_field or 'not inferred'}\n"
            f"SHA-256             {item.sha256[:16]}…\n"
            f"{_meter(item.anomaly_score, 20)}"
        )
        panels.append(Panel(body, title=item.domain, border_style="cyan"))

    for index in range(0, len(panels), 2):
        row = panels[index : index + 2]
        if len(row) == 1:
            row.append(
                Panel(
                    "[dim]Awaiting additional evidence source[/]",
                    border_style="dim",
                )
            )
        cards.add_row(*row)
    console.print(cards)

    ranking = Table(
        title="EVIDENCE PRIORITY QUEUE",
        box=box.SIMPLE_HEAVY,
        expand=True,
    )
    ranking.add_column("#", justify="right")
    ranking.add_column("Source")
    ranking.add_column("Inferred domain")
    ranking.add_column("Method")
    ranking.add_column("Anomaly", justify="right")
    ranking.add_column("Flags", justify="right")
    ordered = sorted(
        package.datasets,
        key=lambda dataset: dataset.anomaly_score,
        reverse=True,
    )
    for rank, item in enumerate(ordered, 1):
        ranking.add_row(
            str(rank),
            item.name,
            item.domain,
            item.analysis_method,
            f"{item.anomaly_score:.1f}",
            str(item.anomaly_flags),
        )
    console.print(ranking)

    if package.correlations:
        correlation = "\n".join(f"• {value}" for value in package.correlations)
    else:
        correlation = "[dim]No compatible overlapping timestamp windows established.[/]"
    console.print(
        Panel(
            correlation,
            title="CROSS-SOURCE TIME EVIDENCE",
            border_style="cyan",
        )
    )

    console.print(
        Panel(
            "INGEST → HASH → PROFILE → INFER → FEATURE DISCOVERY → "
            "AI ANOMALY ANALYSIS → TIME CORRELATION → RISK PRIORITIZATION → "
            "HUMAN REVIEW",
            title="DEFENSE-IN-DEPTH ANALYSIS PATH",
            border_style="blue",
        )
    )
    console.print(
        Panel(
            "No direct PLC/SCADA actuation • No autonomous dosing/valve/pump "
            "commands • No fabricated findings\n"
            "Anomaly ≠ contamination ≠ cyberattack. Findings require qualified "
            "human validation.",
            title="AQUASENTINEL SAFETY BOUNDARY",
            border_style="green",
        )
    )
