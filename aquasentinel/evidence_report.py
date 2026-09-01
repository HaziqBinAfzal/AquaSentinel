"""Human-readable evidence/audit report export for AquaSentinel."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .evidence import EvidencePackage


def build_report(package: EvidencePackage) -> str:
    lines = [
        "# AquaSentinel Evidence & Assurance Report",
        "",
        f"Generated (UTC): {datetime.now(timezone.utc).isoformat()}",
        "Mode: Local, read-only, schema-driven evidence analysis",
        "",
        "## Executive Summary",
        f"- Evidence sources: {len(package.datasets)}",
        f"- Records indexed: {package.total_rows}",
        f"- Advisory anomaly pressure: {package.risk_score:.1f}/100 ({package.risk_level})",
        f"- Model anomaly flags: {package.total_flags}",
        "- Interpretation: anomaly indicators require qualified human validation and are not proof of contamination, unsafe water, or cyber compromise.",
        "",
        "## Evidence Inventory",
    ]
    for item in package.datasets:
        lines.extend([
            "",
            f"### {item.name}",
            f"- SHA-256: `{item.sha256}`",
            f"- File type: {item.file_type}",
            f"- Records: {item.rows}",
            f"- Columns discovered: {len(item.columns)}",
            f"- Primary inferred domain: {item.domain} ({item.confidence * 100:.0f}% schema confidence)",
            f"- Numeric features used: {', '.join(item.numeric_features) if item.numeric_features else 'None'}",
            f"- Missing evidence: {item.missing_pct:.2f}%",
            f"- Analysis method: {item.analysis_method}",
            f"- Analyzed records: {item.analyzed_rows}",
            f"- Anomaly pressure: {item.anomaly_score:.1f}/100",
            f"- Model flags: {item.anomaly_flags}",
            f"- Timestamp field: {item.timestamp_field or 'Not inferred'}",
            f"- Evidence window UTC: {item.time_start or 'Unavailable'} to {item.time_end or 'Unavailable'}",
        ])
        if item.notes:
            lines.append("- Limitations/notes: " + " | ".join(item.notes))
    lines.extend(["", "## Cross-Source Time Evidence"])
    if package.correlations:
        lines.extend(f"- {finding}" for finding in package.correlations)
    else:
        lines.append("- No compatible overlapping timestamp windows were established from the supplied evidence.")
    lines.extend([
        "", "## Assurance Boundary",
        "AquaSentinel does not connect to or control PLCs, SCADA systems, pumps, valves, dosing controllers, or other industrial equipment.",
        "The report is an analytical aid, not a water-safety certification, compliance certification, incident attribution, or authorization for operational action.",
        "No evidence means no metric and no finding should be inferred.",
    ])
    return "\n".join(lines) + "\n"


def export_report(package: EvidencePackage, destination: str | Path) -> Path:
    path = Path(destination).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_report(package), encoding="utf-8")
    return path.resolve()
