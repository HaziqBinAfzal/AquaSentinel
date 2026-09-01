"""Prometheus metrics for AquaSentinel evidence analysis."""
from __future__ import annotations

from prometheus_client import Gauge, start_http_server

from .evidence import EvidencePackage

EVIDENCE_FILES = Gauge(
    "aquasentinel_evidence_files",
    "Number of evidence files in the active analysis",
)
EVIDENCE_ROWS = Gauge(
    "aquasentinel_evidence_rows",
    "Total evidence records indexed",
)
RISK_SCORE = Gauge(
    "aquasentinel_evidence_risk_score",
    "Aggregate advisory evidence risk score",
)
MODEL_FLAGS = Gauge(
    "aquasentinel_model_flags",
    "Total anomaly model flags",
)
DATASET_ROWS = Gauge(
    "aquasentinel_dataset_rows",
    "Records by evidence source",
    ["file", "domain"],
)
DATASET_MISSING = Gauge(
    "aquasentinel_dataset_missing_pct",
    "Missing evidence percentage",
    ["file", "domain"],
)
DATASET_ANOMALY = Gauge(
    "aquasentinel_dataset_anomaly_score",
    "Anomaly pressure by evidence source",
    ["file", "domain"],
)
DATASET_FLAGS = Gauge(
    "aquasentinel_dataset_anomaly_flags",
    "Anomaly flags by evidence source",
    ["file", "domain"],
)


def publish_package(package: EvidencePackage) -> None:
    EVIDENCE_FILES.set(len(package.datasets))
    EVIDENCE_ROWS.set(package.total_rows)
    RISK_SCORE.set(package.risk_score)
    MODEL_FLAGS.set(package.total_flags)

    DATASET_ROWS.clear()
    DATASET_MISSING.clear()
    DATASET_ANOMALY.clear()
    DATASET_FLAGS.clear()

    for item in package.datasets:
        labels = {"file": item.name, "domain": item.domain}
        DATASET_ROWS.labels(**labels).set(item.rows)
        DATASET_MISSING.labels(**labels).set(item.missing_pct)
        DATASET_ANOMALY.labels(**labels).set(item.anomaly_score)
        DATASET_FLAGS.labels(**labels).set(item.anomaly_flags)


def serve_package(package: EvidencePackage, port: int = 9118) -> None:
    publish_package(package)
    start_http_server(port)
