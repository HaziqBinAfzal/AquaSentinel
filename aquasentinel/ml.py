from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from sklearn.ensemble import IsolationForest

from .telemetry import Telemetry, sample

FEATURES = (
    "ph",
    "conductivity",
    "turbidity",
    "residual_chlorine",
    "salinity",
    "feed_pressure",
    "ro_pressure",
    "flow_rate",
    "temperature",
    "tank_level",
    "energy_kwh",
    "membrane_health",
)


def vector(t: Telemetry) -> list[float]:
    return [float(getattr(t, name)) for name in FEATURES]


@dataclass
class QualityMLModel:
    estimator: IsolationForest

    @classmethod
    def train_default(cls, samples: int = 300) -> "QualityMLModel":
        training = [vector(sample("normal", i, seed=1330)) for i in range(samples)]
        model = IsolationForest(
            n_estimators=120,
            contamination=0.03,
            random_state=133,
        )
        model.fit(training)
        return cls(model)

    def score(self, t: Telemetry) -> dict:
        x = [vector(t)]
        prediction = int(self.estimator.predict(x)[0])
        raw = float(self.estimator.decision_function(x)[0])
        # Convert the decision function into a simple 0-100 classroom priority score.
        priority = round(max(0.0, min(100.0, (0.15 - raw) * 250.0)), 1)
        return {
            "ml_state": "ANOMALOUS" if prediction == -1 else "EXPECTED",
            "ml_priority": priority,
            "ml_decision_function": round(raw, 4),
            "features": FEATURES,
        }


def score_many(model: QualityMLModel, rows: Iterable[Telemetry]) -> list[dict]:
    return [model.score(row) for row in rows]
