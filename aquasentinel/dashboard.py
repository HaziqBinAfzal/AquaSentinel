from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def architecture() -> None:
    console.print(Panel.fit(
        "ENTERPRISE / SOC\n      ↓\nINDUSTRIAL DMZ\n      ↓\nOT / SCADA\n      ↓\nSAFETY & QUALITY\n      ↓\nSYNTHETIC TREATMENT PROCESS",
        title="AquaSentinel Trust-Zone Architecture",
    ))


def render(t, result, scenario: str) -> None:
    table = Table(title=f"AquaSentinel AI | {scenario}")
    table.add_column("Domain")
    table.add_column("Evidence")
    table.add_column("Assessment")
    table.add_row("Water quality", f"pH {t.ph} | Cond {t.conductivity} | Turb {t.turbidity} | Cl {t.residual_chlorine}", result["quality_state"])
    table.add_row("RO process", f"Pressure {t.ro_pressure} | Flow {t.flow_rate} | Membrane {t.membrane_health}%", f"Fouling risk {result['fouling_risk']}%")
    table.add_row("OT security", t.cyber_event, f"Cyber priority {result['cyber_score']}%")
    table.add_row("Resources", f"Tank {t.tank_level}% | Energy {t.energy_kwh} kWh", result["recommendation"])
    table.add_row("Decision", "Correlated evidence", "HUMAN REVIEW" if result["human_review_required"] else "MONITOR")
    console.print(table)
