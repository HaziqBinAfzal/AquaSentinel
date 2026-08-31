from rich.console import Console
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


def render(t, result, scenario: str, ml_result: dict | None = None) -> None:
    table = Table(title=f"AquaSentinel AI | {scenario}", show_lines=True)
    table.add_column("Domain", no_wrap=True)
    table.add_column("Live evidence")
    table.add_column("Assessment")
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
    table.add_row(
        "OT security",
        t.cyber_event,
        f"Cyber priority {result['cyber_score']}%",
    )
    if ml_result:
        table.add_row(
            "ML anomaly",
            f"IsolationForest over {len(ml_result['features'])} process features",
            f"{ml_result['ml_state']} | ML priority {ml_result['ml_priority']}%",
        )
    table.add_row(
        "Resources",
        f"Tank {t.tank_level}% | Energy {t.energy_kwh} kWh | Pump {t.pump_state}",
        result["recommendation"],
    )
    table.add_row(
        "Decision",
        "Rule + ML + cyber/process context",
        "HUMAN REVIEW" if result["human_review_required"] or (ml_result and ml_result["ml_state"] == "ANOMALOUS") else "MONITOR",
    )
    console.print(table)
