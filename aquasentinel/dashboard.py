from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

console = Console()


def architecture() -> None:
    console.print(Panel.fit(
        "ENTERPRISE / SOC\n"
        "      ↓ controlled conduit\n"
        "INDUSTRIAL DMZ\n"
        "      ↓ monitored access\n"
        "OT / SCADA ────────→ passive security telemetry\n"
        "      ↓\n"
        "SAFETY & QUALITY ──→ independent validation evidence\n"
        "      ↓\n"
        "SYNTHETIC TREATMENT PROCESS\n"
        "      ↓\n"
        "ANALYTICS → HUMAN REVIEW → AUDIT / REPORT",
        title="AquaSentinel Trust-Zone Architecture",
        subtitle="Synthetic defensive learning lab",
    ))


def build_dashboard(t, result: dict, scenario: str, ml_result: dict | None = None, correlation: dict | None = None, optimization: dict | None = None):
    table = Table(title=f"AquaSentinel AI | {scenario}", show_lines=True, expand=True)
    table.add_column("Domain", no_wrap=True, ratio=1)
    table.add_column("Live evidence", ratio=3)
    table.add_column("Assessment", ratio=2)
    table.add_row(
        "Water quality",
        f"pH {t.ph} | Cond {t.conductivity} | Turb {t.turbidity} | Cl {t.residual_chlorine} | Sal {t.salinity}",
        f"{result['quality_state']} | rule score {result['quality_score']}%",
    )
    table.add_row(
        "RO process",
        f"Feed {t.feed_pressure} | RO {t.ro_pressure} bar | Flow {t.flow_rate} | Membrane {t.membrane_health}%",
        f"Fouling risk {result['fouling_risk']}% | {result['maintenance']}",
    )
    table.add_row("OT security", t.cyber_event, f"Cyber priority {result['cyber_score']}%")
    if correlation:
        table.add_row(
            "Correlation",
            ", ".join(correlation["sources"]),
            f"{correlation['correlation_score']}% | {correlation['disposition']}",
        )
    if ml_result:
        table.add_row(
            "ML anomaly",
            f"IsolationForest over {len(ml_result['features'])} process features",
            f"{ml_result['ml_state']} | ML priority {ml_result['ml_priority']}%",
        )
    if optimization:
        table.add_row(
            "AI optimization",
            f"Mode {optimization['mode']} | Energy target {optimization['energy_target_pct']}% | Production {optimization['production_target_pct']}%",
            optimization["quality_guardrail"],
        )
    else:
        table.add_row(
            "Resources",
            f"Tank {t.tank_level}% | Energy {t.energy_kwh} kWh | Pump {t.pump_state}",
            result["recommendation"],
        )
    needs_review = (
        result["human_review_required"]
        or bool(ml_result and ml_result["ml_state"] == "ANOMALOUS")
        or bool(correlation and correlation["correlation_score"] >= 70)
    )
    table.add_row("Decision", "Rules + ML + cyber + process context", "HUMAN REVIEW" if needs_review else "MONITOR")

    flow = Panel(
        "RAW/SEA WATER → PRETREATMENT → HP PUMP → REVERSE OSMOSIS → POST-TREATMENT → STORAGE → DISTRIBUTION",
        title="Synthetic Desalination Process",
    )
    status = Panel(
        f"Priority: {result['priority']}% | Scenario: {scenario} | Boundary: simulation only — no PLC/SCADA writes",
        title="Safety & Decision Boundary",
    )
    return Group(flow, table, status)


def render(t, result, scenario: str, ml_result: dict | None = None, correlation: dict | None = None, optimization: dict | None = None) -> None:
    console.print(build_dashboard(t, result, scenario, ml_result, correlation, optimization))
