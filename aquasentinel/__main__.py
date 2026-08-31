from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from .compliance import report
from .dashboard import architecture
from .doctor import healthy, run_checks
from .file_analysis import analyze_file, render_file_analysis
from .ingestion import analyze_content
from .webui import run_web

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


def _analysis_check() -> None:
    probe = (
        "timestamp,severity,ph,conductivity,turbidity,ro_pressure,flow_rate,membrane_health\n"
        "2026-01-01T00:00:00Z,info,7.2,420,0.3,58,102,92\n"
        "2026-01-01T00:01:00Z,warning,7.3,425,0.4,59,101,91\n"
    )
    result = analyze_content("self-check.csv", probe)
    if result["source"]["records"] != 2 or "ph" not in result["metrics"]:
        raise SystemExit("File-analysis self-check failed")
    console.print("[green]Local file-analysis check passed[/green]")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AquaSentinel AI local defensive log and water/process data analyzer"
    )
    sub = parser.add_subparsers(dest="cmd")

    web = sub.add_parser("web", help="Open the local browser analysis workstation")
    web.add_argument("--port", type=int, default=8765, help="Localhost port; default 8765")
    web.add_argument("--no-browser", action="store_true", help="Do not open the browser automatically")
    web.add_argument("--check-only", action="store_true", help="Validate web analysis without starting a server")

    analyze = sub.add_parser("analyze", help="Analyze a local .log, .txt, .csv, .json or .jsonl file")
    analyze.add_argument("file", nargs="?", help="Path to the local file")
    analyze.add_argument("--check-only", action="store_true", help="Run a built-in parser self-check for CI/setup")

    sub.add_parser("doctor", help="Check the local AquaSentinel environment and safety boundary")
    sub.add_parser("architecture", help="Show the conceptual defensive architecture")
    sub.add_parser("compliance", help="Show educational NIST/EPA/WHO assurance context")

    args = parser.parse_args()
    if args.cmd == "web":
        run_web(args.port, not args.no_browser, args.check_only)
    elif args.cmd == "analyze":
        if args.check_only:
            _analysis_check()
        elif not args.file:
            raise SystemExit("Provide a file path, for example: aquasentinel analyze plant.log")
        else:
            analyze_file(args.file)
    elif args.cmd == "doctor":
        doctor()
    elif args.cmd == "architecture":
        architecture()
    elif args.cmd == "compliance":
        console.print(report())
    else:
        parser.print_help()
        console.print("\n[bold]Choose an interface:[/bold]")
        console.print("  Browser:  aquasentinel web")
        console.print("  Terminal: aquasentinel analyze <file>")


if __name__ == "__main__":
    main()
