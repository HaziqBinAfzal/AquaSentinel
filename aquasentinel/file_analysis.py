from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .ingestion import analyze_content

console = Console()


def analyze_file(path: str) -> dict:
    source = Path(path).expanduser()
    if not source.is_file():
        raise SystemExit(f"File not found: {source}")
    if source.stat().st_size > 8 * 1024 * 1024:
        raise SystemExit("File is larger than the 8 MB local-analysis limit")
    try:
        content = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        content = source.read_text(encoding="cp1252")
    result = analyze_content(source.name, content)
    render_file_analysis(result)
    return result


def render_file_analysis(result: dict) -> None:
    source = result["source"]
    summary = result["summary"]

    console.print(Panel.fit(
        f"[bold]AquaSentinel AI — Local File Analysis[/bold]\n"
        f"Source: {source['filename']}  |  Format: {source['format'].upper()}  |  Records: {source['records']}\n"
        "Defensive local analysis only — no industrial-control connection",
        border_style="blue",
    ))

    overview = Table(title="Analysis Summary")
    overview.add_column("Item")
    overview.add_column("Result")
    overview.add_row("Decision", summary["decision"])
    overview.add_row("Review score", f"{summary['risk_score']} / 100")
    overview.add_row("Critical entries", str(summary["critical"]))
    overview.add_row("Errors", str(summary["errors"]))
    overview.add_row("Warnings", str(summary["warnings"]))
    overview.add_row("Illustrative-band flags", str(summary["review_flags"]))
    overview.add_row("ML analysis", result["ml"]["state"])
    overview.add_row("ML anomalies", str(result["ml"].get("anomaly_count", 0)))
    console.print(overview)

    metrics = Table(title="Recognized Process / Water Metrics")
    metrics.add_column("Field")
    metrics.add_column("Min", justify="right")
    metrics.add_column("Average", justify="right")
    metrics.add_column("Max", justify="right")
    metrics.add_column("Latest", justify="right")
    if result["metrics"]:
        for name, item in result["metrics"].items():
            metrics.add_row(name, str(item["min"]), str(item["avg"]), str(item["max"]), str(item["last"]))
    else:
        metrics.add_row("No recognized telemetry fields", "-", "-", "-", "-")
    console.print(metrics)

    indicators = Table(title="Observed Log / Security Indicators")
    indicators.add_column("Indicator")
    indicators.add_column("Count", justify="right")
    if result["indicators"]:
        for name, count in result["indicators"].items():
            indicators.add_row(name, str(count))
    else:
        indicators.add_row("No configured indicators found", "0")
    console.print(indicators)

    if result["review_flags"]:
        flags = Table(title="Items for Human Review")
        flags.add_column("Field")
        flags.add_column("Outside classroom band")
        flags.add_column("Observed rows")
        for item in result["review_flags"]:
            flags.add_row(item["field"], str(item["outside_band"]), str(item["count"]))
        console.print(flags)

    console.print(f"[dim]{result['note']}[/dim]")
