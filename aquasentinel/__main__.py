from __future__ import annotations

import argparse
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .compliance import report
from .dashboard import architecture
from .doctor import healthy, run_checks
from .evidence import SUPPORTED_SUFFIXES, analyze_package
from .terminal_command_center import render_command_center

console = Console()


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


def _collect_paths(values: list[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        candidate = Path(value).expanduser()
        if candidate.is_dir():
            paths.extend(sorted(p for p in candidate.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES))
        elif candidate.is_file() and candidate.suffix.lower() in SUPPORTED_SUFFIXES:
            paths.append(candidate)
        else:
            raise SystemExit(f"Unsupported or missing evidence path: {value}")
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(path)
    if not unique:
        raise SystemExit("No supported evidence files were supplied.")
    return unique


def _self_check() -> None:
    console.print("[green]AquaSentinel schema-driven CLI loaded successfully.[/green]")
    console.print("[dim]Normal operation requires user-supplied evidence; no synthetic scenario is auto-loaded.[/dim]")


def main() -> None:
    parser = argparse.ArgumentParser(description="AquaSentinel schema-driven defensive smart-water evidence analysis workstation")
    parser.add_argument("--files", nargs="+", metavar="PATH", help="Evidence files or directories (.csv/.json/.jsonl/.xlsx)")
    parser.add_argument("--command-center", action="store_true", help="Render the terminal Water Cyber Defense Command Center")
    parser.add_argument("--monitor", action="store_true", help="Publish the active evidence package as Prometheus metrics")
    parser.add_argument("--metrics-port", type=int, default=9118, help="Prometheus exporter port; default 9118")
    parser.add_argument("--self-check", action="store_true", help="Validate the schema-driven CLI without loading evidence")
    parser.add_argument("--architecture", action="store_true", help="Show the conceptual defensive architecture")
    parser.add_argument("--compliance", action="store_true", help="Show educational assurance/compliance context")
    args = parser.parse_args()

    if args.self_check:
        _self_check(); return
    if args.architecture:
        architecture(); return
    if args.compliance:
        console.print(report()); return
    if not args.files:
        parser.print_help()
        console.print("\n[bold cyan]Evidence-driven workflow[/bold cyan]")
        console.print("  aquasentinel --files evidence.csv --command-center")
        console.print("  aquasentinel --files evidence_folder --command-center --monitor")
        console.print("\n[dim]AquaSentinel does not auto-load a simulator or assume fixed evidence filenames.[/dim]")
        return

    package = analyze_package(_collect_paths(args.files))
    if args.command_center:
        render_command_center(package, console)
    else:
        table = Table(title="AquaSentinel Evidence Analysis")
        table.add_column("Evidence"); table.add_column("Domain"); table.add_column("Records", justify="right")
        table.add_column("Features", justify="right"); table.add_column("Anomaly", justify="right"); table.add_column("Flags", justify="right")
        for item in package.datasets:
            table.add_row(item.name, item.domain, str(item.rows), str(len(item.numeric_features)), f"{item.anomaly_score:.1f}", str(item.anomaly_flags))
        console.print(table)
        console.print(f"Overall advisory risk: [bold]{package.risk_score:.1f}/100 {package.risk_level}[/bold]")

    if args.monitor:
        from .evidence_metrics import serve_package
        serve_package(package, args.metrics_port)
        console.print(f"\n[bold cyan]LIVE EVIDENCE METRICS[/bold cyan] http://127.0.0.1:{args.metrics_port}/metrics")
        console.print("[dim]This exporter exposes the analyzed evidence package only; it does not connect to plant systems.[/dim]")
        console.print("[yellow]Press Ctrl+C to stop the metrics session.[/yellow]")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[cyan]AquaSentinel monitoring session stopped.[/cyan]")


if __name__ == "__main__":
    main()
