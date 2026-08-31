from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from .analytics import analyze
from .ml import QualityMLModel
from .security import correlate, events_for
from .telemetry import sample


def generate_exam_report(output: str = "reports/aquasentinel_exam_report.json") -> str:
    model = QualityMLModel.train_default()
    scenarios = ["normal", "sensor_anomaly", "quality_anomaly", "dosing_event", "fouling", "optimization"]
    rows = []
    for name in scenarios:
        t = sample(name, 8)
        analysis = analyze(t)
        ml = model.score(t)
        events = events_for(t.cyber_event)
        correlation = correlate(events, analysis["quality_flags"])
        rows.append({
            "scenario": name,
            "telemetry": t.dict(),
            "analysis": analysis,
            "ml": ml,
            "security_events": [e.dict() for e in events],
            "correlation": correlation,
        })

    payload = {
        "project": "AquaSentinel AI",
        "topic": "EduQual Level 6 Topic 133",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "safety_boundary": "Synthetic defensive classroom simulation; not operational water-system guidance.",
        "architecture": ["Enterprise/SOC", "Industrial DMZ", "OT/SCADA", "Safety & Quality", "Synthetic Treatment Process"],
        "evidence": rows,
        "assurance": {
            "standards_context": ["NIST SP 800-82", "EPA public-water context", "WHO water-safety context"],
            "principles": [
                "segmentation and controlled conduits",
                "passive OT visibility",
                "cross-sensor quality validation",
                "AI as advisory prioritization",
                "public-health-first incident response",
                "traceable audit evidence",
            ],
        },
    }
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(p)
