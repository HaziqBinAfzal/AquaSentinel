"""Schema-driven, read-only evidence analysis for AquaSentinel.

This module analyzes user-supplied evidence files without assuming fixed filenames,
file counts, or exact schemas. Findings are advisory and require human review.
"""
from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

SUPPORTED_SUFFIXES = {".csv", ".json", ".jsonl", ".xlsx"}

DOMAIN_HINTS: dict[str, set[str]] = {
    "SCADA / OT": {"scada", "plc", "rtu", "hmi", "protocol", "network", "command", "valve", "pump", "setpoint", "control"},
    "WATER QUALITY": {"ph", "turbidity", "chlorine", "conductivity", "tds", "salinity", "quality", "contamination", "permeate"},
    "DESALINATION / PROCESS": {"membrane", "ro", "pressure", "flow", "recovery", "fouling", "feed", "brine", "temperature", "train"},
    "ENERGY / RESOURCE": {"energy", "power", "kwh", "efficiency", "demand", "consumption", "resource", "recovery"},
    "MAINTENANCE / ASSET": {"maintenance", "asset", "health", "condition", "failure", "workorder", "inspection", "service"},
    "ACCESS / IDENTITY": {"user", "identity", "badge", "access", "login", "role", "failed", "mfa", "operator"},
    "COMPLIANCE / AUDIT": {"audit", "compliance", "approval", "change", "policy", "control", "evidence", "review", "record"},
}


def _tokens(value: str) -> set[str]:
    return {p for p in re.split(r"[^a-z0-9]+", value.lower()) if p}


def _as_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        text = str(value).strip().replace(",", "")
        if not text:
            return None
        number = float(text)
        return number if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None


@dataclass
class EvidenceFile:
    path: str
    name: str
    file_type: str
    rows: int
    columns: list[str]
    domain: str
    confidence: float
    domain_scores: dict[str, float] = field(default_factory=dict)
    numeric_features: list[str] = field(default_factory=list)
    missing_cells: int = 0
    total_cells: int = 0
    anomaly_score: float = 0.0
    anomaly_flags: int = 0
    analyzed_rows: int = 0
    notes: list[str] = field(default_factory=list)

    @property
    def missing_pct(self) -> float:
        return (100.0 * self.missing_cells / self.total_cells) if self.total_cells else 0.0


@dataclass
class EvidencePackage:
    datasets: list[EvidenceFile]
    risk_score: float
    risk_level: str

    @property
    def total_rows(self) -> int:
        return sum(item.rows for item in self.datasets)

    @property
    def total_flags(self) -> int:
        return sum(item.anomaly_flags for item in self.datasets)


def _read_rows(path: Path) -> list[dict[str, Any]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [dict(row) for row in data if isinstance(row, dict)]
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list) and all(isinstance(row, dict) for row in value):
                    return [dict(row) for row in value]
            return [data]
    if suffix == ".jsonl":
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                value = json.loads(line)
                if isinstance(value, dict):
                    rows.append(value)
        return rows
    if suffix == ".xlsx":
        try:
            from openpyxl import load_workbook
        except ImportError as exc:
            raise RuntimeError("XLSX support requires openpyxl") from exc
        workbook = load_workbook(path, read_only=True, data_only=True)
        sheet = workbook.active
        values = sheet.iter_rows(values_only=True)
        header = [str(v).strip() if v is not None else "" for v in next(values, ())]
        return [{header[i]: value for i, value in enumerate(row) if i < len(header) and header[i]} for row in values]
    raise ValueError(f"Unsupported evidence type: {suffix}")


def _infer_domain(columns: list[str]) -> tuple[str, float, dict[str, float]]:
    tokens = set().union(*(_tokens(column) for column in columns)) if columns else set()
    scores: dict[str, float] = {}
    for domain, hints in DOMAIN_HINTS.items():
        matches = len(tokens & hints)
        scores[domain] = min(1.0, matches / 3.0) if matches else 0.0
    domain = max(scores, key=scores.get) if scores else "GENERAL / UNKNOWN"
    confidence = scores.get(domain, 0.0)
    if confidence == 0:
        return "GENERAL / UNKNOWN", 0.0, scores
    return domain, confidence, scores


def _discover_numeric(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    usable: list[str] = []
    for column in columns:
        values = [_as_float(row.get(column)) for row in rows]
        present = [value for value in values if value is not None]
        if len(present) < max(5, int(len(rows) * 0.6)):
            continue
        if len(set(present)) < 2:
            continue
        tokens = _tokens(column)
        if tokens & {"id", "identifier", "timestamp", "time", "date"}:
            continue
        usable.append(column)
    return usable


def analyze_file(path: str | Path) -> EvidenceFile:
    evidence_path = Path(path).expanduser().resolve()
    if not evidence_path.is_file():
        raise FileNotFoundError(evidence_path)
    if evidence_path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise ValueError(f"Unsupported evidence type: {evidence_path.suffix}")
    rows = _read_rows(evidence_path)
    columns = list(dict.fromkeys(key for row in rows for key in row.keys()))
    domain, confidence, scores = _infer_domain(columns)
    numeric = _discover_numeric(rows, columns)
    total = len(rows) * len(columns)
    missing = sum(1 for row in rows for column in columns if row.get(column) in (None, ""))
    result = EvidenceFile(str(evidence_path), evidence_path.name, evidence_path.suffix.lower(), len(rows), columns, domain, confidence, scores, numeric, missing, total)
    if not rows:
        result.notes.append("No records were available for analysis.")
        return result
    if not numeric:
        result.notes.append("No suitable numeric features were discovered; schema profiling only.")
        return result
    matrix = []
    for row in rows:
        vector = [_as_float(row.get(column)) for column in numeric]
        if all(value is not None for value in vector):
            matrix.append(vector)
    result.analyzed_rows = len(matrix)
    if len(matrix) < 20:
        result.notes.append("Too few complete numeric records for Isolation Forest; no model finding produced.")
        return result
    scaled = StandardScaler().fit_transform(matrix)
    model = IsolationForest(n_estimators=160, contamination="auto", random_state=133)
    predictions = model.fit_predict(scaled)
    raw = -model.score_samples(scaled)
    low, high = float(min(raw)), float(max(raw))
    normalized = [100.0 * (float(value) - low) / (high - low) if high > low else 0.0 for value in raw]
    normalized.sort()
    idx = max(0, min(len(normalized) - 1, math.ceil(0.90 * len(normalized)) - 1))
    result.anomaly_score = round(normalized[idx], 1)
    result.anomaly_flags = sum(1 for value in predictions if value == -1)
    result.notes.append("Model findings are anomaly indicators, not proof of contamination, compromise, or unsafe water.")
    return result


def analyze_package(paths: list[str | Path]) -> EvidencePackage:
    datasets = [analyze_file(path) for path in paths]
    weighted = [(item.anomaly_score, item.analyzed_rows or item.rows) for item in datasets if item.rows]
    denominator = sum(weight for _, weight in weighted)
    risk = sum(score * weight for score, weight in weighted) / denominator if denominator else 0.0
    risk = round(risk, 1)
    level = "NORMAL" if risk < 40 else "ELEVATED" if risk < 70 else "HIGH"
    return EvidencePackage(datasets=datasets, risk_score=risk, risk_level=level)
