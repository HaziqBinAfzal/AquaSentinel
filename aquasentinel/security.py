from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone


@dataclass
class SecurityEvent:
    timestamp: str
    source: str
    zone: str
    event_type: str
    severity: int
    detail: str

    def dict(self) -> dict:
        return asdict(self)


def events_for(cyber_event: str) -> list[SecurityEvent]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if cyber_event == "unexpected_dosing_command":
        return [
            SecurityEvent(now, "zeek-sim", "OT/SCADA", "unusual_control_session", 70,
                          "Synthetic connection pattern differs from the approved baseline"),
            SecurityEvent(now, "suricata-sim", "Industrial DMZ", "policy_rule_match", 75,
                          "Synthetic rule match involving a restricted treatment-control service"),
            SecurityEvent(now, "scada-audit", "OT/SCADA", "unexpected_dosing_command", 95,
                          "Synthetic dosing command lacks expected workflow context"),
        ]
    return [
        SecurityEvent(now, "zeek-sim", "OT/SCADA", "baseline_connection", 5,
                      "Synthetic network activity is consistent with the classroom baseline")
    ]


def correlate(events: list[SecurityEvent], quality_flags: list[str]) -> dict:
    max_security = max((e.severity for e in events), default=0)
    cyber_physical = max_security >= 70 and bool(quality_flags)
    if cyber_physical:
        disposition = "HIGH PRIORITY: validate identity + SCADA + independent quality evidence"
        score = min(100, max_security + min(15, 4 * len(quality_flags)))
    elif max_security >= 70:
        disposition = "SECURITY REVIEW: suspicious cyber evidence without confirmed quality impact"
        score = max_security
    elif quality_flags:
        disposition = "PROCESS/QUALITY REVIEW: abnormal process evidence without strong cyber evidence"
        score = min(75, 20 * len(quality_flags))
    else:
        disposition = "BASELINE MONITORING"
        score = max_security
    return {
        "correlation_score": score,
        "cyber_physical": cyber_physical,
        "disposition": disposition,
        "sources": sorted({e.source for e in events}),
    }
