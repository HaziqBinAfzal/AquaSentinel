"""Rich terminal command center for schema-driven AquaSentinel evidence."""
from __future__ import annotations
from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from .evidence import EvidencePackage

def _risk_style(score: float) -> str:
    return "bold red" if score >= 70 else "bold yellow" if score >= 40 else "bold green"

def _meter(score: float, width: int = 28) -> str:
    filled=max(0,min(width,round(width*score/100))); return "█"*filled+"░"*(width-filled)

def render_command_center(package: EvidencePackage, console: Console | None = None) -> None:
    console=console or Console()
    console.print(Panel(Group(Text("≈ A Q U A S E N T I N E L ≈",style="bold cyan",justify="center"),Text("SMART WATER CYBER DEFENSE COMMAND CENTER",style="bold white",justify="center"),Text("Evidence-driven • local • read-only • schema-adaptive • human-reviewed",style="dim cyan",justify="center")),border_style="cyan",box=box.DOUBLE))
    total_cells=sum(d.total_cells for d in package.datasets); quality=100.0-(100.0*sum(d.missing_cells for d in package.datasets)/total_cells) if total_cells else 100.0
    stats=Table.grid(expand=True)
    for _ in range(5): stats.add_column(ratio=1)
    stats.add_row(Panel(f"[bold cyan]{len(package.datasets)}[/]\nEVIDENCE SOURCES",border_style="cyan"),Panel(f"[bold blue]{package.total_rows:,}[/]\nRECORDS INDEXED",border_style="blue"),Panel(f"[{_risk_style(package.risk_score)}]{package.risk_score:.1f}/100[/]\nADVISORY RISK",border_style="yellow"),Panel(f"[bold magenta]{package.total_flags:,}[/]\nMODEL FLAGS",border_style="magenta"),Panel(f"[bold green]{quality:.1f}%[/]\nDATA QUALITY",border_style="green"))
    console.print(stats)
    console.print(Panel(f"[{_risk_style(package.risk_score)}]{_meter(package.risk_score)}  {package.risk_score:.1f}/100  {package.risk_level}[/]",title="GLOBAL WATER / OT ANOMALY PRESSURE",border_style="cyan"))
    status=Table.grid(expand=True); status.add_column(); status.add_column(); status.add_row("[green]● ANALYSIS ENGINE ONLINE[/]","[green]● SHA-256 PROVENANCE ACTIVE[/]"); status.add_row("[cyan]● CONTROL WRITES DISABLED[/]","[yellow]● HUMAN REVIEW REQUIRED[/]"); console.print(Panel(status,title="PLATFORM STATUS",border_style="blue"))
    cards=Table.grid(expand=True); cards.add_column(ratio=1); cards.add_column(ratio=1); panels=[]
    for item in package.datasets:
        body=(f"[bold]{item.name}[/]\nDomain confidence   {item.confidence*100:.0f}%\nRecords             {item.rows:,}\nDiscovered features {len(item.numeric_features)}\nAnalysis method     {item.analysis_method}\nMissing evidence    {item.missing_pct:.1f}%\nAnomaly pressure    [{_risk_style(item.anomaly_score)}]{item.anomaly_score:.1f}/100[/]\nModel flags         {item.anomaly_flags:,}\nTime field          {item.timestamp_field or 'not inferred'}\nSHA-256             {item.sha256[:16]}…\n{_meter(item.anomaly_score,20)}")
        panels.append(Panel(body,title=item.domain,border_style="cyan"))
    for index in range(0,len(panels),2):
        row=panels[index:index+2]
        if len(row)==1: row.append(Panel("[dim]Awaiting additional evidence source[/]",border_style="dim"))
        cards.add_row(*row)
    console.print(cards)
    ranking=Table(title="EVIDENCE PRIORITY QUEUE",box=box.SIMPLE_HEAVY,expand=True); ranking.add_column("#",justify="right"); ranking.add_column("Source"); ranking.add_column("Inferred domain"); ranking.add_column("Method"); ranking.add_column("Anomaly",justify="right"); ranking.add_column("Flags",justify="right")
    for rank,item in enumerate(sorted(package.datasets,key=lambda d:d.anomaly_score,reverse=True),1): ranking.add_row(str(rank),item.name,item.domain,item.analysis_method,f"{item.anomaly_score:.1f}",str(item.anomaly_flags))
    console.print(ranking)
    correlation="\n".join(f"• {value}" for value in package.correlations) if package.correlations else "[dim]No compatible overlapping timestamp windows established.[/]"
    console.print(Panel(correlation,title="CROSS-SOURCE TIME EVIDENCE",border_style="cyan"))
    console.print(Panel("INGEST → HASH → PROFILE → INFER → FEATURE DISCOVERY → AI ANOMALY ANALYSIS → TIME CORRELATION → RISK PRIORITIZATION → HUMAN REVIEW",title="DEFENSE-IN-DEPTH ANALYSIS PATH",border_style="blue"))
    console.print(Panel("No direct PLC/SCADA actuation • No autonomous dosing/valve/pump commands • No fabricated findings\nAnomaly ≠ contamination ≠ cyberattack. Findings require qualified human validation.",title="AQUASENTINEL SAFETY BOUNDARY",border_style="green"))
