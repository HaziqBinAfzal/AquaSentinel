from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import random


@dataclass
class Telemetry:
    timestamp: str
    ph: float
    conductivity: float
    turbidity: float
    residual_chlorine: float
    salinity: float
    feed_pressure: float
    ro_pressure: float
    flow_rate: float
    temperature: float
    tank_level: float
    pump_state: str
    energy_kwh: float
    membrane_health: float
    quality_anomaly_label: str = "normal"
    cyber_event: str = "none"

    def dict(self) -> dict:
        return asdict(self)


def sample(scenario: str = "normal", step: int = 0, seed: int = 133) -> Telemetry:
    # Determinism is intentional for reproducible classroom telemetry. This RNG is
    # never used for credentials, tokens, cryptography, access control or security decisions.
    r = random.Random(seed + step)  # nosec B311
    t = Telemetry(
        timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        ph=round(r.gauss(7.25, .08), 2),
        conductivity=round(r.gauss(420, 18), 1),
        turbidity=round(max(.05, r.gauss(.35, .08)), 2),
        residual_chlorine=round(max(.05, r.gauss(.75, .06)), 2),
        salinity=round(max(.05, r.gauss(.45, .04)), 2),
        feed_pressure=round(r.gauss(4.5, .2), 2),
        ro_pressure=round(r.gauss(58, 1.3), 2),
        flow_rate=round(r.gauss(102, 2.5), 2),
        temperature=round(r.gauss(27, .6), 2),
        tank_level=round(r.gauss(68, 2.0), 2),
        pump_state="RUNNING",
        energy_kwh=round(r.gauss(390, 10), 1),
        membrane_health=round(min(100, max(0, r.gauss(91, 1.2))), 1),
    )
    if scenario == "sensor_anomaly" and step >= 5:
        t.ph = 10.8
        t.quality_anomaly_label = "sensor_review"
    elif scenario == "quality_anomaly" and step >= 5:
        t.ph, t.turbidity, t.residual_chlorine = 6.1, 2.8, .18
        t.conductivity = 720
        t.quality_anomaly_label = "multi_sensor_review"
    elif scenario == "dosing_event" and step >= 5:
        t.cyber_event = "unexpected_dosing_command"
        t.residual_chlorine = .22
    elif scenario == "fouling":
        t.membrane_health = max(45, 91 - step * 2.2)
        t.ro_pressure += step * .65
        t.flow_rate -= step * .7
        t.energy_kwh += step * 4.0
    elif scenario == "optimization":
        t.tank_level = max(25, 78 - step * 1.2)
        t.energy_kwh += 25
    return t
